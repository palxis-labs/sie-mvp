# SECURITY_QUICKSTART.md — 5-Minute Safety Setup

## Who this is for
Operators who want immediate safety improvements with minimal setup.

## 1) Verify your current signed skill

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

If you get `[OK]`, signature + issuer + file integrity checks passed.

---

## 2) Use helper scripts (faster)

### Windows (PowerShell)
```powershell
.\scripts\verify.ps1
```

### Linux/macOS
```bash
PYTHON_BIN=.venv/bin/python ./scripts/verify.sh
```
(Or activate your environment first and run `./scripts/verify.sh`.)

---

## 3) Safe runtime mode recommendation

Start in **warn mode**:
- allow unsigned skills temporarily
- warn loudly for unsigned/missing envelope

Then switch to **strict mode** after signed coverage is complete:
- reject unsigned skills
- reject untrusted/tampered skills

---

## 4) If something looks suspicious

- Stop installing new skills from untrusted sources.
- Verify envelope + `--check-file` again.
- Check trusted issuer list for unexpected entries.
- Rotate exposed tokens/keys.

---

## 5) Do not over-claim what SIE does

SIE helps verify instruction authenticity/integrity.
It does **not** replace sandboxing, host hardening, or key management practices.

---

## Minimal operator rule

If verification fails, do **not** treat that instruction as trusted.
