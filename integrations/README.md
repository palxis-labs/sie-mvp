# SIE Integrations (Drop-in hooks for agent frameworks)

This folder provides framework-agnostic integration patterns:

## 1) Verified instruction loading (fail closed)
Agents should load trusted instruction text ONLY from a verified SIE envelope, not from plaintext skill files.

Use:
- `integrations/sie_loader.py`

Example:
```python
from integrations.sie_loader import load_verified_instructions
instr = load_verified_instructions(
    Path("SKILL.md.sie.json"),
    keyring_path=Path("trusted_issuers.json"),
    check_file_path=Path("SKILL.md"),  # optional tamper detection
)
```

## 2) Channel separation (instructions vs content)
Treat signed envelopes as INSTRUCTIONS (control-plane)
Treat documents/emails/code/tool output as CONTENT (data-plane)
CONTENT must not override policy or introduce new directives

## 3) Indirect injection blocking (MVP policy gate)
Use:
- `sie_policy.py`

Example:
```python
from sie_policy import evaluate_untrusted_content
decision = evaluate_untrusted_content(
    untrusted_content=email_text,
    constraints=instr.constraints,
)
```

## Recommended framework hook points

Before loading any skill/memory/instruction file:
    verify envelope, check issuer trust, fail closed
Before executing tool actions suggested by content:
    evaluate content against constraints