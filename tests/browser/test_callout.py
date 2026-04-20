"""Callout variants — @scope envelope (envelope hardening batch 1, S5).

Verifies that the @scope + @layer envelope form of 041_callout.css preserves
variant rendering and that the upper boundary `.chirpui-callout .chirpui-callout`
keeps outer-callout variant backgrounds and `:has()`-driven header autohide
from bleeding onto a nested callout.

See docs/PLAN-css-scope-and-layer.md § Hardening batch 1.
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


VARIANTS = [
    ("v-info", "chirpui-callout--info"),
    ("v-success", "chirpui-callout--success"),
    ("v-warning", "chirpui-callout--warning"),
    ("v-error", "chirpui-callout--error"),
    ("v-neutral", "chirpui-callout--neutral"),
]


@pytest.mark.parametrize(("section", "modifier"), VARIANTS)
async def test_variant_renders_with_modifier_class(page, base_url, section, modifier):
    await page.goto(base_url + "/callout-variants")
    callout = page.locator(f"[data-testid='{section}'] .chirpui-callout").first
    classes = await callout.get_attribute("class")
    assert modifier in (classes or ""), (
        f"{section}: expected {modifier} in class list, got {classes}"
    )


async def test_warning_has_tinted_background(page, base_url):
    """--warning resolves --chirpui-alert-warning-bg via :scope.chirpui-callout--warning."""
    await page.goto(base_url + "/callout-variants")
    callout = page.locator("[data-testid='v-warning'] .chirpui-callout--warning")
    bg = await callout.evaluate("el => getComputedStyle(el).backgroundColor")
    assert bg
    assert bg != "rgba(0, 0, 0, 0)", f"expected tinted background, got {bg!r}"


async def test_info_has_distinct_border_color(page, base_url):
    """--info sets border-inline-start-color via :scope.chirpui-callout--info."""
    await page.goto(base_url + "/callout-variants")
    callout = page.locator("[data-testid='v-info'] .chirpui-callout--info")
    # border-inline-start maps to border-left-color in LTR.
    border = await callout.evaluate("el => getComputedStyle(el).borderLeftColor")
    assert border
    assert border != "rgba(0, 0, 0, 0)", f"expected resolved border color, got {border!r}"


async def test_nested_inner_callout_keeps_own_variant_background(page, base_url):
    """Outer warning callout must NOT override inner info callout's background.

    Without the @scope upper boundary, an outer rule like
    `.chirpui-callout--warning .chirpui-callout { background: ... }` (none exist
    today, but could be added) would cascade through. The boundary stops the
    rule at the first nested .chirpui-callout, so inner callouts keep their own
    variant background.
    """
    await page.goto(base_url + "/callout-variants")

    outer = page.locator("[data-testid='v-nested'] > .chirpui-callout")
    inner = page.locator("[data-testid='v-nested'] .chirpui-callout .chirpui-callout")
    assert await inner.count() == 1, "expected exactly one nested inner callout"

    outer_bg = await outer.evaluate("el => getComputedStyle(el).backgroundColor")
    inner_bg = await inner.evaluate("el => getComputedStyle(el).backgroundColor")

    # Outer is warning, inner is info — backgrounds resolve from different tokens
    # and must differ.
    assert outer_bg != inner_bg, (
        f"inner callout background matches outer — variant rule may be bleeding "
        f"through the @scope boundary. outer={outer_bg!r} inner={inner_bg!r}"
    )


async def test_header_autohide_does_not_collapse_inner_header(page, base_url):
    """The :has()-driven empty-header autohide must not match across the boundary.

    The rule
    `.chirpui-callout__header:not(:has(.chirpui-callout__icon))…:has(:empty header-actions)`
    is scoped to the nearest .chirpui-callout. Because both the outer and inner
    callouts in the bleed case have a title, no header should be hidden — but
    even if the outer header was empty, the rule should not reach into the
    inner callout's header.
    """
    await page.goto(base_url + "/callout-variants")
    inner_header = page.locator(
        "[data-testid='v-nested'] .chirpui-callout .chirpui-callout .chirpui-callout__header"
    )
    display = await inner_header.evaluate("el => getComputedStyle(el).display")
    assert display != "none", "inner callout header should not be auto-hidden"
