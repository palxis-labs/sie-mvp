# OPENCLAW_PR_TEMPLATE.md — Upstream Submission Template

Use this when proposing SIE loader enforcement to OpenClaw core.

## Title
`feat(security): optional SIE verification for skill loader (warn/strict modes)`

## Summary
This PR adds optional SIE verification at skill load time to reduce trust in unsigned/unverified instruction files.

## Problem
Current skill loading trusts plaintext instruction artifacts by discovery/path conventions. This enables substitution/tampering risks when skill supply chains are noisy.

## Proposed behavior
When `agents.security.sie.enabled=true`:
- signed envelope present + verify pass -> allow
- signed envelope present + verify fail -> reject
- signed envelope missing:
  - strict=false -> allow + warn
  - strict=true -> reject

## Config
```jsonc
{
  "agents": {
    "security": {
      "sie": {
        "enabled": true,
        "strict": false,
        "verifier": "python",
        "verifyScript": "/path/to/sie_verify.py",
        "trustedIssuers": "/path/to/trusted_issuers.json",
        "envelopeSuffix": ".sie.json"
      }
    }
  }
}
```

## Implementation notes
- Loader hook: envelope path resolution + subprocess verify adapter
- Decision logic follows documented matrix (`docs/ENFORCEMENT_BEHAVIOR.md`)
- Structured logs emitted for allow/reject decisions

## Test plan
- unsigned skill + warn mode: allowed with warning
- unsigned skill + strict mode: rejected
- valid signed skill: allowed
- invalid signed skill: rejected
- verifier missing: strict reject, warn allow+warning
- keyring missing: strict reject, warn allow+warning

## Backward compatibility
- Default behavior unchanged when feature disabled
- Migration path: warn mode first, strict mode second

## Security boundaries
This PR verifies instruction authenticity/integrity at load time.
It does not replace sandboxing, host hardening, or key compromise response.

## Rollback
- Set `agents.security.sie.enabled=false`

## Related docs
- `docs/OPENCLAW_INTEGRATION.md`
- `docs/ENFORCEMENT_BEHAVIOR.md`
- `docs/FAILURE_MODES.md`
- `docs/VALIDATION.md`
