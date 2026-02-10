"""Render tests for all chirp-ui components.

Each test verifies:
- Correct HTML structure (BEM classes present)
- Parameter variants (defaults, optional args)
- Slot content injection where applicable
"""

from __future__ import annotations

from kida import Environment


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


class TestCard:
    def test_basic_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            "{% call card() %}Body{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-card__body" in html
        assert "Body" in html

    def test_card_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            '{% call card(title="Hello") %}Content{% end %}'
        ).render()
        assert "chirpui-card__header" in html
        assert "Hello" in html

    def test_card_with_footer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            '{% call card(footer="Footer text") %}Content{% end %}'
        ).render()
        assert "chirpui-card__footer" in html
        assert "Footer text" in html

    def test_card_collapsible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            '{% call card(title="Toggle", collapsible=true) %}Hidden{% end %}'
        ).render()
        assert "<details" in html
        assert "<summary" in html
        assert "chirpui-card--collapsible" in html

    def test_card_collapsible_open(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            '{% call card(title="Open", collapsible=true, open=true) %}Visible{% end %}'
        ).render()
        assert "open" in html

    def test_card_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            "{% call card() %}Just body{% end %}"
        ).render()
        assert "chirpui-card__header" not in html

    def test_card_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
            '{% call card(cls="custom") %}Body{% end %}'
        ).render()
        assert "chirpui-card custom" in html


# ---------------------------------------------------------------------------
# Modal
# ---------------------------------------------------------------------------


class TestModal:
    def test_basic_modal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal" import modal %}'
            '{% call modal("dlg") %}Content{% end %}'
        ).render()
        assert '<dialog id="dlg"' in html
        assert "chirpui-modal" in html
        assert "chirpui-modal__body" in html
        assert "Content" in html

    def test_modal_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal" import modal %}'
            '{% call modal("dlg", title="Settings") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" in html
        assert "Settings" in html
        assert "chirpui-modal__close" in html

    def test_modal_sizes(self, env: Environment) -> None:
        for size in ("small", "medium", "large"):
            html = env.from_string(
                '{% from "chirpui/modal" import modal %}'
                f'{{% call modal("dlg", size="{size}") %}}Body{{% end %}}'
            ).render()
            assert f"chirpui-modal--{size}" in html

    def test_modal_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal" import modal_trigger %}'
            '{{ modal_trigger("dlg", label="Click me") }}'
        ).render()
        assert "chirpui-modal-trigger" in html
        assert "Click me" in html
        assert "dlg" in html

    def test_modal_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal" import modal %}'
            '{% call modal("dlg") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" not in html


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------


class TestTabs:
    def test_tabs_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs" import tabs, tab %}'
            '{% call tabs() %}{{ tab("t1", "Tab One") }}{% end %}'
        ).render()
        assert "chirpui-tabs" in html
        assert 'role="tablist"' in html

    def test_tab_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs" import tab %}'
            '{{ tab("overview", "Overview", active=true) }}'
        ).render()
        assert "chirpui-tab--active" in html
        assert 'aria-selected="true"' in html
        assert "Overview" in html

    def test_tab_inactive(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs" import tab %}'
            '{{ tab("details", "Details") }}'
        ).render()
        assert "chirpui-tab--active" not in html
        assert 'aria-selected="false"' in html

    def test_tab_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs" import tab %}'
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
            '{% from "chirpui/dropdown" import dropdown %}'
            '{% call dropdown(label="Menu") %}<a href="/">Home</a>{% end %}'
        ).render()
        assert "<details" in html
        assert "<summary" in html
        assert "chirpui-dropdown" in html
        assert "chirpui-dropdown__menu" in html
        assert "Menu" in html

    def test_dropdown_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown" import dropdown %}'
            '{% call dropdown(label="Menu", cls="extra") %}Items{% end %}'
        ).render()
        assert "chirpui-dropdown extra" in html


# ---------------------------------------------------------------------------
# Toast
# ---------------------------------------------------------------------------


class TestToast:
    def test_toast_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast" import toast_container %}'
            "{{ toast_container() }}"
        ).render()
        assert 'id="chirpui-toasts"' in html
        assert "chirpui-toast-container" in html
        assert 'aria-live="polite"' in html

    def test_toast_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast" import toast %}'
            '{{ toast("Saved!") }}'
        ).render()
        assert "chirpui-toast--info" in html
        assert "Saved!" in html
        assert "hx-swap-oob" in html

    def test_toast_variants(self, env: Environment) -> None:
        for variant in ("info", "success", "warning", "error"):
            html = env.from_string(
                '{% from "chirpui/toast" import toast %}'
                f'{{{{ toast("msg", variant="{variant}") }}}}'
            ).render()
            assert f"chirpui-toast--{variant}" in html

    def test_toast_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast" import toast %}'
            '{{ toast("msg", dismissible=true) }}'
        ).render()
        assert "chirpui-toast__close" in html

    def test_toast_not_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast" import toast %}'
            '{{ toast("msg", dismissible=false) }}'
        ).render()
        assert "chirpui-toast__close" not in html

    def test_toast_no_oob(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast" import toast %}'
            '{{ toast("msg", oob=false) }}'
        ).render()
        assert "hx-swap-oob" not in html


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


