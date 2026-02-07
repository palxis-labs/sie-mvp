# Test SIE with an OpenClaw-style agent (5 minutes)

This demonstrates instruction authenticity and indirect prompt injection resistance.

No framework modification required — this runs as a pre-loader wrapper.

---

## 1. Clone

```
git clone https://github.com/palxis-labs/sie-mvp
cd sie-mvp
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install pynacl
```

---

## 2. Run the demo

```
python -m integrations.example_agent_wrapper
```

You should see:

```
[BLOCKED] Untrusted content attempted prompt/config/tool disclosure
```

The injected content tries to override instructions and exfiltrate a secret token.
It fails because only signed instructions are authoritative.

---

## What this shows

Agent systems typically merge:

* system prompts
* skills
* documents
* tool output

into a single text channel.

SIE separates:

trusted instructions → signed
untrusted content → data only

So external content cannot become control logic.

---

## How this maps to OpenClaw

Replace skill loading:

instead of:

```
load_markdown("skill.md")
```

use:

```
load_verified_instructions("skill.md.sie.json")
```

No other behavior changes.

---

## Expected outcome

Tampered skills fail to load.
Injected content cannot override agent policy.
