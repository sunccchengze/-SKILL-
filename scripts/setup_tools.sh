#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_BIN="${HOME}/.local/bin"
LOCAL_SHARE="${HOME}/.local/share"
BUN_VERSION="1.3.11"
SPEC_KIT_VERSION="0.16.4"
RUSTDESK_VERSION="1.4.9"
RUSTDESK_DEB_NAME="rustdesk-${RUSTDESK_VERSION}-x86_64.deb"
RUSTDESK_DEB_SIZE="23375776"

mkdir -p "$LOCAL_BIN" "$LOCAL_SHARE"

init_submodule() {
  git -C "$REPO_ROOT" submodule update --init "$1"
}

setup_opencut() {
  local source="$REPO_ROOT/full-sources/tools/opencut"
  init_submodule full-sources/tools/opencut
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm is required to install the pinned Bun runtime." >&2
    return 1
  fi
  if [[ ! -x "$LOCAL_BIN/bun" ]] || [[ "$($LOCAL_BIN/bun --version 2>/dev/null || true)" != "$BUN_VERSION" ]]; then
    npm install --global --prefix "$HOME/.local" "bun@${BUN_VERSION}"
  fi
  (
    cd "$source/apps/web"
    "$LOCAL_BIN/bun" install --no-save
  )
  echo "OpenCut web dependencies are ready (Bun $BUN_VERSION)."
}

setup_spec_kit() {
  local source="$REPO_ROOT/full-sources/tools/spec-kit"
  local venv="$LOCAL_SHARE/specify-cli/venv"
  init_submodule full-sources/tools/spec-kit
  python3 -m venv "$venv"
  "$venv/bin/python" -m pip install --disable-pip-version-check --upgrade "$source"
  ln -sfn "$venv/bin/specify" "$LOCAL_BIN/specify"
  local installed
  installed="$($LOCAL_BIN/specify --version)"
  if [[ "$installed" != "specify $SPEC_KIT_VERSION" ]]; then
    echo "Unexpected Specify CLI version: $installed" >&2
    return 1
  fi
  echo "$installed"
}

setup_rustdesk_source() {
  init_submodule full-sources/tools/rustdesk
  local actual
  actual="$(git -C "$REPO_ROOT/full-sources/tools/rustdesk" rev-parse HEAD)"
  if [[ "$actual" != "6c578292e8ebbbec708b76986ba8c4bc7c509747" ]]; then
    echo "Unexpected RustDesk source commit: $actual" >&2
    return 1
  fi
  echo "RustDesk $RUSTDESK_VERSION source is ready at $actual."
}

setup_rustdesk_package() {
  setup_rustdesk_source
  local install_root="$LOCAL_SHARE/rustdesk"
  local package="${RUSTDESK_PACKAGE:-$install_root/$RUSTDESK_DEB_NAME}"
  local official_url="https://github.com/rustdesk/rustdesk/releases/download/${RUSTDESK_VERSION}/${RUSTDESK_DEB_NAME}"
  mkdir -p "$install_root"

  if [[ -n "${RUSTDESK_PACKAGE:-}" ]]; then
    if [[ ! -f "$package" ]]; then
      echo "RUSTDESK_PACKAGE does not exist: $package" >&2
      return 1
    fi
  elif [[ ! -f "$package" ]] || [[ "$(stat -c %s "$package" 2>/dev/null || echo 0)" != "$RUSTDESK_DEB_SIZE" ]]; then
    rm -f "$package.part"
    if ! curl --fail --location --proto '=https' --tlsv1.2 \
      --retry 4 --retry-all-errors --connect-timeout 30 \
      --output "$package.part" "$official_url"; then
      rm -f "$package.part"
      cat >&2 <<EOF
The official RustDesk release asset could not be downloaded.
Download $RUSTDESK_DEB_NAME from the official RustDesk release page on a
network that can reach GitHub release assets, then rerun:
  RUSTDESK_PACKAGE=/absolute/path/$RUSTDESK_DEB_NAME bash scripts/setup_tools.sh rustdesk-package
No mirror is substituted automatically.
EOF
      return 1
    fi
    mv "$package.part" "$package"
  fi

  local size pkg version arch
  size="$(stat -c %s "$package")"
  pkg="$(dpkg-deb -f "$package" Package)"
  version="$(dpkg-deb -f "$package" Version)"
  arch="$(dpkg-deb -f "$package" Architecture)"
  if [[ "$size" != "$RUSTDESK_DEB_SIZE" || "$pkg" != "rustdesk" || "$version" != "$RUSTDESK_VERSION" || "$arch" != "amd64" ]]; then
    echo "RustDesk package validation failed: size=$size package=$pkg version=$version arch=$arch" >&2
    return 1
  fi

  rm -rf "$install_root/root"
  dpkg-deb --extract "$package" "$install_root/root"
  if [[ ! -x "$install_root/root/usr/bin/rustdesk" ]]; then
    echo "Validated package did not contain usr/bin/rustdesk." >&2
    return 1
  fi
  sha256sum "$package" > "$install_root/SHA256SUMS.local"
  cat > "$LOCAL_BIN/rustdesk" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
root="${HOME}/.local/share/rustdesk/root"
export LD_LIBRARY_PATH="$root/usr/lib:$root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "$root/usr/bin/rustdesk" "$@"
EOF
  chmod +x "$LOCAL_BIN/rustdesk"
  echo "RustDesk package $version ($arch) extracted under $install_root/root."
  echo "A native desktop session and compatible host libraries are still required."
}

usage() {
  cat <<'EOF'
Usage: bash scripts/setup_tools.sh <target>

Targets:
  opencut           Install Bun 1.3.11 and OpenCut web dependencies.
  spec-kit          Install Specify CLI 0.16.4 in a user-local virtualenv.
  rustdesk-source   Initialize and verify the pinned RustDesk 1.4.9 source.
  rustdesk-package  Validate and extract the official x86_64 Debian package.
  all               Set up OpenCut, Spec Kit, and the safe RustDesk source pin.

For rustdesk-package, set RUSTDESK_PACKAGE to an official package already on disk
when direct GitHub release-asset downloads are unavailable.
EOF
}

case "${1:-}" in
  opencut) setup_opencut ;;
  spec-kit) setup_spec_kit ;;
  rustdesk-source) setup_rustdesk_source ;;
  rustdesk-package) setup_rustdesk_package ;;
  all)
    setup_opencut
    setup_spec_kit
    setup_rustdesk_source
    ;;
  -h|--help|help) usage ;;
  *) usage >&2; exit 2 ;;
esac
