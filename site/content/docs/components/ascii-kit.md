---
title: ASCII kit
description: Retro ASCII UI primitives and backgrounds
draft: false
weight: 25
lang: en
type: doc
keywords: [chirp-ui, ascii, retro]
icon: terminal
---

# ASCII kit

The ASCII kit is a collection of retro terminal UI primitives -- borders, dividers, tables, toggles, progress bars, VU meters, 7-segment displays, and more. Every component lives under `chirpui/ascii_*.html` (plus `ascii_split_flap.html` and `ascii_breaker_panel.html`).

All ASCII blocks have `VARIANT_REGISTRY` entries. Use `validate_variant_block` when passing dynamic variant strings.

Pair ASCII components with [Effects](./effects.md) (`scanline`, `grain`) for cohesive retro scenes.

---

## Display

Visual readouts and decorative elements that present information.

| Component | Template | Purpose |
|-----------|----------|---------|
| 7-segment display | `ascii_7seg.html` | LCD-style digit readout |
| Badge | `ascii_badge.html` | Inline status badge with optional glyph |
| Icon | `ascii_icon.html` | Single-character icon with optional animation |
| Sparkline | `ascii_sparkline.html` | Inline mini chart from a list of values |
| Split-flap | `ascii_split_flap.html` | Mechanical departure-board style text |
| Ticker | `ascii_ticker.html` | Scrolling stock-ticker text |

### ascii_7seg

```text
{% from "chirpui/ascii_7seg.html" import ascii_7seg %}

ascii_7seg(text, label=none, variant="", cls="")
```

Renders each character as a tall monospace glyph inside a display frame. Supports digits 0--9, colon, period, dash, and space.

```text
{{ ascii_7seg("08:42", label="UPTIME", variant="accent") }}
```

### ascii_badge

```text
{% from "chirpui/ascii_badge.html" import ascii_badge %}

ascii_badge(text="", glyph="", variant="", frame="", cls="")
```

```text
{{ ascii_badge(text="OK", glyph="*", variant="success", frame="round") }}
```

### ascii_icon

```text
{% from "chirpui/ascii_icon.html" import ascii_icon %}

ascii_icon(char, animation="none", size="md", cls="")
```

`animation` accepts `"none"`, `"pulse"`, `"spin"`, or `"blink"`. `size` accepts `"sm"`, `"md"`, `"lg"`.

```text
{{ ascii_icon("*", animation="pulse", size="lg") }}
```

### ascii_sparkline

```text
{% from "chirpui/ascii_sparkline.html" import ascii_sparkline %}

ascii_sparkline(values=[], variant="", cls="")
```

Pass a list of numbers. The macro maps values to vertical bar characters.

```text
{{ ascii_sparkline(values=[1, 4, 2, 8, 5, 3]) }}
```

### split_flap / split_flap_row / split_flap_board

```text
{% from "chirpui/ascii_split_flap.html" import split_flap, split_flap_row, split_flap_board %}

split_flap(text, variant="", animate=true, cls="")
split_flap_row(cells, cls="")
split_flap_board(title=none, variant="", cls="")
```

`split_flap` renders a single word. Compose rows with `split_flap_row` and wrap in a `split_flap_board` for a full departure-board layout.

```text
{% call split_flap_board(title="DEPARTURES") %}
    {{ split_flap_row(cells=["NYC", "08:30", "ON TIME"]) }}
    {{ split_flap_row(cells=["LAX", "09:15", "DELAYED"]) }}
{% endcall %}
```

### ascii_ticker

```text
{% from "chirpui/ascii_ticker.html" import ascii_ticker %}

ascii_ticker(text, variant="", speed="", cls="")
```

`speed` sets the scroll rate via `--chirpui-duration-*` tokens.

```text
{{ ascii_ticker(text="BREAKING: retro UIs are back", speed="slow") }}
```

---

## Controls

Interactive inputs styled with ASCII box-drawing aesthetics.

| Component | Template | Purpose |
|-----------|----------|---------|
| Breaker panel | `ascii_breaker_panel.html` | Group of on/off breaker switches |
| Checkbox | `ascii_checkbox.html` | Single checkbox or checkbox group |
| Fader | `ascii_fader.html` | Vertical slider (mixer channel style) |
| Knob | `ascii_knob.html` | Rotary selector from a list of options |
| Radio | `ascii_radio.html` | Radio button or radio group |
| Tile button | `ascii_tile_btn.html` | Grid of pressable glyph tiles |
| Toggle / switch | `ascii_toggle.html` | Binary on/off toggle |

### breaker_panel / breaker

```text
{% from "chirpui/ascii_breaker_panel.html" import breaker_panel, breaker %}

breaker_panel(title=none, variant="double", size="", master=none, cls="")
breaker(name, label=none, checked=false, variant="", disabled=false)
```

