# RELEASE_CHECKLIST.md — Security Release Gate

Run this checklist before tagging a release.

## 1) Correctness
- [ ] Verification command passes:
  - `python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- [ ] Tests pass:
  - `python -m unittest discover -s tests -p "test_*.py" -v`

## 2) Security posture
- [ ] Trusted issuer file reviewed
- [ ] No private keys in repo
- [ ] Security claims reviewed against `docs/SECURITY_CLAIMS.md`

## 3) Operator readiness
- [ ] Quickstart commands still valid
- [ ] Failure modes doc aligns with current behavior
- [ ] Validation doc aligns with current behavior

## 4) Documentation coherence
- [ ] README links are current
- [ ] Changelog includes user-relevant changes
- [ ] Integration docs remain explicit about boundaries/non-goals

## 5) Publish hygiene
- [ ] Version/tag decided
- [ ] Release notes drafted
- [ ] Any high-risk caveats called out clearly

## Optional one-command gate

Use helper scripts where available:

- Windows: `.\scripts\validate_all.ps1`
- Linux/macOS: `./scripts/validate_all.sh`
