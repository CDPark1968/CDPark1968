#!/usr/bin/env bash
# Install obsidian-cli (notesmd-cli) for interacting with Obsidian vaults from the terminal

set -euo pipefail

VERSION="v0.3.6"
INSTALL_DIR="/usr/local/bin"
BINARY_NAME="obsidian-cli"

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64) ARCH="amd64" ;;
  arm64|aarch64) ARCH="arm64" ;;
  *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

TARBALL="notesmd-cli_${VERSION#v}_${OS}_${ARCH}.tar.gz"
URL="https://github.com/Yakitrak/notesmd-cli/releases/download/${VERSION}/${TARBALL}"

echo "Downloading obsidian-cli ${VERSION} for ${OS}/${ARCH}..."
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

curl -fsSL "$URL" -o "${TMP_DIR}/${TARBALL}"
tar -xzf "${TMP_DIR}/${TARBALL}" -C "$TMP_DIR"

EXTRACTED=$(find "$TMP_DIR" -name "notesmd-cli" -type f | head -1)
if [ -z "$EXTRACTED" ]; then
  echo "Error: binary not found in archive"
  exit 1
fi

install -m 755 "$EXTRACTED" "${INSTALL_DIR}/notesmd-cli"

if [ ! -f "${INSTALL_DIR}/${BINARY_NAME}" ]; then
  ln -s "${INSTALL_DIR}/notesmd-cli" "${INSTALL_DIR}/${BINARY_NAME}"
fi

echo "Installed: $(notesmd-cli --version)"
echo ""
echo "Usage:"
echo "  notesmd-cli --help"
echo "  obsidian-cli --help  (symlink)"
echo ""
echo "Quick start:"
echo "  notesmd-cli add-vault <vault-name> <vault-path>"
echo "  notesmd-cli list-vaults"
echo "  notesmd-cli open <note-name>"