`master` names a breaker that controls all others. Wrap individual `breaker` calls inside a `breaker_panel`.

```text
{% call breaker_panel(title="POWER", master="main") %}
    {{ breaker("main", label="MAIN", checked=true) }}
    {{ breaker("aux", label="AUX") }}
    {{ breaker("backup", label="BACKUP", disabled=true) }}
{% endcall %}
```

### ascii_checkbox / ascii_checkbox_group

```text
{% from "chirpui/ascii_checkbox.html" import ascii_checkbox, ascii_checkbox_group %}

ascii_checkbox(name, label=none, checked=false, variant="", disabled=false, cls="")
ascii_checkbox_group(legend=none, cls="")
```

```text
{% call ascii_checkbox_group(legend="Options") %}
    {{ ascii_checkbox("opt_a", label="Alpha", checked=true) }}
    {{ ascii_checkbox("opt_b", label="Beta") }}
{% endcall %}
```

### ascii_fader / fader_bank

```text
{% from "chirpui/ascii_fader.html" import ascii_fader, fader_bank %}

ascii_fader(name, value=0, label=none, variant="", cls="")
fader_bank(title=none, cls="")
```

`value` is 0--100. Wrap multiple faders in a `fader_bank` for a mixer-channel layout.

```text
{% call fader_bank(title="MIXER") %}
    {{ ascii_fader("ch1", value=75, label="CH 1") }}
    {{ ascii_fader("ch2", value=40, label="CH 2") }}
{% endcall %}
```

### ascii_knob

```text
{% from "chirpui/ascii_knob.html" import ascii_knob %}

ascii_knob(name, options, selected=none, label=none, variant="", cls="")
```

`options` is a list of values. The knob renders a rotary selector that cycles through them.

```text
{{ ascii_knob("freq", options=["LO", "MID", "HI"], selected="MID", label="FREQ") }}
```

### ascii_radio / ascii_radio_group

```text
{% from "chirpui/ascii_radio.html" import ascii_radio, ascii_radio_group %}

ascii_radio(name, value, label=none, checked=false, disabled=false, cls="")
ascii_radio_group(name=none, legend=none, layout="vertical", variant="", cls="")
```

`layout` accepts `"vertical"` or `"horizontal"`.

```text
{% call ascii_radio_group(name="mode", legend="Mode", layout="horizontal") %}
    {{ ascii_radio("mode", "a", label="Alpha", checked=true) }}
    {{ ascii_radio("mode", "b", label="Beta") }}
{% endcall %}
```

### tile_btn / tile_grid

```text
{% from "chirpui/ascii_tile_btn.html" import tile_btn, tile_grid %}

tile_btn(glyph="■", label=none, variant="", lit=false, toggle=false, name=none, disabled=false, cls="")
tile_grid(cols=4, cls="")
```

`lit` sets initial on-state. `toggle` enables click-to-toggle. Wrap buttons in `tile_grid` with `cols` to control column count.

```text
{% call tile_grid(cols=4) %}
    {{ tile_btn(glyph="▶", label="Play", toggle=true, name="play") }}
    {{ tile_btn(glyph="■", label="Stop", name="stop") }}
    {{ tile_btn(glyph="●", label="Rec", variant="error", toggle=true, name="rec") }}
    {{ tile_btn(glyph="⏸", label="Pause", disabled=true) }}
{% endcall %}
```

### ascii_toggle / ascii_switch

```text
{% from "chirpui/ascii_toggle.html" import ascii_toggle, ascii_switch %}

ascii_toggle(name, checked=false, label=none, variant="", size="", disabled=false, cls="")
ascii_switch(name, checked=false, label=none, variant="", size="", disabled=false, cls="")
```

`ascii_switch` is an alias for `ascii_toggle`. Both produce the same output.

```text
{{ ascii_toggle("dark_mode", checked=true, label="Dark mode", size="lg") }}
```

---

## Layout

Structural and decorative elements for building terminal-style page chrome.

| Component | Template | Purpose |
|-----------|----------|---------|
| Border | `ascii_border.html` | Box-drawing frame around slot content |
| Divider | `ascii_divider.html` | Horizontal rule with glyph decoration |
| Table | `ascii_table.html` | Full ASCII-bordered data table |
| Skeleton | `ascii_skeleton.html` | Loading placeholder lines |
| Empty state | `ascii_empty.html` | Centered empty/no-data message |
| Error page | `ascii_error.html` | Full-page error display (404, 500, etc.) |

### ascii_border

```text
{% from "chirpui/ascii_border.html" import ascii_border %}

ascii_border(variant="", glyph="", cls="")
```

Wraps slot content in a box-drawing frame. `variant` controls the line style; `glyph` sets a decorative corner or rule character.

```text
{% call ascii_border(variant="double") %}
    <p>Framed content</p>
{% endcall %}
```

### ascii_divider

