"""Render tests for all chirp-ui components.

Each test verifies:
- Correct HTML structure (BEM classes present)
- Parameter variants (defaults, optional args)
- Slot content injection where applicable
"""

from __future__ import annotations

from kida import Environment


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------


class TestLayout:
    def test_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import container %}'
            "{% call container() %}Content{% end %}"
        ).render()
        assert "chirpui-container" in html
        assert "Content" in html

    def test_grid(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            "{% call grid() %}A{% end %}"
        ).render()
        assert "chirpui-grid" in html

    def test_grid_cols_2(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(cols=2) %}A{% end %}'
        ).render()
        assert "chirpui-grid--cols-2" in html

    def test_stack(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import stack %}'
            "{% call stack() %}A{% end %}"
        ).render()
        assert "chirpui-stack" in html

    def test_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import block %}'
            '{% call block(span=2) %}A{% end %}'
        ).render()
        assert "chirpui-block--span-2" in html


# ---------------------------------------------------------------------------
# Button
# ---------------------------------------------------------------------------


class TestButton:
    def test_btn_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Click me") }}'
        ).render()
        assert "chirpui-btn" in html
        assert "Click me" in html
        assert "chirpui-btn__label" in html
        assert "<button" in html

    def test_btn_primary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Submit", variant="primary") }}'
        ).render()
        assert "chirpui-btn--primary" in html

    def test_btn_loading(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", variant="primary", loading=true) }}'
        ).render()
        assert "chirpui-btn--loading" in html
        assert 'aria-busy="true"' in html
        assert "chirpui-btn__spinner" in html
        assert "chirpui-spinner" in html

    def test_btn_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Demo", variant="primary", href="/demo") }}'
        ).render()
        assert "<a " in html
        assert 'href="/demo"' in html
        assert "chirpui-btn--primary" in html


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------


class TestStreaming:
    def test_streaming_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block() %}Content{% end %}"
        ).render()
        assert "chirpui-streaming-block" in html
        assert "Content" in html
        assert "aria-live" in html

    def test_streaming_block_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            '{% call streaming_block(streaming=true) %}Partial{% end %}'
        ).render()
        assert "chirpui-streaming-block--active" in html
        assert "chirpui-streaming-block__cursor" in html

    def test_streaming_block_sse_swap_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            '{% call streaming_block(streaming=true, sse_swap_target=true) %}{% end %}'
        ).render()
        assert "sse-swap=\"fragment\"" in html
        assert "hx-target=\"this\"" in html

    def test_copy_btn(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}'
            '{{ copy_btn(label="Copy", copy_text="hello") }}'
        ).render()
        assert "chirpui-copy-btn" in html
        assert 'data-copy-text="hello"' in html

    def test_model_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card(title="Llama 3", badge="42ms") %}Answer{% end %}'
        ).render()
        assert "chirpui-model-card" in html
        assert "Llama 3" in html
        assert "42ms" in html
        assert "Answer" in html

    def test_model_card_sse_streaming(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card("llama3", badge="A", sse_connect="/stream", sse_streaming=true) %}'
            "{% end %}"
        ).render()
        assert "chirpui-model-card" in html
        assert 'sse-connect="/stream"' in html
        assert "hx-ext=\"sse\"" in html
        assert "sse-swap=\"fragment\"" in html


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


class TestCard:
    def test_basic_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            "{% call card() %}Body{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-card__body" in html
        assert "Body" in html

    def test_card_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Hello") %}Content{% end %}'
        ).render()
        assert "chirpui-card__header" in html
        assert "Hello" in html

    def test_card_with_footer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(footer="Footer text") %}Content{% end %}'
        ).render()
        assert "chirpui-card__footer" in html
        assert "Footer text" in html

    def test_card_collapsible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Toggle", collapsible=true) %}Hidden{% end %}'
        ).render()
        assert "<details" in html
        assert "<summary" in html
        assert "chirpui-card--collapsible" in html

    def test_card_collapsible_open(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Open", collapsible=true, open=true) %}Visible{% end %}'
        ).render()
        assert "open" in html

    def test_card_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            "{% call card() %}Just body{% end %}"
        ).render()
        assert "chirpui-card__header" not in html

    def test_card_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(cls="custom") %}Body{% end %}'
        ).render()
        assert "chirpui-card custom" in html


