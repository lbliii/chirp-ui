from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "docs" / "ROADMAP-pre-1.0.md"
PLANS = ROOT / "docs" / "plans"


def test_active_plans_are_mapped_to_roadmap_workstreams() -> None:
    """Every live plan should be anchored to the current roadmap, not free-floating."""
    roadmap = ROADMAP.read_text(encoding="utf-8")
    active_plans = sorted(path.name for path in PLANS.glob("PLAN-*.md"))

    missing = [name for name in active_plans if name not in roadmap]
    assert not missing, "active plans missing roadmap workstream mapping: " + ", ".join(missing)


def test_active_plan_count_stays_intentional() -> None:
    """Planning cleanup should keep live plans bounded and force explicit review on growth."""
    active_plans = sorted(path.name for path in PLANS.glob("PLAN-*.md"))

    assert len(active_plans) <= 5, "active plan count exceeded cap: " + ", ".join(active_plans)


def test_archived_plans_do_not_claim_active_or_draft_status() -> None:
    """Archived plans may mention history, but their status line must not be active/draft."""
    offenders: list[str] = []
    for path in sorted((PLANS / "done").glob("PLAN-*.md")):
        for line in path.read_text(encoding="utf-8").splitlines()[:8]:
            normalized = line.strip().lower().strip("*")
            if normalized in {"status: active", "status: draft"}:
                offenders.append(path.name)
                break

    assert not offenders, "archived plans with active/draft status: " + ", ".join(offenders)


def test_active_plans_expose_next_work_marker() -> None:
    """Live plans should point agents at remaining work, not only historical design."""
    accepted_markers = (
        "## Residual Work",
        "## Next Slice",
        "## Next Batches",
        "## Ranked Backlog",
        "## Recommended Execution Order",
        "## Sprint Structure",
        "## Open items",
        "## Ranked Waves",
    )
    missing: list[str] = []

    for path in sorted(PLANS.glob("PLAN-*.md")):
        text = path.read_text(encoding="utf-8")
        if not any(marker in text for marker in accepted_markers):
            missing.append(path.name)

    assert not missing, "active plans missing a next-work marker: " + ", ".join(missing)
