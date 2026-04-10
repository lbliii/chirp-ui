"""Render tests for all chirp-ui ASCII components.

Each test verifies:
- Correct HTML structure (BEM classes present)
- Parameter variants (defaults, optional args)
- Slot content injection where applicable
- Accessibility attributes on interactive/semantic components
"""

from kida import Environment

# ---------------------------------------------------------------------------
# ascii_7seg
# ---------------------------------------------------------------------------


class TestAscii7Seg:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_7seg.html" import ascii_7seg %}{{ ascii_7seg("42") }}'
        ).render()
        assert "chirpui-ascii-7seg" in html
        assert 'data-char="4"' in html
        assert 'data-char="2"' in html

    def test_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_7seg.html" import ascii_7seg %}'
            '{{ ascii_7seg("99", label="UPTIME") }}'
        ).render()
        assert "chirpui-ascii-7seg__label" in html
        assert "UPTIME" in html

    def test_variant_accent(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_7seg.html" import ascii_7seg %}'
            '{{ ascii_7seg("1", variant="accent") }}'
        ).render()
        assert "chirpui-ascii-7seg--accent" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_7seg.html" import ascii_7seg %}'
            '{{ ascii_7seg("0", cls="custom") }}'
        ).render()
        assert "custom" in html

    def test_frame_aria_hidden(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_7seg.html" import ascii_7seg %}{{ ascii_7seg("1") }}'
        ).render()
        assert 'aria-hidden="true"' in html


# ---------------------------------------------------------------------------
# ascii_badge
# ---------------------------------------------------------------------------


class TestAsciiBadge:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_badge.html" import ascii_badge %}'
            '{{ ascii_badge(text="deployed") }}'
        ).render()
        assert "chirpui-ascii-badge" in html
        assert "deployed" in html

    def test_glyph(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_badge.html" import ascii_badge %}'
            '{{ ascii_badge(text="ok", glyph="✦") }}'
        ).render()
        assert "chirpui-ascii-badge__glyph" in html

    def test_variant_warning(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_badge.html" import ascii_badge %}'
            '{{ ascii_badge(text="warn", variant="warning") }}'
        ).render()
        assert "chirpui-ascii-badge--warning" in html

    def test_frame_bracket(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_badge.html" import ascii_badge %}'
            '{{ ascii_badge(text="ok", frame="bracket") }}'
        ).render()
        assert "[" in html
        assert "]" in html

    def test_frame_none(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_badge.html" import ascii_badge %}'
            '{{ ascii_badge(text="plain", frame="none") }}'
        ).render()
        assert "chirpui-ascii-badge__open" not in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_badge.html" import ascii_badge %}'
            '{{ ascii_badge(text="x", cls="extra") }}'
        ).render()
        assert "extra" in html


# ---------------------------------------------------------------------------
# ascii_border
# ---------------------------------------------------------------------------


class TestAsciiBorder:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_border.html" import ascii_border %}'
            "{% call ascii_border() %}Inside{% end %}"
        ).render()
        assert "chirpui-ascii-border" in html
        assert "Inside" in html

    def test_variant_double(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_border.html" import ascii_border %}'
            '{% call ascii_border(variant="double") %}X{% end %}'
        ).render()
        assert "chirpui-ascii-border--double" in html

    def test_variant_rounded(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_border.html" import ascii_border %}'
            '{% call ascii_border(variant="rounded") %}X{% end %}'
        ).render()
        assert "chirpui-ascii-border--rounded" in html

    def test_glyph(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_border.html" import ascii_border %}'
            '{% call ascii_border(glyph="✦") %}X{% end %}'
        ).render()
        # glyph appears in top border line
        assert "✦" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_border.html" import ascii_border %}'
            '{% call ascii_border(cls="my-border") %}X{% end %}'
        ).render()
        assert "my-border" in html

    def test_decorative_aria_hidden(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_border.html" import ascii_border %}'
            "{% call ascii_border() %}X{% end %}"
        ).render()
        assert 'aria-hidden="true"' in html


# ---------------------------------------------------------------------------
# ascii_breaker_panel
# ---------------------------------------------------------------------------


