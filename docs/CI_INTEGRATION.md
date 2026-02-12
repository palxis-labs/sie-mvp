# CI_INTEGRATION.md — Add SIE Verification to CI

## Goal
Fail CI when signed instruction artifacts are untrusted or tampered.

## Minimal GitHub Actions step

Add this after dependency install:

```yaml
- name: Verify signed instruction artifacts
  run: |
    python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

## Recommended full check order

1. Verify signed artifacts (`sie_verify.py ... --check-file`)
2. Run unit tests (`python -m unittest discover -s tests -p "test_*.py" -v`)

## Failure behavior

CI should fail if:
- issuer is not trusted
- signature is invalid
- file hash does not match signed payload
- envelope is malformed

## Optional hardening

- Enforce helper script in CI:

```yaml
- name: Run full validation
  run: |
    chmod +x scripts/validate_all.sh
    ./scripts/validate_all.sh
```

- Add branch protection requiring CI green before merge.

## Notes

- Keep trusted issuer keyring in repo only if public keys are intended to be public.
- Never commit private signing keys.
