"""Unit tests for chirp-ui template filters."""

from chirp_ui.filters import bem, field_errors, register_filters


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

    def test_non_dict_returns_empty(self) -> None:
        assert field_errors("not a dict", "email") == []
        assert field_errors([], "email") == []
        assert field_errors(42, "email") == []

    def test_dict_without_field_returns_empty(self) -> None:
        assert field_errors({"other": ["err"]}, "email") == []

    def test_dict_with_field_returns_list(self) -> None:
        assert field_errors({"email": ["Invalid email"]}, "email") == ["Invalid email"]
        assert field_errors({"x": ["A", "B"]}, "x") == ["A", "B"]

    def test_empty_dict_returns_empty(self) -> None:
        assert field_errors({}, "any") == []


class TestRegisterFilters:
    def test_registers_bem_and_field_errors(self) -> None:
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
