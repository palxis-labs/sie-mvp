# CI_INTEGRATION.md — Add SIE Verification + Packaging Gates to CI

## Goal
Fail CI when signed instruction artifacts are untrusted/tampered or packaging/installability regresses.

## Required checks

1. Verify signed artifacts:

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

2. Run unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

3. Run clean-environment packaging/install smoke:

```bash
./scripts/smoke_release.sh
```

## GitHub Actions reference

Use `.github/workflows/ci.yml` with two jobs:

- `test-and-verify`: editable install + verification + tests
- `release-gate`: isolated venv, wheel build/install, CLI smoke checks

## Failure behavior

CI should fail if:
- issuer is not trusted
- signature is invalid
- file hash does not match signed payload
- envelope is malformed
- package cannot build/install in a fresh environment
- installed CLI entrypoint (`sie-verify`) fails

## Notes

- Keep trusted issuer keyring in repo only if public keys are intended to be public.
- Never commit private signing keys.
- Protect release branches by requiring both CI jobs green before merge/tag.
