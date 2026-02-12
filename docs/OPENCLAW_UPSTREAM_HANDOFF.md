# OPENCLAW_UPSTREAM_HANDOFF.md — Maintainer Handoff Pack

## Purpose
Single-file handoff for proposing SIE loader enforcement upstream.

## What this pack already provides

- Integration design: `docs/OPENCLAW_INTEGRATION.md`
- Behavior matrix: `docs/ENFORCEMENT_BEHAVIOR.md`
- Failure handling: `docs/FAILURE_MODES.md`
- Execution sequence: `docs/OPENCLAW_EXECUTION_PLAN.md`
- Patch starter: `docs/OPENCLAW_PATCH_SKELETON.md`
- Upstream PR template: `docs/OPENCLAW_PR_TEMPLATE.md`

## Suggested submission order

1. Open an issue in OpenClaw core with scope + behavior matrix.
2. Share minimal patch skeleton and request feedback on config naming.
3. Submit MVP patch behind feature flag (`enabled=false` default if required by maintainers).
4. Add tests for strict/warn behavior and missing runtime/keyring branches.
5. Add docs for migration + rollback in upstream docs.

## Maintainer-friendly boundaries

- Keep first PR small and optional.
- No breaking default behavior.
- No broad refactors in same PR.
- No claims beyond authenticity/integrity at loader boundary.

## Ready-to-copy issue body (short)

```md
### Proposal: Optional SIE verification in skill loader

I’d like to propose an optional, feature-flagged loader check for signed skill instructions.

Core behavior:
- If enabled + envelope valid => allow
- If enabled + envelope invalid => reject
- If enabled + envelope missing:
  - strict=false => allow + warning
  - strict=true => reject

Goal: reduce trust in unsigned/tampered skill instructions without changing default behavior.

I have prepared design docs, behavior matrix, failure handling, and patch skeleton for quick review.
```

## Ready-to-copy implementation checklist

- [ ] Config schema fields for `agents.security.sie.*`
- [ ] Envelope resolution (`SKILL.md` + suffix)
- [ ] Verifier subprocess call
- [ ] strict/warn decision branch
- [ ] structured allow/reject logs
- [ ] branch coverage tests for all matrix paths

## Exit criteria for upstream MVP

- Deterministic strict/warn behavior
- Backward-compatible when disabled
- Documented operator migration path
- Clear rollback toggle
