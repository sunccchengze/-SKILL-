#!/usr/bin/env python3
"""Clean-room acceptance tests for bundles/research-workflow-kit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BUNDLE = REPO / "bundles" / "research-workflow-kit"
ARCHIVE = BUNDLE / "research-workflow-kit.tar.gz"


class ResearchBundleCleanRoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("RESEARCH_KIT_REBUILD") == "1":
            subprocess.run(
                ["python3", "scripts/build_research_bundle.py"],
                cwd=REPO,
                check=True,
            )
        if not ARCHIVE.is_file():
            raise unittest.SkipTest("build with: python3 scripts/build_research_bundle.py")
        cls.temporary = Path(tempfile.mkdtemp(prefix="research-kit-test-"))
        with tarfile.open(ARCHIVE, "r:gz") as archive:
            members = archive.getmembers()
            for member in members:
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts:
                    raise AssertionError(f"unsafe archive path: {member.name}")
                if member.issym() or member.islnk():
                    raise AssertionError(f"archive link is forbidden: {member.name}")
                if not (member.isfile() or member.isdir()):
                    raise AssertionError(f"unsupported archive member: {member.name}")
            # Safe on the repository's Python 3.11 after the checks above;
            # filter="data" is unavailable on this patch version.
            archive.extractall(cls.temporary)
        cls.root = cls.temporary / "research-workflow-kit"
        cls.cli = cls.root / "tools" / "research_kit.py"
        cls.manifest = json.loads((cls.root / "MANIFEST.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temporary)

    def run_cli(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(self.cli), *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_archive_checksum_and_manifest_summary(self) -> None:
        checksum, filename = (BUNDLE / "SHA256SUMS").read_text(encoding="utf-8").split()
        self.assertEqual(ARCHIVE.name, filename)
        self.assertEqual(checksum, hashlib.sha256(ARCHIVE.read_bytes()).hexdigest())
        summary = self.manifest["summary"]
        self.assertEqual(len(self.manifest["skills"]), summary["entries"])
        self.assertEqual(659, summary["bundledPayloads"])
        self.assertEqual(32, summary["metadataOnly"])
        self.assertEqual(26, summary["exactAliasesSuppressed"])
        source_pins = {item["id"]: item for item in self.manifest["sourcePins"]}
        self.assertEqual(12, len(source_pins))
        self.assertIn("openai-skills", source_pins)

    def test_manifest_profile_and_package_hash_verification(self) -> None:
        result = self.run_cli("verify")
        self.assertIn("VERIFY PASS: 659 payload packages", result.stdout)
        bundled = [item for item in self.manifest["skills"] if item["bundled"]]
        install_names = [item["installName"] for item in bundled]
        self.assertEqual(len(install_names), len(set(install_names)))
        for item in self.manifest["skills"]:
            self.assertIn("dependencies", item)
            self.assertIn("platformRequirements", item)
            if not item["bundled"]:
                continue
            package = self.root / item["payloadPath"]
            declarations = (
                item["dependencies"]["declarationFiles"]
                + item["platformRequirements"]["declarationFiles"]
            )
            for relative in declarations:
                self.assertTrue((package / relative).is_file(), f"missing declaration: {item['id']}::{relative}")

    def test_core_profile_clean_install_and_collision_handling(self) -> None:
        target = self.temporary / "core-install"
        result = self.run_cli("install", "--profile", "core", "--target", str(target))
        self.assertIn("Installed 17 skill package(s)", result.stdout)
        packages = [path for path in target.iterdir() if path.is_dir()]
        self.assertEqual(17, len(packages))
        self.assertTrue(all((path / "SKILL.md").is_file() for path in packages))
        self.assertTrue(all((path / "RESEARCH_KIT_PROVENANCE.json").is_file() for path in packages))
        failure = self.run_cli(
            "install", "--profile", "core", "--target", str(target), expected=1
        )
        self.assertIn("target exists", failure.stderr)
        forced = self.run_cli(
            "install", "--profile", "core", "--target", str(target), "--force"
        )
        self.assertIn("Installed 17 skill package(s)", forced.stdout)

    def test_metadata_only_payload_is_blocked_or_explicitly_skipped(self) -> None:
        blocked = next(
            item
            for item in self.manifest["skills"]
            if not item["bundled"] and item["sourceId"] == "hamelnb"
        )
        target = self.temporary / "metadata-install"
        failure = self.run_cli(
            "install", "--id", blocked["id"], "--target", str(target), expected=1
        )
        self.assertIn("metadata-only", failure.stderr)
        skipped = self.run_cli(
            "install",
            "--id",
            blocked["id"],
            "--target",
            str(target),
            "--skip-metadata-only",
        )
        self.assertIn("Installed 0 skill package(s)", skipped.stdout)

    def test_project_initialization_and_force_guard(self) -> None:
        target = self.temporary / "project"
        self.run_cli("init-project", str(target))
        self.assertTrue((target / "00-governance" / "research-charter.md").is_file())
        self.assertTrue((target / "03-evidence" / "claim-source-map.jsonl").is_file())
        self.assertTrue((target / "08-release" / "release-checklist.md").is_file())
        self.assertGreaterEqual(len([path for path in target.rglob("*") if path.is_file()]), 30)
        failure = self.run_cli("init-project", str(target), expected=1)
        self.assertIn("target is not empty", failure.stderr)

    def test_cli_rejects_path_traversal(self) -> None:
        spec = importlib.util.spec_from_file_location("research_kit_clean", self.cli)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with self.assertRaises(ValueError):
            module.safe_relative("../escape")
        with self.assertRaises(ValueError):
            module.safe_relative("/absolute")

    def test_profiles_include_required_routes(self) -> None:
        expected = {
            "core",
            "literature-evidence",
            "quantitative",
            "qualitative-mixed",
            "writing-publication",
            "ml-experiment",
            "life-science-vault",
            "ars-noncommercial",
            "everything",
        }
        actual = {path.stem for path in (self.root / "profiles").glob("*.json")}
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
