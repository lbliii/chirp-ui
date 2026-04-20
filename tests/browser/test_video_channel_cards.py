"""Video / Channel cards — @scope envelope (envelope hardening batch 1, S6).

Verifies that the @scope + @layer envelope forms of 046_video-card.css and
047_channel-card.css preserve rendering and that the upper boundaries
`.chirpui-video-card .chirpui-video-card` and
`.chirpui-channel-card .chirpui-channel-card` keep the bleed-prone hover rules
contained:

- video-card: bare `:scope:hover { border-color, box-shadow }` would otherwise
  cascade through every descendant `.chirpui-video-card`.
- channel-card: `.chirpui-channel-card__link:hover .chirpui-channel-card__name`
  would otherwise tint a nested card's name when the outer link is hovered.

See docs/PLAN-css-scope-and-layer.md § Hardening batch 1.
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_video_card_renders_with_class(page, base_url):
    await page.goto(base_url + "/video-channel-cards")
    card = page.locator("[data-testid='v-video'] .chirpui-video-card").first
    assert await card.count() == 1
    title = page.locator("[data-testid='v-video'] .chirpui-video-card__title")
    assert (await title.inner_text()).strip() == "Sample video"


async def test_channel_card_renders_with_class(page, base_url):
    await page.goto(base_url + "/video-channel-cards")
    card = page.locator("[data-testid='v-channel'] .chirpui-channel-card").first
    assert await card.count() == 1
    name = page.locator("[data-testid='v-channel'] .chirpui-channel-card__name")
    assert (await name.inner_text()).strip() == "Sample Channel"


async def test_video_card_hover_does_not_bleed_into_nested(page, base_url):
    """Outer video-card :hover border-color must not propagate to nested card.

    Without the @scope upper boundary, the bare `:scope:hover` rule
    (`border-color: var(--chirpui-card-hover-border)`) would match every
    descendant `.chirpui-video-card`, flipping inner borders too.
    """
    await page.goto(base_url + "/video-channel-cards")

    inner = page.locator("[data-testid='v-video-inner']")

    # Baseline inner border before any hover.
    inner_border_idle = await inner.evaluate("el => getComputedStyle(el).borderColor")

    # Hover the outer card (force=true tolerates nested-pointer-events quirks).
    outer = page.locator("[data-testid='v-video-outer']")
    await outer.hover(force=True)

    inner_border_hover = await inner.evaluate("el => getComputedStyle(el).borderColor")

    assert inner_border_idle == inner_border_hover, (
        "inner video-card border changed when outer was hovered — "
        f"{inner_border_idle!r} → {inner_border_hover!r}. "
        "The :scope:hover rule may be bleeding through the upper boundary."
    )


async def test_channel_card_link_hover_does_not_bleed_into_nested_name(page, base_url):
    """Outer channel-card link-hover must not tint a nested card's name.

    The descendant rule
    `.chirpui-channel-card__link:hover .chirpui-channel-card__name { color: accent }`
    is the canonical bleed candidate — without the @scope boundary, hovering
    the outer link would re-color the inner name too.
    """
    await page.goto(base_url + "/video-channel-cards")

    inner_name = page.locator("[data-testid='v-channel-inner-name']")
    idle_color = await inner_name.evaluate("el => getComputedStyle(el).color")

    outer_link = page.locator("[data-testid='v-channel-outer-link']")
    await outer_link.hover(force=True)

    hover_color = await inner_name.evaluate("el => getComputedStyle(el).color")

    assert idle_color == hover_color, (
        "inner channel-card name color changed when outer link was hovered — "
        f"{idle_color!r} → {hover_color!r}. "
        "The link:hover .name rule may be bleeding through the upper boundary."
    )
