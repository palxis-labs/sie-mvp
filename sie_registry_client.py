from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from sie_lib import b64d


@dataclass(frozen=True)
class RegistrySnapshot:
    data: Dict[str, Any]


class RegistryClient:
    """
    Loads and verifies the signed registry snapshot.
    Provides objective queries only (no safety opinions).
    """

    def __init__(self, registry_dir: Path = Path("registry")):
        self.registry_dir = registry_dir

    def load_verified_snapshot(self) -> RegistrySnapshot:
        reg_path = self.registry_dir / "registry.json"
        sig_path = self.registry_dir / "registry.sig"
        pub_path = self.registry_dir / "registry_root_public_key.b64"

        if not (reg_path.exists() and sig_path.exists() and pub_path.exists()):
            raise FileNotFoundError("Registry files missing")

        reg_bytes = reg_path.read_bytes()
        sig = b64d(sig_path.read_text(encoding="utf-8").strip())
        pub = b64d(pub_path.read_text(encoding="utf-8").strip())

        vk = VerifyKey(pub)
        try:
            vk.verify(reg_bytes, sig)
        except BadSignatureError as e:
            raise ValueError("Registry signature invalid") from e

        data = json.loads(reg_bytes.decode("utf-8"))
        return RegistrySnapshot(data=data)

    def issuer_public_key(self, issuer_id: str) -> Optional[str]:
        snap = self.load_verified_snapshot()
        for rec in snap.data.get("records", []):
            if rec.get("type") == "issuer" and rec.get("issuer_id") == issuer_id:
                return rec.get("public_key")
        return None

    def is_issuer_present(self, issuer_id: str) -> bool:
        return self.issuer_public_key(issuer_id) is not None

    def is_key_revoked(self, issuer_id: str, public_key_b64: str) -> bool:
        snap = self.load_verified_snapshot()
        for rec in snap.data.get("records", []):
            if rec.get("type") == "revocation" and rec.get("issuer_id") == issuer_id:
                if rec.get("revoked_key") == public_key_b64:
                    return True
        return False
