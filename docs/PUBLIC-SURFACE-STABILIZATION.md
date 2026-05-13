# Public Surface Stabilization

Status: active practice
Date: 2026-05-12

This document records pre-1.0 maturity decisions for public Chirp UI
components. The goal is to make promotion decisions evidence-backed: registry
metadata, render tests, browser or visual audit coverage, and docs should agree.

## Decision States

| State | Meaning |
| --- | --- |
| Promote to stable | The component is safe to teach as normal public vocabulary. |
| Keep experimental | Public and usable, but still settling before 1.0. |
| Recipe-only | Keep as a documented composition until repeated app usage proves a macro. |
| Deprecate later | Retain compatibility now, but do not teach for new app code. |

## Current Slice

The visual audit page now includes proof/marketing patterns next to tokens,
navigation, overlays, and forms. That gives enough evidence to promote the
small proof-pattern set that already had render coverage and browser pattern
usage.

| Component | Decision | Evidence |
| --- | --- | --- |
| `logo-cloud` | Promote to stable | Render tests, product/media recipe usage, token hooks, visual audit coverage. |
| `story-card` | Promote to stable | Render tests for link/slot modes, product recipe usage, visual audit coverage. |
| `cta-band` | Promote to stable | Render tests for standard/slot actions, product/media recipe usage, visual audit coverage. |
| `ascii-badge` | Promote to stable | Render proof covers variants and hidden decorative glyphs; visual audit/browser proof covers the static root. |
| `ascii-border` | Promote to stable | Render proof covers variants and hidden decorative frame glyphs; visual audit/browser proof covers the static root. |
| `ascii-divider` | Promote to stable | Render proof covers separator role, labelled glyph mode, and hidden decorative glyphs; visual audit/browser proof covers the static root. |
| `ascii-empty` | Promote to stable | Render proof covers readable heading/description/action and hidden decorative glyphs; visual audit/browser proof covers the static root. |
| `ascii-progress` | Keep experimental | Render and browser proof now align bounded ARIA, visual fill, and displayed value; visual audit/promotion review remains. |
| `ascii-table` | Keep experimental | Render and browser proof now cover table naming, row cells, headers, and hidden decorative borders; responsive visual audit remains. |
| `ascii-toggle` | Keep experimental | Render and browser proof now cover switch role, keyboard toggling, disabled state, and dense-row focus. |
| `ascii-vu` | Keep experimental | Render and browser proof now align bounded meter value, readout, filled cells, peak marker, and reduced-motion behavior. |
| `split-flap` | Keep experimental | Render and browser proof now expose readable text while hiding animated character boxes and stopping animation under reduced motion. |

## Promotion Rule

Promote a component only when all of these are true:

- the descriptor has explicit `maturity`, `role`, `category`, and `authoring`
  projection through the manifest,
- render tests cover its default and at least one meaningful non-default mode,
- it appears in the visual audit page or an equivalent browser-tested recipe,
- token hooks are documented or intentionally absent,
- no private theme token namespace is required to make it look correct.

## Proof Tracks

Inventory rows use these track labels so follow-up work knows which proof is
missing before a component can change maturity or authoring status.

| Track | Required proof | Collateral |
| --- | --- | --- |
| Motion/effects visual proof | Static showcase coverage plus reduced-motion or browser proof when animation affects interaction. | `examples/design-system-gap-showcase/index.html`, focused render tests, browser tests when computed motion/layout matters. |
| ASCII maturity pass | ARIA, keyboard, disabled/state, reduced-motion, and render coverage appropriate to the ASCII control type. | `PLAN-ascii-maturity.md`, ASCII render tests, browser gauntlet for interactive composites. |
| Marketing pattern proof | Recipe or component examples that prove responsive marketing layout without adding utility vocabulary. | Product/site pattern docs, visual audit coverage, manifest/docs maturity agreement. |
| Layout recipe proof | Existing primitives cannot express the layout cleanly, or the item remains recipe-only. | Dense/layout docs, showcase recipe, no preferred authoring unless promoted. |
| Media recipe proof | Media-site pattern usage stays recipe-first until repeated app usage proves a macro. | `MEDIA-SITE-PATTERNS.md`, visual audit/media examples. |
| Social recipe proof | Social/forum patterns stay recipe-first until repeated app usage proves a macro. | `FORUM-SITE-PATTERNS.md`, visual audit/social examples. |
| Form interaction proof | Render tests plus keyboard/focus/browser proof for interactive editing or token-input behavior. | Form/component tests, browser tests when focus or overflow matters. |
| Control interaction proof | State, invalid fallback, ARIA, keyboard, and layout proof for controls. | Focused render tests plus browser proof for pointer/keyboard behavior. |

