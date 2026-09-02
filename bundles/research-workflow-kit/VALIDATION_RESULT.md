# Release Validation Result

Validated on **2026-08-16 (Asia/Shanghai)** from branch `arena/019ffbe9-skill`.

> This release-side record is intentionally outside the archive: embedding the archive's own checksum inside itself would be recursive. `SHA256SUMS` is the machine-readable source of truth.

## Artifact

- File: `research-workflow-kit.tar.gz`
- Bytes: `55,157,169` (52.60 MiB)
- SHA-256: `6cae45488511c86a9231d8c64713b1ce683e30b148c92ed19264568bcab34942`
- Manifest: 691 entries; 659 bundled payloads; 32 metadata-only; 26 exact aliases suppressed
- Profiles: 9
- Project-template files: 33

## Executed validation

1. `python3 scripts/build_research_bundle.py` was run twice against the pinned local source commits. Both builds produced the exact SHA-256 above.
2. `(cd bundles/research-workflow-kit && sha256sum -c SHA256SUMS)` returned `research-workflow-kit.tar.gz: OK`.
3. The archive was extracted to a fresh `/tmp` directory. From that extraction:
   - `python3 tools/research_kit.py doctor` returned `Quick doctor: PASS`;
   - `python3 tools/research_kit.py verify` returned `VERIFY PASS: 659 payload packages, 9 profiles, 691 manifest entries`;
   - `core` listed and installed 17 collision-safe packages into a new target;
   - all 17 installed packages contained provenance records;
   - `init-project` created all 33 template files;
   - local metadata search returned ranked payload records.
4. `python3 -m unittest discover -s tests -v` passed all 11 repository tests, including 7 clean-room bundle tests for checksum, archive safety, manifest/hash verification, profile install, collisions, metadata-only blocking, path traversal rejection, and project initialization.
5. `python3 scripts/validate_repository.py` exited 0. It reported only pre-existing warnings for uninitialized unrelated official/curated submodules and aggregate collections without a discoverable collection-level license.

## Reproduce

```bash
cd bundles/research-workflow-kit
sha256sum -c SHA256SUMS
cd ../..
python3 -m unittest tests/test_research_bundle.py -v
python3 scripts/validate_repository.py
```
