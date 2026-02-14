# RELEASE_CHECKLIST.md — Security + Packaging Release Gate

Run this checklist before tagging a release.

## 0) Clean-environment installability
- [x] Build artifacts from source:
  - `python3 -m pip install --upgrade pip build`
  - `python3 -m build .`
  - Latest evidence: 2026-02-14 `.venv/bin/python -m pip install --upgrade pip build` + `.venv/bin/python -m build .` succeeded (fallback to project `.venv` required because host `python3 -m pip` is PEP668 externally-managed); full log: `docs/validation-clean-install-20260214-1839Z.log`.
- [x] Install the generated wheel in a fresh virtual environment:
  - `python3 -m venv .tmp-release-venv`
  - `source .tmp-release-venv/bin/activate`
  - `python -m pip install dist/*.whl`
  - Latest evidence: 2026-02-14 `python3 -m venv .tmp-release-venv` + `.tmp-release-venv/bin/python -m pip install dist/*.whl` -> `Successfully installed ... sie-mvp-0.1.0` (`docs/validation-clean-install-20260214-1839Z.log`).
- [x] Installed entrypoints run:
  - `sie-verify --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
  - `python -m sie_verify --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
  - Latest evidence: 2026-02-14 `.tmp-release-venv/bin/sie-verify ...` and `.tmp-release-venv/bin/python -m sie_verify ...` both returned `[OK] Signature verified and basic checks passed.` (`docs/validation-clean-install-20260214-1839Z.log`).

## 1) Correctness
- [x] Verification command passes:
  - `python3 sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
  - Latest evidence: 2026-02-14 `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] Signature verified and basic checks passed.`
- [x] Tests pass:
  - `python3 -m unittest discover -s tests -p "test_*.py" -v`
  - Latest evidence: 2026-02-14 `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v` -> `Ran 40 tests ... OK`

## 2) Security posture
- [x] Trusted issuer file reviewed
  - Latest evidence: 2026-02-14 `.venv/bin/python - <<'PY' ...` decoded `trusted_issuers.json` -> `issuers=1`, `palxislabs` key length `32 bytes` (valid Ed25519 public key size)
- [x] No private keys in repo
  - Latest evidence: 2026-02-14 `grep -R --line-number --exclude-dir=.git -E "BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY|PRIVATE KEY-----" .` -> no matches
- [x] Security claims reviewed against `docs/SECURITY_CLAIMS.md`
  - Latest evidence: 2026-02-14 manual doc sweep (`README.md`, `docs/SECURITY_QUICKSTART.md`, `docs/OPENCLAW_INTEGRATION.md`, `docs/FAILURE_MODES.md`) confirms claims stay within allowed scope (integrity/authenticity/fail-closed/channel separation) and keep explicit non-goals.

## 3) Operator readiness
- [x] Quickstart commands still valid
  - Latest evidence: 2026-02-14 `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] ...`; `PYTHON_BIN=.venv/bin/python ./scripts/verify.sh` -> `[OK] ...`
- [x] Failure modes doc aligns with current behavior
  - Latest evidence: 2026-02-14 `docs/validation-failure-modes-20260214-1710Z.log` from `.venv/bin/python sie_verify.py` checks confirms documented failure outputs/exit codes (untrusted issuer=`2`, malformed envelope=`3`, missing check-file=`3`) and baseline success=`0`.
- [x] Validation doc aligns with current behavior
  - Latest evidence: 2026-02-14 `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] ...`; `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v` -> `Ran 40 tests ... OK`; synced latest run details in `docs/VALIDATION.md`.

## 4) Documentation coherence
- [x] README links are current
  - Latest evidence: 2026-02-14 `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] Signature verified and basic checks passed.`; `python3 - <<'PY' ...` README `.md` reference sweep -> `md_refs=7`, `missing=0`
- [x] Changelog includes user-relevant changes
  - Latest evidence: 2026-02-14 updated `CHANGELOG.md` Unreleased/Changed with release-hardening user-visible updates; fresh validation run in canonical `.venv` confirms changes are paired with working behavior (`.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] ...`; `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v` -> `Ran 40 tests ... OK`)
- [x] Integration docs remain explicit about boundaries/non-goals
  - Latest evidence: 2026-02-14 `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] Signature verified and basic checks passed.`; boundary/non-goal sweep confirms explicit limits in `README.md` (non-goals list) and `docs/OPENCLAW_INTEGRATION.md` (`Security boundaries` section).

## 5) Publish hygiene
- [x] Version/tag decided
  - Latest evidence: 2026-02-14 `grep -n '^version\s*=\s*' pyproject.toml` -> `version = "0.1.0"`; `git tag --list 'v0.1.0'` -> `v0.1.0` (`docs/validation-version-tag-20260214-1848Z.log`).
- [x] Release notes drafted
  - Latest evidence: 2026-02-14 drafted `docs/RELEASE_NOTES_DRAFT.md` with current hardening summary and validation references; fresh verifier + full unit suite evidence logged in `docs/validation-release-notes-20260214-1842Z.log`.
- [x] Any high-risk caveats called out clearly
  - Latest evidence: 2026-02-14 updated `docs/RELEASE_NOTES_DRAFT.md` with explicit high-risk caveat list (authorization boundary, trust-root sensitivity, revocation/rotation dependency, no confidentiality guarantee); paired fresh validation log `docs/validation-high-risk-caveats-20260214-1845Z.log` shows verifier pass + full test suite pass.
- [x] Release readiness report generated from checklist + validation evidence
  - Latest evidence: 2026-02-14 published `docs/RELEASE_READINESS_REPORT.md` using consolidated release-gate state plus fresh verifier/test run evidence from `docs/validation-release-readiness-20260214-1850Z.log`.

## One-command smoke gate (recommended)

- Linux/macOS: `./scripts/smoke_release.sh`
- Windows CI path: use `.github/workflows/ci.yml` release-gate job

## Optional local fast gate

Use helper scripts where available:

- Windows: `.\scripts\validate_all.ps1`
- Linux/macOS: `./scripts/validate_all.sh`