class TestTable:
    def test_basic_table(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table" import table, row %}'
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
            '{% from "chirpui/table" import table %}'
            "{% call table(striped=true) %}{% end %}"
        ).render()
        assert "chirpui-table--striped" in html

    def test_table_no_headers(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table" import table, row %}'
            "{% call table() %}{{ row(\"Data\") }}{% end %}"
        ).render()
        assert "chirpui-table__th" not in html
        assert "chirpui-table__body" in html

    def test_row_renders_cells(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table" import row %}'
            '{{ row("A", "B", "C") }}'
        ).render()
        assert html.count("chirpui-table__td") == 3


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


class TestPagination:
    def test_basic_pagination(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination" import pagination %}'
            '{{ pagination(current=2, total=5, url_pattern="/items?page={page}") }}'
        ).render()
        assert "chirpui-pagination" in html
        assert 'aria-label="Pagination"' in html
        assert 'aria-current="page"' in html

    def test_pagination_hidden_when_single_page(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination" import pagination %}'
            '{{ pagination(current=1, total=1, url_pattern="/items?page={page}") }}'
        ).render()
        assert "chirpui-pagination" not in html

    def test_pagination_prev_disabled_on_first(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination" import pagination %}'
            '{{ pagination(current=1, total=3, url_pattern="/p?page={page}") }}'
        ).render()
        assert "chirpui-pagination__link--disabled" in html

    def test_pagination_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination" import pagination %}'
            '{{ pagination(current=2, total=5, url_pattern="/p?page={page}", '
            'hx_target="#list") }}'
        ).render()
        assert 'hx-target="#list"' in html
        assert "hx-get" in html


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------


class TestAlert:
    def test_basic_alert(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert" import alert %}'
            "{% call alert() %}Hello{% end %}"
        ).render()
        assert "chirpui-alert--info" in html
        assert 'role="alert"' in html
        assert "Hello" in html

    def test_alert_variants(self, env: Environment) -> None:
        for variant in ("info", "success", "warning", "error"):
            html = env.from_string(
                '{% from "chirpui/alert" import alert %}'
                f'{{% call alert(variant="{variant}") %}}msg{{% end %}}'
            ).render()
            assert f"chirpui-alert--{variant}" in html

    def test_alert_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert" import alert %}'
            "{% call alert(dismissible=true) %}msg{% end %}"
        ).render()
        assert "chirpui-alert__close" in html

    def test_alert_not_dismissible_by_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert" import alert %}'
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
            '{% from "chirpui/forms" import text_field %}'
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
            '{% from "chirpui/forms" import text_field %}'
            '{{ text_field("email", label="Email", required=true) }}'
        ).render()
        assert "required" in html
        assert "chirpui-field__required" in html

    def test_text_field_with_hint(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms" import text_field %}'
            '{{ text_field("name", hint="Enter your full name") }}'
        ).render()
        assert "chirpui-field__hint" in html
        assert "Enter your full name" in html

    def test_textarea_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms" import textarea_field %}'
            '{{ textarea_field("desc", value="Content", label="Description", rows=6) }}'
        ).render()
        assert "<textarea" in html
        assert 'rows="6"' in html
        assert "Content" in html

    def test_select_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms" import select_field %}'
            '{% set opts = [{"value": "a", "label": "Alpha"}, '
            '{"value": "b", "label": "Beta"}] %}'
            '{{ select_field("choice", options=opts, selected="b", label="Pick") }}'
        ).render()
        assert "<select" in html
        assert "Alpha" in html
        assert "Beta" in html
        assert "selected" in html

    def test_checkbox_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms" import checkbox_field %}'
            '{{ checkbox_field("agree", label="I agree", checked=true) }}'
        ).render()
        assert 'type="checkbox"' in html
        assert "checked" in html
        assert "I agree" in html

    def test_hidden_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms" import hidden_field %}'
            '{{ hidden_field("id", value="42") }}'
        ).render()
        assert 'type="hidden"' in html
        assert 'name="id"' in html
        assert 'value="42"' in html


# ---------------------------------------------------------------------------
# Composition / Nesting
# ---------------------------------------------------------------------------


class TestComposition:
    def test_card_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card" import card %}'
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
            '{% from "chirpui/card" import card %}'
            '{% from "chirpui/table" import table, row %}'
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
            '{% from "chirpui/card" import card %}'
            '{% from "chirpui/alert" import alert %}'
            '{% call card(title="Status") %}'
            '{% call alert(variant="success") %}All good{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-alert--success" in html
        assert "All good" in html


# ---------------------------------------------------------------------------
# CSS file
# ---------------------------------------------------------------------------


class TestCSS:
    def test_css_file_loads(self, env: Environment) -> None:
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
