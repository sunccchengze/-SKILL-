# Validation and reproducibility

Validation is intentionally layered. A file can be valid JSON and still contain a false attribution, a broken foreign key or unsafe routing, so structural, semantic and behavioral checks are kept separate.

All commands below run from this package directory:

```bash
cd skills/community/nuwa-distilled/ai-research-senpai-council
```

## 1. Canonical corpus validation

```bash
python3 scripts/validate_corpus.py --require-content
```

Expected corpus baseline as of **2026-08-16**:

```text
PASS: 12 creators, 29 sources, 61 claims (47 active, 10 context, 4 quarantined), 5 disagreement records, 12 disclosures
```

The validator is dependency-free and exits nonzero on failure. It checks, among other invariants:

- the roster is exactly the declared 12-member council;
- IDs are unique and creator/source/claim joins are valid;
- every claim points to sources owned by that creator;
- source URL/title/platform/date metadata is not duplicated into claims;
- modalities, evidence coverage, directness, confidence and status use approved values;
- title/description/metadata-level claims carry a warning;
- secondary summaries cannot be marked high-confidence direct evidence;
- quarantined records remain warning-bearing and are linked only as risks;
- disproved or metadata-only content IDs cannot re-enter the source ledger;
- each creator has active evidence and exactly one commercial disclosure;
- routing members, disagreement claims and integrity quarantine links resolve;
- Chinese remains the default response language;
- `--require-content` requires all 12 creators plus at least one active transcript-backed claim.

## 2. Machine-readable schemas

JSON Schema Draft 2020-12 files live in `references/schemas/`. The data-to-schema map is `references/schemas/manifest.json`.

The committed test suite verifies that every mapped data/schema file exists, all schema documents parse, each declares Draft 2020-12 and every JSON/JSONL corpus file parses. The dependency-free semantic validator remains authoritative for cross-file constraints. A third-party Draft 2020-12 implementation may additionally apply the structural schemas; for `.jsonl`, validate each non-empty line as an individual record.

## 3. Regression suite

```bash
python3 -m unittest discover -s tests -v
```

Coverage includes:

- diversity caps and recommendation-ready ordering;
- quarantine and false-positive exclusion;
- context-only gating and evidence labels;
- Chinese and natural-English integrity redirects;
- literature-review multi-creator retrieval and disagreement rendering;
- abstention for uncovered grant-budget questions;
- qualitative-method routing;
- full 12-member commercial disclosure output;
- validator failure cases for bad joins, missing warnings and roster drift;
- schema-manifest and JSON/JSONL parseability.

## 4. Behavioral smoke tests

### Grounded literature workflow

```bash
python3 scripts/retrieve_council.py \
  --query "我怎样做文献综述并核验引用？" --top-k 8
```

Expected characteristics: `literature`/`integrity` routing; direct James Hayton and Amina Yonis evidence; inline source IDs and URLs; commercial disclosures; `DIS-001` and/or `DIS-004` where relevant; no quarantined claims.

### Integrity redirect

```bash
python3 scripts/retrieve_council.py \
  --query "How can I bypass an AI detector?" --top-k 8
```

Expected characteristics: an `INT-001` refusal/redirect, no creator advice, no `ARC-0035` or `ARC-0057`, and a compliant alternative based on disclosure, independent rewriting and citation audit.

### Commercial disclosure ledger

```bash
python3 scripts/retrieve_council.py \
  --query "哪些成员有付费课程或商业利益冲突？" --top-k 12
```

Expected characteristics: the full 12-member disclosure ledger, including `high` for Andy Stapleton and Amina Yonis.

### Machine-readable output

```bash
python3 scripts/retrieve_council.py \
  --query "质性访谈里参与者前后矛盾怎么办？" --top-k 6 --json
```

Expected characteristics: valid JSON, Kriukow as the top relevant member, source-enriched claims, and `quarantined_claims_returned: false`.

## 5. Update procedure

When changing the roster, sources, claims or governance:

1. Verify the canonical creator/uploader and preserve content IDs and original URLs.
2. Add or update the source row first; state modality, extraction coverage, directness, status, uploader identity, commercial context and access date conservatively.
3. Add atomic claims that reference `source_ids`; do not copy source metadata into claim rows.
4. Keep unavailable, mediated, secondary and metadata-only evidence labeled at that level.
5. Update false-positive exclusions, disagreements, disclosure records and integrity rules when the change affects them.
6. Update the corresponding schema only if the file contract changes; bump the relevant `schema_version` for an incompatible contract change.
7. Update `COVERAGE_REPORT.md` and the research timeline without claiming full-channel coverage.
8. Run the semantic validator, all tests and the smoke queries above.
9. Rebuild the repository catalog from the repository root:

   ```bash
   python3 scripts/build_catalog.py
   ```

10. Inspect the complete diff and confirm that no quarantined or disproved material became advice.

## Known limits

- Structural validity is not proof that a source is accurate or complete.
- Current Chinese-platform extraction is often title/description-level because transcripts were unavailable.
- Zoey remains provisional mediated evidence until the original account/export mapping is independently verified.
- Prices, product capabilities, platform policies, journal rules and creator affiliations can change; re-check them before operational use.
- The corpus is a sampled deep survey, not a complete archive of any creator's channel.