# ---------------------------------------------------------------------------
# Modal
# ---------------------------------------------------------------------------


class TestModal:
    def test_basic_modal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}'
            '{% call modal("dlg") %}Content{% end %}'
        ).render()
        assert '<dialog id="dlg"' in html
        assert "chirpui-modal" in html
        assert "chirpui-modal__body" in html
        assert "Content" in html

    def test_modal_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}'
            '{% call modal("dlg", title="Settings") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" in html
        assert "Settings" in html
        assert "chirpui-modal__close" in html

    def test_modal_sizes(self, env: Environment) -> None:
        for size in ("small", "medium", "large"):
            html = env.from_string(
                '{% from "chirpui/modal.html" import modal %}'
                f'{{% call modal("dlg", size="{size}") %}}Body{{% end %}}'
            ).render()
            assert f"chirpui-modal--{size}" in html

    def test_modal_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal_trigger %}'
            '{{ modal_trigger("dlg", label="Click me") }}'
        ).render()
        assert "chirpui-modal-trigger" in html
        assert "Click me" in html
        assert "dlg" in html

    def test_modal_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}'
            '{% call modal("dlg") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" not in html


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------


class TestTabs:
    def test_tabs_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tabs, tab %}'
            '{% call tabs() %}{{ tab("t1", "Tab One") }}{% end %}'
        ).render()
        assert "chirpui-tabs" in html
        assert 'role="tablist"' in html

    def test_tab_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("overview", "Overview", active=true) }}'
        ).render()
        assert "chirpui-tab--active" in html
        assert 'aria-selected="true"' in html
        assert "Overview" in html

    def test_tab_inactive(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("details", "Details") }}'
        ).render()
        assert "chirpui-tab--active" not in html
        assert 'aria-selected="false"' in html

    def test_tab_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("t1", "Tab", url="/tab/1", hx_target="#content") }}'
        ).render()
        assert 'hx-get="/tab/1"' in html
        assert 'hx-target="#content"' in html


# ---------------------------------------------------------------------------
# Dropdown
# ---------------------------------------------------------------------------


class TestDropdown:
    def test_basic_dropdown(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown.html" import dropdown %}'
            '{% call dropdown(label="Menu") %}<a href="/">Home</a>{% end %}'
        ).render()
        assert "<details" in html
        assert "<summary" in html
        assert "chirpui-dropdown" in html
        assert "chirpui-dropdown__menu" in html
        assert "Menu" in html

    def test_dropdown_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown.html" import dropdown %}'
            '{% call dropdown(label="Menu", cls="extra") %}Items{% end %}'
        ).render()
        assert "chirpui-dropdown extra" in html


# ---------------------------------------------------------------------------
# Toast
# ---------------------------------------------------------------------------


class TestToast:
    def test_toast_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast_container %}'
            "{{ toast_container() }}"
        ).render()
        assert 'id="chirpui-toasts"' in html
        assert "chirpui-toast-container" in html
        assert 'aria-live="polite"' in html

    def test_toast_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}'
            '{{ toast("Saved!") }}'
        ).render()
        assert "chirpui-toast--info" in html
        assert "Saved!" in html
        assert "hx-swap-oob" in html

    def test_toast_variants(self, env: Environment) -> None:
        for variant in ("info", "success", "warning", "error"):
            html = env.from_string(
                '{% from "chirpui/toast.html" import toast %}'
                f'{{{{ toast("msg", variant="{variant}") }}}}'
            ).render()
            assert f"chirpui-toast--{variant}" in html

    def test_toast_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}'
            '{{ toast("msg", dismissible=true) }}'
        ).render()
        assert "chirpui-toast__close" in html

    def test_toast_not_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}'
            '{{ toast("msg", dismissible=false) }}'
        ).render()
        assert "chirpui-toast__close" not in html

    def test_toast_no_oob(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}'
            '{{ toast("msg", oob=false) }}'
        ).render()
        assert "hx-swap-oob" not in html


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


