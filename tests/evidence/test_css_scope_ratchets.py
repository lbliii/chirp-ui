from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
PARTIALS = ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials"
PLAN = ROOT / "docs" / "plans" / "PLAN-css-scope-and-layer.md"


def _first_non_comment_token(text: str) -> str:
    text = text.lstrip()
    while text.startswith("/*"):
        end = text.find("*/")
        if end == -1:
            return text
        text = text[end + 2 :].lstrip()
    return text


def _authored_layer_partials() -> list[str]:
    return sorted(
        path.name
        for path in PARTIALS.glob("*.css")
        if _first_non_comment_token(path.read_text(encoding="utf-8")).startswith(
            "@layer chirpui.component"
        )
    )


def test_css_scope_envelope_detection_is_correct() -> None:
    """The "first token is ``@layer chirpui.component``" rule — which the build
    uses to decide whether a partial opts out of wrapping — must classify a known
    envelope partial and a known flat partial correctly.

    The converted *set* is the grep (auto-discovered), deliberately not a
    hand-maintained doc list or tally; the plan must not re-introduce one (that
    was pure bookkeeping that drifted on every conversion).
    """
    authored = _authored_layer_partials()
    assert "045_card.css" in authored, "the card envelope pilot must be detected"
    assert "001_tokens.css" not in authored, "a flat partial must not be detected"
    assert len(authored) >= 1

    plan = PLAN.read_text(encoding="utf-8")
    assert "grep -lE" in plan, "plan must cite the canonical grep command"
    assert "@layer chirpui" in plan, "plan must name the detection token"
    assert "Current converted count:" not in plan, "no hand-maintained tally (it drifts)"
    assert "Converted partials currently include:" not in plan, "no hand-maintained list"


def test_css_scope_plan_names_next_opportunistic_queue_and_proof() -> None:
    text = PLAN.read_text(encoding="utf-8")
    queue = text.split("### Next opportunistic queue", 1)[1].split(
        "### Per-PR conversion template", 1
    )[0]

    for partial in [
        "071_button.css",
        "070_form-fields.css",
        "059_table.css",
        "027_navbar.css",
        "029_sidebar.css",
        "054_tabs.css",
        "067_tabs-panels.css",
    ]:
        assert f"`{partial}`" in queue

    for proof in [
        "browser focus/hover proof",
        "browser focus/error/disabled proof",
        "browser proof for dense rows",
        "mobile overflow behavior",
        "active/focus and overflow behavior",
        "panel ownership",
    ]:
        assert proof in queue