## Closure Batches

Use these batches to finish the 1.0 public surface matrix without reopening the
whole inventory on every pass.

| Batch | Components | Closure gate |
| --- | --- | --- |
| ASCII/TUI controls | `ascii-*`, `split-flap` | Complete the ASCII maturity gate, then promote only controls with ARIA, keyboard, reduced-motion, render, and browser proof. |
| Marketing patterns | `band`, `feature-section`, `feature-stack`, `site-*`, `lifecycle-showcase` | Prove responsive pattern docs and visual audit coverage; keep recipe-only items as patterns unless repeated app use appears. |
| Motion/effects | `aura`, `aurora`, `border-beam`, `confetti`, `dock`, `glitch`, `glow-card`, `gradient-text`, `grain`, `hero-effects`, `holy-light`, `marquee`, `meteor`, `neon`, `number-ticker`, `orbit`, `particle-bg`, `pulsing-btn`, `reveal-on-scroll`, `ripple-btn`, `rune-field`, `scanline`, `shimmer-btn`, `sparkle`, `spotlight-card`, `symbol-rain`, `text-reveal`, `typewriter`, `wobble` | Separate decorative-only effects from interaction-bearing effects; require reduced-motion and visual/browser proof before promotion. |
| Form and controls | `composer-shell`, `facet-chip`, `token-input` | Require focus, keyboard, invalid-state, overflow, and render proof before changing maturity. |
| Recipe-only patterns | `answer-card`, `catalog-rail`, `detail-header`, `live-event-card`, `media-hero-shelf`, `moderation-queue-item`, `thread-reader-layout`, `title-card`, `topic-card`, `watch-companion-layout` | Stay pattern-role and non-preferred until repeated app usage proves a component API. |

## Next Batches

- Promote only the ASCII/TUI static display subset once visual audit coverage
  and generated docs/manifest projections agree.
- Classify the remaining marketing patterns: feature sections, lifecycle
  showcase, comparison/pricing surfaces, and pattern assets.
- Keep interactive, composite, data/status, and motion ASCII/TUI controls under
  `PLAN-ascii-maturity.md` until accessibility, reduced-motion, and gauntlet
  checks settle.
- Review dense navigation composites only after object-page browser proof lands.
- Keep legacy primitive decisions in `PLAN-primitive-vocabulary-hardening.md`.
- Keep first-party legacy-helper cleanup under
  `PLAN-legacy-helper-cleanup-pre-1.0.md`; current static showcase usage is
  inventoried in `STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md`.

## ASCII Promotion Readiness

The first ASCII/TUI promotion wave is intentionally limited to static display
primitives. They do not add keyboard behavior, mutable state, or animation
contracts, and each already has render proof for default and non-default modes.

| Component | Promotion class | Status |
| --- | --- | --- |
| `ascii-badge` | Static display | Promoted; render, visual audit, browser, manifest, and generated docs evidence agree. |
| `ascii-border` | Static display | Promoted; render, visual audit, browser, manifest, and generated docs evidence agree. |
| `ascii-divider` | Static display | Promoted; render, visual audit, browser, manifest, and generated docs evidence agree. |
| `ascii-empty` | Static display | Promoted; render, visual audit, browser, manifest, and generated docs evidence agree. |
| `ascii-error` | Static display deferred | Keep experimental until error-page usage proves heading/action conventions. |
| Interactive controls | Deferred | Keep experimental until keyboard, focus, disabled-state, and browser proof remain green as a group. |
| Composite/data/status/motion displays | Deferred | Keep experimental until reduced-motion, ARIA, and responsive browser proof are complete for each behavior family. |

