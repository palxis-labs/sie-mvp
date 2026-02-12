import argparse
import subprocess
import sys
from pathlib import Path


def verify_with_subprocess(verify_script: Path, envelope: Path, trusted_issuers: Path, skill_file: Path) -> tuple[bool, str]:
    cmd = [
        sys.executable,
        str(verify_script),
        "--file",
        str(envelope),
        "--trusted-issuers",
        str(trusted_issuers),
        "--check-file",
        str(skill_file),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        return True, (r.stdout or "").strip()
    return False, ((r.stdout or "") + (r.stderr or "")).strip()


def main() -> int:
    p = argparse.ArgumentParser(description="Simulate OpenClaw skill loader SIE decision branch.")
    p.add_argument("--skill", required=True, help="Path to SKILL.md")
    p.add_argument("--mode", choices=["warn", "strict"], default="warn", help="Unsigned skill behavior")
    p.add_argument("--verify-script", default="sie_verify.py", help="Path to verifier script")
    p.add_argument("--trusted-issuers", default="trusted_issuers.json", help="Path to trusted issuers keyring")
    p.add_argument("--envelope-suffix", default=".sie.json", help="Envelope suffix (default: .sie.json)")

    args = p.parse_args()

    skill = Path(args.skill)
    if not skill.exists():
        print(f"REJECT: skill file not found: {skill}")
        return 2

    envelope = Path(f"{skill}{args.envelope_suffix}")
    verify_script = Path(args.verify_script)
    trusted_issuers = Path(args.trusted_issuers)

    if not envelope.exists():
        if args.mode == "strict":
            print("REJECT: unsigned skill rejected (strict mode)")
            return 2
        print("ALLOW: unsigned skill allowed (warn mode)")
        return 0

    ok, detail = verify_with_subprocess(verify_script, envelope, trusted_issuers, skill)
    if not ok:
        print(f"REJECT: signed skill verify failed :: {detail}")
        return 2

    print("ALLOW: signed skill verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
