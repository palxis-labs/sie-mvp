#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SMOKE_DIR="${SMOKE_DIR:-$REPO_ROOT/.tmp-smoke}"

rm -rf "$SMOKE_DIR"
mkdir -p "$SMOKE_DIR"

"$PYTHON_BIN" -m venv "$SMOKE_DIR/venv"
source "$SMOKE_DIR/venv/bin/activate"

python -m pip install --upgrade pip build
python -m build "$REPO_ROOT"
python -m pip install "$REPO_ROOT"/dist/*.whl

cd "$REPO_ROOT"

echo "[1/3] CLI entrypoint check"
sie-verify --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md

echo "[2/3] Module check"
python -m sie_verify --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md

echo "[3/3] Unit tests"
python -m unittest discover -s tests -p "test_*.py" -v

echo "[OK] Release smoke validation complete"
