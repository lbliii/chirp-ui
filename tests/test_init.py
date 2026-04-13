"""Unit tests for chirp-ui package init (static_path, get_loader, register_filters)."""

from kida import Environment, PackageLoader

import chirp_ui
from chirp_ui.filters import (
    bem,
    deprecate_param,
    field_errors,
    html_attrs,
    icon,
    validate_size,
    validate_variant,
    validate_variant_block,
)


class TestStaticPath:
    def test_returns_path(self) -> None:
        path = chirp_ui.static_path()
        assert hasattr(path, "exists")
        assert hasattr(path, "is_dir")

    def test_path_exists(self) -> None:
        path = chirp_ui.static_path()
        assert path.exists()

    def test_contains_templates_dir(self) -> None:
        path = chirp_ui.static_path()
        assert path.name == "templates"
        assert (path / "chirpui").exists()
        assert (path / "chirpui.css").exists()


class TestGetLoader:
    def test_returns_package_loader(self) -> None:
        loader = chirp_ui.get_loader()
        assert isinstance(loader, PackageLoader)

    def test_loader_can_load_template(self) -> None:
        env = Environment(loader=chirp_ui.get_loader(), autoescape=True)
        env.filters.update(
            {
                "bem": bem,
                "deprecate_param": deprecate_param,
                "field_errors": field_errors,
                "html_attrs": html_attrs,
                "icon": icon,
                "validate_variant": validate_variant,
                "validate_variant_block": validate_variant_block,
                "validate_size": validate_size,
            }
        )
        # card.html defines macros; import and call to verify loader resolves it
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}{% call card() %}Body{% end %}'
        ).render()
        assert "chirpui-card" in html
        assert "Body" in html


class TestRegisterFilters:
    def test_registers_filters_on_mock_app(self) -> None:
        registered: dict[str, object] = {}

        class MockApp:
            def template_filter(self, name: str):
                def decorator(fn: object) -> object:
                    registered[name] = fn
                    return fn

                return decorator

        app = MockApp()
        chirp_ui.register_filters(app)
        assert "bem" in registered
        assert "field_errors" in registered
        assert "html_attrs" in registered
        assert "icon" in registered
        assert "validate_variant" in registered
        assert "validate_variant_block" in registered
        assert "validate_size" in registered
