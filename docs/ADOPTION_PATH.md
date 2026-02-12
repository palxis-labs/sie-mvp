# ADOPTION_PATH.md — Practical Adoption Sequence

## Objective
Help teams adopt SIE incrementally without disrupting existing agent workflows.

## Stage 0 — Awareness
- Read: `docs/SECURITY_QUICKSTART.md`
- Run baseline verify once
- Confirm who owns trusted issuer keyring maintenance

## Stage 1 — Local verification discipline
- Use `scripts/verify.*` in developer workflow
- Require successful verification before accepting skill changes
- Record verification results in PR description/checklist

## Stage 2 — CI verification gate
- Add verification commands to CI for skill artifacts
- Fail CI on untrusted or tampered envelopes
- Keep logs clear and actionable

## Stage 3 — Runtime integration (warn mode)
- Enable loader integration in warn mode first
- Observe unsigned skill warnings
- Sign legacy skills progressively

## Stage 4 — Runtime strict mode
- Enforce rejection for unsigned/untrusted/tampered skills
- Keep rollback toggle available (`enabled=false`)
- Monitor logs for operational regressions

## Stage 5 — Hardening maturity
- Minimize trusted issuer set
- Define key rotation/revocation process
- Combine SIE with sandboxing and least-privilege tool policies

## Adoption anti-patterns to avoid
- Turning on strict mode before signing coverage is complete
- Treating SIE as a replacement for runtime sandboxing
- Keeping stale or overbroad trusted issuer lists
- Publishing unverifiable security claims
