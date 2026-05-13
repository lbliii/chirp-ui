from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "plans" / "PLAN-bengal-chirpui-library-contract.md"
CHIRP_THEME = ROOT / "docs" / "CHIRP-THEME.md"


def test_bengal_library_asset_modes_are_defined_as_platform_contract() -> None:
    plan = PLAN.read_text(encoding="utf-8")
    wave_3 = plan.split("### Wave 3 — Bengal Library Asset Modes", 1)[1].split("### Wave 4", 1)[0]

    for mode in ("bundle", "link", "none"):
        assert f"| `{mode}` |" in wave_3

    for required in [
        "Bengal owns this mode switch",
        "mode is not Chirp UI package metadata",
        "dev server and static build",
        "fingerprinted",
        "diagnostics",
    ]:
        assert required in wave_3


def test_chirp_theme_docs_keep_current_css_loading_as_transitional() -> None:
    text = CHIRP_THEME.read_text(encoding="utf-8")

    assert "current CSS loading contract is a transitional boundary" in text
    assert "Bengal has first-class library asset modes" in text
    assert "bundle`, `link`, and `none`" in text
