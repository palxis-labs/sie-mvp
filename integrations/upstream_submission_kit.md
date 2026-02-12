# Upstream Submission Kit (OpenClaw)

This is the exact handoff kit for opening upstream issue + PR.

## 1) Open Issue (copy/paste)

### Title
`Proposal: optional SIE verification in skill loader (warn/strict modes)`

### Body
```md
I propose an optional, feature-flagged SIE verification gate in the skill loader.

Behavior:
- unsigned + warn => allow + warning
- unsigned + strict => reject
- signed + valid => allow
- signed + invalid => reject

Goals:
- reduce trust in unsigned/tampered skill instructions
- preserve backward compatibility when feature disabled
- keep first patch minimal and reviewable

Validation basis:
- deterministic reason codes
- integration hook + loader reference flow
- cross-platform test suite currently green (37 tests)
```

## 2) Open PR (copy/paste)

Use generated payload:
- `integrations/upstream_pr_payload.md`

And attach manifest:
- `integrations/upstream_patch_manifest.json`

## 3) PR file scope (integration slice)

See manifest file list. Keep scope strict to avoid review drag.

## 4) Pre-submit command

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python integrations/upstream_patch_bundle.py
python integrations/upstream_pr_payload.py
```

## 5) Reviewer notes

- SIE disabled path is backward compatible (allow).
- Strict/warn behavior is explicit and tested.
- Reason constants are stable for machine consumers.
- This is enforcement at instruction trust boundary, not a sandbox replacement.
