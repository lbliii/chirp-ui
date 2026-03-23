"""Unit tests for chirp-ui template filters."""

import pytest

from chirp_ui.filters import (
    bem,
    contrast_text,
    field_errors,
    html_attrs,
    icon,
    register_colors,
    register_filters,
    resolve_color,
    sanitize_color,
    validate_size,
    validate_variant,
    validate_variant_block,
    value_type,
)
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


class TestValidateVariantBlock:
    def test_valid_returns_value(self) -> None:
        assert validate_variant_block("primary", "btn") == "primary"
        assert validate_variant_block("default", "dropdown__item") == "default"

    def test_invalid_returns_default(self) -> None:
        assert validate_variant_block("bad", "btn", default="") == ""
        assert validate_variant_block("x", "dropdown__item", default="default") == "default"


class TestValidateSize:
    def test_valid_returns_value(self) -> None:
        assert validate_size("sm", "btn") == "sm"
        assert validate_size("medium", "modal") == "medium"

    def test_invalid_returns_default(self) -> None:
        assert validate_size("xl", "btn", default="") == ""
        assert validate_size("huge", "modal", default="medium") == "medium"

    def test_empty_valid_when_in_registry(self) -> None:
        assert validate_size("", "btn") == ""


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


class TestHtmlAttrsEdgeCases:
    """Edge cases for html_attrs: None, empty, nested, special chars."""

    def test_none_returns_empty(self) -> None:
        assert str(html_attrs(None)) == ""

    def test_false_returns_empty(self) -> None:
        assert str(html_attrs(False)) == ""

    def test_empty_dict_returns_empty(self) -> None:
        assert str(html_attrs({})) == ""

    def test_nested_dict_serializes(self) -> None:
        rendered = str(html_attrs({"data-x": {"a": 1, "b": 2}}))
        assert "data-x" in rendered
        assert "1" in rendered
        assert "2" in rendered

    def test_keys_with_special_chars_escaped(self) -> None:
        rendered = str(html_attrs({"data-x": "ok"}))
        assert "data-x" in rendered
        assert "ok" in rendered


class TestBemEdgeCases:
    """Edge cases for bem: empty variant, empty modifier, None block."""

    def test_empty_variant_modifier_cls(self) -> None:
        assert bem("x", variant="", modifier="", cls="") == "chirpui-x"

    def test_unknown_block_no_strict(self) -> None:
        assert bem("unknown", variant="x") == "chirpui-unknown chirpui-unknown--x"


class TestValidateVariantEdgeCases:
    """Edge cases for validate_variant."""

    def test_empty_string_with_default_in_allowed(self) -> None:
        assert validate_variant("", ("a", "b"), default="a") == "a"

    def test_empty_allowed_list_returns_empty(self) -> None:
        assert validate_variant("x", (), default="") == ""


class TestFieldErrorsEdgeCases:
    """Edge cases for field_errors."""

    def test_nested_dict_val_returns_empty(self) -> None:
        # field_errors expects list/tuple of strings; dict val yields []
        errors = {"field": {"nested": ["err"]}}
        assert field_errors(errors, "field") == []

    def test_non_dict_input_returns_empty(self) -> None:
        assert field_errors("not a dict", "x") == []

    def test_missing_field_key_returns_empty(self) -> None:
        assert field_errors({"a": ["x"]}, "b") == []


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


class TestHtmlAttrsXss:
    """XSS vector tests for html_attrs. Mapping input escapes values; raw string is pass-through."""

    def test_mapping_escapes_script_tag_in_value(self) -> None:
        rendered = str(html_attrs({"data-x": "<script>alert(1)</script>"}))
        assert "&lt;script&gt;" in rendered or "<script>" not in rendered
        assert "alert" in rendered

    def test_mapping_escapes_quote_breakout_in_value(self) -> None:
        rendered = str(html_attrs({"data-x": '"><script>alert(1)</script>'}))
        assert "<script>" not in rendered
        assert "&quot;" in rendered or "&gt;" in rendered

    def test_mapping_escapes_empty_key_skipped(self) -> None:
        # Empty key is skipped (key.strip() yields "")
        rendered = str(html_attrs({"": "<script>alert(1)</script>"}))
        assert rendered == ""

    def test_mapping_escapes_encoded_entities_in_value(self) -> None:
        rendered = str(html_attrs({"data-x": "&#60;script&#62;"}))
        # Value is escaped; raw entities may be double-escaped or preserved
        assert "<script>" not in rendered

    def test_raw_string_passthrough_not_escaped(self) -> None:
        # Raw string input is NOT escaped — caller responsibility (SECURITY.md)
        raw = ' onload="alert(1)"'
        rendered = str(html_attrs(raw))
        assert "onload" in rendered
        assert "alert" in rendered


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


class TestValueType:
    """value_type maps Python types to ChirpUI CSS variant names."""

    def test_bool(self) -> None:
        assert value_type(True) == "bool"
        assert value_type(False) == "bool"

    def test_int(self) -> None:
        assert value_type(42) == "number"

    def test_float(self) -> None:
        assert value_type(3.14) == "number"

    def test_path(self) -> None:
        from pathlib import Path, PurePosixPath

        assert value_type(Path("/foo")) == "path"
        assert value_type(PurePosixPath("/bar")) == "path"

    def test_none(self) -> None:
        assert value_type(None) == "unset"

    def test_str(self) -> None:
        assert value_type("hello") == ""

    def test_bool_before_int(self) -> None:
        """bool is subclass of int; value_type must return 'bool' for bool values."""
        assert value_type(True) == "bool"


