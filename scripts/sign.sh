#!/usr/bin/env bash
set -euo pipefail

ISSUER="${1:-palxislabs}"
TARGET="${2:-SKILL.md}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" sie_sign.py --issuer "$ISSUER" --infile "$TARGET"
