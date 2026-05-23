"""Browser evidence for compact header/page hero investigation."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def open_compact_header_candidate(page, base_url: str, *, width: int, height: int):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/compact-header-candidate")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_compact_header_candidate_uses_existing_primitives_only(page, base_url):
    await open_compact_header_candidate(page, base_url, width=1024, height=768)

    fixture = page.get_by_test_id("compact-header-candidate")
    await expect(fixture).to_be_visible()
    assert await fixture.get_attribute("data-reference-implementation") == (
        "compact-header-reference"
    )
    assert await fixture.get_attribute("data-scenario-complete") == "true"
    assert await fixture.get_attribute("data-public-api") == "false"
    assert await fixture.get_attribute("data-existing-primitives") == (
        "page_header page_hero search_header entity_header document_header route_tabs"
    )
    assert await fixture.get_attribute("data-promotion-boundary") == (
        "no compact_page_header docs_header page_hero params markup css manifest"
    )

    await expect(page.locator(".chirpui-page-header--compact")).to_be_visible()
    await expect(page.locator(".chirpui-hero--page-minimal")).to_have_count(2)
    await expect(page.locator(".chirpui-search-header")).to_be_visible()
    await expect(page.locator(".chirpui-entity-header")).to_be_visible()
    await expect(page.locator(".chirpui-document-header")).to_be_visible()
    await expect(page.locator(".chirpui-compact-page-header")).to_have_count(0)
    await expect(page.locator(".chirpui-docs-header")).to_have_count(0)
    await expect(page.locator(".chirpui-catalog-header")).to_have_count(0)


async def test_compact_header_candidate_empty_page_hero_optional_regions_collapse(page, base_url):
    await open_compact_header_candidate(page, base_url, width=1024, height=768)

    hero = page.get_by_test_id("minimal-page-hero-empty-proof")
    await expect(hero.locator(".chirpui-hero__eyebrow")).not_to_be_visible()
    await expect(hero.locator(".chirpui-hero__actions")).not_to_be_visible()
    await expect(hero.locator(".chirpui-hero__metadata")).not_to_be_visible()
    await expect(hero.locator(".chirpui-hero__footer")).not_to_be_visible()

    # The content wrapper is still emitted by the existing page_hero contract.
    await expect(hero.locator(".chirpui-hero__content")).to_have_count(1)


async def test_compact_header_candidate_filled_page_hero_regions_remain_available(page, base_url):
    await open_compact_header_candidate(page, base_url, width=1024, height=768)

    hero = page.get_by_test_id("minimal-page-hero-filled-proof")
    await expect(hero.locator(".chirpui-hero__eyebrow")).to_contain_text("Docs / Reference")
    await expect(hero.locator(".chirpui-hero__actions")).to_contain_text("Copy link")
    await expect(hero.locator(".chirpui-hero__metadata")).to_contain_text("Updated today")
    await expect(hero.locator(".chirpui-hero__content")).to_contain_text("Short contextual content")
    await expect(hero.locator(".chirpui-hero__footer")).to_contain_text("Footer metadata")


@pytest.mark.parametrize(
    ("width", "height"),
    [
        pytest.param(320, 720, id="phone"),
        pytest.param(768, 1024, id="tablet"),
        pytest.param(1280, 900, id="desktop"),
    ],
)
async def test_compact_header_candidate_stays_within_viewport(page, base_url, width, height):
    await open_compact_header_candidate(page, base_url, width=width, height=height)

    await assert_no_document_horizontal_overflow(page, f"compact-header-candidate-{width}x{height}")
    await expect(page.get_by_role("button", name="Primary action")).to_be_visible()
    await expect(
        page.get_by_role("button", name="Secondary action with a deliberately long label")
    ).to_be_visible()
