# Machine-readable schemas

This directory declares the structural contracts for the council's eight canonical corpus and governance files. All schemas use **JSON Schema Draft 2020-12**.

`manifest.json` is the machine-readable map from each data file to its schema. For a `jsonl-record` mapping, validate **each non-empty line as one independent JSON object**; do not validate the whole `.jsonl` file as a JSON array.

| Data | Schema |
|---|---|
| `knowledge/creators.json` | `creators.schema.json` |
| `knowledge/claims.jsonl` | `claim-record.schema.json` |
| `sources/sources.jsonl` | `source-record.schema.json` |
| `sources/false-positives.json` | `false-positives.schema.json` |
| `governance/routing.json` | `routing.schema.json` |
| `governance/disagreements.jsonl` | `disagreement-record.schema.json` |
| `governance/commercial-conflicts.jsonl` | `commercial-conflict-record.schema.json` |
| `governance/integrity-rules.json` | `integrity-rules.schema.json` |

## Division of responsibility

- Schemas validate record shape, required fields, data types, ID patterns, local enums and selected conditional rules.
- `scripts/validate_corpus.py` validates cross-file and semantic invariants: unique IDs, the fixed 12-member roster, source/claim ownership, false-positive exclusion, required active coverage, disagreement links, quarantined-claim links and exactly one disclosure per creator.
- `references/knowledge/SCHEMA.md` explains field meaning and provenance ownership in human-readable form.

Schemas do not make a weak source strong. Evidence modality, directness, status, confidence, warnings and commercial context remain substantive review decisions.
