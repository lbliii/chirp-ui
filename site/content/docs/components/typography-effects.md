---
title: Typography effects
description: gradient_text, glitch_text, neon_text, typewriter, marquee, text_reveal
draft: false
weight: 27
lang: en
type: doc
keywords: [chirp-ui, typography, motion]
icon: text-aa
---

# Typography effects

Hero and marketing typography effects -- gradient fills, glitch distortion, neon glow, typewriter reveals, scrolling marquees, and text entrance animations. Each effect is a single Kida macro that wraps text in a styled element with CSS-driven animation.

All animations use `--chirpui-duration-*` and `--chirpui-easing-*` custom property tokens. Do not use raw `transition` or `animation` durations in templates. See [Motion and transitions](../theming/motion-and-transitions.md) for the full token reference.

---

## Quick reference

| Component | Template | Purpose |
|-----------|----------|---------|
| Glitch text | `glitch_text.html` | RGB-split distortion with pseudo-element layers |
| Gradient text | `gradient_text.html` | CSS gradient fill on text, optionally animated |
| Marquee | `marquee.html` | Continuously scrolling horizontal text or items |
| Neon text | `neon_text.html` | Glowing neon sign effect with color control |
| Text reveal | `text_reveal.html` | Entrance animation (fade, slide, blur, etc.) |
| Typewriter | `typewriter.html` | Character-by-character typing animation |

---

## glitch_text

```text
{% from "chirpui/glitch_text.html" import glitch_text %}

glitch_text(text, variant="", tag="span", cls="")
```

Renders RGB-split distortion text using pseudo-element layers. `variant` controls intensity.

| Param | Default | Notes |
|-------|---------|-------|
| `text` | -- | The text to display |
| `variant` | `""` | `"subtle"` or `"intense"` |
| `tag` | `"span"` | HTML element tag |
| `cls` | `""` | Extra CSS classes |

```text
{{ glitch_text("SYSTEM ERROR") }}
{{ glitch_text("HACK THE PLANET", variant="intense", tag="h1") }}
```

---

## gradient_text

```text
{% from "chirpui/gradient_text.html" import gradient_text %}

gradient_text(text, animated=false, tag="span", cls="")
```

Applies a CSS gradient fill to text via `background-clip: text`. Set `animated=true` to cycle the gradient position.

| Param | Default | Notes |
|-------|---------|-------|
| `text` | -- | The text to display |
| `animated` | `false` | Animate the gradient position |
| `tag` | `"span"` | HTML element tag |
| `cls` | `""` | Extra CSS classes |

```text
{{ gradient_text("Welcome", tag="h1") }}
{{ gradient_text("Shimmering headline", animated=true, tag="h2") }}
```

---

## marquee

```text
{% from "chirpui/marquee.html" import marquee %}

marquee(items=none, speed="", reverse=false, pause_on_hover=true, cls="")
```

Continuously scrolling horizontal content. Pass a list of strings or HTML fragments via `items`, or use the slot for custom markup.

| Param | Default | Notes |
|-------|---------|-------|
| `items` | `none` | List of text strings to scroll |
| `speed` | `""` | Maps to `--chirpui-duration-*` tokens (`"slow"`, `"fast"`) |
| `reverse` | `false` | Scroll right-to-left when false, left-to-right when true |
| `pause_on_hover` | `true` | Pause animation on hover |
| `cls` | `""` | Extra CSS classes |

```text
{{ marquee(items=["Breaking news", "Weather update", "Sports scores"], speed="slow") }}
```

```text
{% call marquee(pause_on_hover=true) %}
    <span>Custom HTML content</span>
{% endcall %}
```

---

## neon_text

```text
{% from "chirpui/neon_text.html" import neon_text %}

neon_text(text, color="cyan", animation="", tag="span", cls="")
```

Renders text with a multi-layered glow effect. `color` sets the hue; `animation` adds optional flicker or pulse.

| Param | Default | Notes |
|-------|---------|-------|
| `text` | -- | The text to display |
| `color` | `"cyan"` | Glow color name (e.g. `"cyan"`, `"pink"`, `"green"`) |
| `animation` | `""` | `"flicker"`, `"pulse"`, or `""` for static |
| `tag` | `"span"` | HTML element tag |
| `cls` | `""` | Extra CSS classes |

```text
{{ neon_text("OPEN", color="pink", tag="h1") }}
{{ neon_text("LIVE", color="green", animation="pulse") }}
```

---

## text_reveal

```text
{% from "chirpui/text_reveal.html" import text_reveal %}

text_reveal(text, variant="", tag="span", cls="")
```

Entrance animation that reveals text on load or when scrolled into view. `variant` controls the reveal style.

| Param | Default | Notes |
|-------|---------|-------|
| `text` | -- | The text to display |
| `variant` | `""` | Reveal style (e.g. `"fade"`, `"slide"`, `"blur"`) |
| `tag` | `"span"` | HTML element tag |
| `cls` | `""` | Extra CSS classes |

```text
{{ text_reveal("Hello world", variant="fade", tag="h2") }}
{{ text_reveal("Sliding in", variant="slide") }}
```

---

## typewriter

```text
{% from "chirpui/typewriter.html" import typewriter %}

typewriter(text, speed="", cursor=true, delay="", tag="span", cls="")
```

Character-by-character typing animation. `speed` and `delay` map to `--chirpui-duration-*` tokens.

| Param | Default | Notes |
|-------|---------|-------|
| `text` | -- | The text to type out |
| `speed` | `""` | Typing speed token (`"slow"`, `"fast"`) |
| `cursor` | `true` | Show a blinking cursor |
| `delay` | `""` | Delay before typing starts |
| `tag` | `"span"` | HTML element tag |
| `cls` | `""` | Extra CSS classes |

```text
{{ typewriter("Initializing system...", speed="fast") }}
{{ typewriter("Welcome back.", cursor=true, delay="slow", tag="p") }}
```

---

## Motion tokens

All duration and easing values in these components are driven by CSS custom properties, not hard-coded values:

- `--chirpui-duration-fast`, `--chirpui-duration-default`, `--chirpui-duration-slow`
- `--chirpui-easing-default`, `--chirpui-easing-bounce`, `--chirpui-easing-elastic`

Override these tokens in your theme to control animation speed globally. The `test_transition_tokens.py` test enforces that no raw duration or easing values appear in templates.

---

## Related

- [ASCII kit](./ascii-kit.md)
- [Effects](./effects.md)
- [Motion and transitions](../theming/motion-and-transitions.md)
