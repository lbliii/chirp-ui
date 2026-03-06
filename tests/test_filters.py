"""Unit tests for chirp-ui template filters."""

import pytest

from chirp_ui.filters import bem, field_errors, html_attrs, icon, register_filters, validate_variant
from chirp_ui.validation import set_strict


class TestBem:
    def test_base_block(self) -> None:
        assert bem("alert") == "chirpui-alert"

    def test_with_variant(self) -> None:
        assert bem("alert", variant="success") == "chirpui-alert chirpui-alert--success"

    def test_with_modifier(self) -> None:
        assert bem("btn", modifier="loading") == "chirpui-btn chirpui-btn--loading"

    def test_with_cls(self) -> None:
        assert bem("card", cls="custom") == "chirpui-card custom"

    def test_combined(self) -> None:
        result = bem("alert", variant="error", modifier="dismissible", cls="my-alert")
        assert "chirpui-alert" in result
        assert "chirpui-alert--error" in result
        assert "chirpui-alert--dismissible" in result
        assert "my-alert" in result

    def test_empty_variant_modifier_cls(self) -> None:
        assert bem("x", variant="", modifier="", cls="") == "chirpui-x"


class TestFieldErrors:
    def test_errors_none_returns_empty(self) -> None:
        assert field_errors(None, "email") == []

    def test_dict_without_field_returns_empty(self) -> None:
        assert field_errors({"other": ["err"]}, "email") == []

    def test_dict_with_field_returns_list(self) -> None:
        assert field_errors({"email": ["Invalid email"]}, "email") == ["Invalid email"]
        assert field_errors({"x": ["A", "B"]}, "x") == ["A", "B"]

    def test_empty_dict_returns_empty(self) -> None:
        assert field_errors({}, "any") == []


class TestValidateVariant:
    """validate_variant returns value if allowed, else default."""

    def test_valid_value_returned(self) -> None:
        assert validate_variant("success", ("info", "success", "error")) == "success"

    def test_invalid_returns_default_when_default_in_allowed(self) -> None:
        assert validate_variant("bad", ("a", "b"), default="a") == "a"

    def test_invalid_returns_first_allowed_when_default_not_in_allowed(self) -> None:
        assert validate_variant("bad", ("a", "b"), default="x") == "a"

    def test_invalid_empty_allowed_returns_empty_string(self) -> None:
        assert validate_variant("bad", (), default="") == ""

    def test_empty_string_valid_when_in_allowed(self) -> None:
        assert validate_variant("", ("", "avatar", "text")) == ""


class TestValidateVariantStrictMode:
    """Strict mode logs warning on invalid variant and returns fallback."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_logs_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = validate_variant("invalid", ("a", "b"))
        assert result == "a"
        assert "chirp_ui" in caplog.text or any("variant" in r.message for r in caplog.records)

    def test_valid_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        validate_variant("a", ("a", "b"))
        assert not any("invalid" in (r.message or "") for r in caplog.records)


class TestHtmlAttrs:
    def test_mapping_renders_attrs(self) -> None:
        rendered = str(html_attrs({"hx-post": "/x", "hx-target": "#y"}))
        assert ' hx-post="/x"' in rendered
        assert ' hx-target="#y"' in rendered

    def test_mapping_omits_falsey_values(self) -> None:
        rendered = str(html_attrs({"disabled": True, "hidden": False, "title": None}))
        assert " disabled" in rendered
        assert "hidden" not in rendered
        assert "title" not in rendered

    def test_string_passthrough(self) -> None:
        rendered = str(html_attrs('hx-get="/q" hx-target="#r"'))
        assert rendered.startswith(" ")
        assert 'hx-get="/q"' in rendered
        assert 'hx-target="#r"' in rendered


class TestIcon:
    def test_resolves_registered_name(self) -> None:
        assert icon("status") == "◎"
        assert icon("add") == "+"
        assert icon("refresh") == "↻"
        assert icon("search") == "⌕"
        assert icon("logs") == "⟳"
        assert icon("cloud") == "☁"

    def test_unknown_name_passes_through(self) -> None:
        assert icon("◎") == "◎"
        assert icon("custom-glyph") == "custom-glyph"


class TestIconStrictMode:
    """Strict mode logs warning on invalid icon name and passes through unchanged."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_logs_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = icon("statis")
        assert result == "statis"
        assert any(
            "icon" in (r.message or "") and "invalid" in (r.message or "") for r in caplog.records
        )
        assert any("statis" in (r.message or "") for r in caplog.records)

    def test_valid_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        icon("status")
        assert not any(
            "invalid" in (r.message or "") and "icon" in (r.message or "") for r in caplog.records
        )

    def test_strict_false_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        set_strict(False)
        icon("statis")
        assert not any("invalid" in (r.message or "") for r in caplog.records)


class TestRegisterFilters:
    def test_registers_bem_field_errors_and_html_attrs(self) -> None:
        registered: dict[str, object] = {}

        class MockApp:
            def template_filter(self, name: str):
                def decorator(fn: object) -> object:
                    registered[name] = fn
                    return fn

                return decorator

        app = MockApp()
        register_filters(app)
        assert "bem" in registered
        assert registered["bem"] is bem
        assert "field_errors" in registered
        assert registered["field_errors"] is field_errors
        assert "html_attrs" in registered
        assert registered["html_attrs"] is html_attrs
        assert "icon" in registered
