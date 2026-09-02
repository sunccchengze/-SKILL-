# Council corpus schema

This document explains field semantics. Draft 2020-12 schemas and the machine-readable data-file mapping live in [`../schemas/`](../schemas/README.md) and [`../schemas/manifest.json`](../schemas/manifest.json).

## Canonical ownership

- `creators.json` owns member identity, role, broad evidence profile and creator-level caveats.
- `../sources/sources.jsonl` owns URL, platform, content ID, title, dates, modality, extraction coverage, uploader status and source-level commercial disclosure.
- `claims.jsonl` owns atomic, retrievable propositions and refers to sources **only by `source_ids`**.
- `../governance/` owns routing, disagreements, conflicts and integrity policy.

Claims must not duplicate source URL, title, platform or publication date.

## `creators.json`

Top-level fields:

- `schema_version`
- `checked_at`
- `creators`: exactly the fixed 12-member first batch

Each creator has:

- `creator_id`, `display_name`, `canonical_name`
- `platforms`, `languages`
- `council_role`, `strengths`
- `evidence_profile`, `commercial_disclosure`, `integrity_flags`, `identity_note`

A role is a routing hint, not proof that every topic has steps-level evidence.

## `sources.jsonl`

One JSON object per canonical source:

```json
{
  "source_id": "SRC-AMINA-001",
  "creator_id": "amina-yonis",
  "platform": "youtube",
  "content_id": "...",
  "title": "...",
  "url": "https://...",
  "published_at": "YYYY-MM-DD or null",
  "fetched_at": "YYYY-MM-DD",
  "modality": "creator_transcript",
  "extraction_coverage": "what was actually available",
  "directness": "direct",
  "status": "live",
  "original_uploader": true,
  "language": "en",
  "commercial_disclosure": "...",
  "notes": "..."
}
```

`modality` values currently used:

- `creator_transcript`
- `creator_authored_outline`
- `creator_description`
- `institutional_profile`
- `secondary_summary`
- `related_video_metadata`
- `mediated_export`

A source may contain transcript plus description; `extraction_coverage` states the full accessible bundle. A claim records the modality that supports that specific proposition.

## `claims.jsonl`

Each line contains one independently retrievable proposition:

```json
{
  "claim_id": "ARC-0039",
  "creator_id": "amina-yonis",
  "statement": "忠实转述的一条原子命题",
  "statement_type": "creator_statement",
  "evidence_modality": "creator_transcript",
  "coverage": "full_transcript",
  "confidence": "high",
  "source_ids": ["SRC-AMINA-001"],
  "topics": ["引文核验"],
  "keywords": ["Scite"],
  "route_tags": ["literature", "ai-workflow"],
  "actions": ["可执行但不扩大原意的转化"],
  "warnings": ["适用条件或证据缺口"],
  "status": "active",
  "directness": "direct",
  "checked_at": "2026-08-16"
}
```

Optional `inherited_claim_ids` link a Zoey council record to the provisional record in `zoey-skill`; it does not upgrade that record.

### `statement_type`

- `creator_statement`: source supports a content proposition.
- `description_level_summary`: the creator description defines scope or product positioning.
- `title_level_theme`: only the existence of a theme is known.
- `institutional_fact`: narrow fact from an institution page.
- `secondary_summary`: a secondary author summarized the creator.
- `commercial_disclosure`: a commercial context fact.
- `risk_notice`: a record needed to prevent unsafe or misleading routing.

### `coverage`

- `full_transcript`: a complete fetchable transcript was inspected.
- `creator_outline`: a detailed creator-authored outline was inspected.
- `institutional_page`: an institution page supports only the named fact.
- `title_description_only`: no transcript; never infer hidden steps.
- `related_collection_metadata`: route-level metadata only.
- `channel_metadata_only`: channel/video listing only.
- `secondary_article`: content is a secondary summary.
- `partial_mediated_export`: user-mediated export with incomplete primary coverage.
- `creator_page_and_description`: combined creator article/page and description evidence.

### `directness`

- `direct`: the relevant creator/institution material itself supports the narrow statement.
- `indirect`: a mediated export relays it without independent primary verification.
- `secondary`: another author summarizes it.

Directness does not imply full extraction. A video title can directly prove that a theme exists while proving none of its steps.

### `confidence`

- `high`: the narrow proposition and its provenance are strongly supported. A title-level claim can be high confidence only about the title/theme itself.
- `medium`: direct but incomplete, description-level, or mediated evidence supports a limited proposition.
- `low`: secondary, compressed, contextual or especially uncertain evidence.

Confidence measures attribution support, not universal validity or causal effect.

### `status`

- `active`: may be retrieved, subject to evidence labels.
- `context_only`: identity, disclosure, scope or limitation; only shown for explicit context queries or maintenance.
- `quarantined`: never returned as legitimate advice. Used for detector evasion, outcome guarantees and unsafe marketing claims.

## Governance joins

- `routing.json` references `creator_id` values.
- `disagreements.jsonl` references `claim_id` values.
- `commercial-conflicts.jsonl` has exactly one row per creator and references canonical `source_id` values.
- `integrity-rules.json` may reference only claims whose status is `quarantined`.
- `false-positives.json` content IDs may not occur in the source ledger. Both validator and retriever enforce this.
