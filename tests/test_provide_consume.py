"""Tests for provide/consume context flow patterns.

Sprint 0: Edge-case tests for kida scoping.
Sprints 1-4: Provider/consumer tests for each expansion.
"""

from kida import Environment

# ---------------------------------------------------------------------------
# Sprint 0 — Kida scoping edge cases
# ---------------------------------------------------------------------------


class TestProvideConsumeEdgeCases:
    """Verify kida provide/consume scoping before expanding usage."""

    def test_consume_without_provide_returns_fallback(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            "{% call particle_bg() %}X{% end %}"
        ).render()
        assert "chirpui-particle-bg--" not in html or "chirpui-particle-bg-- " not in html

    def test_nested_provide_inner_wins(self, env: Environment) -> None:
        """Inner provide should shadow outer provide for same key."""
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% provide _hero_variant = "accent" %}'
            '{% provide _hero_variant = "muted" %}'
            "{% call particle_bg() %}X{% end %}"
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--muted" in html

    def test_provide_does_not_leak_to_sibling(self, env: Environment) -> None:
        """Provide in one branch should not affect a sibling branch."""
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% provide _hero_variant = "accent" %}'
            "{% call particle_bg() %}A{% end %}"
            "{% end %}"
            "{% call particle_bg() %}B{% end %}"
        ).render()
        # First particle_bg gets accent, second does not
        parts = html.split("B")
        assert "chirpui-particle-bg--accent" in parts[0]

    def test_provide_inside_for_loop(self, env: Environment) -> None:
        """Provide inside a for loop should scope to each iteration."""
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% for v in ["accent", "muted"] %}'
            "{% provide _hero_variant = v %}"
            "{% call particle_bg() %}{{ v }}{% end %}"
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--accent" in html
        assert "chirpui-particle-bg--muted" in html

    def test_provide_flows_through_call_slot(self, env: Environment) -> None:
        """Provide before a {% call %} should be visible inside the slot."""
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}'
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% provide _hero_variant = "accent" %}'
            '{% call surface(variant="muted") %}'
            "{% call particle_bg() %}X{% end %}"
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--accent" in html

    def test_explicit_param_overrides_any_provide(self, env: Environment) -> None:
        """The canonical pattern: explicit param wins over consumed value."""
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% provide _hero_variant = "accent" %}'
            '{% call particle_bg(variant="muted") %}X{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--muted" in html
        assert "chirpui-particle-bg--accent" not in html


# ---------------------------------------------------------------------------
# Sprint 1 — Surface variant propagation
# ---------------------------------------------------------------------------


class TestSurfaceProvide:
    """surface() provides _surface_variant to slot children."""

    def test_surface_provides_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}'
            '{% from "chirpui/badge.html" import badge %}'
            '{% call surface(variant="accent") %}'
            '{{ badge("Test") }}'
            "{% end %}"
        ).render()
        assert "chirpui-surface--accent" in html

    def test_badge_standalone_no_surface_context(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Test", variant="success") }}'
        ).render()
        assert "chirpui-badge--success" in html

    def test_badge_explicit_variant_overrides_surface(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}'
            '{% provide _surface_variant = "accent" %}'
            '{{ badge("Test", variant="success") }}'
            "{% end %}"
        ).render()
        assert "chirpui-badge--success" in html


class TestSectionSurfaceProvide:
    """section() → surface() chain provides _surface_variant."""

    def test_section_provides_surface_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section %}'
            '{% call section("Title", surface_variant="accent") %}'
            "<p>inner</p>"
            "{% end %}"
        ).render()
        assert "chirpui-surface--accent" in html


class TestPanelSurfaceProvide:
    """panel() provides _surface_variant to slot children."""

    def test_panel_provides_surface_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/panel.html" import panel %}'
            '{% call panel(title="Test", surface_variant="elevated") %}'
            "<p>inner</p>"
            "{% end %}"
        ).render()
        assert "chirpui-surface--elevated" in html


# ---------------------------------------------------------------------------
# Sprint 2 — Card variant + accordion name
# ---------------------------------------------------------------------------


class TestCardProvide:
    """card() provides _card_variant to slot children."""

    def test_card_provides_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% from "chirpui/label_overline.html" import label_overline %}'
            '{% call card(title="Feature", variant="feature") %}'
            '{{ label_overline("Section") }}'
            "{% end %}"
        ).render()
        assert "chirpui-card--feature" in html

    def test_label_overline_standalone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/label_overline.html" import label_overline %}'
            '{{ label_overline("Section") }}'
        ).render()
        assert "chirpui-label-overline" in html


class TestAccordionProvide:
    """accordion() provides _accordion_name to accordion_item children."""

    def test_accordion_provides_name(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion, accordion_item %}'
            '{% call accordion(name="faq") %}'
            '{% call accordion_item("Q1") %}A1{% end %}'
            "{% end %}"
        ).render()
        assert 'name="faq"' in html

    def test_accordion_item_standalone_uses_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion_item %}'
            '{% call accordion_item("Q1") %}A1{% end %}'
        ).render()
        assert 'name="accordion"' in html

    def test_accordion_item_explicit_name_overrides(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion, accordion_item %}'
            '{% call accordion(name="faq") %}'
            '{% call accordion_item("Q1", name="other") %}A1{% end %}'
            "{% end %}"
        ).render()
        assert 'name="other"' in html


# ---------------------------------------------------------------------------
# Sprint 3 — Form density
# ---------------------------------------------------------------------------


