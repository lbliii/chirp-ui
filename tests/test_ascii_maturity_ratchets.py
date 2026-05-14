import re
from pathlib import Path

from chirp_ui.manifest import build_manifest

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "plans" / "done" / "PLAN-ascii-maturity.md"
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
        "### Interactive Control Gate",
        "### Remaining Not-Now List",
        "ARIA",
        "keyboard",
        "reduced-motion",
        "browser gauntlet",
        "Public surface stabilization",
    ]:
        assert required in text


def test_ascii_interactive_control_gate_covers_first_batch_controls() -> None:
    text = PLAN.read_text(encoding="utf-8")
    gate = text.split("### Interactive Control Gate", 1)[1].split("## Why This Matters", 1)[0]
    controls = {
        match for line in gate.splitlines() for match in re.findall(r"`(ascii-[^`]+)`", line)
    }

    assert controls == {
        "ascii-breaker-panel",
        "ascii-checkbox",
        "ascii-fader",
        "ascii-knob",
        "ascii-modal",
        "ascii-radio-group",
        "ascii-switch",
        "ascii-tabs",
        "ascii-toggle",
    }
    for required in ["Role target", "Keyboard target", "Browser proof"]:
        assert required in gate
