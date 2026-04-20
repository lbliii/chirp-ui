"""Emit ``src/chirp_ui/manifest.json`` as shipped package data.

Pure Python, stdlib only, deterministic. Mirrors
``scripts/build_chirpui_css.py`` — same ``--check`` gate pattern so CI fails
when the committed manifest drifts from the registry.

See ``docs/DESIGN-manifest-signature-extraction.md § Decision 3`` and
``docs/PLAN-agent-grounding-depth.md § Sprint 3``.

Usage
-----
From the repo root::

    python scripts/build_manifest.py          # writes manifest.json
    python scripts/build_manifest.py --check  # exits non-zero if stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from chirp_ui.manifest import build_manifest, to_json

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "src" / "chirp_ui" / "manifest.json"


def build() -> str:
    """Return the canonical manifest JSON — indent=2, sorted keys, trailing NL."""
    text = to_json(build_manifest(), indent=2)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the committed manifest.json is stale.",
    )
    args = parser.parse_args(argv)

    generated = build()

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            sys.stderr.write(
                f"{OUTPUT.relative_to(REPO_ROOT)} is stale relative to the registry.\n"
                f"Run: poe build-manifest\n"
            )
            return 1
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    sys.stdout.write(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(generated):,} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
