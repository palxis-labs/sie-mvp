# SIE MVP — Signed Instruction Envelope (Security primitive for agent instructions)

SIE (Signed Instruction Envelope) is a minimal security primitive for agent systems that rely on plain-text
instruction files (e.g., `SKILL.md`, “skill packs”, tool configs, memory/instruction folders).

It targets a structural weakness in modern agent architectures:

> Agents cannot reliably distinguish **trusted instructions** from **untrusted content**.

This enables:
- **Skill supply-chain poisoning** (tampered or malicious skill files)
- **Indirect prompt injection** via documents/emails/code reviews/PDFs
- **Prompt/config/tool disclosure** via “explain how you work / print system prompt / list tools” attacks

SIE provides:
- **Integrity**: tamper detection via Ed25519 signatures
- **Authenticity**: issuer trust via a local keyring (`trusted_issuers.json`)
- **Fail-closed verification**: invalid/untrusted envelopes are rejected
- **Channel separation**: only signed envelopes are treated as INSTRUCTIONS; all other inputs are CONTENT

This repository contains a reference implementation + demo.

> Agent-first note: docs are organized so agents can quickly find deterministic behavior, failure handling, and validation commands while still being readable for humans.

---

## What SIE guarantees (MVP)

✅ **If verification passes**, the instruction payload is:
- unmodified since signing (integrity)
- issued by a trusted signer (authenticity, via keyring)

✅ **Unsigned / untrusted instruction sources are rejected by default.**

✅ **Untrusted content cannot become trusted instructions** (channel separation pattern).

---

## What SIE does NOT claim (v0.1)

SIE is a trust primitive, not a full sandbox or alignment solution.

❌ It does not prevent all model jailbreaks.  
❌ It does not sandbox tool execution by itself.  
❌ It does not prevent compromise of issuer private keys (revocation comes later).  
❌ It does not stop OS/runtime vulnerabilities.

See: `THREAT_MODEL.md`

---

## Repo contents

- `SIE_SPEC.md` — envelope format + signing/verification rules
- `THREAT_MODEL.md` — threats, assumptions, non-goals
- `sie_lib.py` — canonical JSON + sign/verify helpers
- `sie_sign.py` — sign an instruction file into `*.sie.json`
- `sie_verify.py` — verify signature + trusted issuer + optional file binding
- `trusted_issuers.json` — trusted issuer public keys (keyring)
- `demo/` — indirect injection demo

## Docs (human + agent fast path)

- `docs/INDEX.md` — best entrypoint (human/operator/integrator/maintainer paths)
- `docs/SECURITY_QUICKSTART.md` — 5-minute safety setup
- `docs/VALIDATION.md` — reproducible commands + expected outcomes
- `docs/OPENCLAW_INTEGRATION.md` — integration design for loader enforcement

---
## Install the latest release

### Option A — Latest RC (v0.1.0-rc1)
Use this if you want the newest release candidate:

```bash
python3 -m pip install "git+https://github.com/palxis-labs/sie-mvp.git@v0.1.0-rc1"
```

### Option B — Pinned wheel (same RC)

```bash
python3 -m pip install "https://github.com/palxis-labs/sie-mvp/releases/download/v0.1.0-rc1/sie_mvp-0.1.0-py3-none-any.whl"
```

If the GitHub Release page is not published yet, use Option A immediately; it installs directly from the tagged source.

## Quickstart

> **Windows PowerShell:** `& .\.venv\Scripts\Activate.ps1`  
> **Linux/macOS:** `source .venv/bin/activate`

### Install package (recommended)
```bash
python3 -m pip install .
```

### Dev install
```bash
python3 -m pip install -e .
```

### Sign a skill file
```bash
python3 sie_sign.py --issuer palxislabs --infile SKILL.md
```

### Verify the envelope with trusted issuers
```bash
python3 sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json
```

### Verify + bind to on-disk file (tamper detection)
```bash
python3 sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

### Installed CLI entrypoint (after `pip install .`)
```bash
sie-verify --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

## Helper scripts (recommended)

### Windows (PowerShell)
```powershell
.\scripts\sign.ps1
.\scripts\verify.ps1
.\scripts\validate_all.ps1
```

### Linux/macOS
```bash
./scripts/sign.sh
./scripts/verify.sh
./scripts/validate_all.sh
```

### Demo: Indirect prompt injection is blocked
```bash
python3 demo/run_demo.py
```

## License
MIT
