# VALIDATION.md — Reproducible Verification Checklist

## Purpose
Provide a deterministic command sequence to validate core SIE verifier claims.

## CLI Exit Code Contract
- `0` = verification success
- `2` = verification/trust failure (bad signature, untrusted issuer, missing issuer, hash mismatch)
- `3` = input/config error (missing file, malformed JSON, invalid keyring format)

## Prerequisites
- Python environment available
- `pynacl` installed
- Files present: `SKILL.md`, `SKILL.md.sie.json`, `trusted_issuers.json`

## 1) Baseline verify should pass

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json
```

Expected:
- Exit code `0`
- Output contains `[OK] Signature verified and basic checks passed.`

---

## 2) File binding verify should pass

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected:
- Exit code `0`
- Output contains `[OK] Signature verified and basic checks passed.`

---

## 3) Tamper test should fail (verification failure)

### 3a) Backup
```bash
cp SKILL.md SKILL.md.bak
```

### 3b) Modify file
```bash
echo "# tamper" >> SKILL.md
```

### 3c) Verify with file check
```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected:
- Exit code `2`
- Output contains hash mismatch failure

### 3d) Restore file
```bash
mv SKILL.md.bak SKILL.md
```

---

## 4) Untrusted issuer should fail (verification failure)

Create temporary empty issuer map and verify:

```bash
printf '{}' > tmp_issuers.json
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers tmp_issuers.json
```

Expected:
- Exit code `2`
- Output contains issuer-not-trusted failure

Cleanup:

```bash
rm -f tmp_issuers.json
```

---

## 5) Malformed envelope should fail (input error)

```bash
printf '{not-json' > tmp_bad.sie.json
python sie_verify.py --file tmp_bad.sie.json --trusted-issuers trusted_issuers.json
```

Expected:
- Exit code `3`
- Output contains invalid JSON failure

Cleanup:

```bash
rm -f tmp_bad.sie.json
```

---

## 6) Missing check-file should fail (input error)

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file DOES_NOT_EXIST.md
```

Expected:
- Exit code `3`
- Output contains check file not found

---

## 7) Re-sign after legitimate edit

If `SKILL.md` changed intentionally:

```bash
python sie_sign.py --issuer palxislabs --infile SKILL.md
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected:
- Exit code `0`
- Verify returns `[OK]`

---

## 8) Packaging/installability smoke (release gate)

```bash
./scripts/smoke_release.sh
```

Expected:
- Wheel builds successfully
- Wheel installs in a fresh venv
- Installed `sie-verify` command succeeds
- Unit tests pass in the clean environment

---

## Windows notes
- Activate env: `& .\.venv\Scripts\Activate.ps1`
- Use helper scripts:
  - `.\scripts\sign.ps1`
  - `.\scripts\verify.ps1`

## Linux/macOS notes
- Activate env: `source .venv/bin/activate`
- Use helper scripts:
  - `./scripts/sign.sh`
  - `./scripts/verify.sh`
  - `./scripts/smoke_release.sh`

## Latest validation run log
- Date (UTC): 2026-02-14 16:10
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Quickstart helper verification: `PYTHON_BIN=.venv/bin/python ./scripts/verify.sh` -> `[OK] Signature verified and basic checks passed.`
- Quickstart doc alignment update: Linux/macOS helper now explicitly documents `.venv`/`PYTHON_BIN` path in `docs/SECURITY_QUICKSTART.md`.
- Note: project `.venv` remains the canonical release-validation environment.
- Date (UTC): 2026-02-14 17:10
- Failure-mode validation log: `docs/validation-failure-modes-20260214-1710Z.log`
- Recorded results: baseline success exit `0`; untrusted issuer exit `2`; malformed envelope exit `3`; missing check-file exit `3`.
- Doc sync: `docs/FAILURE_MODES.md` updated with verified outputs and exit-code mapping.
- Date (UTC): 2026-02-14 18:22
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Test command: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v`
- Test result: `Ran 40 tests ... OK`
- Doc sync: operator-readiness gate `Validation doc aligns with current behavior` marked complete in `docs/RELEASE_CHECKLIST.md` with this evidence.
- Date (UTC): 2026-02-14 18:27
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- README reference check command: `python3 - <<'PY' ...` (backticked `.md` refs in `README.md`)
- README reference check result: `md_refs=7`, `missing=0`
- Doc sync: `docs/RELEASE_CHECKLIST.md` item `README links are current` marked complete with fresh evidence.
- Date (UTC): 2026-02-14 18:36
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Test command: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v`
- Test result: `Ran 40 tests ... OK`
- Doc sync: `CHANGELOG.md` updated with user-relevant hardening changes; `docs/RELEASE_CHECKLIST.md` item `Changelog includes user-relevant changes` marked complete with this validation evidence.
- Date (UTC): 2026-02-14 18:39
- Clean-install validation log: `docs/validation-clean-install-20260214-1839Z.log`
- Packaging/build result: `.venv/bin/python -m build .` succeeded (used as fallback because host `python3 -m pip` is PEP668 externally-managed).
- Fresh venv install result: `.tmp-release-venv/bin/python -m pip install dist/*.whl` -> `Successfully installed ... sie-mvp-0.1.0`.
- Installed entrypoint results: `.tmp-release-venv/bin/sie-verify ...` and `.tmp-release-venv/bin/python -m sie_verify ...` both -> `[OK] Signature verified and basic checks passed.`
- Doc sync: `docs/RELEASE_CHECKLIST.md` section `0) Clean-environment installability` marked complete with this evidence.
- Date (UTC): 2026-02-14 18:42
- Validation log: `docs/validation-release-notes-20260214-1842Z.log`
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Test command: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v`
- Test result: `Ran 40 tests ... OK`
- Doc sync: drafted `docs/RELEASE_NOTES_DRAFT.md` and marked `Release notes drafted` complete in `docs/RELEASE_CHECKLIST.md`.
- Date (UTC): 2026-02-14 18:45
- Validation log: `docs/validation-high-risk-caveats-20260214-1845Z.log`
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Test command: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v`
- Test result: `Ran 40 tests ... OK`
- Doc sync: updated `docs/RELEASE_NOTES_DRAFT.md` with explicit high-risk caveats and marked publish-hygiene item `Any high-risk caveats called out clearly` complete in `docs/RELEASE_CHECKLIST.md`.
- Date (UTC): 2026-02-14 18:48
- Validation log: `docs/validation-version-tag-20260214-1848Z.log`
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Test command: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v`
- Test result: `Ran 40 tests ... OK`
- Version/tag evidence: `pyproject.toml` contains `version = "0.1.0"`; `git tag --list 'v0.1.0'` returns existing release tag.
- Doc sync: marked publish-hygiene item `Version/tag decided` complete in `docs/RELEASE_CHECKLIST.md`.
- Date (UTC): 2026-02-14 18:50
- Validation log: `docs/validation-release-readiness-20260214-1850Z.log`
- Verification command: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- Verification result: `[OK] Signature verified and basic checks passed.`
- Test command: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v`
- Test result: `Ran 40 tests ... OK`
- Doc sync: published `docs/RELEASE_READINESS_REPORT.md` and marked checklist item `Release readiness report generated from checklist + validation evidence` complete in `docs/RELEASE_CHECKLIST.md`.
