from pathlib import Path

PARTIALS_DIR = (
    Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates" / "css" / "partials"
)
CSS_PATH = Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates" / "chirpui.css"


def test_density_scale_tokens_shipped() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    for token in (
        "--chirpui-density-cell-padding-y",
        "--chirpui-density-field-margin-bottom",
        "--chirpui-density-header-padding",
        "--chirpui-density-grid-gap",
    ):
        assert token in css


def test_density_container_classes_cascade() -> None:
    css = (PARTIALS_DIR / "183_density-scale.css").read_text(encoding="utf-8")
    assert '[data-density="compact"]' in css
    assert ".chirpui-density--compact" in css
    assert '[data-density="dense"]' in css
    assert ".chirpui-density--dense" in css


def test_component_compact_modifiers_alias_density_tokens() -> None:
    css = (PARTIALS_DIR / "183_density-scale.css").read_text(encoding="utf-8")
    for selector in (
        ".chirpui-table--compact",
        ".chirpui-field--dense",
        ".chirpui-page-header--compact",
        ".chirpui-timeline--compact",
        ".chirpui-data-grid--compact",
    ):
        assert selector in css


def test_table_compact_uses_density_tokens() -> None:
    css = (PARTIALS_DIR / "059_table.css").read_text(encoding="utf-8")
    assert "var(--chirpui-density-cell-padding-y)" in css
    assert "var(--chirpui-density-cell-padding-x)" in css


def test_fab_respects_touch_target_floor() -> None:
    css = (PARTIALS_DIR / "182_fab.css").read_text(encoding="utf-8")
    assert "min-block-size: var(--chirpui-control-touch-target)" in css
    assert "z-index: var(--chirpui-z-fab)" in css
