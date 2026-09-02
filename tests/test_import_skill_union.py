#!/usr/bin/env python3
"""Focused tests for compact instructional-body identity."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from import_skill_union import instructional_sha256, normalized_instruction_bytes  # noqa: E402


class InstructionIdentityTests(unittest.TestCase):
    def test_frontmatter_line_endings_and_outer_space_do_not_change_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packaged = root / "packaged.md"
            plain = root / "plain.md"
            packaged.write_bytes(
                b"---\r\nname: example\r\ndescription: Packaged copy\r\n---\r\n\r\n"
                b"# Instructions\r\n\r\nDo the work.\r\n"
            )
            plain.write_bytes(b"\n# Instructions\n\nDo the work.\n\n")

            self.assertEqual(
                normalized_instruction_bytes(packaged),
                b"# Instructions\n\nDo the work.",
            )
            self.assertEqual(
                instructional_sha256(packaged), instructional_sha256(plain)
            )

    def test_instruction_changes_remain_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first.md"
            second = root / "second.md"
            first.write_text("# Instructions\n\nDo A.\n", encoding="utf-8")
            second.write_text("# Instructions\n\nDo B.\n", encoding="utf-8")

            self.assertNotEqual(
                instructional_sha256(first), instructional_sha256(second)
            )


if __name__ == "__main__":
    unittest.main()
