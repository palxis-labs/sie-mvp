# Palxis Registry Service (Neutral Trust Infrastructure)

Palxis Registry is a signed, verifiable issuer directory for agent instruction artifacts (SIE).
It provides objective trust signals only: issuer presence, key history, and revocation state.

It does **not** provide “safe/unsafe” ratings or recommendations.
Agents (and their operators) remain in control of policy decisions.

---

## What problem it solves

In many agent ecosystems, “skills” and instruction bundles are distributed as plain text.
This creates:
- tampering risk (local or supply-chain)
- untrusted publishers
- no reliable revocation path after compromise
- fragmented trust decisions across frameworks

Palxis Registry provides a neutral trust root so agents can answer:
- Who issued this instruction?
- Is this issuer known?
- Is this key revoked?
- Has the issuer rotated keys?

---

## How it works (MVP)

- Registry snapshots are published as static files:
  - `registry.json` (records)
  - `registry.sig` (Ed25519 signature over `registry.json`)
  - `registry_root_public_key.b64` (pinned verification key)

- Clients download and verify signatures locally (fail-closed).
- Mirrors can host the same files; clients accept the first valid signature.

---

## Record types (objective)

- **Issuer record**: issuer_id → public key + metadata
- **Revocation record**: key or artifact revoked + timestamp + reason

Optional (future): event/evidence records (telemetry), still objective.

---

## Tiers

### Community (Free)
- Public signed snapshot URL
- Best-effort updates
- Open format and client code
- No SLA

### Pro (Paid)
For teams shipping agent skills/policies to customers.
- Private issuer entries (not publicly listed)
- Assisted key rotation
- Revocation publish SLA (e.g., 15 minutes)
- Signed snapshot hosting under stable endpoints

### Enterprise
For organizations with internal agent ecosystems.
- Dedicated registry root and private snapshots
- Multiple mirrors / regional hosting
- Audit exports and compliance support
- Incident response support for key compromise

---

## Onboarding as an issuer (MVP)
1) Generate an issuer signing keypair (Ed25519)
2) Submit issuer_id + public key + metadata to Palxis
3) Palxis publishes the issuer record in the next signed snapshot
4) You sign instruction envelopes (SIE) using your issuer private key

---

## Key rotation and revocation (MVP)
- **Rotation**: publish new issuer public key record (and optional “replaces” metadata)
- **Revocation**: publish revocation record for compromised key or specific artifact id
- Clients enforce revocations automatically after snapshot refresh

---

## Status
This is an MVP reference implementation. The objective is interoperability and adoption.