class TestTable:
    def test_basic_table(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name", "Email"]) %}'
            '{{ row("Alice", "alice@example.com") }}'
            "{% end %}"
        ).render()
        assert "chirpui-table" in html
        assert "chirpui-table__th" in html
        assert "Name" in html
        assert "Email" in html
        assert "Alice" in html
        assert "alice@example.com" in html

    def test_table_striped(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            "{% call table(striped=true) %}{% end %}"
        ).render()
        assert "chirpui-table--striped" in html

    def test_table_no_headers(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table() %}{{ row("Data") }}{% end %}'
        ).render()
        assert "chirpui-table__th" not in html
        assert "chirpui-table__body" in html

    def test_row_renders_cells(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import row %}'
            '{{ row("A", "B", "C") }}'
        ).render()
        assert html.count("chirpui-table__td") == 3


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


class TestPagination:
    def test_basic_pagination(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            '{{ pagination(current=2, total=5,'
            ' url_pattern="/items?page={page}") }}'
        ).render()
        assert "chirpui-pagination" in html
        assert 'aria-label="Pagination"' in html
        assert 'aria-current="page"' in html

    def test_pagination_hidden_when_single_page(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            '{{ pagination(current=1, total=1,'
            ' url_pattern="/items?page={page}") }}'
        ).render()
        assert "chirpui-pagination" not in html

    def test_pagination_prev_disabled_on_first(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            '{{ pagination(current=1, total=3,'
            ' url_pattern="/p?page={page}") }}'
        ).render()
        assert "chirpui-pagination__link--disabled" in html

    def test_pagination_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            '{{ pagination(current=2, total=5,'
            ' url_pattern="/p?page={page}",'
            ' hx_target="#list") }}'
        ).render()
        assert 'hx-target="#list"' in html
        assert "hx-get" in html


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------


class TestAlert:
    def test_basic_alert(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            "{% call alert() %}Hello{% end %}"
        ).render()
        assert "chirpui-alert--info" in html
        assert 'role="alert"' in html
        assert "Hello" in html

    def test_alert_variants(self, env: Environment) -> None:
        for variant in ("info", "success", "warning", "error"):
            html = env.from_string(
                '{% from "chirpui/alert.html" import alert %}'
                f'{{% call alert(variant="{variant}") %}}msg{{% end %}}'
            ).render()
            assert f"chirpui-alert--{variant}" in html

    def test_alert_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            "{% call alert(dismissible=true) %}msg{% end %}"
        ).render()
        assert "chirpui-alert__close" in html

    def test_alert_not_dismissible_by_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            "{% call alert() %}msg{% end %}"
        ).render()
        assert "chirpui-alert__close" not in html


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------


