import json
import unittest
from pathlib import Path

from sie_lib import verify_envelope


class TestCryptoVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.envelope_path = cls.repo_root / "SKILL.md.sie.json"
        cls.skill_path = cls.repo_root / "SKILL.md"
        cls.keyring_path = cls.repo_root / "trusted_issuers.json"

        if not cls.envelope_path.exists():
            raise RuntimeError("SKILL.md.sie.json not found for tests")

    def load_env_and_pubkey(self):
        env = json.loads(self.envelope_path.read_text(encoding="utf-8"))
        issuer = env.get("issuer")
        keyring = json.loads(self.keyring_path.read_text(encoding="utf-8"))
        pub = keyring.get(issuer)
        if not pub:
            raise RuntimeError("Issuer not found in keyring for tests")
        return env, pub

    def test_valid_signature_verifies(self):
        env, pub = self.load_env_and_pubkey()
        verify_envelope(env, pub)  # should not raise

    def test_tampered_envelope_fails(self):
        env, pub = self.load_env_and_pubkey()
        env["payload"]["content"] += "\nTAMPER"
        with self.assertRaises(ValueError):
            verify_envelope(env, pub)


if __name__ == "__main__":
    unittest.main()