class TestAsciiBreakerPanel:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_breaker_panel.html" import breaker_panel, breaker %}'
            '{% call breaker_panel(title="Services") %}'
            '{{ breaker("api", label="API", checked=true) }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-breaker-panel" in html
        assert "Services" in html
        assert "API" in html

    def test_master_switch(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_breaker_panel.html" import breaker_panel %}'
            '{% call breaker_panel(title="Prod", master="main") %}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-breaker-panel__master" in html

    def test_breaker_checked_indicator(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_breaker_panel.html" import breaker_panel, breaker %}'
            "{% call breaker_panel() %}"
            '{{ breaker("db", label="DB", checked=true) }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-indicator--success" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_breaker_panel.html" import breaker_panel %}'
            '{% call breaker_panel(cls="extra") %}{% end %}'
        ).render()
        assert "extra" in html


# ---------------------------------------------------------------------------
# ascii_checkbox
# ---------------------------------------------------------------------------


class TestAsciiCheckbox:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_checkbox.html" import ascii_checkbox %}'
            '{{ ascii_checkbox("terms", label="Accept") }}'
        ).render()
        assert "chirpui-ascii-checkbox" in html
        assert 'type="checkbox"' in html
        assert "Accept" in html

    def test_checked(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_checkbox.html" import ascii_checkbox %}'
            '{{ ascii_checkbox("opt", checked=true) }}'
        ).render()
        assert "checked" in html

    def test_disabled(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_checkbox.html" import ascii_checkbox %}'
            '{{ ascii_checkbox("opt", disabled=true) }}'
        ).render()
        assert "disabled" in html
        assert "chirpui-ascii-checkbox--disabled" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_checkbox.html" import ascii_checkbox %}'
            '{{ ascii_checkbox("opt", variant="success") }}'
        ).render()
        assert "chirpui-ascii-checkbox--success" in html

    def test_group(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_checkbox.html" import ascii_checkbox, ascii_checkbox_group %}'
            '{% call ascii_checkbox_group(legend="Opts") %}'
            '{{ ascii_checkbox("a", label="A") }}'
            "{% end %}"
        ).render()
        assert "<fieldset" in html
        assert "<legend" in html
        assert "Opts" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_checkbox.html" import ascii_checkbox %}'
            '{{ ascii_checkbox("x", cls="extra") }}'
        ).render()
        assert "extra" in html


# ---------------------------------------------------------------------------
# ascii_divider
# ---------------------------------------------------------------------------


class TestAsciiDivider:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_divider.html" import ascii_divider %}{{ ascii_divider() }}'
        ).render()
        assert "chirpui-ascii-divider" in html
        assert 'role="separator"' in html

    def test_glyph(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_divider.html" import ascii_divider %}'
            '{{ ascii_divider(glyph="✦") }}'
        ).render()
        assert "✦" in html
        assert "chirpui-ascii-divider__glyph" in html

    def test_variant_double(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_divider.html" import ascii_divider %}'
            '{{ ascii_divider(variant="double") }}'
        ).render()
        assert "chirpui-ascii-divider--double" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_divider.html" import ascii_divider %}'
            '{{ ascii_divider(cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_empty
# ---------------------------------------------------------------------------


class TestAsciiEmpty:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_empty.html" import ascii_empty %}'
            "{% call ascii_empty() %}{% end %}"
        ).render()
        assert "chirpui-ascii-empty" in html
        assert "Nothing here" in html

    def test_custom_heading(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_empty.html" import ascii_empty %}'
            '{% call ascii_empty(heading="No results", description="Try again") %}{% end %}'
        ).render()
        assert "No results" in html
        assert "Try again" in html

    def test_variant_muted(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_empty.html" import ascii_empty %}'
            '{% call ascii_empty(variant="muted") %}{% end %}'
        ).render()
        assert "chirpui-ascii-empty--muted" in html

    def test_slot_content(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_empty.html" import ascii_empty %}'
            "{% call ascii_empty() %}<button>Reset</button>{% end %}"
        ).render()
        assert "<button>Reset</button>" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_empty.html" import ascii_empty %}'
            '{% call ascii_empty(cls="wide") %}{% end %}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_error
# ---------------------------------------------------------------------------


