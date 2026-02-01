from __future__ import annotations

from pathlib import Path

from integrations.sie_loader import load_verified_instructions
from sie_policy import evaluate_untrusted_content


def main() -> int:
    # 1) Load trusted instructions (fail closed if invalid)
    instr = load_verified_instructions(
        Path("SKILL.md.sie.json"),
        keyring_path=Path("trusted_issuers.json"),
        check_file_path=Path("SKILL.md"),  # optional
    )

    print("=== LOADED TRUSTED INSTRUCTIONS ===")
    print(f"Issuer: {instr.issuer}")
    print(f"Envelope ID: {instr.envelope_id}")
    print(instr.content.strip())
    print()

    # 2) Treat external inputs as untrusted content
    untrusted_email = (Path("demo") / "injected_email.txt").read_text(encoding="utf-8")

    decision = evaluate_untrusted_content(
        untrusted_content=untrusted_email,
        constraints=instr.constraints,
        extra_patterns=("BANANA_CODE_ALPHA",),
    )

    print("=== DECISION ON UNTRUSTED CONTENT ===")
    if not decision.allowed:
        print("[BLOCKED] " + decision.reason)
    else:
        print("[ALLOW] " + decision.reason)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
