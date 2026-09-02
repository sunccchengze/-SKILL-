---
name: official-source-router
description: Route product- and platform-specific work across 859 pinned skill entry paths from OpenAI, Vercel, and Microsoft official repositories. Use when selecting a first-party workflow, resolving duplicate skill names, initializing an official source, checking provenance or license boundaries, or combining official skills with the repository's maintained workflows.
---

# Official Source Router

Use the official-source layer when publisher-specific behavior, current platform conventions, or an upstream-complete package matters. Treat “official” as provenance—not as a universal license or automatic permission to execute side effects.

## Route

1. Convert the request into platform, deliverable, action, environment, and risk terms.
2. Search all catalog layers:

   ```bash
   python scripts/search_skills.py "<platform> <deliverable> <action>" --json
   ```

3. Compare candidates by `sourceId`, `path`, description, fixed commit, and license. Keep same-name records distinct.
4. Prefer:
   - a repository-maintained entry for repository governance or cross-source orchestration;
   - the publisher's current official source for product-specific implementation;
   - `openai-plugins` over the upstream-deprecated `openai-skills` when both cover the task;
   - a legacy source only when the current source lacks the required workflow or exact reproduction is required.
5. Initialize only the selected source if its path is absent:

   ```bash
   git submodule update --init <submodule-path>
   ```

6. Read the complete package: `SKILL.md`, references, scripts, dependency files, `LICENSE*`, `NOTICE*`, and connector configuration.
7. Execute with the normal safety gates. Obtain explicit confirmation before writes, deploys, sends, deletes, payments, permission changes, or production actions.

## Resolve duplicates

A display name is not a unique identity. Use `sourceId:path` from `catalog/official-skills.json`.

Install by source when names collide:

```bash
python scripts/install_skills.py \
  --name <exact-name> \
  --source <source-id> \
  --target <agent-skill-directory>
```

If one source contains the same name at multiple paths, also pass the exact `--path`. Selection without those filters remains deterministic, but an explicit path is required whenever the packages have materially different scope.

## License gate

Before copying, modifying, or redistributing a package:

- do not infer one repository-wide license from its publisher;
- follow each package's actual license and nested notices;
- treat `openai-plugins` as mixed/per-plugin and `openai-skills` as per-skill;
- note that the Vercel fixed README declares MIT while its fixed tree lacks an independent root license file;
- apply Microsoft's root MIT license together with any nested notices or third-party terms.

Do not route installation or redistribution through the inherited Anthropic `docx`, `pdf`, `pptx`, or `xlsx` community snapshots unless the applicable Anthropic agreement expressly permits it. Their included licenses restrict extraction/retention outside the services, copying, derivative works, and distribution.

## Deliverable

Report:

- selected skill name, `sourceId`, and exact path;
- why it outranked alternatives;
- fixed source commit and stated license label;
- whether source initialization is required;
- required credentials, dependencies, and side-effect confirmations;
- any unresolved license or execution risk.

See `guides/OFFICIAL_SOURCES.md` for source pins, commands, status, and detailed legal boundaries.