class TestAsciiError:
    def test_404_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_error.html" import ascii_error %}'
            "{% call ascii_error() %}{% end %}"
        ).render()
        assert "chirpui-ascii-error" in html
        assert "Page not found" in html

    def test_500(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_error.html" import ascii_error %}'
            '{% call ascii_error(code="500") %}{% end %}'
        ).render()
        assert "Internal server error" in html
        assert "500" in html

    def test_403(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_error.html" import ascii_error %}'
            '{% call ascii_error(code="403") %}{% end %}'
        ).render()
        assert "Access denied" in html

    def test_custom_heading(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_error.html" import ascii_error %}'
            '{% call ascii_error(code="500", heading="Oops") %}{% end %}'
        ).render()
        assert "Oops" in html

    def test_slot_content(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_error.html" import ascii_error %}'
            '{% call ascii_error() %}<a href="/">Home</a>{% end %}'
        ).render()
        assert "Home" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_error.html" import ascii_error %}'
            '{% call ascii_error(cls="full") %}{% end %}'
        ).render()
        assert "full" in html


# ---------------------------------------------------------------------------
# ascii_fader
# ---------------------------------------------------------------------------


class TestAsciiFader:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader %}'
            '{{ ascii_fader("vol", value=50, label="VOL") }}'
        ).render()
        assert "chirpui-ascii-fader" in html
        assert "VOL" in html

    def test_range_input(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader %}'
            '{{ ascii_fader("vol", value=75, label="Volume") }}'
        ).render()
        assert 'type="range"' in html
        assert 'min="0"' in html
        assert 'max="100"' in html
        assert 'aria-label="Volume"' in html

    def test_value_rendering(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader %}'
            '{{ ascii_fader("vol", value=100) }}'
        ).render()
        # All 8 segments should be filled at 100%
        assert html.count("chirpui-ascii-fader__segment--filled") == 8

    def test_value_zero(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader %}'
            '{{ ascii_fader("vol", value=0) }}'
        ).render()
        assert "chirpui-ascii-fader__segment--filled" not in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader %}'
            '{{ ascii_fader("vol", variant="accent") }}'
        ).render()
        assert "chirpui-ascii-fader--accent" in html

    def test_fader_bank(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader, fader_bank %}'
            '{% call fader_bank(title="Mix") %}'
            '{{ ascii_fader("ch1", value=80, label="CH1") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-fader-bank" in html
        assert "Mix" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_fader.html" import ascii_fader %}'
            '{{ ascii_fader("x", cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_icon
# ---------------------------------------------------------------------------


class TestAsciiIcon:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}{{ ascii_icon("✦") }}'
        ).render()
        assert "chirpui-ascii" in html
        assert "✦" in html
        assert 'aria-hidden="true"' in html

    def test_animation_blink(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("✦", animation="blink") }}'
        ).render()
        assert "chirpui-ascii--blink" in html

    def test_animation_rotate(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("x", animation="rotate") }}'
        ).render()
        assert "chirpui-ascii--rotate" in html
        # Rotate uses 4 directional chars
        assert "◜" in html

    def test_size_lg(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}{{ ascii_icon("◆", size="lg") }}'
        ).render()
        assert "chirpui-ascii--lg" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("x", cls="my-icon") }}'
        ).render()
        assert "my-icon" in html


# ---------------------------------------------------------------------------
# ascii_indicator
# ---------------------------------------------------------------------------


class TestAsciiIndicator:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator %}'
            '{{ indicator("PWR", variant="success") }}'
        ).render()
        assert "chirpui-ascii-indicator" in html
        assert "chirpui-ascii-indicator--success" in html
        assert "PWR" in html

    def test_blink(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator %}'
            '{{ indicator("X", blink=true) }}'
        ).render()
        assert "chirpui-ascii-indicator--blink" in html

    def test_blink_fast(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator %}'
            '{{ indicator("ERR", variant="error", blink="fast") }}'
        ).render()
        assert "chirpui-ascii-indicator--blink-fast" in html

    def test_glyph_round(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator %}'
            '{{ indicator(glyph="round") }}'
        ).render()
        assert "●" in html

    def test_indicator_row(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator, indicator_row %}'
            "{% call indicator_row() %}"
            '{{ indicator("A") }}{{ indicator("B") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-indicator-row" in html

    def test_indicator_row_nowrap(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator_row %}'
            "{% call indicator_row(nowrap=true) %}{% end %}"
        ).render()
        assert "chirpui-ascii-indicator-row--nowrap" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_indicator.html" import indicator %}{{ indicator(cls="extra") }}'
        ).render()
        assert "extra" in html


