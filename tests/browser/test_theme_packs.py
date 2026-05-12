"""Browser proof for packaged token-only theme packs."""

import pytest

from chirp_ui.theme_packs import THEME_PACKS

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

EXPECTED_TOKENS = {
    "atlas": {
        "light": {
            "--chirpui-bg": "oklch(0.985 0.004 250)",
            "--chirpui-surface": "oklch(1 0 0)",
            "--chirpui-text": "oklch(0.22 0.032 250)",
            "--chirpui-accent": "oklch(0.56 0.16 250)",
        },
        "dark": {
            "--chirpui-bg": "oklch(0.17 0.024 250)",
            "--chirpui-surface": "oklch(0.24 0.03 250)",
            "--chirpui-text": "oklch(0.94 0.008 250)",
            "--chirpui-accent": "oklch(0.75 0.13 250)",
        },
    },
    "ember": {
        "light": {
            "--chirpui-bg": "oklch(0.982 0.01 78)",
            "--chirpui-surface": "oklch(0.995 0.006 78)",
            "--chirpui-text": "oklch(0.23 0.035 55)",
            "--chirpui-accent": "oklch(0.58 0.16 42)",
        },
        "dark": {
            "--chirpui-bg": "oklch(0.17 0.032 48)",
            "--chirpui-surface": "oklch(0.24 0.04 48)",
            "--chirpui-text": "oklch(0.94 0.014 70)",
            "--chirpui-accent": "oklch(0.74 0.14 48)",
        },
    },
    "sage": {
        "light": {
            "--chirpui-bg": "oklch(0.982 0.008 145)",
            "--chirpui-surface": "oklch(0.995 0.004 145)",
            "--chirpui-text": "oklch(0.22 0.03 145)",
            "--chirpui-accent": "oklch(0.55 0.13 155)",
        },
        "dark": {
            "--chirpui-bg": "oklch(0.17 0.024 145)",
            "--chirpui-surface": "oklch(0.24 0.03 145)",
            "--chirpui-text": "oklch(0.94 0.01 145)",
            "--chirpui-accent": "oklch(0.72 0.12 155)",
        },
    },
}


async def _computed_tokens(page, names: tuple[str, ...]) -> dict[str, str]:
    return await page.evaluate(
        """(names) => {
            const style = getComputedStyle(document.documentElement);
            return Object.fromEntries(
                names.map((name) => [name, style.getPropertyValue(name).trim()])
            );
        }""",
        list(names),
    )


async def _computed_element_styles(
    page, selector: str, properties: tuple[str, ...]
) -> dict[str, str]:
    return await page.locator(selector).first.evaluate(
        """(element, properties) => {
            const style = getComputedStyle(element);
            return Object.fromEntries(
                properties.map((property) => [property, style.getPropertyValue(property).trim()])
            );
        }""",
        list(properties),
    )


@pytest.mark.parametrize("pack", THEME_PACKS, ids=[pack.name for pack in THEME_PACKS])
@pytest.mark.parametrize("mode", ["light", "dark"])
async def test_theme_pack_light_and_dark_modes_resolve_pack_tokens(page, base_url, pack, mode):
    """Theme pack resources should win in Chromium, not just in static CSS syntax checks."""
    await page.goto(f"{base_url}/theme-pack-preview/{pack.name}/{mode}")

    assert await page.get_attribute("html", "data-theme") == mode
    assert await page.get_attribute("html", "data-theme-pack") == pack.name
    assert await page.locator(f'link[href="/static/{pack.path}"]').count() == 1
    assert await page.locator("[data-testid='card-probe']").is_visible()
    assert await page.locator("[data-testid='surface-probe']").is_visible()

    expected = EXPECTED_TOKENS[pack.name][mode]
    assert await _computed_tokens(page, tuple(expected)) == expected


@pytest.mark.parametrize("pack", THEME_PACKS, ids=[pack.name for pack in THEME_PACKS])
async def test_theme_pack_system_mode_tracks_browser_color_scheme(page, base_url, pack):
    """System mode should follow the browser preference for every packaged theme pack."""
    await page.emulate_media(color_scheme="light")
    await page.goto(f"{base_url}/theme-pack-preview/{pack.name}/system")
    light_tokens = await _computed_tokens(page, ("--chirpui-bg", "--chirpui-text"))

    await page.emulate_media(color_scheme="dark")
    await page.reload()
    dark_tokens = await _computed_tokens(page, ("--chirpui-bg", "--chirpui-text"))

    assert await page.get_attribute("html", "data-theme") == "system"
    assert light_tokens == {
        "--chirpui-bg": EXPECTED_TOKENS[pack.name]["light"]["--chirpui-bg"],
        "--chirpui-text": EXPECTED_TOKENS[pack.name]["light"]["--chirpui-text"],
    }
    assert dark_tokens == {
        "--chirpui-bg": EXPECTED_TOKENS[pack.name]["dark"]["--chirpui-bg"],
        "--chirpui-text": EXPECTED_TOKENS[pack.name]["dark"]["--chirpui-text"],
    }
    assert light_tokens != dark_tokens


@pytest.mark.parametrize("pack", THEME_PACKS, ids=[pack.name for pack in THEME_PACKS])
@pytest.mark.parametrize("mode", ["light", "dark"])
@pytest.mark.parametrize(
    ("viewport_width", "viewport_height"),
    [(1280, 900), (390, 760)],
    ids=["desktop", "mobile"],
)
async def test_theme_pack_surface_mix_renders_without_responsive_overflow(
    page,
    base_url,
    pack,
    mode,
    viewport_width,
    viewport_height,
):
    """Theme packs should hold across common component surfaces and viewports."""
    await page.set_viewport_size({"width": viewport_width, "height": viewport_height})
    await page.goto(f"{base_url}/theme-pack-preview/{pack.name}/{mode}")

    for testid in (
        "navigation-probe",
        "form-probe",
        "overlay-probe",
        "dense-data-probe",
    ):
        assert await page.locator(f"[data-testid='{testid}']").is_visible()

    overflow = await page.evaluate(
        "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
    )
    assert overflow <= 1

    input_styles = await _computed_element_styles(
        page,
        "[data-testid='form-probe'] .chirpui-field__input",
        ("background-color", "border-color", "color"),
    )
    nav_styles = await _computed_element_styles(
        page,
        "[data-testid='navigation-probe'] .chirpui-primary-nav__link",
        ("background-color", "color"),
    )
    table_styles = await _computed_element_styles(
        page,
        "[data-testid='dense-data-probe'] .chirpui-table__td",
        ("border-color", "color"),
    )
    overlay_styles = await _computed_element_styles(
        page,
        "[data-testid='overlay-probe'] .chirpui-overlay",
        ("position", "background-image"),
    )

    assert all(input_styles.values())
    assert all(nav_styles.values())
    assert all(table_styles.values())
    assert overlay_styles["position"] == "absolute"
    assert overlay_styles["background-image"] != "none"
