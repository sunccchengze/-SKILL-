#!/usr/bin/env python3
"""Regression coverage for preferred overlap search and installation behavior."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FOCUSED_NAMES = {
    "applicationinsights-web-ts",
    "chroma",
    "gh-address-comments",
    "popular-web-designs",
}


class OverlapBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        policy = json.loads(
            (REPO / "catalog/overlap-policy.json").read_text(encoding="utf-8")
        )
        catalogs = [
            json.loads((REPO / relative).read_text(encoding="utf-8"))
            for relative in (
                "catalog/skills.json",
                "catalog/research-skills.json",
                "catalog/official-skills.json",
                "catalog/curated-skills.json",
            )
        ]
        cls.records_by_path = {
            record["path"]: record
            for catalog in catalogs
            for record in catalog["skills"]
        }
        cls.alias_by_name = {
            cls.records_by_path[alias["path"]]["name"]: alias
            for alias in policy["aliases"]
            if cls.records_by_path[alias["path"]]["name"] in FOCUSED_NAMES
        }
        if set(cls.alias_by_name) != FOCUSED_NAMES:
            raise AssertionError("focused overlap fixtures are missing or ambiguous")

    def search(self, name: str, include_aliases: bool = False) -> list[dict[str, object]]:
        command = [
            sys.executable,
            "scripts/search_skills.py",
            name,
            "--json",
            "--limit",
            "100",
        ]
        if include_aliases:
            command.insert(-3, "--include-aliases")
        return json.loads(subprocess.check_output(command, cwd=REPO, text=True))

    def install_dry_run(self, *arguments: str) -> str:
        with tempfile.TemporaryDirectory() as target:
            return subprocess.check_output(
                [
                    sys.executable,
                    "scripts/install_skills.py",
                    *arguments,
                    "--target",
                    target,
                    "--dry-run",
                ],
                cwd=REPO,
                text=True,
            )

    def test_search_prefers_canonical_and_can_expand_aliases(self) -> None:
        for name, alias in self.alias_by_name.items():
            with self.subTest(name=name):
                canonical_path = alias["canonicalPath"]
                alias_path = alias["path"]

                default_results = self.search(name)
                default_paths = {record["path"] for record in default_results}
                self.assertIn(canonical_path, default_paths)
                self.assertNotIn(alias_path, default_paths)

                expanded_results = self.search(name, include_aliases=True)
                expanded_by_path = {
                    record["path"]: record for record in expanded_results
                }
                self.assertEqual(
                    expanded_by_path[alias_path]["aliasOf"], canonical_path
                )
                self.assertEqual(
                    expanded_by_path[alias_path]["aliasReason"], alias["reason"]
                )
                expanded_paths = [record["path"] for record in expanded_results]
                self.assertLess(
                    expanded_paths.index(canonical_path),
                    expanded_paths.index(alias_path),
                )

    def test_installer_defaults_and_explicit_alias_access(self) -> None:
        checks = [
            (("--name", "gh-address-comments"), "openai-plugins"),
            (
                ("--name", "gh-address-comments", "--source", "openai-skills"),
                "alias: superseded-source",
            ),
            (("--name", "chroma"), "[hermes-agent"),
            (
                ("--name", "chroma", "--source", "ai-research-skills"),
                "alias: equivalent-instruction-body",
            ),
            (("--name", "popular-web-designs"), "[popular-web-designs"),
            (
                ("--name", "popular-web-designs", "--source", "hermes-agent"),
                "alias: host-specific-alias",
            ),
            (
                ("--name", "applicationinsights-web-ts"),
                ".github/skills/applicationinsights-web-ts",
            ),
            (
                (
                    "--name",
                    "applicationinsights-web-ts",
                    "--path",
                    self.alias_by_name["applicationinsights-web-ts"]["path"],
                ),
                "alias: packaging-duplicate",
            ),
        ]
        for arguments, expected in checks:
            with self.subTest(arguments=arguments):
                self.assertIn(expected, self.install_dry_run(*arguments))


if __name__ == "__main__":
    unittest.main()
