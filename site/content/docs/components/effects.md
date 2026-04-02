---
title: Effects
description: Aurora, grain, particles, orbit, sparkle, confetti, and backgrounds
draft: false
weight: 26
lang: en
type: doc
keywords: [chirp-ui, effects, background]
icon: sparkle
---

# Effects

Decorative backgrounds, ambient motion, and micro-interaction animations. All effects are CSS-driven (a few use Alpine.js for triggers). They respect `prefers-reduced-motion` via `--chirpui-duration-*` / `--chirpui-easing-*` tokens.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `aurora.html` | `aurora` | Drifting gradient blobs |
| `border_beam.html` | `border_beam` | Animated conic-gradient border |
| `confetti.html` | `confetti`, `confetti_trigger` | Celebration burst (Alpine event) |
| `constellation.html` | `constellation` | Twinkling ASCII starfield |
| `grain.html` | `grain` | Film grain overlay (SVG noise) |
| `holy_light.html` | `holy_light` | Ascending sparkles with parallax |
| `meteor.html` | `meteor` | Diagonal streak animation |
| `orbit.html` | `orbit` | Items rotating around a center |
| `particle_bg.html` | `particle_bg` | Floating dot particles |
| `reveal_on_scroll.html` | `reveal_on_scroll` | Fade-in on viewport entry |
| `scanline.html` | `scanline` | CRT/retro line overlay |
| `sparkle.html` | `sparkle` | Staggered star twinkle |
| `symbol_rain.html` | `symbol_rain` | Matrix-style cascading characters |
| `wobble.html` | `wobble`, `jello`, `rubber_band`, `bounce_in` | Micro-interaction animations |
| `hero_effects.html` | `hero_effects` | Hero section wrapper with effect selection |

## aurora

Drifting gradient blobs behind content. Pure CSS.

```text
{% from "chirpui/aurora.html" import aurora %}

{% call aurora(variant="intense") %}
  <h1>Welcome</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | `str` | `""` | `"intense"` or `"subtle"` |
| `cls` | `str` | `""` | Extra CSS classes |

## border_beam

Container with animated conic-gradient border beam effect.

```text
{% from "chirpui/border_beam.html" import border_beam %}

{% call border_beam(variant="accent") %}
  <p>Content with glowing border</p>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | `str` | `""` | `"default"`, `"accent"`, `"success"`, `"warning"` |
| `cls` | `str` | `""` | Extra CSS classes |
| `attrs` | `str` | `""` | Extra HTML attributes |
| `attrs_map` | `dict` | `none` | Extra HTML attributes map |

## confetti / confetti_trigger

Alpine-triggered celebration burst. Dispatch a window event to activate.

```text
{% from "chirpui/confetti.html" import confetti, confetti_trigger %}

{{ confetti(count=40, event="celebrate") }}
{{ confetti_trigger("Celebrate!", event="celebrate") }}
```

### confetti params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | `int` | `40` | Number of confetti pieces |
| `event` | `str` | `"confetti"` | Alpine event name to listen for |
| `cls` | `str` | `""` | Extra CSS classes |

### confetti_trigger params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `label` | `str` | required | Button text |
| `event` | `str` | `"confetti"` | Alpine event to dispatch |
| `tag` | `str` | `"button"` | HTML element tag |
| `cls` | `str` | `""` | Extra CSS classes |

Confetti auto-hides after 3.5 seconds.

## constellation

Twinkling ASCII starfield with gentle drift. Pure CSS.

```text
{% from "chirpui/constellation.html" import constellation %}

{% call constellation(variant="warm", density="dense") %}
  <h1>Starfield hero</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `density` | `str` | `""` | `"sparse"` (6 stars), default (10), `"dense"` (16) |
| `variant` | `str` | `""` | `"warm"`, `"cool"`, `"mono"` |
| `cls` | `str` | `""` | Extra CSS classes |

## grain

Film grain texture overlay via SVG noise filter. Pure CSS.

```text
{% from "chirpui/grain.html" import grain %}