class TestForms:
    """Test form macros.

    Note: ``field_errors`` filter is provided by Chirp, not chirp-ui.
    These tests exercise the macros without error display (errors=none).
    """

    def test_text_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("title", value="Hello", label="Title") }}'
        ).render()
        assert "chirpui-field" in html
        assert "chirpui-field__label" in html
        assert "chirpui-field__input" in html
        assert 'name="title"' in html
        assert 'value="Hello"' in html
        assert "Title" in html

    def test_text_field_required(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email", required=true) }}'
        ).render()
        assert "required" in html
        assert "chirpui-field__required" in html

    def test_text_field_with_hint(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("name", hint="Enter your full name") }}'
        ).render()
        assert "chirpui-field__hint" in html
        assert "Enter your full name" in html

    def test_textarea_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import textarea_field %}'
            '{{ textarea_field("desc", value="Content",'
            ' label="Description", rows=6) }}'
        ).render()
        assert "<textarea" in html
        assert 'rows="6"' in html
        assert "Content" in html

    def test_select_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import select_field %}'
            '{% set opts = [{"value": "a", "label": "Alpha"},'
            ' {"value": "b", "label": "Beta"}] %}'
            '{{ select_field("choice", options=opts,'
            ' selected="b", label="Pick") }}'
        ).render()
        assert "<select" in html
        assert "Alpha" in html
        assert "Beta" in html
        assert "selected" in html

    def test_checkbox_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import checkbox_field %}'
            '{{ checkbox_field("agree", label="I agree", checked=true) }}'
        ).render()
        assert 'type="checkbox"' in html
        assert "checked" in html
        assert "I agree" in html

    def test_hidden_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import hidden_field %}'
            '{{ hidden_field("id", value="42") }}'
        ).render()
        assert 'type="hidden"' in html
        assert 'name="id"' in html
        assert 'value="42"' in html

    def test_toggle_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import toggle_field %}'
            '{{ toggle_field("notify", label="Notifications", checked=true) }}'
        ).render()
        assert "chirpui-field--toggle" in html
        assert "chirpui-toggle" in html
        assert "chirpui-toggle__track" in html
        assert "Notifications" in html
        assert "checked" in html


# ---------------------------------------------------------------------------
# Wave 1: Divider, Link, Breadcrumbs, List, Accordion, Collapse, Tooltip
# ---------------------------------------------------------------------------


class TestDivider:
    def test_divider_line_only(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}'
            "{{ divider() }}"
        ).render()
        assert "chirpui-divider" in html
        assert 'role="separator"' in html

    def test_divider_with_text(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}'
            '{{ divider("OR") }}'
        ).render()
        assert "chirpui-divider__text" in html
        assert "OR" in html

    def test_divider_horizontal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}'
            '{{ divider("OR", horizontal=true) }}'
        ).render()
        assert "chirpui-divider--horizontal" in html

    def test_divider_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}'
            '{{ divider("OR", variant="primary") }}'
        ).render()
        assert "chirpui-divider--primary" in html


class TestLink:
    def test_link_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/link.html" import link %}'
            '{{ link("Home", href="/") }}'
        ).render()
        assert "chirpui-link" in html
        assert 'href="/"' in html
        assert "Home" in html

    def test_link_external(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/link.html" import link %}'
            '{{ link("Docs", href="https://example.com", external=true) }}'
        ).render()
        assert 'target="_blank"' in html
        assert 'rel="noopener noreferrer"' in html


class TestBreadcrumbs:
    def test_breadcrumbs_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
            '{% set items = [{"label": "Home", "href": "/"}, {"label": "Current"}] %}'
            "{{ breadcrumbs(items) }}"
        ).render()
        assert "chirpui-breadcrumbs" in html
        assert 'aria-label="Breadcrumb"' in html
        assert "Home" in html
        assert "Current" in html
        assert 'href="/"' in html
        assert 'aria-current="page"' in html


class TestList:
    def test_list_with_items(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group %}'
            '{% set items = ["A", "B", "C"] %}'
            '{{ list_group(items) }}'
        ).render()
        assert "chirpui-list" in html
        assert "chirpui-list__item" in html
        assert "A" in html and "B" in html and "C" in html

    def test_list_with_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group, list_item %}'
            "{% call list_group() %}"
            '{% call list_item() %}Row one{% end %}'
            '{% call list_item() %}Row two{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-list" in html
        assert "Row one" in html
        assert "Row two" in html

    def test_list_bordered(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group %}'
            '{% set items = ["A"] %}'
            '{{ list_group(items, bordered=true) }}'
        ).render()
        assert "chirpui-list--bordered" in html