# ---------------------------------------------------------------------------
# ascii_knob
# ---------------------------------------------------------------------------


class TestAsciiKnob:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_knob.html" import ascii_knob %}'
            '{{ ascii_knob("vol", options=["Low", "Med", "High"]) }}'
        ).render()
        assert "chirpui-ascii-knob" in html
        assert "<fieldset" in html
        assert 'type="radio"' in html

    def test_selected(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_knob.html" import ascii_knob %}'
            '{{ ascii_knob("vol", options=["A", "B"], selected="B") }}'
        ).render()
        assert "checked" in html

    def test_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_knob.html" import ascii_knob %}'
            '{{ ascii_knob("m", options=["X"], label="Mode") }}'
        ).render()
        assert "<legend" in html
        assert "Mode" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_knob.html" import ascii_knob %}'
            '{{ ascii_knob("x", options=["A"], variant="accent") }}'
        ).render()
        assert "chirpui-ascii-knob--accent" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_knob.html" import ascii_knob %}'
            '{{ ascii_knob("x", options=["A"], cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_progress
# ---------------------------------------------------------------------------


class TestAsciiProgress:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_progress.html" import ascii_progress %}'
            "{{ ascii_progress(value=50) }}"
        ).render()
        assert "chirpui-ascii-progress" in html
        assert 'role="progressbar"' in html
        assert 'aria-valuenow="50"' in html

    def test_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_progress.html" import ascii_progress %}'
            '{{ ascii_progress(value=10, label="Loading") }}'
        ).render()
        assert 'aria-label="Loading"' in html
        assert "Loading" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_progress.html" import ascii_progress %}'
            '{{ ascii_progress(value=100, variant="success") }}'
        ).render()
        assert "chirpui-ascii-progress--success" in html

    def test_full_bar(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_progress.html" import ascii_progress %}'
            "{{ ascii_progress(value=100, width=10) }}"
        ).render()
        assert html.count("chirpui-ascii-progress__filled") == 10

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_progress.html" import ascii_progress %}'
            '{{ ascii_progress(cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_radio
# ---------------------------------------------------------------------------


class TestAsciiRadio:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_radio.html" import ascii_radio %}'
            '{{ ascii_radio("prio", "low", label="Low") }}'
        ).render()
        assert "chirpui-ascii-radio" in html
        assert 'type="radio"' in html
        assert "Low" in html

    def test_checked(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_radio.html" import ascii_radio %}'
            '{{ ascii_radio("prio", "hi", checked=true) }}'
        ).render()
        assert "checked" in html

    def test_disabled(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_radio.html" import ascii_radio %}'
            '{{ ascii_radio("x", "v", disabled=true) }}'
        ).render()
        assert "disabled" in html
        assert "chirpui-ascii-radio--disabled" in html

    def test_group(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_radio.html" import ascii_radio, ascii_radio_group %}'
            '{% call ascii_radio_group(legend="Level") %}'
            '{{ ascii_radio("lvl", "a", label="A") }}'
            "{% end %}"
        ).render()
        assert "<fieldset" in html
        assert "Level" in html

    def test_group_horizontal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_radio.html" import ascii_radio_group %}'
            '{% call ascii_radio_group(layout="horizontal") %}{% end %}'
        ).render()
        assert "chirpui-ascii-radio-group--horizontal" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_radio.html" import ascii_radio %}'
            '{{ ascii_radio("x", "v", cls="extra") }}'
        ).render()
        assert "extra" in html


# ---------------------------------------------------------------------------
# ascii_skeleton
# ---------------------------------------------------------------------------


