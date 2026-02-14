import json
import subprocess
import sys
from pathlib import Path
import unittest


EXIT_OK = 0
EXIT_VERIFY_FAIL = 2
EXIT_INPUT_ERROR = 3

try:
    import nacl  # noqa: F401
    NACL_AVAILABLE = True
except Exception:
    NACL_AVAILABLE = False


class TestVerifyCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.python = sys.executable
        cls.verify = cls.root / "sie_verify.py"
        cls.env_file = cls.root / "SKILL.md.sie.json"
        cls.skill_file = cls.root / "SKILL.md"
        cls.keyring = cls.root / "trusted_issuers.json"

    def run_cmd(self, *args):
        return subprocess.run(
            [self.python, str(self.verify), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    @unittest.skipUnless(NACL_AVAILABLE, "pynacl not installed")
    def test_verify_ok_with_trusted_issuers(self):
        r = self.run_cmd(
            "--file", str(self.env_file),
            "--trusted-issuers", str(self.keyring),
        )
        self.assertEqual(r.returncode, EXIT_OK, msg=r.stdout + r.stderr)
        self.assertIn("[OK]", r.stdout)

    @unittest.skipUnless(NACL_AVAILABLE, "pynacl not installed")
    def test_verify_ok_with_check_file(self):
        r = self.run_cmd(
            "--file", str(self.env_file),
            "--trusted-issuers", str(self.keyring),
            "--check-file", str(self.skill_file),
        )
        self.assertEqual(r.returncode, EXIT_OK, msg=r.stdout + r.stderr)
        self.assertIn("[OK]", r.stdout)

    @unittest.skipUnless(NACL_AVAILABLE, "pynacl not installed")
    def test_verify_ok_with_pubkey_override(self):
        env = json.loads(self.env_file.read_text(encoding="utf-8"))
        issuer = env.get("issuer")
        keyring = json.loads(self.keyring.read_text(encoding="utf-8"))
        pub = keyring[issuer]

        r = self.run_cmd(
            "--file", str(self.env_file),
            "--pubkey", pub,
        )
        self.assertEqual(r.returncode, EXIT_OK, msg=r.stdout + r.stderr)
        self.assertIn("[OK]", r.stdout)

    @unittest.skipUnless(NACL_AVAILABLE, "pynacl not installed")
    def test_payload_issuer_without_top_level_fails_signature(self):
        env = json.loads(self.env_file.read_text(encoding="utf-8"))
        issuer = env.get("issuer")
        env.pop("issuer", None)
        env.setdefault("payload", {})["issuer"] = issuer

        tmp_env = self.root / "tests" / "tmp_payload_issuer.sie.json"
        try:
            tmp_env.write_text(json.dumps(env), encoding="utf-8")
            r = self.run_cmd(
                "--file", str(tmp_env),
                "--trusted-issuers", str(self.keyring),
            )
            self.assertEqual(r.returncode, EXIT_VERIFY_FAIL)
            self.assertIn("bad signature", (r.stdout + r.stderr).lower())
        finally:
            tmp_env.unlink(missing_ok=True)

    def test_untrusted_issuer_fails(self):
        bad_keyring = self.root / "tests" / "tmp_bad_issuers.json"
        bad_keyring.write_text("{}", encoding="utf-8")
        try:
            r = self.run_cmd(
                "--file", str(self.env_file),
                "--trusted-issuers", str(bad_keyring),
            )
            self.assertEqual(r.returncode, EXIT_VERIFY_FAIL)
            self.assertIn("not trusted", (r.stdout + r.stderr).lower())
        finally:
            bad_keyring.unlink(missing_ok=True)

    @unittest.skipUnless(NACL_AVAILABLE, "pynacl not installed")
    def test_hash_mismatch_fails(self):
        tampered = self.root / "tests" / "tmp_tampered_skill.md"
        try:
            tampered.write_text(self.skill_file.read_text(encoding="utf-8") + "\n# tamper\n", encoding="utf-8")
            r = self.run_cmd(
                "--file", str(self.env_file),
                "--trusted-issuers", str(self.keyring),
                "--check-file", str(tampered),
            )
            self.assertEqual(r.returncode, EXIT_VERIFY_FAIL)
            self.assertIn("hash", (r.stdout + r.stderr).lower())
        finally:
            tampered.unlink(missing_ok=True)

    def test_missing_issuer_fails(self):
        env = json.loads(self.env_file.read_text(encoding="utf-8"))
        env.pop("issuer", None)
        env.get("payload", {}).pop("issuer", None)

        tmp_env = self.root / "tests" / "tmp_missing_issuer.sie.json"
        try:
            tmp_env.write_text(json.dumps(env), encoding="utf-8")
            r = self.run_cmd(
                "--file", str(tmp_env),
                "--trusted-issuers", str(self.keyring),
            )
            self.assertEqual(r.returncode, EXIT_VERIFY_FAIL)
            self.assertIn("missing issuer", (r.stdout + r.stderr).lower())
        finally:
            tmp_env.unlink(missing_ok=True)

    def test_malformed_envelope_json_fails_with_input_error(self):
        bad_env = self.root / "tests" / "tmp_malformed.sie.json"
        try:
            bad_env.write_text("{not-json", encoding="utf-8")
            r = self.run_cmd(
                "--file", str(bad_env),
                "--trusted-issuers", str(self.keyring),
            )
            self.assertEqual(r.returncode, EXIT_INPUT_ERROR)
            self.assertIn("not valid json", (r.stdout + r.stderr).lower())
        finally:
            bad_env.unlink(missing_ok=True)

    def test_missing_envelope_file_fails_with_input_error(self):
        r = self.run_cmd(
            "--file", str(self.root / "tests" / "does_not_exist.sie.json"),
            "--trusted-issuers", str(self.keyring),
        )
        self.assertEqual(r.returncode, EXIT_INPUT_ERROR)
        self.assertIn("envelope file not found", (r.stdout + r.stderr).lower())

    def test_missing_check_file_fails_with_input_error(self):
        r = self.run_cmd(
            "--file", str(self.env_file),
            "--trusted-issuers", str(self.keyring),
            "--check-file", str(self.root / "tests" / "missing_skill.md"),
        )
        self.assertEqual(r.returncode, EXIT_INPUT_ERROR)
        self.assertIn("check file not found", (r.stdout + r.stderr).lower())

    def test_bad_trusted_issuer_format_fails_with_input_error(self):
        bad_keyring = self.root / "tests" / "tmp_bad_keyring_array.json"
        bad_keyring.write_text("[]", encoding="utf-8")
        try:
            r = self.run_cmd(
                "--file", str(self.env_file),
                "--trusted-issuers", str(bad_keyring),
            )
            self.assertEqual(r.returncode, EXIT_INPUT_ERROR)
            self.assertIn("must be a json object", (r.stdout + r.stderr).lower())
        finally:
            bad_keyring.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
