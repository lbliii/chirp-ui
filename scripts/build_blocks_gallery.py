"""Emit ``examples/component-showcase/generated/blocks_gallery.json``.

Pure Python, deterministic. Mirrors ``scripts/build_manifest.py`` — same
``--check`` gate pattern so CI fails when the committed gallery drifts from
the registry.

See issue #211 — registry-generated copy-paste blocks gallery.

Usage
-----
From the repo root::

    python scripts/build_blocks_gallery.py          # writes blocks_gallery.json
    python scripts/build_blocks_gallery.py --check  # exits non-zero if stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from chirp_ui.blocks_gallery import build_gallery, to_json_gallery, to_json_gallery_check

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "examples" / "component-showcase" / "generated" / "blocks_gallery.json"


def build() -> str:
    """Return canonical blocks gallery JSON."""
    return to_json_gallery(build_gallery(with_previews=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the committed blocks_gallery.json is stale.",
    )
    parser.add_argument(
        "--no-previews",
        action="store_true",
        help="Skip live preview rendering (faster; for debugging only).",
    )
    args = parser.parse_args(argv)

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        generated_full = (
            build() if not args.no_previews else to_json_gallery(build_gallery(with_previews=False))
        )
        generated_check = to_json_gallery_check(json.loads(generated_full))
        current_check = to_json_gallery_check(json.loads(current)) if current else ""
        if current_check != generated_check:
            sys.stderr.write(
                f"{OUTPUT.relative_to(REPO_ROOT)} is stale relative to the registry.\n"
                f"Run: poe build-blocks-gallery\n"
            )
            return 1
        return 0

    generated = (
        to_json_gallery(build_gallery(with_previews=not args.no_previews))
        if args.no_previews
        else build()
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated, encoding="utf-8")
    sys.stdout.write(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(generated):,} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