{% call grain(variant="heavy", animated=true) %}
  <div>Film-like background</div>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | `str` | `""` | `"heavy"` or `"subtle"` |
| `animated` | `bool` | `false` | Animate the grain texture |
| `cls` | `str` | `""` | Extra CSS classes |

## holy_light

Ascending sparkles with parallax depth layers and golden glow. Pure CSS.

```text
{% from "chirpui/holy_light.html" import holy_light %}

{% call holy_light(variant="silver", intensity="intense") %}
  <h1>Radiant hero</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `intensity` | `str` | `""` | `"subtle"` or `"intense"` |
| `variant` | `str` | `""` | `"gold"`, `"silver"`, `"holy"` |
| `cls` | `str` | `""` | Extra CSS classes |

Renders three parallax layers (far, mid, near) with ascending mote glyphs.

## meteor

Diagonal streak animation for hero backgrounds.

```text
{% from "chirpui/meteor.html" import meteor %}

{% call meteor(count=6, variant="accent") %}
  <h1>Launch Day</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | `int` | `4` | Number of streaks |
| `variant` | `str` | `""` | `"accent"` or `"muted"` |
| `cls` | `str` | `""` | Extra CSS classes |

## orbit

Items rotating around a center element. Pure CSS.

```text
{% from "chirpui/orbit.html" import orbit %}

{% call orbit(items=["A", "B", "C", "D"], size="sm", speed="fast") %}
  <strong>Center</strong>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `items` | `list` | `[]` | Items to orbit (text, emoji, etc.) |
| `size` | `str` | `""` | `"sm"`, `"lg"`, `"xl"` |
| `speed` | `str` | `""` | `"fast"` or `"slow"` |
| `reverse` | `bool` | `false` | Reverse rotation direction |
| `cls` | `str` | `""` | Extra CSS classes |

The default slot fills the center element.

## particle_bg

Floating dot particles behind content. Pure CSS.

```text
{% from "chirpui/particle_bg.html" import particle_bg %}

{% call particle_bg(count=12, variant="accent") %}
  <h1>Hero with particles</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | `int` | `8` | Number of particles |
| `variant` | `str` | `""` | `"accent"` or `"muted"` |
| `cls` | `str` | `""` | Extra CSS classes |

## reveal_on_scroll

Fade-in animation when content enters the viewport. Uses Alpine Intersect plugin.

```text
{% from "chirpui/reveal_on_scroll.html" import reveal_on_scroll %}

{% call reveal_on_scroll() %}
  <p>This content fades in when scrolled into view.</p>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cls` | `str` | `""` | Extra CSS classes |

Runs once per element (`.once` modifier). Requires the Alpine Intersect plugin.

## scanline

CRT/retro repeating-gradient line overlay. Pure CSS.

```text
{% from "chirpui/scanline.html" import scanline %}

{% call scanline(variant="crt") %}
  <div>Retro terminal text</div>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | `str` | `""` | `"heavy"` or `"crt"` |
| `cls` | `str` | `""` | Extra CSS classes |

## sparkle

Staggered star twinkle effect wrapping content.

```text
{% from "chirpui/sparkle.html" import sparkle %}

{% call sparkle(variant="gold", count=4) %}
  <h2>Golden text</h2>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | `int` | `6` | Number of sparkle stars |
| `variant` | `str` | `""` | `"gold"`, `"white"`, `"rainbow"` |
| `cls` | `str` | `""` | Extra CSS classes |

## symbol_rain

Matrix-style cascading ASCII characters. Pure CSS.

```text
{% from "chirpui/symbol_rain.html" import symbol_rain %}

{% call symbol_rain(variant="gold", count=8) %}
  <h1>Hero with falling symbols</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `count` | `int` | `6` | Number of falling columns |
| `variant` | `str` | `""` | `"accent"`, `"gold"`, `"muted"` |
| `cls` | `str` | `""` | Extra CSS classes |

## wobble / jello / rubber_band / bounce_in

Micro-interaction animation wrappers. Apply on hover, click, or one-shot on load.

```text
{% from "chirpui/wobble.html" import wobble, jello, rubber_band, bounce_in %}

