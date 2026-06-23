"""Load the generated blocks gallery payload for the component showcase."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

GALLERY_PATH = Path(__file__).resolve().parent.parent / "generated" / "blocks_gallery.json"


@cache
def load_blocks_gallery() -> dict[str, Any]:
    """Return the committed blocks gallery JSON."""
    if not GALLERY_PATH.is_file():
        msg = (
            f"Missing {GALLERY_PATH.name}. Run: poe build-blocks-gallery "
            "from the repo root."
        )
        raise FileNotFoundError(msg)
    return json.loads(GALLERY_PATH.read_text(encoding="utf-8"))
