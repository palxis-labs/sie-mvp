import argparse
import json
import os
from pathlib import Path

from sie_lib import generate_keypair, new_instruction_envelope, sign_envelope, canonical_json


def main() -> int:
    p = argparse.ArgumentParser(description="Sign an instruction file into a .sie.json envelope (SIE v0.1).")
    p.add_argument("--issuer", required=True, help="Issuer identifier, e.g. palxislabs")
    p.add_argument("--infile", required=True, help="Path to instruction file, e.g. SKILL.md")
    p.add_argument("--outfile", required=False, help="Output .sie.json path (default: <infile>.sie.json)")
    p.add_argument("--scope", nargs="*", default=["read_files"], help="Declared scope list")
    p.add_argument("--deny-prompt-disclosure", action="store_true", help="Set deny_prompt_disclosure constraint")
    p.add_argument("--no-external-urls", action="store_true", help="Set no_external_urls constraint")
    p.add_argument("--max-output-tokens", type=int, default=2000, help="Set max_output_tokens constraint")
    p.add_argument("--keyfile", default=".sie_private_key.b64", help="Where to store/load the private key (base64)")
    p.add_argument("--new-keys", action="store_true", help="Generate a new keypair and overwrite keyfile")
    args = p.parse_args()

    infile = Path(args.infile)
    if not infile.exists():
        raise SystemExit(f"Input file not found: {infile}")

    outfile = Path(args.outfile) if args.outfile else infile.with_suffix(infile.suffix + ".sie.json")

    keyfile = Path(args.keyfile)

    if args.new_keys or not keyfile.exists():
        pub, priv = generate_keypair()
        keyfile.write_text(priv, encoding="utf-8")
        # Also write public key beside it for convenience
        Path(str(keyfile) + ".pub").write_text(pub, encoding="utf-8")
        print(f"[ok] Generated new Ed25519 keypair.")
        print(f"     Private key: {keyfile}  (KEEP SECRET)")
        print(f"     Public key : {keyfile}.pub")
    else:
        priv = keyfile.read_text(encoding="utf-8").strip()
        pub_path = Path(str(keyfile) + ".pub")
        if pub_path.exists():
            pub = pub_path.read_text(encoding="utf-8").strip()
        else:
            pub = None

    content = infile.read_text(encoding="utf-8")

    constraints = {
        "no_external_urls": bool(args.no_external_urls),
        "max_output_tokens": int(args.max_output_tokens),
        "deny_prompt_disclosure": bool(args.deny_prompt_disclosure),
    }

    env = new_instruction_envelope(
        issuer=args.issuer,
        scope=list(args.scope),
        constraints=constraints,
        payload_name=infile.name,
        payload_content_type="text/markdown",
        payload_content=content,
        public_key_b64=pub if pub else None,
    )

    signed = sign_envelope(env, priv)

    outfile.write_text(canonical_json(signed), encoding="utf-8")
    print(f"[ok] Wrote signed envelope: {outfile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