```text
{% from "chirpui/ascii_divider.html" import ascii_divider %}

ascii_divider(glyph="", variant="", cls="")
```

```text
{{ ascii_divider(glyph="◆", variant="double") }}
```

### ascii_table / ascii_row

```text
{% from "chirpui/ascii_table.html" import ascii_table, ascii_row %}

ascii_table(headers=none, variant="single", align=none, compact=false, striped=false, sticky_header=false, cls="")
ascii_row(*cells, align=none)
```

`variant` accepts `"single"` or `"double"` for border style. `align` is a list of alignment strings (`"left"`, `"center"`, `"right"`) per column.

```text
{% call ascii_table(headers=["Name", "Status", "Ping"], variant="single", striped=true) %}
    {{ ascii_row("alpha", "UP", "12ms") }}
    {{ ascii_row("beta", "DOWN", "---") }}
{% endcall %}
```

### ascii_skeleton

```text
{% from "chirpui/ascii_skeleton.html" import ascii_skeleton %}

ascii_skeleton(variant="", lines=1, width="", cls="")
```

```text
{{ ascii_skeleton(lines=3, width="80%") }}
```

### ascii_empty

```text
{% from "chirpui/ascii_empty.html" import ascii_empty %}

ascii_empty(glyph="◇", heading="Nothing here", description="", variant="default", cls="")
```

```text
{{ ascii_empty(glyph="☆", heading="No results", description="Try adjusting your filters.") }}
```

### ascii_error

```text
{% from "chirpui/ascii_error.html" import ascii_error %}

ascii_error(code="404", heading="", description="", cls="")
```

```text
{{ ascii_error(code="500", heading="Server Error", description="Something went wrong.") }}
```

---

## Feedback

Meters, indicators, and progress elements that communicate state.

| Component | Template | Purpose |
|-----------|----------|---------|
| Indicator | `ascii_indicator.html` | Status dot with optional blink |
| Progress bar | `ascii_progress.html` | Horizontal fill bar |
| Stepper | `ascii_stepper.html` | Multi-step progress tracker |
| Spinner | `ascii_spinner.html` | Animated loading character |
| VU meter | `ascii_vu_meter.html` | Audio-style level meter |

### indicator / indicator_row

```text
{% from "chirpui/ascii_indicator.html" import indicator, indicator_row %}

indicator(label=none, variant="success", blink=false, glyph="square", cls="")
indicator_row(cls="", nowrap=false)
```

`variant` accepts `"success"`, `"warning"`, `"error"`, `"info"`, etc. `glyph` accepts `"square"`, `"circle"`, `"diamond"`. Wrap indicators in `indicator_row` for horizontal layout; `nowrap=true` prevents wrapping.

```text
{% call indicator_row(nowrap=true) %}
    {{ indicator(label="API", variant="success") }}
    {{ indicator(label="DB", variant="warning", blink=true) }}
    {{ indicator(label="Cache", variant="error") }}
{% endcall %}
```

### ascii_progress

```text
{% from "chirpui/ascii_progress.html" import ascii_progress %}

ascii_progress(value=0, label="", variant="", width=20, cls="")
```

`value` is 0--100. `width` sets the character count of the bar.

```text
{{ ascii_progress(value=65, label="Upload", variant="accent", width=30) }}
```

### ascii_stepper

```text
{% from "chirpui/ascii_stepper.html" import ascii_stepper %}

ascii_stepper(steps, current=0, variant="", cls="")
```

`steps` is a list of step labels. `current` is a zero-based index.

```text
{{ ascii_stepper(steps=["Connect", "Configure", "Deploy"], current=1) }}
```

### ascii_spinner

```text
{% from "chirpui/ascii_spinner.html" import ascii_spinner %}

ascii_spinner(charset="braille", size="md", label="", cls="")
```

`charset` controls the animation characters (`"braille"`, `"line"`, `"dots"`, etc.). `size` accepts `"sm"`, `"md"`, `"lg"`.

```text
{{ ascii_spinner(charset="braille", label="Loading...") }}
```

### ascii_vu_meter / vu_meter_stack

```text
{% from "chirpui/ascii_vu_meter.html" import ascii_vu_meter, vu_meter_stack %}

ascii_vu_meter(name=none, value=0, label=none, variant="", width=20, peak=false, animate=false, cls="")
vu_meter_stack(title=none, cls="")
```

`value` is 0--100. `peak` enables a peak-hold indicator. `animate` enables smooth value transitions. Wrap multiple meters in `vu_meter_stack` for a vertical column layout.

```text
{% call vu_meter_stack(title="LEVELS") %}
    {{ ascii_vu_meter(name="left", value=72, label="L", peak=true) }}
    {{ ascii_vu_meter(name="right", value=58, label="R", peak=true) }}
{% endcall %}
```

---

## Related

- [Typography effects](./typography-effects.md)
- [Effects](./effects.md)
