"""Contract: card + surface respond to chirpui-layout container width (#209).

The context rail (~20rem) and main column each establish a named inline-size
container so card/surface adapt to column width, not just viewport breakpoints.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CSS = REPO / "src" / "chirp_ui" / "templates" / "css" / "partials"


def test_app_shell_regions_establish_layout_container() -> None:
    shell = (CSS / "083_app-shell.css").read_text(encoding="utf-8")
    for region in (".chirpui-app-shell__main", ".chirpui-app-shell__context-rail"):
        start = shell.index(region)
        block = shell[start : start + 400]
        assert "container-type: inline-size" in block, (
            f"{region} must establish inline-size container"
        )
        assert "container-name: chirpui-layout" in block, f"{region} must name chirpui-layout"


def test_card_uses_container_queries_not_viewport_for_header_actions() -> None:
    card = (CSS / "045_card.css").read_text(encoding="utf-8")
    assert "@container chirpui-layout (width < 36rem)" in card
    assert ".chirpui-card__header-actions" in card
    assert "@media (max-width: 36rem)" not in card


def test_card_stacks_horizontal_variant_in_narrow_container() -> None:
    card = (CSS / "045_card.css").read_text(encoding="utf-8")
    assert "@container chirpui-layout (width < 28rem)" in card
    assert "chirpui-card--horizontal" in card


def test_surface_tightens_padding_in_narrow_container() -> None:
    surface = (CSS / "039_surface.css").read_text(encoding="utf-8")
    assert "@container chirpui-layout (width < 28rem)" in surface
    assert "chirpui-surface--no-padding" in surface
