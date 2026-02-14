import argparse
import hashlib
import json
from pathlib import Path

EXIT_OK = 0
EXIT_VERIFY_FAIL = 2
EXIT_INPUT_ERROR = 3


class InputError(ValueError):
    """User/input/configuration error (missing files, malformed JSON, bad keyring)."""


class VerificationError(ValueError):
    """Cryptographic or trust verification failure."""


def fail(msg: str, code: int) -> int:
    print(f"[FAIL] {msg}")
    return code


def load_json_file(path: Path, kind: str) -> dict:
    if not path.exists():
        raise InputError(f"{kind} not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise InputError(f"{kind} is not valid JSON: {path}") from e
    if not isinstance(data, dict):
        raise InputError(f"{kind} must be a JSON object")
    return data


def load_trusted_issuers(path: Path) -> dict:
    return load_json_file(path, "Trusted issuer file")


def resolve_issuer(env: dict) -> str:
    issuer = env.get("issuer") or env.get("payload", {}).get("issuer")
    if not issuer:
        raise VerificationError("Envelope missing issuer field")
    return issuer


def resolve_pubkey(env: dict, args) -> str:
    # 1) Explicit CLI pubkey override (highest priority)
    if args.pubkey:
        return args.pubkey

    # 2) Trusted keyring lookup by issuer
    issuer = resolve_issuer(env)
    keyring = load_trusted_issuers(Path(args.trusted_issuers))
    pub = keyring.get(issuer)
    if not pub:
        raise VerificationError(f"Issuer '{issuer}' is not trusted.")
    return pub


def main() -> int:
    p = argparse.ArgumentParser(description="Verify a .sie.json envelope (SIE v0.1).")
    p.add_argument("--file", required=True, help="Path to .sie.json file")
    p.add_argument("--pubkey", required=False, help="Public key base64 override")
    p.add_argument(
        "--check-file",
        required=False,
        help="Path to external file to hash-check against payload.sha256",
    )
    p.add_argument(
        "--trusted-issuers",
        required=False,
        default="trusted_issuers.json",
        help="Path to trusted issuer keyring JSON (default: trusted_issuers.json)",
    )

    args = p.parse_args()

    try:
        env = load_json_file(Path(args.file), "Envelope file")

        pub = resolve_pubkey(env, args)

        cf = None
        if args.check_file:
            cf = Path(args.check_file)
            if not cf.exists():
                raise InputError(f"Check file not found: {cf}")

        try:
            from sie_lib import verify_envelope
        except Exception as e:
            raise InputError(f"Verifier dependency unavailable: {e}") from e

        try:
            verify_envelope(env, pub)
        except ValueError as e:
            raise VerificationError(str(e)) from e

        if cf is not None:
            # Hash text content with UTF-8 to stay consistent with signing flow
            # across platforms/checkouts (e.g., Windows CRLF conversions).
            disk_hash = hashlib.sha256(cf.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            env_hash = env.get("payload", {}).get("sha256")

            if not env_hash:
                raise VerificationError("Envelope has no payload.sha256 to compare against.")

            if disk_hash != env_hash:
                raise VerificationError(
                    "External file hash does not match signed payload.sha256 (file was modified)."
                )

    except InputError as e:
        return fail(str(e), EXIT_INPUT_ERROR)
    except VerificationError as e:
        return fail(str(e), EXIT_VERIFY_FAIL)

    print("[OK] Signature verified and basic checks passed.")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
