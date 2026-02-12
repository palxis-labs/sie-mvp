# CONTRIBUTING_SECURITY.md — Security-Focused Contribution Rules

## Purpose
Help contributors add features without weakening core trust guarantees.

## Required checks before PR

- [ ] `python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- [ ] `python -m unittest discover -s tests -p "test_*.py" -v`
- [ ] No secrets/tokens/private keys in staged changes

## Security-sensitive areas (extra review)

Changes touching these files should get explicit security review:
- `sie_verify.py`
- `sie_sign.py`
- `sie_lib.py`
- `trusted_issuers.json`
- any loader/integration enforcement code

## Rules for verifier changes

- Do not convert failures into silent warnings by default.
- Keep exit codes deterministic.
- Preserve clear operator-facing failure reasons.
- Add/adjust tests whenever verifier behavior changes.

## Rules for docs and claims

- Claims must map to reproducible commands/tests in repo.
- Avoid “solves all prompt injection” language.
- Keep boundaries explicit: SIE is not a sandbox replacement.

## Key management hygiene

- Public keys may be committed if intentionally public.
- Private signing keys must never be committed.
- If key compromise is suspected, remove affected issuer from trust set immediately.

## Suggested PR checklist snippet

```md
- [ ] Verification command passes
- [ ] Test suite passes
- [ ] No secrets committed
- [ ] Security claims remain accurate
- [ ] Failure behavior remains fail-closed where intended
```