class TestAsciiSkeleton:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_skeleton.html" import ascii_skeleton %}{{ ascii_skeleton() }}'
        ).render()
        assert "chirpui-ascii-skeleton" in html
        assert 'aria-hidden="true"' in html

    def test_variant_text(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_skeleton.html" import ascii_skeleton %}'
            '{{ ascii_skeleton(variant="text", lines=3) }}'
        ).render()
        assert "chirpui-ascii-skeleton--text" in html
        assert html.count("chirpui-ascii-skeleton__line") == 3

    def test_variant_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_skeleton.html" import ascii_skeleton %}'
            '{{ ascii_skeleton(variant="card") }}'
        ).render()
        assert "chirpui-ascii-skeleton--card" in html
        assert "chirpui-ascii-skeleton__line--header" in html

    def test_variant_avatar(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_skeleton.html" import ascii_skeleton %}'
            '{{ ascii_skeleton(variant="avatar") }}'
        ).render()
        assert "chirpui-ascii-skeleton--avatar" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_skeleton.html" import ascii_skeleton %}'
            '{{ ascii_skeleton(cls="shimmer") }}'
        ).render()
        assert "shimmer" in html


# ---------------------------------------------------------------------------
# ascii_sparkline
# ---------------------------------------------------------------------------


class TestAsciiSparkline:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_sparkline.html" import ascii_sparkline %}'
            "{{ ascii_sparkline(values=[1, 5, 3, 7]) }}"
        ).render()
        assert "chirpui-ascii-sparkline" in html
        assert 'role="img"' in html

    def test_aria_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_sparkline.html" import ascii_sparkline %}'
            "{{ ascii_sparkline(values=[2, 4]) }}"
        ).render()
        assert "Sparkline:" in html

    def test_variant_accent(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_sparkline.html" import ascii_sparkline %}'
            '{{ ascii_sparkline(values=[1, 2], variant="accent") }}'
        ).render()
        assert "chirpui-ascii-sparkline--accent" in html

    def test_bar_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_sparkline.html" import ascii_sparkline %}'
            "{{ ascii_sparkline(values=[1, 2, 3]) }}"
        ).render()
        assert html.count("chirpui-ascii-sparkline__bar") == 3

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_sparkline.html" import ascii_sparkline %}'
            '{{ ascii_sparkline(values=[1], cls="inline") }}'
        ).render()
        assert "inline" in html


# ---------------------------------------------------------------------------
# ascii_spinner
# ---------------------------------------------------------------------------


class TestAsciiSpinner:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_spinner.html" import ascii_spinner %}{{ ascii_spinner() }}'
        ).render()
        assert "chirpui-ascii-spinner" in html
        assert 'role="status"' in html
        assert 'aria-label="Loading"' in html

    def test_charset_box(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_spinner.html" import ascii_spinner %}'
            '{{ ascii_spinner(charset="box") }}'
        ).render()
        assert "chirpui-ascii-spinner--box" in html
        assert "◜" in html

    def test_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_spinner.html" import ascii_spinner %}'
            '{{ ascii_spinner(label="Fetching...") }}'
        ).render()
        assert 'aria-label="Fetching..."' in html
        assert "Fetching..." in html

    def test_size(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_spinner.html" import ascii_spinner %}'
            '{{ ascii_spinner(size="lg") }}'
        ).render()
        assert "chirpui-ascii-spinner--lg" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_spinner.html" import ascii_spinner %}'
            '{{ ascii_spinner(cls="center") }}'
        ).render()
        assert "center" in html


# ---------------------------------------------------------------------------
# ascii_split_flap
# ---------------------------------------------------------------------------


class TestAsciiSplitFlap:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_split_flap.html" import split_flap %}{{ split_flap("HI") }}'
        ).render()
        assert "chirpui-split-flap" in html
        assert html.count("chirpui-split-flap__char") == 2

    def test_variant_amber(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_split_flap.html" import split_flap %}'
            '{{ split_flap("X", variant="amber") }}'
        ).render()
        assert "chirpui-split-flap--amber" in html

    def test_animate_false(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_split_flap.html" import split_flap %}'
            '{{ split_flap("X", animate=false) }}'
        ).render()
        assert "chirpui-split-flap--animate" not in html

    def test_board(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_split_flap.html" import split_flap_board, split_flap_row %}'
            '{% call split_flap_board(title="DEPARTURES") %}'
            '{{ split_flap_row(cells=["08:42", "NYC"]) }}'
            "{% end %}"
        ).render()
        assert "chirpui-split-flap-board" in html
        assert "DEPARTURES" in html
        assert "chirpui-split-flap-row" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_split_flap.html" import split_flap %}'
            '{{ split_flap("X", cls="mono") }}'
        ).render()
        assert "mono" in html