{% call wobble(trigger="hover") %}
  <button>Hover me</button>
{% end %}

{% call jello() %}
  <div>Jello on load</div>
{% end %}

{% call rubber_band(trigger="hover") %}
  <span>Stretch!</span>
{% end %}

{% call bounce_in() %}
  <div class="chirpui-card">Appears with bounce</div>
{% end %}
```

| Macro | Params | Description |
|-------|--------|-------------|
| `wobble` | `trigger="load"`, `cls=""` | Side-to-side wobble |
| `jello` | `trigger="load"`, `cls=""` | Jello squish |
| `rubber_band` | `trigger="load"`, `cls=""` | Elastic stretch |
| `bounce_in` | `cls=""` | Bounce entrance (load only) |

`trigger` accepts `"load"` (plays on render) or `"hover"` (plays on `:hover`).

## hero_effects

Wrapper that delegates to the appropriate background effect based on the `effect` parameter. Simplifies hero sections.

```text
{% from "chirpui/hero_effects.html" import hero_effects %}

{% call hero_effects(effect="particles", variant="accent") %}
  <h1>Welcome</h1>
  <p>Tagline with floating particles behind</p>
{% end %}

{% call hero_effects(effect="meteors") %}
  <h1>Launch Day</h1>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `effect` | `str` | `"particles"` | Effect type: `"particles"`, `"meteors"`, `"spotlight"`, `"symbol-rain"`, `"holy-light"`, `"runes"`, `"constellation"` |
| `variant` | `str` | `""` | Passed to the chosen effect |
| `cls` | `str` | `""` | Extra CSS classes |

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-aurora` | Aurora wrapper |
| `chirpui-aurora--intense/subtle` | Aurora variant |
| `chirpui-border-beam` | Border beam wrapper |
| `chirpui-confetti` | Confetti container |
| `chirpui-constellation` | Constellation wrapper |
| `chirpui-constellation--warm/cool/mono` | Color variant |
| `chirpui-constellation--sparse/dense` | Density |
| `chirpui-grain` | Grain overlay |
| `chirpui-grain--heavy/subtle` | Grain intensity |
| `chirpui-grain--animated` | Animated grain |
| `chirpui-holy-light` | Holy light wrapper |
| `chirpui-meteor` | Meteor wrapper |
| `chirpui-orbit` | Orbit wrapper |
| `chirpui-orbit--sm/lg/xl` | Orbit size |
| `chirpui-orbit--fast/slow` | Orbit speed |
| `chirpui-orbit--reverse` | Reverse direction |
| `chirpui-particle-bg` | Particle background |
| `chirpui-reveal-on-scroll` | Reveal wrapper |
| `chirpui-scanline` | Scanline overlay |
| `chirpui-scanline--heavy/crt` | Scanline variant |
| `chirpui-sparkle` | Sparkle wrapper |
| `chirpui-sparkle--gold/white/rainbow` | Sparkle color |
| `chirpui-symbol-rain` | Symbol rain wrapper |
| `chirpui-wobble` | Wobble on load |
| `chirpui-hover-wobble` | Wobble on hover |
| `chirpui-jello` | Jello on load |
| `chirpui-hover-jello` | Jello on hover |
| `chirpui-rubber-band` | Rubber band on load |
| `chirpui-hover-rubber` | Rubber band on hover |
| `chirpui-bounce-in` | Bounce entrance |
| `chirpui-hero-effects` | Hero effects wrapper |

## Performance

Prefer CSS-driven effects. All animations use `--chirpui-duration-*` / `--chirpui-easing-*` tokens and respect `prefers-reduced-motion`. See [Motion and transitions](../theming/motion-and-transitions.md).

## Related

- [Theming](../theming/design-tokens.md)