class TestAccordion:
    def test_accordion_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion_item %}'
            '{% call accordion_item("Title", name="faq") %}Content{% end %}'
        ).render()
        assert "<details" in html
        assert 'name="faq"' in html
        assert "chirpui-accordion__item" in html
        assert "chirpui-accordion__trigger" in html
        assert "chirpui-accordion__content" in html
        assert "Title" in html
        assert "Content" in html

    def test_accordion_item_open(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion_item %}'
            '{% call accordion_item("Q", open=true) %}A{% end %}'
        ).render()
        assert "open" in html


class TestCollapse:
    def test_collapse_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/collapse.html" import collapse %}'
            '{% call collapse(trigger="Expand") %}Hidden{% end %}'
        ).render()
        assert "<details" in html
        assert "chirpui-collapse" in html
        assert "chirpui-collapse__trigger" in html
        assert "Expand" in html
        assert "Hidden" in html


class TestTooltip:
    def test_tooltip_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tooltip.html" import tooltip %}'
            '{% call tooltip(hint="Help text") %}Hover me{% end %}'
        ).render()
        assert "chirpui-tooltip" in html
        assert 'data-tooltip="Help text"' in html
        assert 'title="Help text"' in html
        assert "Hover me" in html


# ---------------------------------------------------------------------------
# Composition / Nesting
# ---------------------------------------------------------------------------


class TestComposition:
    def test_card_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Outer") %}'
            '{% call card(title="Inner") %}'
            "Nested content"
            "{% end %}"
            "{% end %}"
        ).render()
        assert html.count("chirpui-card__header") == 2
        assert "Outer" in html
        assert "Inner" in html
        assert "Nested content" in html

    def test_table_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% from "chirpui/table.html" import table, row %}'
            '{% call card(title="Users") %}'
            '{% call table(headers=["Name"]) %}'
            '{{ row("Alice") }}'
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-table" in html
        assert "Alice" in html

    def test_alert_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% from "chirpui/alert.html" import alert %}'
            '{% call card(title="Status") %}'
            '{% call alert(variant="success") %}All good{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-alert--success" in html
        assert "All good" in html


# ---------------------------------------------------------------------------
# ASCII Icon
# ---------------------------------------------------------------------------


class TestAsciiIcon:
    def test_static_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("✦") }}'
        ).render()
        assert "chirpui-ascii" in html
        assert "chirpui-ascii--md" in html
        assert "chirpui-ascii__char" in html
        assert "✦" in html
        assert 'aria-hidden="true"' in html

    def test_animation_variants(self, env: Environment) -> None:
        for anim in ("blink", "pulse", "shrink", "grow", "spin", "bounce", "throb", "wiggle", "glow"):
            html = env.from_string(
                '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
                f'{{{{ ascii_icon("◆", animation="{anim}") }}}}'
            ).render()
            assert f"chirpui-ascii--{anim}" in html
            assert "chirpui-ascii__char" in html
            assert "◆" in html

    def test_rotate_produces_four_spans(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("x", animation="rotate") }}'
        ).render()
        assert "chirpui-ascii--rotate" in html
        for i in range(1, 5):
            assert f"chirpui-ascii__char--{i}" in html
        assert "chirpui-ascii__char--2" in html
        assert "chirpui-ascii__char--3" in html
        assert "chirpui-ascii__char--4" in html
        assert "◜" in html and "◝" in html and "◞" in html and "◟" in html

    def test_sizes(self, env: Environment) -> None:
        for size in ("sm", "md", "lg", "xl"):
            html = env.from_string(
                '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
                f'{{{{ ascii_icon("●", size="{size}") }}}}'
            ).render()
            assert f"chirpui-ascii--{size}" in html

    def test_no_animation_class_when_none(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("★", animation="none") }}'
        ).render()
        assert "chirpui-ascii--none" not in html
        assert "chirpui-ascii--blink" not in html

    def test_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("◇", cls="my-icon") }}'
        ).render()
        assert "my-icon" in html


