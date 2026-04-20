"""Surface variants — @scope envelope (envelope hardening batch 1, S4).

Verifies that the @scope + @layer envelope form of 039_surface.css preserves
variant rendering and that the upper boundary `.chirpui-surface .chirpui-surface`
keeps outer-surface variant rules (cornered corner accents, --muted background)
from bleeding onto a nested surface.

See docs/PLAN-css-scope-and-layer.md § Hardening batch 1.
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


VARIANTS = [
    ("v-default", "chirpui-surface--default"),
    ("v-muted", "chirpui-surface--muted"),
    ("v-elevated", "chirpui-surface--elevated"),
    ("v-accent", "chirpui-surface--accent"),
    ("v-glass", "chirpui-surface--glass"),
]


@pytest.mark.parametrize(("section", "modifier"), VARIANTS)
async def test_variant_renders_with_modifier_class(page, base_url, section, modifier):
    await page.goto(base_url + "/surface-variants")
    surface = page.locator(f"[data-testid='{section}'] .chirpui-surface").first
    classes = await surface.get_attribute("class")
    assert modifier in (classes or ""), (
        f"{section}: expected {modifier} in class list, got {classes}"
    )


async def test_muted_has_subtle_background(page, base_url):
    """--muted resolves to var(--chirpui-bg-subtle) via :scope.chirpui-surface--muted."""
    await page.goto(base_url + "/surface-variants")
    surface = page.locator("[data-testid='v-muted'] .chirpui-surface--muted")
    bg = await surface.evaluate("el => getComputedStyle(el).backgroundColor")
    assert bg, "background-color should resolve to a value"
    assert bg != "rgba(0, 0, 0, 0)", f"expected non-transparent background, got {bg!r}"


async def test_elevated_resolves_surface_elevated_token(page, base_url):
    """--elevated reads --chirpui-surface-elevated for background via the @scope rule.

    (Box-shadow is intentionally not asserted: --chirpui-elevation-2 is defined
    with `light-dark(...)`, which only applies to color values, so the shadow
    falls back to `none` independent of this conversion.)
    """
    await page.goto(base_url + "/surface-variants")
    surface = page.locator("[data-testid='v-elevated'] .chirpui-surface--elevated")
    elev_var = await surface.evaluate(
        "el => getComputedStyle(el).getPropertyValue('--chirpui-surface-elevated').trim()"
    )
    assert elev_var, "expected --chirpui-surface-elevated to resolve to a value"


async def test_glass_has_backdrop_filter(page, base_url):
    """--glass applies backdrop-filter via the @supports + @scope rule."""
    await page.goto(base_url + "/surface-variants")
    surface = page.locator("[data-testid='v-glass'] .chirpui-surface--glass")
    backdrop = await surface.evaluate(
        "el => getComputedStyle(el).backdropFilter || getComputedStyle(el).webkitBackdropFilter"
    )
    assert "blur" in backdrop, f"expected backdrop-filter blur, got {backdrop!r}"


async def test_cornered_is_position_relative(page, base_url):
    """--cornered sets position: relative (so ::before/::after can absolute-position)."""
    await page.goto(base_url + "/surface-variants")
    surface = page.locator("[data-testid='v-cornered'] .chirpui-surface--cornered").first
    position = await surface.evaluate("el => getComputedStyle(el).position")
    assert position == "relative"


async def test_cornered_pseudo_elements_render(page, base_url):
    """--cornered ::before has non-zero width (the corner accent rule applies)."""
    await page.goto(base_url + "/surface-variants")
    surface = page.locator("[data-testid='v-cornered'] .chirpui-surface--cornered").first
    width = await surface.evaluate("el => getComputedStyle(el, '::before').width")
    # Width is the --chirpui-corner-accent-size token; just verify it's resolved.
    assert width, f"expected resolved ::before width, got {width!r}"
    assert width not in ("auto", "0px"), f"::before width should be set, got {width!r}"


async def test_nested_inner_surface_is_not_cornered(page, base_url):
    """Outer surface's --cornered must NOT propagate to an inner nested surface.

    The outer surface has class `chirpui-surface--cornered` (position: relative,
    ::before/::after corner accents). The @scope upper boundary stops the rule
    at the first nested .chirpui-surface — so the inner surface should NOT have
    `position: relative` from the outer's variant rule, nor a non-zero ::before
    width inherited from the outer cornered ::before.

    Without the boundary, you'd be safe in this specific case anyway because
    the outer rule targets `:scope.chirpui-surface--cornered` (modifier on the
    scope root), not descendants. This test pins the convention: future
    descendant-style rules added inside the envelope will be stopped here.
    """
    await page.goto(base_url + "/surface-variants")

    # The inner surface — second .chirpui-surface inside the nested section.
    inner = page.locator("[data-testid='v-nested'] .chirpui-surface .chirpui-surface")
    assert await inner.count() == 1, "expected exactly one nested inner surface"

    # Inner should not be cornered: no `chirpui-surface--cornered` modifier,
    # and no ::before content (the cornered accents only attach to .chirpui-surface--cornered).
    inner_classes = await inner.get_attribute("class") or ""
    assert "chirpui-surface--cornered" not in inner_classes

    # Inner ::before should resolve to "none" content (no pseudo-element rule fires).
    inner_before_content = await inner.evaluate("el => getComputedStyle(el, '::before').content")
    assert inner_before_content == "none", (
        f"inner surface ::before unexpectedly rendered (content={inner_before_content!r}) — "
        "an outer-surface descendant rule may be bleeding through the @scope boundary"
    )