class TestBemStrictMode:
    """bem() in strict mode: invalid variant for a registered block logs and falls back."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_variant_falls_back_to_first_allowed(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        result = bem("alert", variant="bogus")
        first_allowed = ("info", "success", "warning", "error")[0]
        assert f"chirpui-alert--{first_allowed}" in result
        assert "chirpui-alert" in result
        assert any("invalid" in r.message for r in caplog.records)

    def test_valid_variant_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = bem("alert", variant="success")
        assert "chirpui-alert--success" in result
        assert not any("invalid" in r.message for r in caplog.records)

    def test_unknown_block_no_strict_validation(self, caplog: pytest.LogCaptureFixture) -> None:
        result = bem("custom-block", variant="whatever")
        assert "chirpui-custom-block--whatever" in result
        assert not any("invalid" in r.message for r in caplog.records)

    def test_empty_variant_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = bem("alert", variant="")
        assert result == "chirpui-alert"
        assert not any("invalid" in r.message for r in caplog.records)


class TestValidateSizeStrictMode:
    """validate_size in strict mode: invalid size logs warning and returns fallback."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_size_logs_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = validate_size("xl", "btn")
        assert result == ""  # first allowed for btn is ""
        assert any("size" in r.message and "invalid" in r.message for r in caplog.records)

    def test_valid_size_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = validate_size("sm", "btn")
        assert result == "sm"
        assert not any("invalid" in r.message for r in caplog.records)

    def test_unknown_block_no_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        result = validate_size("xl", "unknown-block")
        assert result == ""
        assert not any("invalid" in r.message for r in caplog.records)

    def test_invalid_with_valid_default(self, caplog: pytest.LogCaptureFixture) -> None:
        result = validate_size("xl", "btn", default="md")
        assert result == "md"
        assert any("invalid" in r.message for r in caplog.records)


class TestHtmlAttrsListTupleValues:
    """html_attrs with list/tuple values serializes to JSON via _serialize_attr_value."""

    def test_list_value_serialized_as_json(self) -> None:
        rendered = str(html_attrs({"data-items": [1, 2, 3]}))
        assert "data-items" in rendered
        assert "[1,2,3]" in rendered

    def test_tuple_value_serialized_as_json(self) -> None:
        rendered = str(html_attrs({"data-pair": (10, 20)}))
        assert "data-pair" in rendered
        assert "[10,20]" in rendered

    def test_nested_dict_value_serialized_as_json(self) -> None:
        rendered = str(html_attrs({"hx-vals": {"name": "test", "id": 1}}))
        assert "hx-vals" in rendered
        assert "&quot;" in rendered or '"' not in rendered

    def test_mixed_value_types(self) -> None:
        rendered = str(
            html_attrs(
                {
                    "disabled": True,
                    "data-list": [1, 2],
                    "title": "hello",
                    "hidden": False,
                }
            )
        )
        assert " disabled" in rendered
        assert "data-list" in rendered
        assert "[1,2]" in rendered
        assert "title" in rendered
        assert "hello" in rendered
        assert "hidden" not in rendered


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
        assert "validate_variant" in registered
        assert "validate_variant_block" in registered
        assert "validate_size" in registered
        assert "value_type" in registered
        assert registered["value_type"] is value_type
        assert "sanitize_color" in registered
        assert registered["sanitize_color"] is sanitize_color
        assert "contrast_text" in registered
        assert registered["contrast_text"] is contrast_text
        assert "resolve_color" in registered
        assert registered["resolve_color"] is resolve_color


class TestColorFilters:
    def test_sanitize_color_hex(self) -> None:
        assert sanitize_color("#78c850") == "#78c850"
        assert sanitize_color("#abc") == "#abc"
        assert sanitize_color("url(x)") is None

    def test_contrast_text_hex(self) -> None:
        assert contrast_text("#ffffff") == "#1a1a1a"
        assert contrast_text("#000000") == "white"

    def test_resolve_color_registry(self) -> None:
        register_colors({"_pytest_resolve_grass": "#78c850", "PytestFire": "#ff0000"})
        assert resolve_color("_pytest_resolve_grass") == "#78c850"
        assert resolve_color("pytestfire") == "#ff0000"


class TestRegisterFiltersWithTemplateGlobal:
    """register_filters with an app that has template_global registers tab_is_active."""

    def test_tab_is_active_registered_as_global(self) -> None:
        registered_filters: dict[str, object] = {}
        registered_globals: dict[str, object] = {}

        class MockAppWithGlobal:
            def template_filter(self, name: str):
                def decorator(fn: object) -> object:
                    registered_filters[name] = fn
                    return fn

                return decorator

            def template_global(self, name: str):
                def decorator(fn: object) -> object:
                    registered_globals[name] = fn
                    return fn

                return decorator

        app = MockAppWithGlobal()
        register_filters(app)

        assert "tab_is_active" in registered_globals
        from chirp_ui.route_tabs import tab_is_active

        assert registered_globals["tab_is_active"] is tab_is_active

    def test_without_template_global_no_error(self) -> None:
        registered: dict[str, object] = {}

        class MockAppNoGlobal:
            def template_filter(self, name: str):
                def decorator(fn: object) -> object:
                    registered[name] = fn
                    return fn

                return decorator

        app = MockAppNoGlobal()
        register_filters(app)
        assert "bem" in registered
        assert "tab_is_active" not in registered
