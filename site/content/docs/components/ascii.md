---
title: ASCII Primitives
description: Terminal-aesthetic UI components using Unicode box-drawing characters
draft: false
weight: 30
lang: en
type: doc
keywords: [chirp-ui, ascii, terminal, retro, box-drawing, unicode]
category: components
---

# ASCII Primitives

27 pure-CSS components that render UI using Unicode box-drawing characters, braille patterns, and block elements. No JavaScript required (interactive controls use native HTML inputs).

## Design philosophy

- **Monospace-native** — all components use `font-family: monospace` and box-drawing characters for frames
- **No JavaScript** — interactive controls (toggle, checkbox, radio, knob, fader) use real `<input>` elements with CSS-only visual treatment
- **Accessible** — native form elements provide keyboard support; decorative characters use `aria-hidden="true"`; semantic roles on progress, spinner, table, and meter components

## Component reference

### Composites

| Component | Import | Description |
|-----------|--------|-------------|
| `ascii_card` | `chirpui/ascii_card.html` | Box-drawn card with optional title bar and glyph |
| `ascii_tabs` | `chirpui/ascii_tabs.html` | Tab bar with bracket indicators, htmx-compatible |
| `ascii_modal` | `chirpui/ascii_modal.html` | Native `<dialog>` with monospace styling |

### Display

| Component | Import | Description |
|-----------|--------|-------------|
| `ascii_7seg` | `chirpui/ascii_7seg.html` | LCD-style digit readout |
| `ascii_badge` | `chirpui/ascii_badge.html` | Inline label with pipe/bracket/angle frames |
| `ascii_border` | `chirpui/ascii_border.html` | Box-drawing frame around content |
| `ascii_divider` | `chirpui/ascii_divider.html` | Horizontal rule with optional glyph |
| `ascii_empty` | `chirpui/ascii_empty.html` | Empty state with glyph and heading |
| `ascii_error` | `chirpui/ascii_error.html` | Stylized error pages (404, 403, 500, 503, timeout) |
| `ascii_icon` | `chirpui/ascii_icon.html` | Animated Unicode symbol (blink, pulse, rotate) |
| `ascii_indicator` | `chirpui/ascii_indicator.html` | LED-style status light with blink |
| `ascii_progress` | `chirpui/ascii_progress.html` | Progress bar with block characters |
| `ascii_skeleton` | `chirpui/ascii_skeleton.html` | Loading placeholder with cycling braille |
| `ascii_sparkline` | `chirpui/ascii_sparkline.html` | Inline data visualization |
| `ascii_spinner` | `chirpui/ascii_spinner.html` | Character-cycling loading spinner |
| `ascii_split_flap` | `chirpui/ascii_split_flap.html` | Departure-board style display |
| `ascii_stepper` | `chirpui/ascii_stepper.html` | Pipeline progress indicator |
| `ascii_table` | `chirpui/ascii_table.html` | Table with box-drawing borders |
| `ascii_ticker` | `chirpui/ascii_ticker.html` | Scrolling text banner |

### Controls

| Component | Import | Description |
|-----------|--------|-------------|
| `ascii_checkbox` | `chirpui/ascii_checkbox.html` | Checkbox with Unicode ballot characters |
| `ascii_fader` | `chirpui/ascii_fader.html` | Vertical mixing-board fader (range input) |
| `ascii_knob` | `chirpui/ascii_knob.html` | Rotary dial selector (radio group) |
| `ascii_radio` | `chirpui/ascii_radio.html` | Radio buttons with circle characters |
| `ascii_toggle` | `chirpui/ascii_toggle.html` | Horizontal switch + vertical breaker (`ascii_switch`) |
| `ascii_tile_btn` | `chirpui/ascii_tile_btn.html` | Mainframe pushbutton, toggle or momentary |
| `ascii_breaker_panel` | `chirpui/ascii_breaker_panel.html` | Framed panel of breaker switches |

### Data

| Component | Import | Description |
|-----------|--------|-------------|
| `ascii_vu_meter` | `chirpui/ascii_vu_meter.html` | Horizontal bouncing level meter |

## Usage

```html
{% from "chirpui/ascii_card.html" import ascii_card %}
{% from "chirpui/ascii_fader.html" import ascii_fader, fader_bank %}
{% from "chirpui/ascii_indicator.html" import indicator, indicator_row %}

{# Box-drawn card #}
{% call ascii_card(title="System Status", variant="rounded", glyph="◆") %}
    <p>All services operational.</p>
{% end %}

{# Mixing board faders #}
{% call fader_bank(title="Audio Mix") %}
    {{ ascii_fader("ch1", value=80, label="CH1") }}
    {{ ascii_fader("ch2", value=60, label="CH2", variant="accent") }}
{% end %}

{# Status indicator row #}
{% call indicator_row() %}
    {{ indicator("API", variant="success", blink=true) }}
    {{ indicator("DB", variant="success") }}
    {{ indicator("Cache", variant="error", blink="fast") }}
{% end %}
```

## Variants

Most ASCII components accept a `variant` parameter. Common variants:

| Variant | Components | Visual |
|---------|-----------|--------|
| `single` | border, card, table | `┌─┐ │ └─┘` |
| `double` | border, card, table, modal | `╔═╗ ║ ╚═╝` |
| `rounded` | border, card, table | `╭─╮ │ ╰─╯` |
| `heavy` | border, card, table, modal | `┏━┓ ┃ ┗━┛` |
| `accent` | knob, fader, badge, tabs | Themed accent color |
| `success` / `warning` / `error` | badge, fader, indicator, toggle | Semantic colors |

## Keyboard interaction

Interactive ASCII controls use native HTML form elements:

| Control | Element | Keyboard |
|---------|---------|----------|
| `ascii_toggle` | `<input type="checkbox">` | Space to toggle |
| `ascii_checkbox` | `<input type="checkbox">` | Space to toggle |
| `ascii_radio` | `<input type="radio">` | Arrow keys to cycle |
| `ascii_knob` | `<input type="radio">` (group) | Arrow keys to select |
| `ascii_fader` | `<input type="range">` | Arrow keys to adjust |
| `ascii_tile_btn` | `<button>` or `<input type="checkbox">` | Enter/Space to activate |