# ---------------------------------------------------------------------------
# ascii_stepper
# ---------------------------------------------------------------------------


class TestAsciiStepper:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_stepper.html" import ascii_stepper %}'
            '{{ ascii_stepper(steps=["Build", "Test", "Deploy"], current=1) }}'
        ).render()
        assert "chirpui-ascii-stepper" in html
        assert 'role="navigation"' in html

    def test_step_states(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_stepper.html" import ascii_stepper %}'
            '{{ ascii_stepper(steps=["A", "B", "C"], current=1) }}'
        ).render()
        assert "chirpui-ascii-stepper__step--complete" in html
        assert "chirpui-ascii-stepper__step--active" in html
        assert "chirpui-ascii-stepper__step--pending" in html

    def test_connector(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_stepper.html" import ascii_stepper %}'
            '{{ ascii_stepper(steps=["A", "B"], current=0) }}'
        ).render()
        assert "chirpui-ascii-stepper__connector" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_stepper.html" import ascii_stepper %}'
            '{{ ascii_stepper(steps=["X"], variant="success") }}'
        ).render()
        assert "chirpui-ascii-stepper--success" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_stepper.html" import ascii_stepper %}'
            '{{ ascii_stepper(steps=["X"], cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_table
# ---------------------------------------------------------------------------


class TestAsciiTable:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_table.html" import ascii_table, ascii_row %}'
            '{% call ascii_table(headers=["Name", "Status"]) %}'
            '{{ ascii_row("api", "OK") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-table" in html
        assert 'role="table"' in html
        assert 'role="columnheader"' in html
        assert 'role="cell"' in html

    def test_variant_double(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_table.html" import ascii_table %}'
            '{% call ascii_table(headers=["X"], variant="double") %}{% end %}'
        ).render()
        assert "chirpui-ascii-table--double" in html

    def test_compact(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_table.html" import ascii_table %}'
            '{% call ascii_table(headers=["X"], compact=true) %}{% end %}'
        ).render()
        assert "chirpui-ascii-table--compact" in html

    def test_striped(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_table.html" import ascii_table %}'
            '{% call ascii_table(headers=["X"], striped=true) %}{% end %}'
        ).render()
        assert "chirpui-ascii-table--striped" in html

    def test_alignment(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_table.html" import ascii_table, ascii_row %}'
            '{% call ascii_table(headers=["A", "B"], align=["left", "right"]) %}'
            '{{ ascii_row("x", "y") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-table__cell--left" in html
        assert "chirpui-ascii-table__cell--right" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_table.html" import ascii_table %}'
            '{% call ascii_table(cls="wide") %}{% end %}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_ticker
# ---------------------------------------------------------------------------


class TestAsciiTicker:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_ticker.html" import ascii_ticker %}'
            '{{ ascii_ticker("Breaking news") }}'
        ).render()
        assert "chirpui-ascii-ticker" in html
        assert 'role="marquee"' in html
        assert "Breaking news" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_ticker.html" import ascii_ticker %}'
            '{{ ascii_ticker("X", variant="warning") }}'
        ).render()
        assert "chirpui-ascii-ticker--warning" in html

    def test_speed(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_ticker.html" import ascii_ticker %}'
            '{{ ascii_ticker("X", speed="fast") }}'
        ).render()
        assert "chirpui-ascii-ticker--fast" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_ticker.html" import ascii_ticker %}'
            '{{ ascii_ticker("X", cls="banner") }}'
        ).render()
        assert "banner" in html


# ---------------------------------------------------------------------------
# ascii_tile_btn
# ---------------------------------------------------------------------------


