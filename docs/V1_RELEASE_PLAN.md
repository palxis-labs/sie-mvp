# V1_RELEASE_PLAN.md — Production-Ready v1.0 Plan

## Goal
Ship SIE v1.0 as a practical, production-safe package: deterministic verifier behavior, tested enforcement semantics, reproducible validation, and a clear operator installation path (including agent auto-install).

## Scope Boundaries (v1.0)
In scope:
- Verifier correctness + deterministic CLI contract
- Trusted issuer + file-binding enforcement behavior
- OpenClaw integration path and rollout docs
- Reproducible test/validation evidence

Out of scope:
- Key transparency service
- Key revocation backend
- Non-Python verifier runtime replacement

---

## Block Plan (2–3 day blocks)

## Block 1 (Days 1–2) — **P0** Verifier Determinism + Evidence Baseline

### Objectives
- Audit verifier behavior matrix (success/failure classes)
- Close test gaps for error handling and exit-code determinism
- Align `docs/VALIDATION.md` with actual CLI behavior

### Acceptance Criteria
- Explicit exit-code contract documented and tested
- Verification failures return a deterministic failure code
- Input/config failures return a deterministic failure code
- Validation doc commands and expected outputs match current implementation

### Definition of Done
- `tests/test_verify_cli.py` covers core success + failure matrix
- `sie_verify.py` returns stable exit codes with stable `[OK]/[FAIL]` output format
- Full test suite passes

---

## Block 2 (Days 3–5) — **P0** Enforcement Readiness (Strict/Warn)

### Objectives
- Lock strict/warn loader decision semantics
- Ensure docs and integration artifacts are internally consistent
- Add/verify tests for enforcement branch behavior in integration simulations

### Acceptance Criteria
- `docs/ENFORCEMENT_BEHAVIOR.md` is canonical and consistent with tests
- Fail-closed behavior for invalid signed content is explicit
- Warn-mode migration guidance is actionable

### Definition of Done
- Enforcement decision table complete and unambiguous
- Integration tests cover unsigned/invalid/untrusted cases
- Operator rollback path documented

---

## Block 3 (Days 6–8) — **P1** Install + Operator Experience

### Objectives
- Provide a frictionless install/validation path
- Define agent auto-install path for OpenClaw environments
- Finalize quickstart/release checklist for first-time operators

### Acceptance Criteria
- Linux/macOS + Windows install/verify path is copy-paste reproducible
- Auto-install path is documented with prerequisites and safety constraints
- One-command validation flow is available (`validate_all` scripts)

### Definition of Done
- `README.md` and docs cross-link to install + validation flow
- `docs/RELEASE_CHECKLIST.md` can be executed end-to-end without ambiguity
- Known failure modes + remediation linked from install docs

---

## Block 4 (Days 9–10) — **P1** Release Gate + Packaging

### Objectives
- Run release gate with fresh environment assumptions
- Validate security claims against shipped behavior
- Publish v1.0 release notes/changelog entry

### Acceptance Criteria
- Full test suite green
- Validation checklist green
- No doc overclaims vs implemented behavior

### Definition of Done
- `CHANGELOG.md` contains v1.0-ready notes
- All release checklist items pass
- Remaining risks and non-goals are explicit

---

## Priorities Summary
- **P0:** deterministic verifier contract; enforcement semantics; test evidence
- **P1:** operator install/autoinstall experience; release hygiene
- **P2 (post-v1.0):** revocation/transparency, TS-native verifier

## Install Path (Operator)
1. Install Python 3.11+
2. `pip install -e .`
3. Verify baseline:
   - `python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
4. Run full tests:
   - `python -m unittest discover -s tests -p "test_*.py" -v`

## Agent Auto-Install Path (OpenClaw-focused)
1. Bundle repo with verifier + scripts into agent environment image
2. On startup, run dependency bootstrap (`pip install -e .` or pinned wheel)
3. Ensure keyring path is provisioned and readable before enabling strict mode
4. Start in warn mode for inventorying unsigned skills
5. Promote to strict mode once signing coverage is complete

Safety notes:
- Never auto-trust unknown issuers during auto-install
- Treat missing keyring/runtime as blocking in strict mode
- Keep rollback: `enabled=false` documented and operator-controlled
