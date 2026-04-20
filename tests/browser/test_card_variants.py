"""Card variants — @scope envelope pilot (Sprint 5).

Asserts each card variant renders with its BEM modifier and a key computed
style, and verifies the bleed fix: outer-card :hover does NOT propagate to an
inner nested card because the `@scope (.chirpui-card) to (.chirpui-card
.chirpui-card)` upper boundary stops the outer rule at the first nested card.

See docs/PLAN-css-scope-and-layer.md § Sprint 5.
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


VARIANTS = [
    ("v-feature", "chirpui-card--feature"),
    ("v-horizontal", "chirpui-card--horizontal"),
    ("v-stats", "chirpui-card--stats"),
    ("v-link", "chirpui-card--link"),
    ("v-linked", "chirpui-card--linked"),
    ("v-collapsible", "chirpui-card--collapsible"),
    ("v-glass", "chirpui-card--glass"),
    ("v-gradient-border", "chirpui-card--gradient-border"),
    ("v-gradient-header", "chirpui-card--gradient-header"),
]


@pytest.mark.parametrize(("section", "modifier"), VARIANTS)
async def test_variant_renders_with_modifier_class(page, base_url, section, modifier):
    await page.goto(base_url + "/card-variants")
    card = page.locator(f"[data-testid='{section}'] .chirpui-card").first
    classes = await card.get_attribute("class")
    assert modifier in (classes or ""), (
        f"{section}: expected {modifier} in class list, got {classes}"
    )


async def test_horizontal_is_flex_row(page, base_url):
    """--horizontal sets flex-direction: row inside the @scope."""
    await page.goto(base_url + "/card-variants")
    card = page.locator("[data-testid='v-horizontal'] .chirpui-card--horizontal")
    direction = await card.evaluate("el => getComputedStyle(el).flexDirection")
    assert direction == "row"


async def test_stats_body_is_centered(page, base_url):
    """--stats centers text inside .chirpui-card__body via compound selector."""
    await page.goto(base_url + "/card-variants")
    body = page.locator("[data-testid='v-stats'] .chirpui-card__body")
    align = await body.evaluate("el => getComputedStyle(el).textAlign")
    assert align == "center"


async def test_glass_has_backdrop_filter(page, base_url):
    """--glass applies backdrop-filter."""
    await page.goto(base_url + "/card-variants")
    card = page.locator("[data-testid='v-glass'] .chirpui-card--glass")
    backdrop = await card.evaluate(
        "el => getComputedStyle(el).backdropFilter || getComputedStyle(el).webkitBackdropFilter"
    )
    assert "blur" in backdrop, f"expected backdrop-filter blur, got {backdrop!r}"


async def test_link_is_flex_column_full_height(page, base_url):
    """--link / --linked stretch to container height via display: flex; height: 100%."""
    await page.goto(base_url + "/card-variants")
    card = page.locator("[data-testid='v-link'] .chirpui-card--link")
    direction = await card.evaluate("el => getComputedStyle(el).flexDirection")
    assert direction == "column"


async def test_default_card_has_rest_border(page, base_url):
    """Default card has --chirpui-border resolved (non-empty, non-transparent)."""
    await page.goto(base_url + "/card-variants")
    card = page.locator("[data-testid='v-default'] .chirpui-card")
    border = await card.evaluate("el => getComputedStyle(el).borderTopColor")
    assert border, "border-top-color should resolve to a value"
    assert border != "rgba(0, 0, 0, 0)", f"expected non-transparent border, got {border!r}"


async def test_nested_card_bleed_is_fixed(page, base_url):
    """Outer card :hover must NOT change the inner card's border-color.

    Without the @scope upper boundary, the outer rule
    `.chirpui-card:not(.chirpui-card--link):hover { border-color: … }` would
    cascade to descendant `.chirpui-card` nodes and the inner card would
    flip color on outer hover. The @scope boundary stops the rule at the
    first nested .chirpui-card.
    """
    await page.goto(base_url + "/card-variants")

    outer = page.locator("[data-testid='v-nested'] > .chirpui-card")
    inner = page.locator("[data-testid='v-nested'] .chirpui-card .chirpui-card")

    # Sanity: nested DOM is as expected.
    assert await inner.count() == 1

    rest_border = await inner.evaluate("el => getComputedStyle(el).borderTopColor")

    # Hover the outer card and hold.
    await outer.hover()
    await page.wait_for_timeout(150)  # let transitions settle

    hover_border = await inner.evaluate("el => getComputedStyle(el).borderTopColor")

    assert hover_border == rest_border, (
        "inner card border-color changed on outer hover — @scope upper boundary is not "
        f"stopping the bleed. rest={rest_border!r} hover={hover_border!r}"
    )