class TestAsciiTileBtn:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn %}'
            '{{ tile_btn("F1", label="EXEC") }}'
        ).render()
        assert "chirpui-ascii-tile-btn" in html
        assert "<button" in html
        assert "EXEC" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn %}'
            '{{ tile_btn(variant="success") }}'
        ).render()
        assert "chirpui-ascii-tile-btn--success" in html

    def test_lit(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn %}{{ tile_btn(lit=true) }}'
        ).render()
        assert "chirpui-ascii-tile-btn--lit" in html

    def test_toggle_mode(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn %}'
            '{{ tile_btn(toggle=true, name="pwr") }}'
        ).render()
        assert "<label" in html
        assert 'type="checkbox"' in html

    def test_disabled(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn %}{{ tile_btn(disabled=true) }}'
        ).render()
        assert "disabled" in html
        assert "chirpui-ascii-tile-btn--disabled" in html

    def test_tile_grid(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn, tile_grid %}'
            "{% call tile_grid(cols=3) %}"
            '{{ tile_btn("1") }}{{ tile_btn("2") }}{{ tile_btn("3") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-tile-grid" in html
        assert "--_tile-cols: 3" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tile_btn.html" import tile_btn %}{{ tile_btn(cls="big") }}'
        ).render()
        assert "big" in html


# ---------------------------------------------------------------------------
# ascii_toggle
# ---------------------------------------------------------------------------


class TestAsciiToggle:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_toggle %}'
            '{{ ascii_toggle("dark", label="Dark Mode") }}'
        ).render()
        assert "chirpui-ascii-toggle" in html
        assert 'type="checkbox"' in html
        assert "Dark Mode" in html

    def test_checked(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_toggle %}'
            '{{ ascii_toggle("x", checked=true) }}'
        ).render()
        assert "checked" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_toggle %}'
            '{{ ascii_toggle("x", variant="success") }}'
        ).render()
        assert "chirpui-ascii-toggle--success" in html

    def test_size_sm(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_toggle %}'
            '{{ ascii_toggle("x", size="sm") }}'
        ).render()
        assert "chirpui-ascii-toggle--sm" in html

    def test_disabled(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_toggle %}'
            '{{ ascii_toggle("x", disabled=true) }}'
        ).render()
        assert "disabled" in html
        assert "chirpui-ascii-toggle--disabled" in html

    def test_switch_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_switch %}'
            '{{ ascii_switch("pwr", label="Power", variant="danger") }}'
        ).render()
        assert "chirpui-ascii-switch" in html
        assert "chirpui-ascii-switch--danger" in html
        assert "Power" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_toggle.html" import ascii_toggle %}'
            '{{ ascii_toggle("x", cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_vu_meter
# ---------------------------------------------------------------------------


class TestAsciiVuMeter:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter %}'
            '{{ ascii_vu_meter("cpu", value=65, label="CPU") }}'
        ).render()
        assert "chirpui-ascii-vu" in html
        assert "CPU" in html
        assert "65%" in html
        assert 'role="meter"' in html
        assert 'aria-valuenow="65"' in html
        assert 'aria-label="CPU"' in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter %}'
            '{{ ascii_vu_meter(variant="warning") }}'
        ).render()
        assert "chirpui-ascii-vu--warning" in html

    def test_peak(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter %}'
            "{{ ascii_vu_meter(value=50, peak=true, width=10) }}"
        ).render()
        assert "chirpui-ascii-vu__cell--peak" in html

    def test_animate(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter %}'
            "{{ ascii_vu_meter(animate=true) }}"
        ).render()
        assert "chirpui-ascii-vu--animate" in html

    def test_stack(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter, vu_meter_stack %}'
            '{% call vu_meter_stack(title="Audio") %}'
            '{{ ascii_vu_meter("L", value=72, label="L") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-vu-stack" in html
        assert "Audio" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter %}'
            '{{ ascii_vu_meter(cls="wide") }}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_card (new composite)
# ---------------------------------------------------------------------------


