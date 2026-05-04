import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_scanline_and_grain_overlays_are_visible(page, base_url):
    await page.goto(base_url + "/effects-visual")

    scanline = page.locator("[data-testid='scanline'] .chirpui-scanline").first
    scanline_before = await scanline.evaluate(
        """el => {
            const style = getComputedStyle(el, "::before");
            return {
                content: style.content,
                backgroundImage: style.backgroundImage,
                width: style.width,
                height: style.height,
            };
        }"""
    )
    scanline_after = await scanline.evaluate(
        """el => {
            const style = getComputedStyle(el, "::after");
            return {
                content: style.content,
                backgroundImage: style.backgroundImage,
                width: style.width,
                height: style.height,
            };
        }"""
    )
    assert scanline_before["content"] != "none"
    assert "gradient" in scanline_before["backgroundImage"]
    assert scanline_after["content"] != "none"
    assert "repeating-linear-gradient" in scanline_after["backgroundImage"]
    assert scanline_after["width"] != "0px"
    assert scanline_after["height"] != "0px"

    grain = page.locator("[data-testid='grain'] .chirpui-grain").first
    grain_after = await grain.evaluate(
        """el => {
            const style = getComputedStyle(el, "::after");
            return {
                content: style.content,
                backgroundImage: style.backgroundImage,
                backgroundSize: style.backgroundSize,
                opacity: Number(style.opacity),
                width: style.width,
                height: style.height,
            };
        }"""
    )
    assert grain_after["content"] != "none"
    assert "data:image/svg+xml" in grain_after["backgroundImage"]
    assert "97px 89px" in grain_after["backgroundSize"]
    assert grain_after["opacity"] > 0
    assert grain_after["width"] != "0px"
    assert grain_after["height"] != "0px"


async def test_particle_background_dots_are_visible_and_scattered(page, base_url):
    await page.goto(base_url + "/effects-visual")

    dots = await page.eval_on_selector_all(
        "[data-testid='particle'] .chirpui-particle-bg__dot",
        """dots => dots.map((dot) => {
            const style = getComputedStyle(dot);
            return {
                left: Number.parseFloat(dot.style.left),
                top: Number.parseFloat(dot.style.top),
                width: style.width,
                height: style.height,
                opacity: Number(style.opacity),
                backgroundColor: style.backgroundColor,
            };
        })""",
    )
    assert len(dots) == 12
    assert all(dot["width"] != "0px" and dot["height"] != "0px" for dot in dots)
    assert all(dot["opacity"] > 0 for dot in dots)
    assert all(dot["backgroundColor"] != "rgba(0, 0, 0, 0)" for dot in dots)

    xs = [dot["left"] for dot in dots]
    ys = [dot["top"] for dot in dots]
    assert max(xs) - min(xs) > 70
    assert max(ys) - min(ys) > 60
    assert xs != sorted(xs)
    assert ys != sorted(ys)


async def test_decorative_background_effects_have_nonzero_layers(page, base_url):
    await page.goto(base_url + "/effects-visual")

    selectors = {
        "aurora": ".chirpui-aurora__blob",
        "meteor": ".chirpui-meteor__streak",
        "symbol-rain": ".chirpui-symbol-rain__drop",
        "holy-light": ".chirpui-holy-light__mote",
        "rune-field": ".chirpui-rune-field__rune",
        "constellation": ".chirpui-constellation__star",
    }

    for testid, selector in selectors.items():
        layers = await page.eval_on_selector_all(
            f"[data-testid='{testid}'] {selector}",
            """layers => layers.map((layer) => {
                const style = getComputedStyle(layer);
                const rect = layer.getBoundingClientRect();
                return {
                    width: rect.width,
                    height: rect.height,
                    opacity: Number(style.opacity),
                    display: style.display,
                };
            })""",
        )
        assert layers, f"{testid} should render decorative layers"
        assert any(layer["width"] > 0 and layer["height"] > 0 for layer in layers), (
            f"{testid} should have at least one nonzero decorative layer"
        )
        assert any(layer["opacity"] > 0 and layer["display"] != "none" for layer in layers), (
            f"{testid} should have at least one visible decorative layer"
        )