## Experimental Disposition Inventory

Every public templated component with `maturity=experimental` needs a named
pre-1.0 disposition. This table is intentionally conservative: it does not
promote a component by existing alone, and it treats pattern-role entries as
recipe-first until repeated app usage proves that a macro should become stable
vocabulary.

| Component | Decision | Track |
| --- | --- | --- |
| `animated-counter` | Keep experimental | Motion/effects visual proof. |
| `answer-card` | Recipe-only | Social recipe proof; promote only after repeated app use. |
| `ascii-7seg` | Keep experimental | ASCII maturity pass. |
| `ascii-breaker-panel` | Keep experimental | ASCII maturity pass. |
| `ascii-card` | Keep experimental | ASCII maturity pass. |
| `ascii-checkbox` | Keep experimental | ASCII maturity pass. |
| `ascii-error` | Keep experimental | ASCII maturity pass. |
| `ascii-fader` | Keep experimental | ASCII maturity pass. |
| `ascii-indicator` | Keep experimental | ASCII maturity pass. |
| `ascii-knob` | Keep experimental | ASCII maturity pass. |
| `ascii-modal` | Keep experimental | ASCII maturity pass. |
| `ascii-progress` | Keep experimental | ASCII maturity pass. |
| `ascii-radio-group` | Keep experimental | ASCII maturity pass. |
| `ascii-skeleton` | Keep experimental | ASCII maturity pass. |
| `ascii-sparkline` | Keep experimental | ASCII maturity pass. |
| `ascii-spinner` | Keep experimental | ASCII maturity pass. |
| `ascii-stepper` | Keep experimental | ASCII maturity pass. |
| `ascii-switch` | Keep experimental | ASCII maturity pass. |
| `ascii-tab` | Keep experimental | ASCII maturity pass. |
| `ascii-table` | Keep experimental | ASCII maturity pass. |
| `ascii-tabs` | Keep experimental | ASCII maturity pass. |
| `ascii-ticker` | Keep experimental | ASCII maturity pass. |
| `ascii-tile-btn` | Keep experimental | ASCII maturity pass. |
| `ascii-toggle` | Keep experimental | ASCII maturity pass. |
| `ascii-vu` | Keep experimental | ASCII maturity pass. |
| `aura` | Keep experimental | Motion/effects visual proof. |
| `aurora` | Keep experimental | Motion/effects visual proof. |
| `band` | Keep experimental | Marketing pattern proof. |
| `border-beam` | Keep experimental | Motion/effects visual proof. |
| `catalog-rail` | Recipe-only | Media recipe proof; promote only after repeated app use. |
| `composer-shell` | Keep experimental | Form interaction proof. |
| `confetti` | Keep experimental | Motion/effects visual proof. |
| `constellation` | Keep experimental | Motion/effects visual proof. |
| `detail-header` | Recipe-only | Layout recipe proof; promote only after repeated app use. |
| `dock` | Keep experimental | Motion/effects visual proof. |
| `facet-chip` | Keep experimental | Control interaction proof. |
| `feature-section` | Keep experimental | Marketing pattern proof. |
| `feature-stack` | Keep experimental | Marketing pattern proof. |
| `glitch` | Keep experimental | Motion/effects visual proof. |
| `glow-card` | Keep experimental | Motion/effects visual proof. |
| `gradient-text` | Keep experimental | Motion/effects visual proof. |
| `grain` | Keep experimental | Motion/effects visual proof. |
| `hero-effects` | Keep experimental | Motion/effects visual proof. |
| `holy-light` | Keep experimental | Motion/effects visual proof. |
| `lifecycle-showcase` | Recipe-only | Marketing pattern proof; promote only after repeated app use. |
| `live-event-card` | Recipe-only | Media recipe proof; promote only after repeated app use. |
| `marquee` | Keep experimental | Motion/effects visual proof. |
| `media-hero-shelf` | Recipe-only | Media recipe proof; promote only after repeated app use. |
| `meteor` | Keep experimental | Motion/effects visual proof. |
| `moderation-queue-item` | Recipe-only | Social recipe proof; promote only after repeated app use. |
| `neon` | Keep experimental | Motion/effects visual proof. |
| `number-ticker` | Keep experimental | Motion/effects visual proof. |
| `orbit` | Keep experimental | Motion/effects visual proof. |
| `particle-bg` | Keep experimental | Motion/effects visual proof. |
| `pulsing-btn` | Keep experimental | Motion/effects visual proof. |
| `reveal-on-scroll` | Keep experimental | Motion/effects visual proof. |
| `ripple-btn` | Keep experimental | Motion/effects visual proof. |
| `rune-field` | Keep experimental | Motion/effects visual proof. |
| `scanline` | Keep experimental | Motion/effects visual proof. |
| `search-header` | Keep experimental | Layout recipe proof. |
| `section-collapsible` | Keep experimental | Layout recipe proof. |
| `shimmer-btn` | Keep experimental | Motion/effects visual proof. |
| `site-footer` | Keep experimental | Marketing pattern proof. |
| `site-header` | Keep experimental | Marketing pattern proof. |
| `site-nav-link` | Keep experimental | Marketing pattern proof. |
| `site-shell` | Keep experimental | Marketing pattern proof. |
| `sparkle` | Keep experimental | Motion/effects visual proof. |
| `split-flap` | Keep experimental | ASCII maturity pass. |
| `spotlight-card` | Keep experimental | Motion/effects visual proof. |
| `symbol-rain` | Keep experimental | Motion/effects visual proof. |
| `text-reveal` | Keep experimental | Motion/effects visual proof. |
| `thread-reader-layout` | Recipe-only | Social recipe proof; promote only after repeated app use. |
| `title-card` | Recipe-only | Media recipe proof; promote only after repeated app use. |
| `token-input` | Keep experimental | Form interaction proof. |
| `topic-card` | Recipe-only | Social recipe proof; promote only after repeated app use. |
| `typewriter` | Keep experimental | Motion/effects visual proof. |
| `watch-companion-layout` | Recipe-only | Media recipe proof; promote only after repeated app use. |
| `wobble` | Keep experimental | Motion/effects visual proof. |