class TestAsciiCard:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            "{% call ascii_card() %}Body{% end %}"
        ).render()
        assert "chirpui-ascii-card" in html
        assert "Body" in html

    def test_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            '{% call ascii_card(title="Status") %}OK{% end %}'
        ).render()
        assert "Status" in html
        assert "chirpui-ascii-card__divider" in html

    def test_no_title_no_divider(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            "{% call ascii_card() %}X{% end %}"
        ).render()
        assert "chirpui-ascii-card__divider" not in html

    def test_variant_double(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            '{% call ascii_card(variant="double") %}X{% end %}'
        ).render()
        assert "chirpui-ascii-card--double" in html

    def test_variant_rounded(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            '{% call ascii_card(variant="rounded") %}X{% end %}'
        ).render()
        assert "chirpui-ascii-card--rounded" in html

    def test_glyph(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            '{% call ascii_card(title="Info", glyph="◆") %}X{% end %}'
        ).render()
        assert "◆" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            '{% call ascii_card(cls="wide") %}X{% end %}'
        ).render()
        assert "wide" in html

    def test_decorative_aria_hidden(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_card.html" import ascii_card %}'
            "{% call ascii_card() %}X{% end %}"
        ).render()
        assert 'aria-hidden="true"' in html


# ---------------------------------------------------------------------------
# ascii_tabs (new composite)
# ---------------------------------------------------------------------------


class TestAsciiTabs:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tabs, ascii_tab %}'
            "{% call ascii_tabs() %}"
            '{{ ascii_tab("ov", "Overview", active=true) }}'
            '{{ ascii_tab("det", "Details") }}'
            "{% end %}"
        ).render()
        assert "chirpui-ascii-tabs" in html
        assert 'role="tablist"' in html

    def test_active_tab(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tab %}'
            '{{ ascii_tab("ov", "Overview", active=true) }}'
        ).render()
        assert "chirpui-ascii-tab--active" in html
        assert 'role="tab"' in html
        assert 'aria-selected="true"' in html
        assert "chirpui-ascii-tab__bracket" in html

    def test_inactive_tab(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tab %}{{ ascii_tab("det", "Details") }}'
        ).render()
        assert "chirpui-ascii-tab--active" not in html
        assert 'aria-selected="false"' in html
        assert "chirpui-ascii-tab__bracket" not in html

    def test_htmx_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tab %}'
            '{{ ascii_tab("ov", "Overview", url="/tabs/ov", hx_target="#panel") }}'
        ).render()
        assert 'hx-boost="false"' in html
        assert 'hx-get="/tabs/ov"' in html
        assert 'hx-target="#panel"' in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tabs %}'
            '{% call ascii_tabs(variant="accent") %}{% end %}'
        ).render()
        assert "chirpui-ascii-tabs--accent" in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tabs %}'
            '{% call ascii_tabs(cls="wide") %}{% end %}'
        ).render()
        assert "wide" in html


# ---------------------------------------------------------------------------
# ascii_modal (new composite)
# ---------------------------------------------------------------------------


class TestAsciiModal:
    def test_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_modal.html" import ascii_modal %}'
            '{% call ascii_modal("dlg", title="Settings") %}Body{% end %}'
        ).render()
        assert "chirpui-ascii-modal" in html
        assert "<dialog" in html
        assert "Settings" in html
        assert "Body" in html

    def test_close_button(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_modal.html" import ascii_modal %}'
            '{% call ascii_modal("dlg", title="X") %}{% end %}'
        ).render()
        assert 'aria-label="Close"' in html

    def test_variant_double(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_modal.html" import ascii_modal %}'
            '{% call ascii_modal("dlg", variant="double") %}X{% end %}'
        ).render()
        assert "chirpui-ascii-modal--double" in html

    def test_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_modal.html" import ascii_modal_trigger %}'
            '{{ ascii_modal_trigger("dlg", label="Open") }}'
        ).render()
        assert "chirpui-ascii-modal-trigger" in html
        assert "Open" in html

    def test_id(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_modal.html" import ascii_modal %}'
            '{% call ascii_modal("my-dialog") %}X{% end %}'
        ).render()
        assert 'id="my-dialog"' in html

    def test_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_modal.html" import ascii_modal %}'
            '{% call ascii_modal("dlg", cls="wide") %}X{% end %}'
        ).render()
        assert "wide" in html
