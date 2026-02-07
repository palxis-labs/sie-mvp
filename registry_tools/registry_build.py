from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from sie_lib import canonical_json, generate_keypair, b64d, b64e
from nacl.signing import SigningKey

def load_or_create_registry_root_keys(priv_path: Path, pub_path: Path, new_keys: bool) -> tuple[str, str]:
    if new_keys or (not priv_path.exists()) or (not pub_path.exists()):
        pub, priv = generate_keypair()
        priv_path.write_text(priv, encoding="utf-8")
        pub_path.write_text(pub, encoding="utf-8")
        print(f"[ok] Generated registry root keypair.")
        print(f"     Private: {priv_path}  (KEEP SECRET)")
        print(f"     Public : {pub_path}")
        return priv, pub

    priv = priv_path.read_text(encoding="utf-8").strip()
    pub = pub_path.read_text(encoding="utf-8").strip()
    return priv, pub


def main() -> int:
    p = argparse.ArgumentParser(description="Build and sign the Palxis Registry snapshot (MVP).")
    p.add_argument("--outdir", default="registry", help="Output directory (default: registry/)")
    p.add_argument("--issuer-id", default="palxislabs", help="Issuer id to include as first record")
    p.add_argument("--issuer-pubkey-file", default=".sie_private_key.b64.pub",
                   help="Path to issuer public key (base64), e.g. .sie_private_key.b64.pub")
    p.add_argument("--new-registry-keys", action="store_true", help="Generate new registry root keys")
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Registry Root keys
    priv_path = Path(".registry_root_private_key.b64")
    pub_path = outdir / "registry_root_public_key.b64"
    registry_priv, registry_pub = load_or_create_registry_root_keys(priv_path, pub_path, args.new_registry_keys)

    # Issuer record (issuer pubkey is the SIE issuer key)
    issuer_pubkey_path = Path(args.issuer_pubkey_file)
    if not issuer_pubkey_path.exists():
        raise SystemExit(
            f"Issuer public key file not found: {issuer_pubkey_path}\n"
            f"Tip: ensure you have run sie_sign.py at least once and it created .sie_private_key.b64.pub"
        )

    issuer_pubkey = issuer_pubkey_path.read_text(encoding="utf-8").strip()

    records: List[Dict[str, Any]] = [
        {
            "type": "issuer",
            "issuer_id": args.issuer_id,
            "public_key": issuer_pubkey,
            "created": "2026-02-07T00:00:00Z",
            "expires": None,
            "metadata": {
                "name": "Palxis Labs",
                "contact": "palxislabs@gmail.com",
            },
        }
    ]

    registry_obj = {
        "version": "0.1",
        "generated_at": "2026-02-07T00:00:00Z",
        "records": records,
    }

    registry_json = canonical_json(registry_obj).encode("utf-8")

    # Sign the exact bytes of registry.json (this must match verification)
    sk = SigningKey(b64d(registry_priv))
    sig_b64 = b64e(sk.sign(registry_json).signature)

    (outdir / "registry.json").write_bytes(registry_json)
    (outdir / "registry.sig").write_text(sig_b64, encoding="utf-8")

    print("[ok] Wrote registry snapshot:")
    print(f"     {outdir / 'registry.json'}")
    print(f"     {outdir / 'registry.sig'}")
    print(f"[ok] Registry root public key:")
    print(f"     {pub_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
