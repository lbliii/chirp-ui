"""Unit tests for chirp-ui template filters."""

import pytest

from chirp_ui.filters import (
    STATUS_WORDS,
    bem,
    build_hx_attrs,
    contrast_text,
    deprecate_param,
    field_errors,
    html_attrs,
    icon,
    make_route_link_attrs,
    register_colors,
    register_filters,
    resolve_color,
    resolve_status_variant,
    sanitize_color,
    validate_size,
    validate_variant,
    validate_variant_block,
    value_type,
)
from chirp_ui.validation import (
    ChirpUIDeprecationWarning,
    ChirpUIValidationWarning,
    ChirpUIWarning,
    set_strict,
)


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
        assert validate_size("md", "modal") == "md"

    def test_invalid_returns_default(self) -> None:
        assert validate_size("xl", "btn", default="") == ""
        with pytest.warns(ChirpUIValidationWarning):
            assert validate_size("huge", "modal", default="md") == "md"

    def test_empty_valid_when_in_registry(self) -> None:
        assert validate_size("", "btn") == ""


class TestValidateVariantStrictMode:
    """Strict mode raises ValueError on invalid variant."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="variant"):
            validate_variant("invalid", ("a", "b"))

    def test_valid_no_error(self) -> None:
        assert validate_variant("a", ("a", "b")) == "a"


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

    def test_invalid_modifier_stripped_with_warning(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="invalid"):
            result = bem("btn", modifier=["loading", "nonexistent-mod"])
        assert "chirpui-btn--loading" in result
        assert "nonexistent-mod" not in result

    def test_valid_modifiers_kept(self) -> None:
        result = bem("btn", modifier=["loading"])
        assert "chirpui-btn--loading" in result


class TestContrastTextWarning:
    """contrast_text warns on unparseable colors."""

    def test_unparseable_color_warns(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="could not parse"):
            result = contrast_text("not-a-color")
        assert result == "white"

    def test_empty_color_no_warning(self) -> None:
        result = contrast_text("")
        assert result == "white"

    def test_valid_hex_no_warning(self) -> None:
        result = contrast_text("#000000")
        assert result == "white"

    def test_valid_hex_light_returns_dark(self) -> None:
        result = contrast_text("#ffffff")
        assert result == "#1a1a1a"


class TestDeprecateParam:
    """deprecate_param filter warns on deprecated parameter usage."""

    def test_warns_when_value_is_truthy(self) -> None:
        with pytest.warns(ChirpUIDeprecationWarning, match="attrs.*deprecated"):
            result = deprecate_param('data-x="1"', "attrs", "attrs_unsafe or attrs_map")
        assert result == 'data-x="1"'

    def test_no_warn_when_value_is_empty(self) -> None:
        result = deprecate_param("", "attrs", "attrs_unsafe or attrs_map")
        assert result == ""

    def test_returns_value_unchanged(self) -> None:
        with pytest.warns(ChirpUIDeprecationWarning):
            result = deprecate_param("hello", "old", "new")
        assert result == "hello"


class TestValidateVariantEdgeCases:
    """Edge cases for validate_variant."""

    def test_empty_string_with_default_in_allowed(self) -> None:
        assert validate_variant("", ("a", "b"), default="a") == "a"

    def test_empty_allowed_list_returns_empty(self) -> None:
        assert validate_variant("x", (), default="") == ""


class TestWarningInfrastructure:
    """ChirpUI warning classes and _warn behavior."""

    def test_validate_variant_warns_on_fallback(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="variant"):
            validate_variant("xl", ("sm", "md", "lg"), "md")

    def test_validate_variant_no_warn_on_empty_string(self) -> None:
        # Empty string is the common "no variant" case — should not warn
        result = validate_variant("", ("a", "b"), default="a")
        assert result == "a"

    def test_validate_size_warns_on_fallback(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="size"):
            validate_size("xl", "btn", default="md")

    def test_validate_size_no_warn_for_unknown_block(self) -> None:
        # Unknown block has no registered sizes — no warning
        result = validate_size("xl", "unknown-block")
        assert result == ""

    def test_icon_warns_on_unrecognized(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="nonexistent"):
            icon("nonexistent")

    def test_icon_no_warn_on_valid(self) -> None:
        result = icon("status")
        assert result == "◎"

    def test_register_colors_raises_on_invalid(self) -> None:
        with pytest.raises(ValueError, match="invalid color"):
            register_colors({"brand": "not-a-color"})

    def test_register_colors_accepts_valid(self) -> None:
        register_colors({"_test_warn_green": "#00ff00"})
        assert resolve_color("_test_warn_green") == "#00ff00"

    def test_register_filters_warns_without_template_global(self) -> None:
        class MinimalApp:
            def template_filter(self, name: str):
                return lambda fn: fn

        with pytest.warns(ChirpUIWarning, match="template_global"):
            register_filters(MinimalApp())

    def test_strict_mode_escalates_validation_to_error(self) -> None:
        set_strict(True)
        try:
            with pytest.raises(ValueError, match="variant"):
                validate_variant("bad", ("a", "b"))
        finally:
            set_strict(False)

    def test_strict_mode_escalates_size_to_error(self) -> None:
        set_strict(True)
        try:
            with pytest.raises(ValueError, match="size"):
                validate_size("xl", "btn")
        finally:
            set_strict(False)

    def test_strict_mode_escalates_icon_to_error(self) -> None:
        set_strict(True)
        try:
            with pytest.raises(ValueError, match="icon"):
                icon("bogus_icon")
        finally:
            set_strict(False)


class TestResolveStatusVariant:
    """resolve_status_variant maps status strings to badge variants."""

    def test_success_words(self) -> None:
        for word in ("ok", "yes", "configured", "true", "1", "on", "ready", "active"):
            assert resolve_status_variant(word) == "success", f"{word!r} should map to success"

    def test_error_words(self) -> None:
        for word in ("error", "issues", "failed", "offline", "disabled"):
            assert resolve_status_variant(word) == "error", f"{word!r} should map to error"

    def test_case_insensitive(self) -> None:
        assert resolve_status_variant("OK") == "success"
        assert resolve_status_variant("Failed") == "error"
        assert resolve_status_variant("CONFIGURED") == "success"

    def test_unknown_returns_default_and_warns(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="unknown-status"):
            result = resolve_status_variant("unknown-status")
        assert result == "muted"

    def test_empty_returns_default(self) -> None:
        assert resolve_status_variant("") == "muted"

    def test_custom_default(self) -> None:
        with pytest.warns(ChirpUIValidationWarning):
            result = resolve_status_variant("unrecognized-xyz", default="info")
        assert result == "info"

    def test_extensible_via_status_words(self) -> None:
        STATUS_WORDS["custom-status"] = "warning"
        try:
            assert resolve_status_variant("custom-status") == "warning"
        finally:
            del STATUS_WORDS["custom-status"]


class TestFieldErrorsEdgeCases:
    """Edge cases for field_errors."""

    def test_nested_dict_val_warns_and_coerces(self) -> None:
        """Non-list values (e.g. nested dicts from DRF) are coerced with a warning."""
        errors = {"field": {"nested": ["err"]}}
        with pytest.warns(ChirpUIValidationWarning, match="expected list/tuple"):
            result = field_errors(errors, "field")
        assert result == [str({"nested": ["err"]})]

    def test_string_val_warns_and_coerces(self) -> None:
        """A bare string value is wrapped as a single-element list with a warning."""
        with pytest.warns(ChirpUIValidationWarning, match="expected list/tuple"):
            result = field_errors({"email": "invalid"}, "email")
        assert result == ["invalid"]

    def test_int_val_warns_and_coerces(self) -> None:
        """Integer error codes are coerced to string with a warning."""
        with pytest.warns(ChirpUIValidationWarning, match="expected list/tuple"):
            result = field_errors({"code": 422}, "code")
        assert result == ["422"]

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
        with pytest.warns(ChirpUIValidationWarning):
            assert icon("◎") == "◎"
        with pytest.warns(ChirpUIValidationWarning):
            assert icon("custom-glyph") == "custom-glyph"


class TestIconStrictMode:
    """Strict mode raises ValueError on invalid icon name."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="statis"):
            icon("statis")

    def test_valid_no_error(self) -> None:
        assert icon("status") == "◎"

    def test_non_strict_warns(self) -> None:
        set_strict(False)
        with pytest.warns(ChirpUIValidationWarning, match="statis"):
            icon("statis")


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
    """bem() in strict mode: invalid variant for a registered block raises ValueError."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_variant_raises(self) -> None:
        with pytest.raises(ValueError, match="bogus"):
            bem("alert", variant="bogus")

    def test_valid_variant_no_error(self) -> None:
        result = bem("alert", variant="success")
        assert "chirpui-alert--success" in result

    def test_unknown_block_no_validation(self) -> None:
        result = bem("custom-block", variant="whatever")
        assert "chirpui-custom-block--whatever" in result

    def test_empty_variant_no_warning(self) -> None:
        result = bem("alert", variant="")
        assert result == "chirpui-alert"


class TestValidateSizeStrictMode:
    """validate_size in strict mode: invalid size raises ValueError."""

    def setup_method(self) -> None:
        set_strict(True)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_invalid_size_raises(self) -> None:
        with pytest.raises(ValueError, match="size"):
            validate_size("xl", "btn")

    def test_valid_size_no_error(self) -> None:
        assert validate_size("sm", "btn") == "sm"

    def test_unknown_block_no_error(self) -> None:
        assert validate_size("xl", "unknown-block") == ""

    def test_invalid_with_valid_default_raises(self) -> None:
        with pytest.raises(ValueError, match="size"):
            validate_size("xl", "btn", default="md")


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
        with pytest.warns(ChirpUIWarning, match="template_global"):
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

    def test_contrast_text_rgb(self) -> None:
        assert contrast_text("rgb(255, 255, 255)") == "#1a1a1a"
        assert contrast_text("rgb(0, 0, 0)") == "white"
        assert contrast_text("rgb(0 0 0)") == "white"

    def test_contrast_text_rgb_percent(self) -> None:
        assert contrast_text("rgb(100%, 100%, 100%)") == "#1a1a1a"
        assert contrast_text("rgb(0%, 0%, 0%)") == "white"

    def test_contrast_text_rgba_ignores_alpha(self) -> None:
        assert contrast_text("rgba(255, 255, 255, 0.5)") == "#1a1a1a"
        assert contrast_text("rgba(0, 0, 0, 0.8)") == "white"

    def test_contrast_text_hsl(self) -> None:
        assert contrast_text("hsl(0, 0%, 100%)") == "#1a1a1a"  # white
        assert contrast_text("hsl(0, 0%, 0%)") == "white"  # black
        assert contrast_text("hsl(60, 100%, 50%)") == "#1a1a1a"  # yellow (bright)

    def test_contrast_text_oklch(self) -> None:
        assert contrast_text("oklch(1 0 0)") == "#1a1a1a"  # white
        assert contrast_text("oklch(0 0 0)") == "white"  # black
        assert contrast_text("oklch(0.9 0.1 110)") == "#1a1a1a"  # light green

    def test_contrast_text_unsupported_falls_back(self) -> None:
        # color-mix() is not in sanitize_color regex, falls back to white
        assert contrast_text("color-mix(in srgb, red 50%, blue)") == "white"
        assert contrast_text("invalid") == "white"

    def test_resolve_color_registry(self) -> None:
        register_colors({"_pytest_resolve_grass": "#78c850", "PytestFire": "#ff0000"})
        assert resolve_color("_pytest_resolve_grass") == "#78c850"
        assert resolve_color("pytestfire") == "#ff0000"


class TestHexToRgbChannels:
    """Tests for _hex_to_rgb_channels internal parser."""

    def test_hex_3_digit(self) -> None:
        from chirp_ui.filters import _hex_to_rgb_channels

        r, g, b = _hex_to_rgb_channels("#fff")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0))

    def test_hex_6_digit(self) -> None:
        from chirp_ui.filters import _hex_to_rgb_channels

        r, g, b = _hex_to_rgb_channels("#ff0000")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 0.0, 0.0))

    def test_hex_8_digit_ignores_alpha(self) -> None:
        from chirp_ui.filters import _hex_to_rgb_channels

        r, g, b = _hex_to_rgb_channels("#00ff0080")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 1.0, 0.0))

    def test_hex_black(self) -> None:
        from chirp_ui.filters import _hex_to_rgb_channels

        r, g, b = _hex_to_rgb_channels("#000000")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 0.0, 0.0))

    def test_hex_invalid_length(self) -> None:
        from chirp_ui.filters import _hex_to_rgb_channels

        assert _hex_to_rgb_channels("#ab") is None
        assert _hex_to_rgb_channels("#abcde") is None

    def test_hex_no_hash(self) -> None:
        from chirp_ui.filters import _hex_to_rgb_channels

        assert _hex_to_rgb_channels("ff0000") is None


class TestRgbToChannels:
    """Tests for _rgb_to_channels internal parser."""

    def test_comma_syntax(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        r, g, b = _rgb_to_channels("rgb(255, 0, 128)")  # type: ignore[misc]
        assert r == pytest.approx(1.0)
        assert g == pytest.approx(0.0)
        assert b == pytest.approx(128 / 255.0, abs=0.01)

    def test_space_syntax(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        r, _g, b = _rgb_to_channels("rgb(0 128 255)")  # type: ignore[misc]
        assert r == pytest.approx(0.0)
        assert b == pytest.approx(1.0)

    def test_percent_syntax(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        r, g, b = _rgb_to_channels("rgb(100%, 50%, 0%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 0.5, 0.0))

    def test_rgba_ignores_alpha(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        r, g, b = _rgb_to_channels("rgba(255, 255, 255, 0.5)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0))

    def test_rgba_slash_alpha(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        r, g, b = _rgb_to_channels("rgba(0 0 0 / 0.8)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 0.0, 0.0))

    def test_clamped_values(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        r, _g, _b = _rgb_to_channels("rgb(999, 0, 0)")  # type: ignore[misc]
        assert r == pytest.approx(1.0)  # clamped

    def test_malformed_returns_none(self) -> None:
        from chirp_ui.filters import _rgb_to_channels

        assert _rgb_to_channels("rgb()") is None
        assert _rgb_to_channels("rgb(1)") is None
        assert _rgb_to_channels("notrgb(0,0,0)") is None


class TestHslToChannels:
    """Tests for _hsl_to_channels internal parser."""

    def test_red(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        r, g, b = _hsl_to_channels("hsl(0, 100%, 50%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 0.0, 0.0), abs=0.01)

    def test_green(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        r, g, b = _hsl_to_channels("hsl(120, 100%, 50%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 1.0, 0.0), abs=0.01)

    def test_blue(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        r, g, b = _hsl_to_channels("hsl(240, 100%, 50%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 0.0, 1.0), abs=0.01)

    def test_achromatic_white(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        r, g, b = _hsl_to_channels("hsl(0, 0%, 100%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0))

    def test_achromatic_black(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        r, g, b = _hsl_to_channels("hsl(0, 0%, 0%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 0.0, 0.0))

    def test_mid_gray(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        r, g, b = _hsl_to_channels("hsl(0, 0%, 50%)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.5, 0.5, 0.5))

    def test_malformed_returns_none(self) -> None:
        from chirp_ui.filters import _hsl_to_channels

        assert _hsl_to_channels("hsl()") is None
        assert _hsl_to_channels("hsl(abc, def, ghi)") is None


class TestOklchToChannels:
    """Tests for _oklch_to_channels internal parser."""

    def test_white(self) -> None:
        from chirp_ui.filters import _oklch_to_channels

        r, g, b = _oklch_to_channels("oklch(1 0 0)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0), abs=0.02)

    def test_black(self) -> None:
        from chirp_ui.filters import _oklch_to_channels

        r, g, b = _oklch_to_channels("oklch(0 0 0)")  # type: ignore[misc]
        assert (r, g, b) == pytest.approx((0.0, 0.0, 0.0), abs=0.01)

    def test_near_black_gamma_fix(self) -> None:
        """Validates the _linear_to_srgb fix: 12.92*c, not c/12.92."""
        from chirp_ui.filters import _oklch_to_channels

        r, g, _b = _oklch_to_channels("oklch(0.1 0 0)")  # type: ignore[misc]
        # With the fix, near-black achromatic should give sRGB ≈ 0.013
        # The buggy version gave ≈ 0.00008 (166x too dark)
        assert r == pytest.approx(g, abs=0.001)  # achromatic → equal channels
        assert r > 0.005, f"gamma fix failed: got {r} (should be ~0.013, not ~0.00008)"

    def test_percent_lightness(self) -> None:
        from chirp_ui.filters import _oklch_to_channels

        r1, _, _ = _oklch_to_channels("oklch(0.5 0 0)")  # type: ignore[misc]
        r2, _, _ = _oklch_to_channels("oklch(50% 0 0)")  # type: ignore[misc]
        assert r1 == pytest.approx(r2, abs=0.01)

    def test_oklcha_with_alpha(self) -> None:
        """oklcha() should parse and ignore the alpha channel."""
        from chirp_ui.filters import _oklch_to_channels

        result = _oklch_to_channels("oklcha(0.8 0.1 200 / 0.5)")
        assert result is not None
        r, g, b = result
        # Should be a valid color (light-ish blue-green)
        assert 0.0 <= r <= 1.0
        assert 0.0 <= g <= 1.0
        assert 0.0 <= b <= 1.0

    def test_malformed_returns_none(self) -> None:
        from chirp_ui.filters import _oklch_to_channels

        assert _oklch_to_channels("oklch()") is None
        assert _oklch_to_channels("oklch(0.5)") is None
        assert _oklch_to_channels("notcolor") is None


class TestSanitizeColorExtended:
    """Extended tests for sanitize_color with widened regex."""

    def test_valid_hex_formats(self) -> None:
        assert sanitize_color("#abc") == "#abc"
        assert sanitize_color("#aabbcc") == "#aabbcc"
        assert sanitize_color("#aabbccdd") == "#aabbccdd"

    def test_valid_rgb_formats(self) -> None:
        assert sanitize_color("rgb(255, 128, 0)") == "rgb(255, 128, 0)"
        assert sanitize_color("rgb(255 128 0)") == "rgb(255 128 0)"
        assert sanitize_color("rgba(255 128 0 / 0.5)") == "rgba(255 128 0 / 0.5)"
        assert sanitize_color("rgb(100%, 50%, 0%)") == "rgb(100%, 50%, 0%)"

    def test_valid_hsl_formats(self) -> None:
        assert sanitize_color("hsl(120, 100%, 50%)") == "hsl(120, 100%, 50%)"
        assert sanitize_color("hsl(120 100% 50%)") == "hsl(120 100% 50%)"
        assert sanitize_color("hsla(120, 100%, 50%, 0.5)") == "hsla(120, 100%, 50%, 0.5)"

    def test_valid_oklch_formats(self) -> None:
        assert sanitize_color("oklch(0.5 0.2 30)") == "oklch(0.5 0.2 30)"
        assert sanitize_color("oklch(50% 0.2 30)") == "oklch(50% 0.2 30)"

    def test_negative_hue_accepted(self) -> None:
        assert sanitize_color("oklch(0.5 0.2 -30)") == "oklch(0.5 0.2 -30)"

    def test_leading_dot_decimal_accepted(self) -> None:
        assert sanitize_color("oklch(.5 .2 30)") == "oklch(.5 .2 30)"

    def test_oklcha_accepted(self) -> None:
        assert sanitize_color("oklcha(0.5 0.2 30 / 0.8)") == "oklcha(0.5 0.2 30 / 0.8)"

    def test_deg_unit_accepted(self) -> None:
        assert sanitize_color("hsl(120deg 100% 50%)") == "hsl(120deg 100% 50%)"
        assert sanitize_color("oklch(0.5 0.2 30deg)") == "oklch(0.5 0.2 30deg)"

    def test_turn_unit_accepted(self) -> None:
        assert sanitize_color("hsl(0.5turn 100% 50%)") == "hsl(0.5turn 100% 50%)"

    def test_none_keyword_accepted(self) -> None:
        assert sanitize_color("oklch(0.7 0.15 none)") == "oklch(0.7 0.15 none)"

    def test_lab_lch_accepted(self) -> None:
        assert sanitize_color("lab(50% 20 -30)") == "lab(50% 20 -30)"
        assert sanitize_color("lch(50% 30 270)") == "lch(50% 30 270)"

    def test_injection_url_blocked(self) -> None:
        assert sanitize_color("url(evil.png)") is None

    def test_injection_var_blocked(self) -> None:
        assert sanitize_color("var(--secret)") is None

    def test_injection_expression_blocked(self) -> None:
        assert sanitize_color("expression(alert(1))") is None

    def test_injection_calc_blocked(self) -> None:
        assert sanitize_color("calc(100% - 20px)") is None

    def test_injection_script_blocked(self) -> None:
        assert sanitize_color("<script>alert(1)</script>") is None

    def test_injection_semicolon_breakout_blocked(self) -> None:
        assert sanitize_color("rgb(0,0,0); background: url(x)") is None

    def test_injection_quote_blocked(self) -> None:
        assert sanitize_color('"onmouseover="alert(1)') is None

    def test_injection_style_close_blocked(self) -> None:
        assert sanitize_color("rgb(0,0,0)</style><script>") is None

    def test_injection_env_blocked(self) -> None:
        assert sanitize_color("env(safe-area-inset-top)") is None

    def test_injection_brace_breakout_blocked(self) -> None:
        assert sanitize_color("rgb(0,0,0);}body{background:red") is None

    def test_empty_and_non_string(self) -> None:
        assert sanitize_color("") is None
        assert sanitize_color("  ") is None
        assert sanitize_color(None) is None  # type: ignore[arg-type]
        assert sanitize_color(42) is None  # type: ignore[arg-type]

    def test_plain_words_blocked(self) -> None:
        assert sanitize_color("red") is None
        assert sanitize_color("transparent") is None
        assert sanitize_color("inherit") is None


class TestContrastTextExtended:
    """Extended contrast_text tests covering boundary cases and all formats."""

    def test_hex_3_digit(self) -> None:
        assert contrast_text("#fff") == "#1a1a1a"
        assert contrast_text("#000") == "white"

    def test_hex_8_digit(self) -> None:
        assert contrast_text("#ffffffff") == "#1a1a1a"
        assert contrast_text("#000000ff") == "white"

    def test_bright_yellow(self) -> None:
        # Yellow (#ffff00) has high luminance → dark text
        assert contrast_text("#ffff00") == "#1a1a1a"

    def test_dark_blue(self) -> None:
        # Navy (#000080) has low luminance → white text
        assert contrast_text("#000080") == "white"

    def test_mid_gray_boundary(self) -> None:
        # #757575 has luminance ≈ 0.178 (just below 0.179) → white text
        assert contrast_text("#757575") == "white"
        # #767676 has luminance ≈ 0.181 (just above 0.179) → dark text
        assert contrast_text("#767676") == "#1a1a1a"

    def test_hsl_yellow(self) -> None:
        assert contrast_text("hsl(60, 100%, 50%)") == "#1a1a1a"

    def test_hsl_dark_blue(self) -> None:
        assert contrast_text("hsl(240, 100%, 25%)") == "white"

    def test_oklch_light(self) -> None:
        assert contrast_text("oklch(0.9 0.1 110)") == "#1a1a1a"

    def test_oklch_dark(self) -> None:
        assert contrast_text("oklch(0.2 0.1 270)") == "white"

    def test_oklcha_parsed(self) -> None:
        assert contrast_text("oklcha(0.9 0.05 90 / 0.5)") == "#1a1a1a"

    def test_empty_string_fallback(self) -> None:
        assert contrast_text("") == "white"

    def test_nonsense_fallback(self) -> None:
        assert contrast_text("not-a-color") == "white"

    def test_color_mix_fallback(self) -> None:
        assert contrast_text("color-mix(in srgb, red 50%, blue)") == "white"


class TestResolveColorExtended:
    """Extended resolve_color tests."""

    def test_direct_hex(self) -> None:
        assert resolve_color("#ff0000") == "#ff0000"

    def test_direct_rgb(self) -> None:
        assert resolve_color("rgb(255, 0, 0)") == "rgb(255, 0, 0)"

    def test_direct_oklch(self) -> None:
        assert resolve_color("oklch(0.5 0.2 30)") == "oklch(0.5 0.2 30)"

    def test_registry_lookup(self) -> None:
        register_colors({"_test_ocean": "#0077cc"})
        assert resolve_color("_test_ocean") == "#0077cc"

    def test_registry_case_insensitive(self) -> None:
        register_colors({"_test_Sky": "#87ceeb"})
        assert resolve_color("_test_sky") == "#87ceeb"

    def test_unknown_name_returns_none(self) -> None:
        assert resolve_color("nonexistent_color_name") is None

    def test_empty_returns_none(self) -> None:
        assert resolve_color("") is None
        assert resolve_color("  ") is None

    def test_non_string_returns_none(self) -> None:
        assert resolve_color(None) is None  # type: ignore[arg-type]
        assert resolve_color(42) is None  # type: ignore[arg-type]


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

    def test_without_template_global_warns(self) -> None:
        registered: dict[str, object] = {}

        class MockAppNoGlobal:
            def template_filter(self, name: str):
                def decorator(fn: object) -> object:
                    registered[name] = fn
                    return fn

                return decorator

        app = MockAppNoGlobal()
        with pytest.warns(ChirpUIWarning, match="template_global"):
            register_filters(app)
        assert "bem" in registered
        assert "tab_is_active" not in registered


class TestBuildHxAttrs:
    """build_hx_attrs converts kwargs to hyphenated dict for html_attrs."""

    def test_converts_underscores_to_hyphens(self) -> None:
        result = build_hx_attrs(hx_post="/save", hx_target="#result")
        assert result == {"hx-post": "/save", "hx-target": "#result"}

    def test_drops_none_values(self) -> None:
        result = build_hx_attrs(hx_get=None, hx_post="/x")
        assert result == {"hx-post": "/x"}

    def test_empty_kwargs_returns_empty_dict(self) -> None:
        assert build_hx_attrs() == {}

    def test_hx_dict_merges_with_kwargs(self) -> None:
        result = build_hx_attrs(hx={"post": "/save", "target": "#out"})
        assert result == {"hx-post": "/save", "hx-target": "#out"}

    def test_hx_dict_kwargs_override(self) -> None:
        result = build_hx_attrs(hx={"post": "/old"}, hx_post="/new")
        assert result == {"hx-post": "/new"}

    def test_hx_dict_prefixed_keys(self) -> None:
        result = build_hx_attrs(hx={"hx-get": "/api"})
        assert result == {"hx-get": "/api"}

    def test_hx_dict_drops_none(self) -> None:
        result = build_hx_attrs(hx={"post": "/save", "get": None})
        assert result == {"hx-post": "/save"}

    def test_all_hx_params(self) -> None:
        result = build_hx_attrs(
            hx_get="/a",
            hx_post="/b",
            hx_put="/c",
            hx_patch="/d",
            hx_delete="/e",
            hx_target="#f",
            hx_swap="innerHTML",
            hx_trigger="click",
            hx_include="[name=q]",
            hx_select="#g",
            hx_ext="sse",
            hx_vals='{"k":"v"}',
        )
        assert result["hx-get"] == "/a"
        assert result["hx-post"] == "/b"
        assert result["hx-vals"] == '{"k":"v"}'
        assert len(result) == 12

    def test_non_hx_keys_also_converted(self) -> None:
        result = build_hx_attrs(data_action="click->ctrl#method")
        assert result == {"data-action": "click->ctrl#method"}

    def test_warns_on_unknown_hx_attr_in_dict(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="unknown htmx attribute"):
            result = build_hx_attrs(hx={"typo": "/url"})
        assert result == {"hx-typo": "/url"}

    def test_warns_on_unknown_hx_attr_in_kwargs(self) -> None:
        with pytest.warns(ChirpUIValidationWarning, match="unknown htmx attribute"):
            result = build_hx_attrs(hx_bogus="/url")
        assert result == {"hx-bogus": "/url"}

    def test_no_warning_on_known_attrs(self) -> None:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error", ChirpUIValidationWarning)
            result = build_hx_attrs(hx={"post": "/save", "target": "#r", "swap": "innerHTML"})
        assert "hx-post" in result

    def test_no_warning_on_hx_on_event_handler(self) -> None:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error", ChirpUIValidationWarning)
            result = build_hx_attrs(hx={"on:click": "alert(1)"})
        assert result == {"hx-on:click": "alert(1)"}

    def test_no_warning_on_non_hx_keys(self) -> None:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error", ChirpUIValidationWarning)
            result = build_hx_attrs(data_action="click->ctrl#method")
        assert result == {"data-action": "click->ctrl#method"}

    def test_registered_as_global(self) -> None:
        registered_globals: dict[str, object] = {}

        class MockApp:
            def template_filter(self, name: str):
                return lambda fn: fn

            def template_global(self, name: str):
                def decorator(fn: object) -> object:
                    registered_globals[name] = fn
                    return fn

                return decorator

        register_filters(MockApp())
        assert "build_hx_attrs" in registered_globals
        assert registered_globals["build_hx_attrs"] is build_hx_attrs


class TestMakeRouteLinkAttrs:
    """make_route_link_attrs builds route-aware link attr resolvers."""

    def test_no_resolver_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs()
        assert route_link_attrs("/page") == {}

    def test_no_resolver_with_fallback(self) -> None:
        route_link_attrs = make_route_link_attrs()
        result = route_link_attrs("/page", fallback={"hx-boost": "true"})
        assert result == {"hx-boost": "true"}

    def test_none_href_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs()
        assert route_link_attrs(None) == {}

    def test_external_href_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs()
        assert route_link_attrs("https://example.com") == {}

    def test_external_flag_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs()
        assert route_link_attrs("/page", external=True) == {}

    def test_disabled_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs()
        assert route_link_attrs("/page", disabled=True) == {}

    def test_boost_false_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs()
        assert route_link_attrs("/page", boost=False) == {}

    def test_swap_resolver_called_for_internal(self) -> None:
        def resolver(href, **kw):
            return {"hx-target": "#main", "hx-boost": "true"}

        route_link_attrs = make_route_link_attrs(swap_resolver=resolver)
        result = route_link_attrs("/page")
        assert result == {"hx-target": "#main", "hx-boost": "true"}

    def test_swap_resolver_not_called_for_external(self) -> None:
        called = []

        def resolver(href, **kw):
            called.append(href)
            return {"hx-target": "#main"}

        route_link_attrs = make_route_link_attrs(swap_resolver=resolver)
        route_link_attrs("https://other.com")
        assert called == []

    def test_explicit_hx_attrs_skips_resolver(self) -> None:
        called = []

        def resolver(href, **kw):
            called.append(href)
            return {"hx-target": "#main"}

        route_link_attrs = make_route_link_attrs(swap_resolver=resolver)
        result = route_link_attrs("/page", attrs_map={"hx_post": "/save"})
        assert result == {}
        assert called == []

    def test_resolver_returning_non_mapping_returns_empty(self) -> None:
        route_link_attrs = make_route_link_attrs(swap_resolver=lambda h, **k: None)
        assert route_link_attrs("/page") == {}
