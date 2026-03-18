# Modern CSS Backgrounds & Effects — chirp-ui Design System Proposal

**Status:** Proposal  
**Date:** 2026-03-04  
**Scope:** Gradients, gradient borders, mesh gradients, parallax, glassmorphism, and related effects for cards, containers, sections, topbars, sidebars.

---

## 1. Modern CSS Techniques (2024–2026)

### 1.1 Gradients

| Type | Use Case | Example |
|------|----------|---------|
| **Linear** | Backgrounds, progress bars, overlays | `linear-gradient(135deg, a 0%, b 100%)` |
| **Radial** | Spotlight, glowing orbs | `radial-gradient(circle at 30% 20%, a, b)` |
| **Conic** | Pie charts, color wheels, rainbow borders | `conic-gradient(from 0deg, red, gold, green)` |

**Hard stops** — Same color at adjacent stops = no blend, sharp edge:

```css
linear-gradient(to right, red 0%, red 50%, blue 50%, blue 100%)
```

**Animated gradients** — `background-size: 400% 400%` + `@keyframes` for fluid motion (no JS).

---

### 1.2 Gradient Borders

| Method | Pros | Cons |
|--------|------|------|
| **border-image** | Native, simple | Incompatible with `border-radius` |
| **background-clip** | Works with radius | Needs `background-origin: padding-box, border-box` |
| **Pseudo-element** | Full control, radius OK | Extra layer, z-index care |
| **clip-path** | Modern, clean | `clip-path: inset(0 round 5px)` with gradient bg |

**Recommended for chirp-ui:** `background-clip` + dual backgrounds (Alex Overbeck pattern):

```css
.gradient-border {
  background: linear-gradient(var(--chirpui-surface), var(--chirpui-surface)),
              linear-gradient(to right, var(--chirpui-accent), var(--chirpui-accent-secondary));
  background-origin: padding-box, border-box;
  background-repeat: no-repeat;
  border: 2px solid transparent;
  border-radius: var(--chirpui-radius);
}
```

---

### 1.3 Mesh Gradients (2D Gradients)

**Status:** No native CSS support. Workarounds:

1. **Overlay radial gradients** — Multiple `radial-gradient` layers with blur to simulate mesh
2. **Pre-made images** — Export from Figma/Illustrator, use as `background-image`
3. **Future:** `freeform-gradient()` in CSSWG proposal ([w3c/csswg-drafts#7648](https://github.com/w3c/csswg-drafts/issues/7648))

**BBC-style ambient** (Josh Tumath):

```css
/* Simulated mesh: overlay blurred radial gradients */
.mesh-ambient {
  background:
    radial-gradient(ellipse 80% 50% at 20% 40%, oklch(0.6 0.15 250 / 0.4), transparent),
    radial-gradient(ellipse 60% 80% at 80% 20%, oklch(0.7 0.12 180 / 0.3), transparent),
    var(--chirpui-bg);
}
```

---

### 1.4 Glassmorphism / Frosted Glass

**chirp-ui already has:** `surface--glass`, `surface--frosted`, `surface--smoke` with `backdrop-filter: blur()`.

**Enhancement (Josh Comeau):** Use translucent (not transparent) backgrounds on layered elements so blur builds up realistically. `backdrop-filter` is baseline-compatible as of 2024.

---

### 1.5 Parallax & Scroll-Driven Animations

**Native CSS (Chrome 115+):**

- `animation-timeline: scroll()` or `view()`
- `scroll-timeline`, `view-timeline`
- Animations progress with scroll, not time

**Performant parallax (Chrome for Developers):**

- `perspective` on container + `translateZ()` / `scale()` on children
- GPU-accelerated; avoid `background-position` (repaints)

**Traditional:** `background-attachment: fixed` (limited support, can cause jank).

---

### 1.6 Mask-Based Borders

CSS `mask` + gradients for zig-zag, wavy, or custom edge shapes. Hard stops define boundaries.

---

## 2. chirp-ui Current State

| Component | Background/Style | Notes |
|-----------|------------------|-------|
| **surface** | default, muted, elevated, accent, glass, frosted, smoke | Glass/frosted use backdrop-filter |
| **hero** | solid, muted, gradient | Gradient = accent tint 135deg |
| **card** | `--chirpui-surface`, solid border | `card--glass` exists |
| **section** | Uses surface; `surface_variant` | Same as surface |
| **app_shell topbar** | `--chirpui-surface`, solid border | Sticky, z-50 |
| **app_shell sidebar** | Inherits; `border-right` | No glass/gradient |
| **overlay** | dark, gradient-bottom, gradient-top | For text-on-image |
| **navbar** | Solid | Sticky variant |

**Existing tokens:** `--chirpui-overlay-gradient-*`, `--chirpui-glass-*`, `--chirpui-frosted-*`, `--chirpui-smoke-*`.

---

## 3. Proposed Additions

### 3.1 New Design Tokens

```css
/* Gradient presets — theme-overridable */
--chirpui-gradient-subtle: linear-gradient(
  135deg,
  var(--chirpui-bg-subtle) 0%,
  color-mix(in oklch, var(--chirpui-accent) 6%, var(--chirpui-bg)) 100%
);
--chirpui-gradient-accent: linear-gradient(
  135deg,
  color-mix(in oklch, var(--chirpui-accent) 15%, white) 0%,
  color-mix(in oklch, var(--chirpui-accent) 8%, var(--chirpui-bg)) 100%
);
--chirpui-gradient-mesh: /* simulated mesh via radial overlays */;
--chirpui-gradient-border: linear-gradient(
  to right,
  var(--chirpui-accent),
  var(--chirpui-accent-secondary),
  var(--chirpui-accent)
);

/* Hard-stop gradient (e.g. 50/50 split) */
--chirpui-gradient-split: linear-gradient(
  to right,
  var(--chirpui-surface) 0%,
  var(--chirpui-surface) 50%,
  var(--chirpui-bg-subtle) 50%,
  var(--chirpui-bg-subtle) 100%
);
```

### 3.2 Surface Variants (extend)

| New Variant | Description |
|-------------|-------------|
| `gradient-subtle` | Uses `--chirpui-gradient-subtle` |
| `gradient-accent` | Uses `--chirpui-gradient-accent` |
| `gradient-mesh` | Simulated mesh (radial overlays) |
| `gradient-border` | Solid fill + gradient border via background-clip |

### 3.3 Card Variants (extend)

| New Variant | Description |
|-------------|-------------|
| `card--gradient-border` | Gradient border, rounded (background-clip) |
| `card--gradient-header` | Gradient in header strip only |

### 3.4 Section / Blade

**Sections exist** (`section`, `section_header`, `section_collapsible`). "Blade" = full-width section with distinct background. Propose:

- `blade` macro or `section(full_width=true, surface_variant="gradient-subtle")` for hero-like full-width blocks
- Optional `parallax` modifier for scroll-driven subtle motion (opt-in, `@supports`)

### 3.5 App Shell Modifiers

| Modifier | Topbar | Sidebar |
|----------|--------|---------|
| `topbar_variant="glass"` | backdrop-filter, translucent | — |
| `topbar_variant="gradient"` | Subtle gradient bg | — |
| `sidebar_variant="glass"` | — | backdrop-filter |
| `sidebar_variant="muted"` | — | `--chirpui-bg-subtle` |

Add `topbar_variant` and `sidebar_variant` params to `app_shell()`.

### 3.6 Hero Extensions

- `hero--mesh` — Mesh-style ambient background
- `hero--animated-gradient` — Optional animated gradient (prefers-reduced-motion: respect)

---

## 4. Implementation Phases

### Phase 1 — Tokens & Surface (low risk)

1. Add gradient tokens to `:root`
2. Add `gradient-subtle`, `gradient-accent` to surface variants
3. Document in COMPONENT-OPTIONS.md

### Phase 2 — Cards & Borders

1. Add `card--gradient-border` using background-clip pattern
2. Add `gradient-border` surface variant
3. Ensure fallback for older browsers (solid border)

### Phase 3 — App Shell & Blade

1. Add `topbar_variant`, `sidebar_variant` to app_shell
2. Implement glass/gradient for topbar and sidebar
3. Add `blade` or extend section for full-width gradient sections

### Phase 4 — Advanced (opt-in)

1. Mesh gradient surface variant (radial overlay simulation)
2. Parallax section modifier with `@supports (animation-timeline: scroll())`
3. Animated gradient hero with `prefers-reduced-motion` check

---

## 5. Browser Support Notes

| Feature | Support |
|---------|---------|
| `backdrop-filter` | Baseline (2024) |
| `color-mix`, `oklch` | Modern; fallbacks in place |
| `animation-timeline: scroll()` | Chrome 115+, limited elsewhere |
| `background-clip` + dual bg | Wide |
| `border-image` | Wide (no radius) |

Use `@supports` for progressive enhancement. Glass falls back to solid when `backdrop-filter` unavailable (already done).

---

## 6. References

- [CSS Gradients Complete Guide 2026](https://devtoolbox.dedyn.io/blog/css-gradients-complete-guide)
- [Gradient Borders in CSS](https://css-tricks.com/gradient-borders-in-css/) — background-clip, border-image, pseudo-element
- [Mesh Gradients in CSS](https://www.joshtumath.uk/posts/2024-06-11-mesh-gradients-in-css/) — BBC ambients, freeform-gradient proposal
- [Scroll-Driven Animations](https://codelabs.developers.google.com/scroll-driven-animations)
- [Performant Parallaxing](https://developer.chrome.com/blog/performant-parallaxing)
- [Next-level frosted glass](https://www.joshwcomeau.com/css/backdrop-filter/)
