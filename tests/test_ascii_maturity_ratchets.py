from pathlib import Path

from chirp_ui.manifest import build_manifest

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "plans" / "PLAN-ascii-maturity.md"
PUBLIC_SURFACE = ROOT / "docs" / "PUBLIC-SURFACE-STABILIZATION.md"


def _ascii_maturity_components() -> list[str]:
    manifest = build_manifest()["components"]
    return sorted(
        name
        for name, entry in manifest.items()
        if entry["template"]
        and entry["maturity"] == "experimental"
        and (name.startswith("ascii-") or name == "split-flap")
    )


def test_ascii_experimental_components_remain_owned_by_ascii_maturity_track() -> None:
    public_surface = PUBLIC_SURFACE.read_text(encoding="utf-8")

    for name in _ascii_maturity_components():
        assert f"| `{name}` | Keep experimental | ASCII maturity pass. |" in public_surface


def test_ascii_maturity_plan_names_accessibility_keyboard_and_browser_gates() -> None:
    text = PLAN.read_text(encoding="utf-8")

    for required in [
        "## Next Slice",
        "ARIA",
        "keyboard",
        "reduced-motion",
        "browser gauntlet",
        "Public surface stabilization",
    ]:
        assert required in text
