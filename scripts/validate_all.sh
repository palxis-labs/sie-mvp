#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[1/4] Verify envelope trust"
"$PYTHON_BIN" sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json

echo "[2/4] Verify envelope + file binding"
"$PYTHON_BIN" sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md

echo "[3/4] Run unit tests"
"$PYTHON_BIN" -m unittest discover -s tests -p "test_*.py" -v

echo "[4/4] Validation complete"
