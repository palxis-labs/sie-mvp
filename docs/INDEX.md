# Docs Index — Start Here

If you only read one page first, read: **`SECURITY_QUICKSTART.md`**.

## Fast paths

### 1) Human operator (5–15 min)
1. `SECURITY_QUICKSTART.md`
2. `VALIDATION.md`
3. `FAILURE_MODES.md`

### 2) Agent/integrator (OpenClaw/MCP runtime)
1. `OPENCLAW_INTEGRATION.md`
2. `ENFORCEMENT_BEHAVIOR.md`
3. `OPENCLAW_PATCH_SKELETON.md`
4. `OPENCLAW_UPSTREAM_HANDOFF.md`

### 3) Maintainer/release owner
1. `MAINTAINER_CHECKLIST.md`
2. `RELEASE_CHECKLIST.md`
3. `SECURITY_CLAIMS.md`
4. `CONTRIBUTING_SECURITY.md`

## Supporting docs
- `OPERATOR_CHECKLIST.md` — rollout + incident response
- `CI_INTEGRATION.md` — CI gate for signed artifact verification
- `ADOPTION_PATH.md` — staged rollout (warn → strict)
- `DEMO_SCRIPT.md` — 5-minute live demo
- `IMPLEMENTATION_TICKETS.md` — implementation work breakdown
- `OPENCLAW_EXECUTION_PLAN.md` — phased execution sequence
- `OPENCLAW_PR_TEMPLATE.md` — upstream PR template
- `IMPLEMENTATION_RISKS.md` — known risks + mitigations

## Reading principle
- Start small, verify claims, then enforce.
- Do not treat SIE as a sandbox replacement.
