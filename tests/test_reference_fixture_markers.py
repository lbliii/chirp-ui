from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "tests" / "browser" / "templates"
APP = ROOT / "tests" / "browser" / "app.py"


REFERENCE_FIXTURES = {
    "page_actions_candidate_page.html": {
        "testid": "page-actions-candidate",
        "implementation": "page-actions-ai",
        "primitives": "page_header page_hero dropdown_menu share_menu action_bar copy_btn",
        "blocked": "no page_actions macro runtime descriptor css manifest generated-options",
    },
    "linked_nav_candidate_page.html": {
        "testid": "linked-nav-candidate",
        "implementation": "linked-nav-catalog",
        "primitives": "sidebar sidebar_section sidebar_link nav_tree-linked drawer drawer_trigger",
        "blocked": "no nav_tree params sidebar branch macros css manifest docs_shell",
    },
    "compact_header_candidate_page.html": {
        "testid": "compact-header-candidate",
        "implementation": "compact-header-reference",
        "primitives": "page_header page_hero search_header entity_header document_header route_tabs",
        "blocked": "no compact_page_header docs_header page_hero params markup css manifest",
    },
    "dense_reference_data_reference_page.html": {
        "testid": "dense-reference-data-reference",
        "implementation": "dense-reference-data",
        "primitives": (
            "resource_index resource_card filter_rail filter_bar search_header "
            "table params_table card badge callout"
        ),
        "blocked": "no data_grid virtual_table reference_page_macro filter_count_api css manifest runtime",
    },
}


def test_reference_browser_fixtures_keep_marker_contracts() -> None:
    for filename, expected in REFERENCE_FIXTURES.items():
        text = (TEMPLATES / filename).read_text(encoding="utf-8")

        assert f'data-testid="{expected["testid"]}"' in text
        assert f'data-reference-implementation="{expected["implementation"]}"' in text
        assert 'data-scenario-complete="true"' in text
        assert 'data-public-api="false"' in text
        assert f'data-existing-primitives="{expected["primitives"]}"' in text
        assert f'data-promotion-boundary="{expected["blocked"]}"' in text


def test_reference_browser_routes_stay_private_test_routes() -> None:
    text = APP.read_text(encoding="utf-8")

    for route in [
        "/page-actions-candidate",
        "/linked-nav-candidate",
        "/compact-header-candidate",
        "/dense-reference-data-reference",
    ]:
        assert f'@app.route("{route}")' in text

    template_text = "\n".join(
        (TEMPLATES / filename).read_text(encoding="utf-8")
        for filename in REFERENCE_FIXTURES
    )
    for public_name in [
        "{{ page_actions(",
        "{% call page_actions(",
        "{{ compact_page_header(",
        "{% call compact_page_header(",
        "{{ reference_page(",
        "{% call reference_page(",
        "{{ data_grid(",
        "{% call data_grid(",
    ]:
        assert public_name not in template_text