# ---------------------------------------------------------------------------
# Spinner
# ---------------------------------------------------------------------------


class TestSpinner:
    def test_spinner_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/spinner.html" import spinner %}'
            "{{ spinner() }}"
        ).render()
        assert "chirpui-spinner" in html
        assert "chirpui-spinner__mote" in html
        assert "✦" in html
        assert 'role="status"' in html
        assert 'aria-label="Loading"' in html

    def test_spinner_sizes(self, env: Environment) -> None:
        for size in ("sm", "md", "lg"):
            html = env.from_string(
                '{% from "chirpui/spinner.html" import spinner %}'
                f'{{{{ spinner(size="{size}") }}}}'
            ).render()
            assert f"chirpui-spinner--{size}" in html

    def test_spinner_thinking(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/spinner.html" import spinner_thinking %}'
            "{{ spinner_thinking() }}"
        ).render()
        assert "chirpui-spinner-thinking" in html
        assert "chirpui-spinner__char" in html
        assert "◜" in html
        assert 'aria-label="Processing"' in html


# ---------------------------------------------------------------------------
# Avatar
# ---------------------------------------------------------------------------


class TestAvatar:
    def test_avatar_initials(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}'
            '{{ avatar(initials="AB", alt="Alice") }}'
        ).render()
        assert "chirpui-avatar" in html
        assert "chirpui-avatar__initials" in html
        assert "AB" in html

    def test_avatar_size_variants(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}'
            '{{ avatar(initials="X", size="lg") }}'
        ).render()
        assert "chirpui-avatar--lg" in html


# ---------------------------------------------------------------------------
# Video Card
# ---------------------------------------------------------------------------


class TestVideoCard:
    def test_video_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/video_card.html" import video_card %}'
            '{{ video_card(href="/v", thumbnail="/t.jpg", duration="4:32", title="Test") }}'
        ).render()
        assert "chirpui-video-card" in html
        assert "4:32" in html
        assert "Test" in html


# ---------------------------------------------------------------------------
# CSS file
# ---------------------------------------------------------------------------


class TestCSS:
    def test_css_file_loads(self) -> None:
        """Verify the CSS file exists and is loadable from the templates dir."""
        from pathlib import Path

        css_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "chirp_ui"
            / "templates"
            / "chirpui.css"
        )
        assert css_path.exists()
        content = css_path.read_text()
        assert "--chirpui-border" in content
        assert "--chirpui-radius" in content
        assert ".chirpui-card" in content
        assert ".chirpui-modal" in content
        assert ".chirpui-tabs" in content
        assert ".chirpui-dropdown" in content
        assert ".chirpui-toast" in content
        assert ".chirpui-table" in content
        assert ".chirpui-pagination" in content
        assert ".chirpui-alert" in content
        assert ".chirpui-field" in content
        assert ".chirpui-btn" in content
        assert ".chirpui-ascii" in content
        assert ".chirpui-spinner" in content
        assert ".chirpui-divider" in content
        assert ".chirpui-breadcrumbs" in content
        assert ".chirpui-list" in content
        assert ".chirpui-accordion" in content
        assert ".chirpui-collapse" in content
        assert ".chirpui-tooltip" in content
        assert ".chirpui-toggle" in content

    def test_ascii_animation_classes_exist(self) -> None:
        """All ascii animation variants must have matching CSS."""
        from pathlib import Path

        css_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "chirp_ui"
            / "templates"
            / "chirpui.css"
        )
        content = css_path.read_text()
        animations = ("blink", "pulse", "shrink", "grow", "spin", "bounce", "throb", "wiggle", "glow", "rotate")
        for anim in animations:
            assert f".chirpui-ascii--{anim}" in content, f"Missing CSS for ascii animation: {anim}"
        assert "@keyframes chirpui-ascii-blink" in content
        assert "@keyframes chirpui-ascii-pulse" in content
        assert "@keyframes chirpui-ascii-rotate-cycle" in content
