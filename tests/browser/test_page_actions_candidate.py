from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine


async def _assert_no_document_horizontal_overflow(page) -> None:
    metrics = await page.evaluate(
        """() => ({
            clientWidth: document.documentElement.clientWidth,
            scrollWidth: document.documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth,
        })"""
    )
    assert metrics["scrollWidth"] <= metrics["clientWidth"] + 1, metrics
    assert metrics["bodyScrollWidth"] <= metrics["clientWidth"] + 1, metrics


async def test_page_actions_candidate_uses_existing_primitives_only(page, base_url):
    await page.goto(base_url + "/page-actions-candidate")
    await wait_for_alpine(page)

    fixture = page.get_by_test_id("page-actions-candidate")
    await expect(fixture).to_be_visible()
    assert await fixture.get_attribute("data-public-api") == "false"
    assert await fixture.get_attribute("data-existing-primitives") == (
        "page_header dropdown_menu share_menu action_bar copy_btn"
    )

    await expect(page.locator(".chirpui-page-header")).to_be_visible()
    await expect(page.locator(".chirpui-dropdown#candidate-page-tools")).to_be_visible()
    await expect(page.locator(".chirpui-share-menu")).to_be_visible()
    await expect(page.locator(".chirpui-action-bar")).to_be_visible()
    await expect(page.locator(".chirpui-copy-btn")).to_be_visible()
    await expect(page.locator(".chirpui-message-bubble--assistant")).to_be_visible()
    await expect(page.locator(".chirpui-page-actions")).to_have_count(0)
    await expect(page.locator("[data-chirpui-component='page-actions']")).to_have_count(0)


async def test_page_actions_candidate_dropdown_exposes_non_social_commands(page, base_url):
    await page.goto(base_url + "/page-actions-candidate")
    await wait_for_alpine(page)

    await page.get_by_text("Page tools").click()
    menu = page.locator("#candidate-page-tools .chirpui-dropdown__menu")
    await expect(menu).to_be_visible()
    await expect(menu.get_by_role("menuitem", name="Open current fixture")).to_be_visible()
    await expect(
        menu.get_by_role("menuitem", name="Open prompt text", exact=True)
    ).to_be_visible()
    await expect(menu.get_by_role("menuitem", name="Copy sample text")).to_be_visible()
    await expect(
        menu.get_by_role(
            "menuitem",
            name=(
                "Open prompt text with a deliberately long label that should stay inside "
                "the existing dropdown menu"
            ),
        )
    ).to_be_visible()
    await expect(menu.get_by_role("menuitem", name="Review existing primitives")).to_be_visible()

    open_prompt = menu.get_by_role("menuitem", name="Open prompt text", exact=True)
    assert await open_prompt.get_attribute("href") == "/page-actions-candidate/prompt.txt"
    copy_sample = menu.get_by_role("menuitem", name="Copy sample text")
    assert await copy_sample.get_attribute("data-action") == "copy-sample-text"


async def test_page_actions_candidate_long_dropdown_label_stays_contained(page, base_url):
    await page.set_viewport_size({"width": 320, "height": 720})
    await page.goto(base_url + "/page-actions-candidate")
    await wait_for_alpine(page)

    await page.get_by_text("Page tools").click()
    menu = page.locator("#candidate-page-tools .chirpui-dropdown__menu")
    long_item = menu.get_by_role(
        "menuitem",
        name="Open prompt text with a deliberately long label that should stay inside the existing dropdown menu",
    )
    await expect(menu).to_be_visible()
    await expect(long_item).to_be_visible()

    metrics = await page.evaluate(
        """() => {
            const menu = document.querySelector("#candidate-page-tools .chirpui-dropdown__menu");
            const item = Array.from(menu.querySelectorAll("[role='menuitem']")).find(
                (node) => node.textContent.includes("deliberately long label")
            );
            const menuRect = menu.getBoundingClientRect();
            const itemRect = item.getBoundingClientRect();
            return {
                viewportWidth: document.documentElement.clientWidth,
                menuLeft: menuRect.left,
                menuRight: menuRect.right,
                itemLeft: itemRect.left,
                itemRight: itemRect.right,
                scrollWidth: document.documentElement.scrollWidth,
            };
        }"""
    )
    assert metrics["menuLeft"] >= 0, metrics
    assert metrics["itemLeft"] >= metrics["menuLeft"], metrics
    assert metrics["menuRight"] <= metrics["viewportWidth"] + 1, metrics
    assert metrics["itemRight"] <= metrics["menuRight"] + 1, metrics
    assert metrics["scrollWidth"] <= metrics["viewportWidth"] + 1, metrics


async def test_page_actions_candidate_prompt_route_and_copy_feedback(page, base_url):
    await page.goto(base_url + "/page-actions-candidate")
    await wait_for_alpine(page)

    await page.evaluate("""
        navigator.clipboard.writeText = async (text) => {
            window._lastCopied = text;
        };
    """)

    prompt_text = await page.get_by_test_id("candidate-prompt-text").text_content()
    await page.get_by_role("button", name="Copy prompt text").click()
    await expect(page.locator(".chirpui-copy-btn__done")).to_be_visible()
    assert await page.evaluate("window._lastCopied") == prompt_text

    response = await page.request.get(base_url + "/page-actions-candidate/prompt.txt")
    assert response.ok
    assert await response.text() == prompt_text


async def test_page_actions_candidate_responsive_without_new_api(page, base_url):
    for width, height in [(320, 720), (390, 800), (768, 900), (1024, 900)]:
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(base_url + "/page-actions-candidate")
        await wait_for_alpine(page)

        await expect(page.get_by_test_id("candidate-header-actions")).to_be_visible()
        await expect(page.locator(".chirpui-page-actions")).to_have_count(0)
        await _assert_no_document_horizontal_overflow(page)
