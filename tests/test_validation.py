"""Unit tests for chirp-ui validation module (set_strict, _is_strict, registries)."""

import threading

from chirp_ui.validation import (
    SIZE_REGISTRY,
    VARIANT_REGISTRY,
    _is_strict,
    set_strict,
)


class TestSetStrict:
    """set_strict / _is_strict ContextVar behavior."""

    def setup_method(self) -> None:
        set_strict(False)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_default_is_not_strict(self) -> None:
        assert _is_strict() is False

    def test_set_strict_true(self) -> None:
        set_strict(True)
        assert _is_strict() is True

    def test_set_strict_false_after_true(self) -> None:
        set_strict(True)
        assert _is_strict() is True
        set_strict(False)
        assert _is_strict() is False

    def test_toggle_repeatedly(self) -> None:
        for _ in range(5):
            set_strict(True)
            assert _is_strict() is True
            set_strict(False)
            assert _is_strict() is False


class TestStrictContextVarIsolation:
    """ContextVar isolation across threads."""

    def setup_method(self) -> None:
        set_strict(False)

    def teardown_method(self) -> None:
        set_strict(False)

    def test_child_set_does_not_leak_to_parent(self) -> None:
        set_strict(False)

        def child_fn() -> None:
            set_strict(True)
            assert _is_strict() is True

        t = threading.Thread(target=child_fn)
        t.start()
        t.join()

        assert _is_strict() is False, "child's set_strict should not leak to parent"


class TestVariantRegistry:
    """VARIANT_REGISTRY structure and content checks."""

    def test_registry_is_nonempty(self) -> None:
        assert len(VARIANT_REGISTRY) > 0

    def test_all_keys_are_strings(self) -> None:
        for block in VARIANT_REGISTRY:
            assert isinstance(block, str)

    def test_all_values_are_tuples_of_strings(self) -> None:
        for block, variants in VARIANT_REGISTRY.items():
            assert isinstance(variants, tuple), f"{block} value is not a tuple"
            for v in variants:
                assert isinstance(v, str), f"{block} variant {v!r} is not str"

    def test_known_blocks_present(self) -> None:
        expected = {"alert", "badge", "btn", "surface", "toast"}
        missing = expected - set(VARIANT_REGISTRY)
        assert not missing, f"expected blocks missing: {missing}"

    def test_alert_variants(self) -> None:
        assert "info" in VARIANT_REGISTRY["alert"]
        assert "success" in VARIANT_REGISTRY["alert"]
        assert "warning" in VARIANT_REGISTRY["alert"]
        assert "error" in VARIANT_REGISTRY["alert"]

    def test_no_duplicate_variants(self) -> None:
        for block, variants in VARIANT_REGISTRY.items():
            assert len(variants) == len(set(variants)), f"{block} has duplicate variants"


class TestSizeRegistry:
    """SIZE_REGISTRY structure and content checks."""

    def test_registry_is_nonempty(self) -> None:
        assert len(SIZE_REGISTRY) > 0

    def test_all_values_are_tuples_of_strings(self) -> None:
        for block, sizes in SIZE_REGISTRY.items():
            assert isinstance(sizes, tuple), f"{block} value is not a tuple"
            for s in sizes:
                assert isinstance(s, str), f"{block} size {s!r} is not str"

    def test_known_blocks_present(self) -> None:
        expected = {"btn", "modal"}
        missing = expected - set(SIZE_REGISTRY)
        assert not missing, f"expected blocks missing: {missing}"

    def test_btn_sizes(self) -> None:
        assert "sm" in SIZE_REGISTRY["btn"]
        assert "md" in SIZE_REGISTRY["btn"]
        assert "lg" in SIZE_REGISTRY["btn"]

    def test_no_duplicate_sizes(self) -> None:
        for block, sizes in SIZE_REGISTRY.items():
            assert len(sizes) == len(set(sizes)), f"{block} has duplicate sizes"


class TestDescriptorCoverage:
    """Every template in chirpui/ must have a ComponentDescriptor (or be excluded)."""

    # Composition-only templates with no chirpui-* CSS blocks of their own.
    EXCLUDED = frozenset(
        {
            "app_layout",
            "app_shell_layout",
            "ascii_icon",
            "auth",
            "bento_grid",
            "command_bar",
            "config_card",
            "config_dashboard",
            "islands",
            "layout",
            "modal_overlay",
            "nav_link",
            "oob",
            "search_header",
            "share_menu",
            "shell_frame",
            "state_primitives",
            "status_with_hint",
            "tabbed_page_layout",
            "tabs_panels",
        }
    )

    def test_descriptor_coverage(self) -> None:
        """All non-excluded templates must have at least one COMPONENTS entry."""
        from pathlib import Path

        from chirp_ui.components import COMPONENTS

        templates = {p.stem for p in Path("src/chirp_ui/templates/chirpui").glob("*.html")}
        registered = {c.template.replace(".html", "") for c in COMPONENTS.values() if c.template}
        unregistered = sorted(templates - registered - self.EXCLUDED)
        assert not unregistered, (
            f"Templates without ComponentDescriptor (add descriptor or exclude): {unregistered}"
        )

    def test_excluded_templates_exist(self) -> None:
        """Every excluded template must actually exist (stale exclusions are bugs)."""
        from pathlib import Path

        templates = {p.stem for p in Path("src/chirp_ui/templates/chirpui").glob("*.html")}
        stale = sorted(self.EXCLUDED - templates)
        assert not stale, f"Excluded templates no longer exist: {stale}"
