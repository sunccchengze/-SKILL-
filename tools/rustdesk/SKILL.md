---
name: rustdesk
description: Install, verify, and operate the repository-pinned RustDesk native remote-desktop client with explicit authorization and security boundaries. Use for RustDesk source/package setup, native runtime checks, or approved remote-support procedures. Never use it for covert, unauthorized, or persistent access.
---

# RustDesk native remote desktop

Use the stable source pin at `full-sources/tools/rustdesk`. RustDesk is a native GUI and remote-control system, not a browser preview.

## Installation workflow

1. Read `guides/TOOLS.md`, confirm the `1.4.9` source tag and exact commit, and identify the host OS/architecture.
2. Initialize the source checkout:

   ```bash
   bash scripts/setup_tools.sh rustdesk-source
   ```

3. Prefer an official OS package. On Debian-compatible x86_64 hosts, either let the helper retrieve the official release asset or provide an already downloaded official package:

   ```bash
   RUSTDESK_PACKAGE=/absolute/path/rustdesk-1.4.9-x86_64.deb \
     bash scripts/setup_tools.sh rustdesk-package
   ```

4. Validate package identity, version, architecture, nonzero size, and extraction before invoking it. The helper installs under `~/.local/share/rustdesk`; it does not alter system package state.
5. Run only in an interactive desktop session with explicit authorization:

   ```bash
   bash scripts/run_rustdesk.sh
   ```

6. Verify separately: source pin, package integrity/metadata, dynamic-library readiness, GUI launch, and an authorized connection. Do not collapse these into one “installed” claim.

## Security rules

- Obtain informed authorization from the owner of every endpoint and session.
- Show the user when control, clipboard, audio, file transfer, tunneling, or unattended access is active.
- Use least privilege, strong credentials, current server/client versions, and a trusted relay or self-hosted deployment when required.
- Do not bypass consent prompts, hide execution, weaken endpoint controls, harvest credentials, or create persistence.
- Redact IDs, passwords, addresses, logs, screenshots, and transferred files from reports.

## Failure handling

If an official release asset cannot be reached, keep the verified source checkout and report binary installation as blocked. Do not substitute an unverified mirror or claim that a source gitlink is a runnable GUI.
