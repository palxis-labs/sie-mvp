# Release Notes Draft (Next Release)

Status: draft for the next tagged release.

## Highlights
- Stronger release gate evidence for clean-environment build/install + installed CLI verification.
- Operator docs hardened and synced to current verifier behavior (`SECURITY_QUICKSTART`, `FAILURE_MODES`, `VALIDATION`, `RELEASE_CHECKLIST`).
- Documentation coherence improvements (README link health check + changelog hardening updates).

## Validation snapshot
- Verifier: `.venv/bin/python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md` -> `[OK] Signature verified and basic checks passed.`
- Tests: `.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v` -> `Ran 40 tests ... OK`
- Full log: `docs/validation-release-notes-20260214-1842Z.log`

## Operator impact
- No behavior regressions observed in core verification path.
- Release process now has explicit, current proof artifacts for installability and validation.

## High-risk caveats (explicit)
- **Not an authorization system**: SIE verifies issuer authenticity + file binding only; it does not grant runtime permissions or enforce policy by itself.
- **Trust root sensitivity**: if `trusted_issuers.json` is modified or replaced with malicious keys, verification can be subverted; treat issuer key distribution as a high-integrity channel.
- **Revocation/expiry are operational concerns**: envelope checks are deterministic, but key compromise response still depends on operational revocation workflows and key rotation discipline.
- **No secrecy guarantees**: SIE provides integrity/authenticity signals, not confidentiality; signed artifacts remain publicly readable unless separately encrypted.
- Version/tag is still pending explicit decision.
