---
name: opencut
description: Install, run, inspect, and verify the repository-pinned OpenCut web video editor locally. Use for OpenCut setup, local preview, editor troubleshooting, or changes to the pinned OpenCut source. Do not use it as a generic video-editing substitute when no OpenCut runtime is involved.
---

# OpenCut local editor

Use the repository-pinned source at `full-sources/tools/opencut`, not an unpinned clone.

## Standard workflow

1. Read `guides/TOOLS.md` and confirm the pinned commit in `catalog/sources.lock.json`.
2. Install user-local prerequisites and web dependencies:

   ```bash
   bash scripts/setup_tools.sh opencut
   ```

3. Run the browser app on an explicit host and port:

   ```bash
   HOST=0.0.0.0 PORT=5173 bash scripts/run_opencut.sh
   ```

4. Verify the returned page over HTTP, then exercise the requested editor path in a browser.
5. Before changing source, inspect the current upstream architecture: the pinned `main` includes both web work and newer desktop foundations and may differ from older OpenCut tutorials.
6. Keep `node_modules`, generated route files, build output, and caches untracked. Commit only intentional source changes in an appropriate upstream workflow; this repository normally records only the gitlink.

## Completion evidence

Report the exact pinned commit, Bun version, URL, HTTP result, and the interaction actually tested. A listening port alone is not proof that editor behavior works.

## Boundaries

- Imported media may be sensitive; do not upload or transmit it without permission.
- Do not expose the development server beyond the requested environment.
- Treat third-party codecs, fonts, and generated media according to their own licenses.
- If Cloudflare request metadata cannot be fetched during local startup, distinguish a non-fatal development fallback from an application failure.
