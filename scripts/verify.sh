#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-SKILL.md.sie.json}"
KEYRING="${2:-trusted_issuers.json}"
TARGET="${3:-SKILL.md}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" sie_verify.py --file "$FILE" --trusted-issuers "$KEYRING" --check-file "$TARGET"
