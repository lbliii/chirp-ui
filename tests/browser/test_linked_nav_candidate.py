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


async def test_linked_nav_candidate_uses_existing_primitives_only(page, base_url):
    await page.goto(base_url + "/linked-nav-candidate")
    await wait_for_alpine(page)

    fixture = page.get_by_test_id("linked-nav-candidate")
    await expect(fixture).to_be_visible()
    assert await fixture.get_attribute("data-public-api") == "false"
    assert await fixture.get_attribute("data-existing-primitives") == (
        "sidebar sidebar_section sidebar_link nav_tree-linked drawer drawer_trigger"
    )

    await expect(page.locator(".chirpui-sidebar")).to_be_visible()
    await expect(page.locator(".chirpui-sidebar__link--active")).to_be_visible()
    await expect(
        page.get_by_test_id("linked-nav-sidebar-tree").locator(
            ".chirpui-nav-tree--linked-branches"
        )
    ).to_be_visible()
    await expect(page.locator(".chirpui-docs-sidebar")).to_have_count(0)
    await expect(page.locator(".chirpui-catalog-sidebar")).to_have_count(0)


async def test_linked_nav_candidate_branch_links_and_server_open_children(page, base_url):
    await page.goto(base_url + "/linked-nav-candidate")
    await wait_for_alpine(page)

    tree = page.get_by_test_id("linked-nav-sidebar-tree")
    await expect(tree.locator("summary")).to_have_count(0)

    guide = tree.get_by_role("link", name="Guide 4")
    await expect(guide).to_be_visible()
    assert await guide.get_attribute("href") == "/linked-nav-candidate/guide"

    active_child = tree.get_by_role("link", name="Install")
    await expect(active_child).to_be_visible()
    assert await active_child.get_attribute("aria-current") == "page"

    closed_branch = tree.get_by_role("link", name="Reference")
    await expect(closed_branch).to_be_visible()
    assert await closed_branch.get_attribute("href") == "/linked-nav-candidate/reference"
    await expect(tree.get_by_text("Hidden child until server marks branch open")).to_have_count(0)

    await expect(tree.get_by_text("No-href group")).to_be_visible()
    await expect(tree.get_by_role("link", name="Grouped child")).to_be_visible()


async def test_linked_nav_candidate_parent_active_descendant_is_app_shaped(page, base_url):
    await page.goto(base_url + "/linked-nav-candidate")
    await wait_for_alpine(page)

    tree = page.get_by_test_id("linked-nav-sidebar-tree")
    guide = tree.get_by_role("link", name="Guide 4")
    active_child = tree.get_by_role("link", name="Install")

    await expect(guide).to_be_visible()
    await expect(active_child).to_be_visible()
    assert await active_child.get_attribute("aria-current") == "page"
    assert await guide.get_attribute("aria-current") is None

    guide_class = await guide.get_attribute("class")
    assert "chirpui-nav-tree__link--active" not in (guide_class or "")


async def test_linked_nav_candidate_long_child_label_stays_inside_sidebar(page, base_url):
    await page.set_viewport_size({"width": 768, "height": 720})
    await page.goto(base_url + "/linked-nav-candidate")
    await wait_for_alpine(page)

    long_child = page.get_by_role(
        "link",
        name=(
            "Configuration with a deliberately long child label that must wrap "
            "inside the sidebar"
        ),
    )
    await expect(long_child).to_be_visible()
    await _assert_no_document_horizontal_overflow(page)

    metrics = await long_child.evaluate(
        """(node) => {
            const sidebar = document.querySelector(".chirpui-sidebar");
            const nodeRect = node.getBoundingClientRect();
            const sidebarRect = sidebar.getBoundingClientRect();
            return {
                nodeLeft: nodeRect.left,
                nodeRight: nodeRect.right,
                sidebarLeft: sidebarRect.left,
                sidebarRight: sidebarRect.right,
            };
        }"""
    )
    assert metrics["nodeLeft"] >= metrics["sidebarLeft"] - 1, metrics
    assert metrics["nodeRight"] <= metrics["sidebarRight"] + 1, metrics


async def test_linked_nav_candidate_phone_drawer_preserves_linked_tree(page, base_url):
    await page.set_viewport_size({"width": 320, "height": 720})
    await page.goto(base_url + "/linked-nav-candidate")
    await wait_for_alpine(page)

    await expect(page.locator(".linked-nav-candidate-sidebar")).to_be_hidden()
    trigger = page.get_by_role("button", name="Open section navigation")
    await expect(trigger).to_be_visible()

    await trigger.click()
    drawer = page.locator("#linked-nav-candidate-drawer")
    await expect(drawer).to_be_visible()
    assert await drawer.evaluate("el => el.open")

    tree = page.get_by_test_id("linked-nav-drawer-tree")
    await expect(tree.locator("summary")).to_have_count(0)
    await expect(tree.get_by_role("link", name="Guide 4")).to_be_visible()
    active_child = tree.get_by_role("link", name="Install")
    await expect(active_child).to_be_visible()
    assert await active_child.get_attribute("aria-current") == "page"
    await expect(tree.get_by_text("Hidden child until server marks branch open")).to_have_count(0)

    long_child = tree.get_by_role(
        "link",
        name=(
            "Configuration with a deliberately long child label that must wrap "
            "inside the sidebar"
        ),
    )
    await expect(long_child).to_be_visible()
    await _assert_no_document_horizontal_overflow(page)

    metrics = await long_child.evaluate(
        """(node) => {
            const drawer = document.querySelector("#linked-nav-candidate-drawer");
            const nodeRect = node.getBoundingClientRect();
            const drawerRect = drawer.getBoundingClientRect();
            return {
                nodeLeft: nodeRect.left,
                nodeRight: nodeRect.right,
                drawerLeft: drawerRect.left,
                drawerRight: drawerRect.right,
            };
        }"""
    )
    assert metrics["nodeLeft"] >= metrics["drawerLeft"] - 1, metrics
    assert metrics["nodeRight"] <= metrics["drawerRight"] + 1, metrics

    await page.keyboard.press("Escape")
    await expect(drawer).not_to_be_visible()
    assert not await drawer.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.textContent?.includes('Open section navigation')"
    )
