# OPERATOR_CHECKLIST.md — Safe Rollout & Incident Response

## Who this is for
Operators deploying SIE verification for agent skill instructions.

## Goal
Improve instruction trust (integrity + issuer authenticity) without breaking existing workflows.

---

## Pre-deploy checklist

- [ ] Confirm you have a backup/rollback path for current skill configuration.
- [ ] Ensure `trusted_issuers.json` contains only issuers you explicitly trust.
- [ ] Ensure private signing keys are **not** in this repo.
- [ ] Verify your runtime can execute the verifier (`python` / `python3`).
- [ ] Verify your loader/runtime can pass:
  - `--file`
  - `--trusted-issuers`
  - `--check-file`

### Quick local validation

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected: `[OK] Signature verified and basic checks passed.`

---

## Safe rollout strategy

### Phase 1 — Warn mode (recommended first)
- `enabled=true`
- `strict=false`
- Allow unsigned skills temporarily, but log warnings loudly.

### Phase 2 — Strict mode
- `enabled=true`
- `strict=true`
- Reject unsigned/untrusted/tampered skills.

Only switch to strict mode after signed coverage is complete.

---

## Day-1 operational checks

- [ ] Every loaded signed skill verifies successfully.
- [ ] Unsigned skills are visible in logs (warn mode) or blocked (strict mode).
- [ ] Verification failures include actionable reason.
- [ ] No silent fallback from failed verification to trusted execution.

---

## Incident response checklist

Use this if you suspect a malicious or substituted skill.

### Immediate containment

- [ ] Pause new skill installs from untrusted/community sources.
- [ ] Switch runtime to strict enforcement if safe.
- [ ] Snapshot current skill directories for forensics.
- [ ] Record exact timestamp and observed indicators.

### Investigation

- [ ] Compare installed `SKILL.md` with known-good source.
- [ ] Verify envelope + file binding (`--check-file`).
- [ ] Inspect trusted issuer list for unauthorized entries.
- [ ] Check `~/.ssh/authorized_keys` for unknown keys.
- [ ] Check for unexpected binaries/scripts in temp/download paths.

### Recovery

- [ ] Remove compromised skills/artifacts.
- [ ] Rotate exposed secrets/tokens.
- [ ] Reinstall skills from trusted source with verification.
- [ ] Re-run verification and document post-incident state.

---

## Practical safety defaults

- Prefer pinned source (author/path/commit), not broad repo-wide discovery.
- Keep trusted issuer keyring minimal and reviewed.
- Treat all external content as untrusted unless verified.
- Keep logs sufficient for audit but never store secrets in plaintext logs.

---

## User-facing clarity rules

When a skill is rejected, report in plain language:
- what was rejected
- why it was rejected
- what operator can do next

Example:

"Skill `X` was rejected because issuer `Y` is not in trusted_issuers.json. Add issuer `Y` if trusted, then retry verification."

---

## Non-goals reminder

SIE verification does **not** replace:
- runtime sandboxing
- least-privilege tool policy
- host hardening
- key compromise response plans

Use SIE as one control in a broader security posture.
