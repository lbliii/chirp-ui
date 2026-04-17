"""Tests for the Alpine runtime detection manifest and helper."""

import re
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from chirp_ui.alpine import (
    ALPINE_REQUIRED_COMPONENTS,
    AlpineRequirement,
    AlpineRuntimeCheck,
    check_alpine_runtime,
)

TEMPLATE_DIR = Path("src/chirp_ui/templates/chirpui")


class TestAlpineRequirement:
    def test_is_frozen(self) -> None:
        req = AlpineRequirement(factory="chirpuiTest", macros=("test",))
        with pytest.raises(FrozenInstanceError):
            req.factory = "other"  # type: ignore[misc]

    def test_conditional_defaults_none(self) -> None:
        req = AlpineRequirement(factory="chirpuiTest", macros=("test",))
        assert req.conditional is None


class TestManifest:
    def test_every_entry_keyed_by_factory_name(self) -> None:
        for key, requirement in ALPINE_REQUIRED_COMPONENTS.items():
            assert key == requirement.factory, (
                f"manifest key {key!r} must match requirement.factory {requirement.factory!r}"
            )

    def test_every_factory_starts_with_chirpui_prefix(self) -> None:
        for factory in ALPINE_REQUIRED_COMPONENTS:
            assert factory.startswith("chirpui"), (
                f"factory {factory!r} must start with 'chirpui' so runtime detection works"
            )

    def test_every_requirement_has_at_least_one_macro(self) -> None:
        for req in ALPINE_REQUIRED_COMPONENTS.values():
            assert req.macros, f"{req.factory} must list at least one macro"

    def test_referenced_macros_exist_as_templates(self) -> None:
        templates = {p.stem for p in TEMPLATE_DIR.glob("*.html")}
        for req in ALPINE_REQUIRED_COMPONENTS.values():
            missing = set(req.macros) - templates
            assert not missing, (
                f"{req.factory} references macros with no template: {sorted(missing)}"
            )

    def test_manifest_covers_every_named_factory_in_templates(self) -> None:
        """Drift detector: any `x-data="chirpuiXxx("` in templates must be manifested."""
        factory_pattern = re.compile(r"""x-data=["'](chirpui\w+)\s*\(""")
        found: set[str] = set()
        for template in TEMPLATE_DIR.glob("*.html"):
            found.update(factory_pattern.findall(template.read_text()))

        missing = found - ALPINE_REQUIRED_COMPONENTS.keys()
        assert not missing, (
            f"factories used in templates but not in ALPINE_REQUIRED_COMPONENTS: {sorted(missing)}"
        )

        stale = ALPINE_REQUIRED_COMPONENTS.keys() - found
        assert not stale, (
            f"factories in manifest with no template usage (remove them): {sorted(stale)}"
        )


class TestCheckAlpineRuntime:
    def test_empty_html_is_ok(self) -> None:
        result = check_alpine_runtime("")
        assert result.ok is True
        assert result.script_loaded is False
        assert result.factories_used == frozenset()
        assert result.missing == frozenset()

    def test_no_factories_is_ok_even_without_script(self) -> None:
        html = "<html><body><p>nothing interactive here</p></body></html>"
        result = check_alpine_runtime(html)
        assert result.ok is True
        assert result.factories_used == frozenset()

    def test_factory_without_script_is_not_ok(self) -> None:
        html = '<div x-data="chirpuiThemeToggle()"></div>'
        result = check_alpine_runtime(html)
        assert result.ok is False
        assert result.script_loaded is False
        assert result.factories_used == frozenset({"chirpuiThemeToggle"})
        assert result.missing == frozenset({"chirpuiThemeToggle"})

    def test_factory_with_script_is_ok(self) -> None:
        html = (
            '<script src="/static/chirpui-alpine.js"></script>'
            '<div x-data="chirpuiThemeToggle()"></div>'
        )
        result = check_alpine_runtime(html)
        assert result.ok is True
        assert result.script_loaded is True
        assert result.missing == frozenset()

    def test_detects_multiple_factories(self) -> None:
        html = (
            '<div x-data="chirpuiThemeToggle()"></div>'
            '<div x-data="chirpuiDialogTarget()"></div>'
            '<div x-data="chirpuiDropdown()"></div>'
        )
        result = check_alpine_runtime(html)
        assert result.factories_used == frozenset(
            {"chirpuiThemeToggle", "chirpuiDialogTarget", "chirpuiDropdown"}
        )
        assert result.missing == result.factories_used

    def test_dedupes_repeated_factories(self) -> None:
        html = (
            '<div x-data="chirpuiCopy()"></div>'
            '<div x-data="chirpuiCopy()"></div>'
            '<div x-data="chirpuiCopy()"></div>'
        )
        result = check_alpine_runtime(html)
        assert result.factories_used == frozenset({"chirpuiCopy"})

    def test_ignores_anonymous_x_data(self) -> None:
        html = '<div x-data="{ shown: false }"></div><div x-data="{ active: false }"></div>'
        result = check_alpine_runtime(html)
        assert result.factories_used == frozenset()
        assert result.ok is True

    def test_accepts_single_quoted_x_data(self) -> None:
        html = "<div x-data='chirpuiThemeToggle()'></div>"
        result = check_alpine_runtime(html)
        assert result.factories_used == frozenset({"chirpuiThemeToggle"})

    def test_factory_with_arguments_detected(self) -> None:
        html = '<div x-data="chirpuiSidebar({ collapsible: true, resizable: true })"></div>'
        result = check_alpine_runtime(html)
        assert result.factories_used == frozenset({"chirpuiSidebar"})

    def test_script_detection_tolerates_path_prefix(self) -> None:
        html = (
            '<script src="../static/assets/chirpui-alpine.js"></script>'
            '<div x-data="chirpuiThemeToggle()"></div>'
        )
        result = check_alpine_runtime(html)
        assert result.script_loaded is True
        assert result.ok is True

    def test_script_detection_tolerates_minified_suffix(self) -> None:
        html = (
            '<script src="/static/chirpui-alpine.js?v=1"></script>'
            '<div x-data="chirpuiCopy()"></div>'
        )
        result = check_alpine_runtime(html)
        assert result.script_loaded is True
        assert result.ok is True

    def test_non_chirpui_factory_is_ignored(self) -> None:
        html = '<div x-data="someOtherApp()"></div>'
        result = check_alpine_runtime(html)
        assert result.factories_used == frozenset()
        assert result.ok is True

    def test_result_is_frozen(self) -> None:
        result = check_alpine_runtime("")
        with pytest.raises(FrozenInstanceError):
            result.ok = False  # type: ignore[misc]


class TestExports:
    def test_public_api_exports(self) -> None:
        import chirp_ui

        assert chirp_ui.ALPINE_REQUIRED_COMPONENTS is ALPINE_REQUIRED_COMPONENTS
        assert chirp_ui.AlpineRequirement is AlpineRequirement
        assert chirp_ui.AlpineRuntimeCheck is AlpineRuntimeCheck
        assert chirp_ui.check_alpine_runtime is check_alpine_runtime