## Legacy Helper Authoring Policy

Legacy helpers remain public compatibility surface before 1.0, but generated
docs and examples should not present them as preferred authoring. The manifest
must continue to project these entries as `authoring=compatibility`, and
`find --authoring preferred` should not include utility-like typography or
spacing helpers.

Initial policy:

- `mt-sm`, `mt-md`, and `mb-md` are deprecate-later candidates.
- `font-*`, `ui-*`, and `text-muted` stay compatibility until first-party page
  chrome is clean and a removal path exists.
- `visually-hidden`, `focus-ring`, and `list-reset` stay narrow
  accessibility/reset helpers.
- `truncate`, `clamp-*`, `scroll-x`, `min-w-0`, and `placeholder-inline` stay
  narrow containment escape hatches.

## 1.0 Helper Decision Gate

No helper removal is approved by this document alone. A helper can be removed at
the 1.0 boundary only when a migration path exists, first-party usage has been
counted, and release notes call out the breaking change.

| Helpers | 1.0 decision | Migration path | Gate |
| --- | --- | --- | --- |
| `mt-sm`, `mt-md`, `mb-md` | Docs-only deprecation now; possible 1.0 removal candidate. | Replace with `stack()`, `flow`, component slots, or local page chrome. | Zero first-party usage outside legacy examples. |
| `font-*`, `ui-*`, `text-muted` | Keep compatibility through 1.0 unless a separate removal RFC lands. | Replace page chrome with local classes; replace product UI with component slots or tokens. | First-party audit and showcase chrome remain helper-free. |
| `truncate`, `clamp-*`, `scroll-x`, `min-w-0`, `placeholder-inline` | Keep compatibility. | Prefer component-native containment first; use helper only for narrow escape hatches. | Component alternatives cover the same overflow/text-bounding cases. |
| `visually-hidden`, `focus-ring`, `list-reset` | Keep. | No migration required; these remain narrow accessibility/reset helpers. | Revisit only if component-native input hiding fully replaces the helper. |
