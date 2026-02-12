from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

UPSTREAM_PATCH_FILES = [
    "integrations/sie_enforcement.py",
    "integrations/openclaw_sie_config.py",
    "integrations/openclaw_hook.py",
    "integrations/openclaw_loader_reference.py",
    "integrations/__init__.py",
    "integrations/openclaw_loader_sim.py",
    "sie_verify.py",
    "tests/test_sie_enforcement.py",
    "tests/test_openclaw_sie_config.py",
    "tests/test_openclaw_hook.py",
    "tests/test_openclaw_loader_reference.py",
    "tests/test_loader_sim.py",
    "tests/test_verify_cli.py",
    "tests/test_integration_api.py",
]


def build_manifest(paths: Iterable[str], *, repo_root: Path) -> dict:
    files = []
    missing = []
    for rel in paths:
        p = repo_root / rel
        if p.exists():
            files.append(rel)
        else:
            missing.append(rel)

    return {
        "bundle": "openclaw-sie-integration-mvp",
        "fileCount": len(files),
        "files": files,
        "missing": missing,
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = build_manifest(UPSTREAM_PATCH_FILES, repo_root=repo_root)
    out = repo_root / "integrations" / "upstream_patch_manifest.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    if manifest["missing"]:
        print("Missing files detected:")
        for f in manifest["missing"]:
            print(f"- {f}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
