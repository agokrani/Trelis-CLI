"""Apply overlay.yaml to openapi.json and write build/openapi.merged.json.

Read by `make regen` before invoking the SDK generator. Keeps upstream
openapi.json untouched while letting us inject the missing
`securitySchemes` / `security` / `servers` blocks.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "openapi.json"
OVERLAY = ROOT / "overlay.yaml"
OUT_DIR = ROOT / "build"
OUT = OUT_DIR / "openapi.merged.json"


def deep_merge(base: dict, patch: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def main() -> None:
    spec = json.loads(SPEC.read_text())
    overlay = yaml.safe_load(OVERLAY.read_text()) or {}
    merged = deep_merge(spec, overlay)
    OUT_DIR.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(merged, indent=2))
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
