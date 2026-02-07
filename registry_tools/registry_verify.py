from __future__ import annotations

import argparse
import base64
from pathlib import Path

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def main() -> int:
    p = argparse.ArgumentParser(description="Verify registry snapshot signature (MVP).")
    p.add_argument("--dir", default="registry", help="Registry directory (default: registry/)")
    args = p.parse_args()

    d = Path(args.dir)
    reg_path = d / "registry.json"
    sig_path = d / "registry.sig"
    pub_path = d / "registry_root_public_key.b64"

    if not reg_path.exists() or not sig_path.exists() or not pub_path.exists():
        raise SystemExit("Missing registry files. Expected registry.json, registry.sig, registry_root_public_key.b64")

    reg_bytes = reg_path.read_bytes()
    sig = b64d(sig_path.read_text(encoding="utf-8").strip())
    pub = b64d(pub_path.read_text(encoding="utf-8").strip())

    vk = VerifyKey(pub)
    try:
        # Signature was created over the canonical registry bytes (as utf-8)
        vk.verify(reg_bytes, sig)
    except BadSignatureError:
        print("[FAIL] Bad registry signature")
        return 2

    print("[OK] Registry signature verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
