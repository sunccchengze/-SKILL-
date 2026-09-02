from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "references" / "schemas"


class SchemaContractTests(unittest.TestCase):
    def test_manifest_maps_parseable_data_to_draft_2020_12_schemas(self) -> None:
        manifest = json.loads((SCHEMA_DIR / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["json_schema_draft"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(len(manifest["mappings"]), 8)

        for mapping in manifest["mappings"]:
            with self.subTest(data_file=mapping["data_file"]):
                data_path = ROOT / mapping["data_file"]
                schema_path = ROOT / mapping["schema_file"]
                self.assertTrue(data_path.is_file())
                self.assertTrue(schema_path.is_file())

                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                self.assertIn("$id", schema)

                if mapping["format"] == "json-document":
                    json.loads(data_path.read_text(encoding="utf-8"))
                else:
                    self.assertEqual(mapping["format"], "jsonl-record")
                    rows = [
                        json.loads(line)
                        for line in data_path.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ]
                    self.assertTrue(rows)


if __name__ == "__main__":
    unittest.main()
