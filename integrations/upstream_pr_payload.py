from __future__ import annotations

import json
from pathlib import Path


def build_pr_payload(manifest: dict) -> str:
    files = "\n".join(f"- `{f}`" for f in manifest.get("files", []))
    return f"""## Summary
Add a minimal, optional SIE enforcement integration slice for loader-time trust decisions.

## Behavior
- unsigned + warn => allow
- unsigned + strict => reject
- signed + valid => allow
- signed + invalid => reject

## Included files ({manifest.get('fileCount', 0)})
{files}

## Validation
```bash
python -m unittest discover -s tests -p \"test_*.py\" -v
```

## Notes
- Backward compatible when SIE is disabled.
- Reason codes are stable constants for machine consumers.
"""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "integrations" / "upstream_patch_manifest.json"
    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload = build_pr_payload(manifest)
    out = root / "integrations" / "upstream_pr_payload.md"
    out.write_text(payload, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