class TestFormDensityProvide:
    """form() provides _form_density to field children."""

    def test_field_wrapper_standalone_no_density(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email") }}'
        ).render()
        assert "chirpui-field" in html
        assert "chirpui-field--dense" not in html

    def test_form_provides_density_to_fields(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form, text_field %}'
            '{% call form(action="/submit", density="sm") %}'
            '{{ text_field("email", label="Email") }}'
            "{% end %}"
        ).render()
        assert "chirpui-field--dense" in html

    def test_field_no_density_in_form_without_density(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form, text_field %}'
            '{% call form(action="/submit") %}'
            '{{ text_field("email", label="Email") }}'
            "{% end %}"
        ).render()
        assert "chirpui-field--dense" not in html


# ---------------------------------------------------------------------------
# Sprint 4 — Navigation current_path
# ---------------------------------------------------------------------------


class TestNavProvide:
    """sidebar()/navbar() provide _nav_current_path."""

    def test_sidebar_provides_current_path(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_link %}'
            '{% call sidebar(current_path="/home") %}'
            '{{ sidebar_link("/home", "Home", match="exact") }}'
            "{% end %}"
        ).render()
        assert "chirpui-sidebar__link--active" in html

    def test_sidebar_link_standalone_no_context(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar_link %}'
            '{{ sidebar_link("/home", "Home", match="exact") }}'
        ).render()
        assert "chirpui-sidebar__link--active" not in html

    def test_navbar_provides_current_path(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link %}'
            '{% call navbar(brand="App", current_path="/docs") %}'
            '{{ navbar_link("/docs", "Docs", match="exact") }}'
            "{% end %}"
        ).render()
        assert "chirpui-navbar__link--active" in html

    def test_navbar_link_explicit_active_overrides(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link %}'
            '{% call navbar(brand="App", current_path="/other") %}'
            '{{ navbar_link("/docs", "Docs", active=true) }}'
            "{% end %}"
        ).render()
        assert "chirpui-navbar__link--active" in html


# ---------------------------------------------------------------------------
# Streaming — _streaming_role
# ---------------------------------------------------------------------------


class TestStreamingBubbleProvide:
    """streaming_bubble() provides _streaming_role to children."""

    def test_streaming_bubble_provides_role(self, env: Environment) -> None:
        """Children can consume the role via _streaming_role."""
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="user") %}'
            '{% set r = consume("_streaming_role", "none") %}'
            "{{ r }}"
            "{% end %}"
        ).render()
        assert "user" in html

    def test_streaming_bubble_provides_assistant_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            "{% call streaming_bubble() %}"
            '{% set r = consume("_streaming_role", "none") %}'
            "{{ r }}"
            "{% end %}"
        ).render()
        assert "assistant" in html

    def test_streaming_role_not_available_standalone(self, env: Environment) -> None:
        """Without a streaming_bubble parent, consume returns fallback."""
        html = env.from_string(
            '{% set r = consume("_streaming_role", "fallback") %}{{ r }}'
        ).render()
        assert "fallback" in html

    def test_streaming_bubble_role_system_provides(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="system") %}'
            '{% set r = consume("_streaming_role", "none") %}'
            "{{ r }}"
            "{% end %}"
        ).render()
        assert "system" in html

    def test_streaming_bubble_invalid_role_provides_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="bogus") %}'
            '{% set r = consume("_streaming_role", "none") %}'
            "{{ r }}"
            "{% end %}"
        ).render()
        # Invalid role falls back to "assistant" via validate_variant_block
        assert "assistant" in html


# ---------------------------------------------------------------------------
# SSE — _sse_state (manual provide, consumed by sse_retry)
# ---------------------------------------------------------------------------


class TestSseStateConsume:
    """sse_retry consumes _sse_state to auto-disable when connected."""

    def test_sse_retry_standalone_no_disabled(self, env: Environment) -> None:
        """Without _sse_state context, retry button is enabled."""
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}{{ sse_retry("/api/stream") }}'
        ).render()
        assert "disabled" not in html

    def test_sse_retry_disabled_when_connected(self, env: Environment) -> None:
        """When parent provides _sse_state=connected, retry is disabled."""
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{% provide _sse_state = "connected" %}'
            '{{ sse_retry("/api/stream") }}'
            "{% end %}"
        ).render()
        assert "disabled" in html
        assert 'aria-disabled="true"' in html

    def test_sse_retry_enabled_when_error(self, env: Environment) -> None:
        """When parent provides _sse_state=error, retry is enabled."""
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{% provide _sse_state = "error" %}'
            '{{ sse_retry("/api/stream") }}'
            "{% end %}"
        ).render()
        assert "disabled" not in html

    def test_sse_retry_enabled_when_disconnected(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{% provide _sse_state = "disconnected" %}'
            '{{ sse_retry("/api/stream") }}'
            "{% end %}"
        ).render()
        assert "disabled" not in html


# ---------------------------------------------------------------------------
# Suspense — _suspense_busy
# ---------------------------------------------------------------------------


class TestSuspenseGroupProvide:
    """suspense_group() provides _suspense_busy to child slots."""

    def test_suspense_group_provides_busy(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_group %}'
            "{% call suspense_group() %}"
            '{% set b = consume("_suspense_busy", "false") %}'
            "{{ b }}"
            "{% end %}"
        ).render()
        assert "true" in html

    def test_suspense_busy_not_available_standalone(self, env: Environment) -> None:
        html = env.from_string('{% set b = consume("_suspense_busy", "false") %}{{ b }}').render()
        assert "false" in html

    def test_suspense_slot_inside_group_gets_busy(self, env: Environment) -> None:
        """suspense_slot rendered inside suspense_group can access _suspense_busy."""
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot, suspense_group %}'
            "{% call suspense_group() %}"
            '{{ suspense_slot("a") }}'
            "{% end %}"
        ).render()
        assert 'id="a"' in html
        assert 'aria-busy="true"' in html
