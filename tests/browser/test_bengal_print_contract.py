"""Browser proof for the packaged Bengal theme print/PDF contract."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.async_api import expect

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = "/tests/browser/templates/bengal_print_contract.html"

PRINT_WIDTHS = [
    pytest.param(794, "a4-portrait", id="a4-portrait"),
    pytest.param(816, "letter-portrait", id="letter-portrait"),
    pytest.param(1124, "a3-portrait", id="a3-portrait"),
    pytest.param(1056, "letter-landscape", id="letter-landscape"),
    pytest.param(1588, "a3-landscape", id="a3-landscape"),
]


@pytest.fixture(scope="module")
def static_repo_url():
    handler = partial(SimpleHTTPRequestHandler, directory=str(REPO_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


async def open_print_fixture(page, static_repo_url: str, width: int = 1124) -> None:
    await page.set_viewport_size({"width": width, "height": 1000})
    await page.goto(f"{static_repo_url}{FIXTURE_PATH}")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_function("() => window.BengalMain")


async def dispatch_print_event(page, name: str) -> None:
    await page.evaluate("name => window.dispatchEvent(new Event(name))", name)


async def test_print_preserves_tabs_and_closed_disclosures(page, static_repo_url):
    await open_print_fixture(page, static_repo_url)

    legacy_inactive = page.locator("#legacy-template")
    disclosure = page.locator("details.dropdown")
    await expect(legacy_inactive).to_be_hidden()
    assert not await disclosure.evaluate("element => element.open")

    await page.emulate_media(media="print")
    await dispatch_print_event(page, "beforeprint")

    for selector in (
        "header",
        "nav",
        ".docs-nav",
        ".toc-sidebar",
        "button",
        "footer",
        ".tab-nav",
    ):
        await expect(page.locator(selector).first).to_be_hidden()

    for selector in (
        "#legacy-python",
        "#legacy-template",
        "#native-first",
        "#native-second",
        ".dropdown-content",
    ):
        await expect(page.locator(selector)).to_be_visible()

    assert await disclosure.evaluate("element => element.open")
    assert (
        await legacy_inactive.evaluate("element => getComputedStyle(element, '::before').content")
        == '"Template"'
    )

    embed_fallbacks = {
        ".video-embed": '"Video content — see the online version."',
        ".audio-embed": '"Audio content — see the online version."',
        ".code-embed": '"Interactive code example — see the online version."',
        ".terminal-embed": '"Terminal recording — see the online version."',
    }
    for selector, expected in embed_fallbacks.items():
        await expect(page.locator(selector)).to_be_visible()
        assert (
            await page.locator(selector).evaluate(
                "element => getComputedStyle(element, '::after').content"
            )
            == expected
        )
        assert (
            await page.locator(selector).evaluate(
                "element => element.getBoundingClientRect().height"
            )
            < 100
        )
        assert (
            await page.locator(selector).evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            == "rgba(0, 0, 0, 0)"
        )

    await expect(page.locator(".video-embed iframe")).to_be_hidden()
    await expect(page.locator(".audio-embed audio")).to_be_hidden()
    await expect(page.locator(".code-embed iframe")).to_be_hidden()

    await dispatch_print_event(page, "afterprint")
    assert not await disclosure.evaluate("element => element.open")


async def test_dark_mode_print_forces_legible_light_paper_palette(page, static_repo_url):
    await open_print_fixture(page, static_repo_url)
    await page.evaluate("document.documentElement.dataset.theme = 'dark'")
    await page.emulate_media(media="print", color_scheme="dark")
    await dispatch_print_event(page, "beforeprint")

    styles = await page.evaluate(
        """() => {
            const read = (selector) => {
                const style = getComputedStyle(document.querySelector(selector));
                return {
                    background: style.backgroundColor,
                    color: style.color,
                    fontSize: parseFloat(style.fontSize),
                    lineHeight: parseFloat(style.lineHeight),
                    opacity: style.opacity,
                };
            };
            const list = document.querySelector('.print-related-list');
            const penultimate = list.children[list.children.length - 2];
            const listItemStyle = getComputedStyle(list.children[0]);
            return {
                root: read('html'),
                body: read('body'),
                paragraph: read('.print-lead-in'),
                callout: read('.print-callout-copy'),
                table: read('.print-table-copy'),
                code: read('.rosettes code'),
                keyword: read('.syntax-control'),
                string: read('.syntax-string'),
                listMargin: parseFloat(listItemStyle.marginBlockStart),
                penultimateBreakAfter: getComputedStyle(penultimate).breakAfter,
            };
        }"""
    )

    assert styles["root"]["background"] == "rgb(255, 255, 255)"
    assert styles["body"]["background"] == "rgb(255, 255, 255)"
    for name in ("paragraph", "callout", "table", "code"):
        assert styles[name]["color"] == "rgb(17, 17, 17)", {name: styles[name]}
        assert styles[name]["opacity"] == "1", {name: styles[name]}

    assert styles["paragraph"]["fontSize"] >= 14.5
    assert styles["callout"]["fontSize"] >= 14.5
    assert styles["table"]["fontSize"] >= 12
    assert styles["code"]["fontSize"] >= 12
    assert styles["keyword"]["color"] == "rgb(91, 33, 182)"
    assert styles["string"]["color"] == "rgb(22, 101, 52)"
    assert styles["listMargin"] <= 3
    assert styles["penultimateBreakAfter"] == "avoid-page"


async def test_print_lifecycle_sanitizes_links_and_marks_only_long_blocks(page, static_repo_url):
    await open_print_fixture(page, static_repo_url)
    await page.emulate_media(media="print")
    await dispatch_print_event(page, "beforeprint")

    assert await page.locator("#named-external-link").get_attribute("data-print-href") == (
        "https://example.com/reference?mode=full"
    )
    assert await page.locator("#url-external-link").get_attribute("data-print-href") is None
    await expect(page.locator(".print-document-meta")).to_have_count(1)
    await expect(page.locator(".print-document-meta__title")).to_have_text("Bengal print contract")
    await expect(page.locator(".print-document-meta__source a")).to_have_text(
        "https://docs.example.com/print-contract/"
    )

    assert await page.locator("#long-code").get_attribute("data-print-breakable") == "true"
    assert await page.locator("#long-callout").get_attribute("data-print-breakable") == "true"
    assert await page.locator(".tabs pre").first.get_attribute("data-print-breakable") is None
    assert (
        await page.locator("#long-code").evaluate(
            "element => getComputedStyle(element).breakInside"
        )
        == "auto"
    )

    await dispatch_print_event(page, "afterprint")
    await expect(page.locator(".print-document-meta")).to_have_count(0)
    assert await page.locator("#named-external-link").get_attribute("data-print-href") is None
    assert await page.locator("#long-code").get_attribute("data-print-breakable") is None


@pytest.mark.parametrize(("width", "paper"), PRINT_WIDTHS)
async def test_print_layout_uses_available_paper_width(
    page, static_repo_url, width: int, paper: str
):
    await open_print_fixture(page, static_repo_url, width)
    await page.emulate_media(media="print")
    await dispatch_print_event(page, "beforeprint")

    dimensions = await page.evaluate(
        """() => {
            const root = document.documentElement;
            const article = document.querySelector('.chirp-theme-docs-layout__article');
            const content = document.querySelector('.chirp-theme-docs-layout__content');
            return {
                rootWidth: root.clientWidth,
                articleWidth: article.getBoundingClientRect().width,
                contentWidth: content.getBoundingClientRect().width,
                overflow: Math.ceil(root.scrollWidth - root.clientWidth),
            };
        }"""
    )

    assert dimensions["overflow"] <= 1, {paper: dimensions}
    assert dimensions["contentWidth"] >= dimensions["rootWidth"] * 0.95, {paper: dimensions}
    assert dimensions["articleWidth"] >= dimensions["rootWidth"] * 0.95, {paper: dimensions}


async def test_pdf_runs_print_lifecycle_and_restores_disclosures(page, static_repo_url, tmp_path):
    await page.add_init_script(
        """window.__printEvents = [];
        window.addEventListener('beforeprint', () => window.__printEvents.push('beforeprint'));
        window.addEventListener('afterprint', () => window.__printEvents.push('afterprint'));
        """
    )
    await open_print_fixture(page, static_repo_url)

    output = tmp_path / "bengal-print-contract.pdf"
    await page.pdf(
        path=str(output),
        format="A4",
        print_background=True,
        display_header_footer=False,
        tagged=True,
        outline=True,
    )

    pdf_bytes = output.read_bytes()
    assert pdf_bytes.startswith(b"%PDF-")
    assert output.stat().st_size > 10_000
    for marker in (b"/StructTreeRoot", b"/MarkInfo", b"/Outlines", b"/Lang (en)"):
        assert marker in pdf_bytes
    assert await page.evaluate("window.__printEvents") == ["beforeprint", "afterprint"]
    assert not await page.locator("details.dropdown").evaluate("element => element.open")
    await expect(page.locator(".print-document-meta")).to_have_count(0)
