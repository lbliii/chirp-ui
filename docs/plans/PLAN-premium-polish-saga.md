# PLAN: Premium Polish Saga

Status: proposed
Date: 2026-06-16
Trigger: A dogfood pass against the Railway dashboard (studied while building the
`lucky_cat` $MEOW trading demo, <https://luckycat-production.up.railway.app/>)
showed that chirp-ui already has the *machinery* for "expensive" product polish
but does not yet ship it as a **default**, expose it as **systematic primitives**,
or **prove** it across the full archetype spread. A trading dashboard is where
"premium feel" is load-bearing — it is a good forcing function for the gap.

## Mission

Make a fresh `use_chirp_ui()` app look like an expensive, designed product —
for *any* app type (data/finance, content, ops, agent, marketing) — before the
author writes a line of custom CSS, and **gate** that quality so it cannot
regress.

This is a sub-plan that **feeds Saga 4 (Polish, Performance & Premium Defaults)**
and **extends `PLAN-visual-taste-floor-saga.md`**. It does not fork a new
structure; it fills Saga 4's open epics with concrete, grounded deliverables and
adds one archetype to the taste-floor proof loop.

## The honest reframe (why this is "systematize + default + prove", not "build")

An architecture audit (2026-06-16) found chirp-ui already ships:

- **248 tokens** across color, spacing, radius, type, z-index, motion, shadow/
  elevation, glass/frosted/smoke, gradient/mesh, aura/ambient, neumorphic.
- A full **motion system**: duration scale, easing library (incl. an
  `ease-spring` cubic-bezier), `@keyframes` durations, and a **global
  `prefers-reduced-motion` cap**.
- A **semantic-core theme model** already (`light-dark()` + an OKLCH upgrade path
  via `@supports`, with `color-mix(in oklch)` for derived states) — so the
  "tiny HSL swap" lesson from Railway is **already true** here.
- `font-variant-numeric: tabular-nums` in **~25 components** — but hand-copied
  inline, not a token or utility.
- Per-component density modifiers (`--compact`/`--relaxed`/`--dense`) and a
  `.chirpui-table__td--mono` row treatment — but no unified density *scale*.
- A planned **Saga 4** and a **taste-floor plan** (7 taste laws, composition
  taxonomy, 4 golden screens, archetype matrix) plus the **proof loop**
  (66+ Playwright gauntlets, evidence tests, `lead-designer` /
  `accessibility-auditor` agents, showcase app).

So the path to "expensive polish for any app" is three gaps, not a rebuild:

1. **Systematize what is ad-hoc** — promote `tabular-nums`, density, and the
   missing micro-affordances (sliding indicator, FAB) to first-class primitives.
2. **Raise the default** — the default token profile is still essentially
   "Tailwind sky"; a fresh app inherits the machinery but a generic identity.
   This is the keystone (Saga 4 epic #206, currently unfilled).
3. **Prove it across the full archetype spread** — the taste floor has no
   data-dense / financial archetype. "Any app type" is only credible once the
   `lucky_cat` shape is a ratcheted golden screen.

## Problem Statement

chirp-ui has a strong **contract** floor and a strong **capability** floor, but a
generic **default** and an **un-systematized polish surface**:

- Numbers don't line up by default (tabular-nums is opt-in per component, copied
  by hand) — the single biggest "toy vs. real" tell on data/finance UIs.
- Active-nav state hard-cuts between items (no shared moving indicator).
- There is no FAB primitive and no mobile command-palette affordance.
- Density is a pile of per-component magic numbers, not a scale.
- The default accent/identity reads as a framework default, not a product.
- "Polish" is reviewed by taste, not gated by a ratchet, and is proven against
  4 archetypes that exclude the densest, most number-heavy class of app.

## Non-Goals

- Do **not** add Tailwind-compatible utilities or shorthand class vocabularies.
  (The one new utility, `.chirpui-tabular`, is a single token-backed helper, not
  a vocabulary — see Phase A.)
- Do **not** rename or break any `chirpui-*` BEM class or the `@layer` cascade
  order. Everything here is additive.
- Do **not** add a bundled webfont in this saga — keep the
  zero-runtime-dependency ethos; the font question stays a separate stop-and-ask
  (already decoupled in Saga 4 / #206).
- Do **not** introduce a non-pure-Python CSS build step (free-threading
  constraint — Lightning CSS bindings remain out).
- Do **not** copy Railway/shadcn/Tailwind UI anatomy as chirp-ui taste. The
  lessons are *patterns* (sliding indicator, tabular numerics, live regions),
  expressed in chirp-ui's own token + BEM vocabulary.

## What "expensive" decomposes into (the polish dimensions)

To make polish a ratchet and not a vibe, score every component against named
dimensions:

| Dimension | Current state | Gap to "expensive" |
|---|---|---|
| Motion & continuity | tokens exist; transitions mostly color/opacity | sliding indicators, sonner-grade stacked feedback, spring presets, view-transition continuity |
| Numerics & type discipline | tabular-nums scattered inline; role matrix documented, not shipped | `--chirpui-nums-tabular` token + `.chirpui-tabular`; ship role-based rem ramp |
| Material & depth | strong (aura/glass/elevation) | tasteful *defaults* + expose aura tokens at `:root` |
| Theming & default identity | OKLCH semantic core exists; default is generic | distinctive default profile (keystone) |
| Responsive & density | per-component compact/relaxed | unified density scale; container queries (card+surface); per-column mobile width |
| Micro-affordances | copy, status dots present | `fab()`, command-palette mobile trigger, sliding pill |
| A11y-as-polish | strong gauntlets | live regions for logs/streams; focus continuity through swaps |

## Phased Path

### Phase A — Systematize the primitives (low-risk, highest visible lift)
- `--chirpui-nums-tabular` token + `.chirpui-tabular` utility; refactor the ~25
  inline uses to it; make it the default for `data_grid` / `stat` / `badge` /
  ticker numerics. *(Issue: tabular numerics token)*
- Unified **density scale** (`--chirpui-density-*` driving padding + line-height)
  so `--compact`/`--relaxed` stop being per-component magic numbers.
  *(Issue: density scale)*
- **Sliding-pill active indicator** for `route_tabs` + shell rail — CSS-only
  `--chirpui-pill-x` / `--chirpui-pill-y`, responsive axis flip, reduced-motion
  snap. *(Issue: sliding pill)*
- **`fab()` primitive.** *(Issue: fab + palette FAB)*

### Phase B — Raise the default identity (keystone; Saga 4 / #206)
- Distinctive default token profile (replace Tailwind-sky) — pure-token,
  in-identity; ship it AA-clean (fold in the open `--chirpui-accent` contrast
  bug #241).
- Role-based rem type ramp (display/headline/title/body/label) — spec'd in
  `docs/decisions/typography-role-matrix.md`, not yet emitted.
- Layered-gradient hero presets + expose `--chirpui-aura-*` at `:root` for theme
  control. *(Issue: hero gradients + aura tokens)*

### Phase C — Feedback & continuity (taste-floor; Saga 4 / #207–#208)
- sonner-grade toasts: stacking, swipe-dismiss, HTMX-native loading→success/error.
- Live regions for logs/streaming (`role="log" aria-relevant="additions text"`
  + a `role="status"` load sentinel). *(Issue: live regions)*
- Spring/transform motion presets wired to the existing `ease-spring` token;
  extend the motion-token test to `animation`/`animation-duration` (#208).

### Phase D — Prove "any app type"
- Add a **data-dense / market archetype** to `docs/screens/archetype-matrix.md`,
  with **`lucky_cat` as the reference golden screen**. *(Issue: archetype + golden screen)*
- `data_grid` **rendering fork** decision (real-`<table>` default vs opt-in
  ARIA-grid-over-div for resize/virtualization), with a resize-handle + per-column
  mobile-width contract on `grid_state.Column`. *(Issue: data_grid fork)*
- Extend the **taste-law ratchet** + Playwright gauntlets + `lead-designer`
  screenshot critique to run **per-archetype**, so a polish regression fails CI.

## Proof Loop (how we know it's expensive, for any app)

Every phase output earns its quality the same way:

1. A **golden-screen entry per archetype** (`docs/screens/`), including the new
   data-dense one.
2. A **`lead-designer` agent screenshot critique** against the polish dimensions.
3. A **taste-law ratchet test** (extends the taste-floor ratchet).
4. A **browser gauntlet** (extends `tests/browser/`).

The infra for all four already exists. This saga adds (a) the data-dense
archetype and (b) a polish ratchet keyed to the dimensions table above.

## Mapping to Saga 4 & the dogfood issues

| Deliverable | Issue | Phase | Feeds |
|---|---|---|---|
| Tabular numerics token + `.chirpui-tabular` | #257 | A | #206 (type discipline) |
| Density scale | #258 | A | #209 / taste floor |
| Sliding-pill indicator | #255 | A | Saga 2 rail + #206 |
| `fab()` + palette FAB | #256 | A | Saga 2 mobile chrome |
| Hero gradients + aura at `:root` | #259 | B | #206 |
| Default identity + role-based type | #206 | B | #206 (keystone) |
| sonner-grade feedback | #207 | C | #207 |
| Live regions (logs/streaming) | #260 | C | #207 / a11y |
| Motion-token test extension | #208 | C | #208 |
| Data-dense archetype + `lucky_cat` golden screen | #262 | D | taste floor + Saga 4 proof |
| `data_grid` rendering fork | #261 | D | Saga 3 data grid wave |

## Constraints & Risks

- **Free-threading tooling** — CSS build stays pure-Python; the CSS-subset
  emitter (#206 sibling) must stay stdlib. No Lightning CSS.
- **Public API** = the BEM classes + `@layer` order. All work is additive; no
  renames.
- **AA contrast** — the new default identity must ship accessible; resolve
  `--chirpui-accent` contrast (#241) as part of Phase B, not after.
- **Density honesty** — a density scale must respect the `--chirpui-control-
  touch-target` floor (44px) so "compact" never breaks touch a11y.
- **Scope creep on container queries** — keep #209 narrowed to card + surface.

## Related Plans

| Plan | Relationship |
|---|---|
| `docs/strategy/roadmap-next.md` | This is the implementation plan for Saga 4's polish epics. |
| `PLAN-visual-taste-floor-saga.md` | This saga adds the data-dense archetype + polish ratchet to it. |
| `docs/decisions/typography-role-matrix.md` | Phase B ships the role-based ramp it specs. |
| `PLAN-content-type-refinement.md` | Shares the type-and-accent vocabulary (mono eyebrow, clamped title). |
| `PLAN-component-maturity-gap-sweep.md` | `data_grid` fork (Phase D) coordinates with the primitives gap ledger. |
