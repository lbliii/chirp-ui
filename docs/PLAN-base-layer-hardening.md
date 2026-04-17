# Epic: Base-Layer Hardening — Preflight-Style Defaults

**Status**: Complete (Sprints 20–26 landed 2026-04-17)
**Created**: 2026-04-17
**Target**: 0.6.x
**Estimated Effort**: 8–12h (6 small sprints)
**Dependencies**: Sprint 20 (overflow containment — landed on `lbliii/overflow-containment`)
**Source**: Post-sprint-20 audit comparing `chirpui.css` base-element handling against Tailwind's **Preflight** reset. Sprint 20 hardened *container* defaults (surface/callout/field-input). The remaining gaps are *base element* defaults — global rules on `<img>`, `<pre>`, `<table>`, `<button>`, motion, color-scheme, and scroll behavior — that close the same class of "content punches past its boundary" bugs at the root instead of per-component.

---

## Why This Matters

Sprint 20 answered the question *"do containers hold their content?"* — now surfaces, callouts, and form controls have `min-width: 0`, `overflow-wrap`, and sensible `max-width` defaults. But **base elements still have browser defaults**. A raw `<img>` dropped inside a `.chirpui-surface` can still overflow. A `<pre>` outside `.chirpui-prose` can still widen its cell. A range input ignores the brand color. Animations run at full speed for users with `prefers-reduced-motion: reduce`. These are *one-rule-fixes-everywhere* bugs — the highest leverage-per-line we can ship.

**Consequences of the current state:**

1. **Media elements overflow silently** — `.chirpui-card__media img` has `width: 100%; height: auto` (chirpui.css:4734), but a raw `<img>` inside `.chirpui-surface` or `.chirpui-card__body` has no such rule. SVG/video/iframe/canvas/embed have no treatment at all. Any app dropping a 2000px-wide product image into a card punches past the layout.
2. **`<pre>` and `<table>` outside `.chirpui-prose` have no containment** — `chirpui.css:3731` handles `:where(.chirpui-prose) pre` with `overflow-x: auto`. A `<pre>` inside `.chirpui-card__body` with a long stack trace blows out the card width. Same for `<table>` — prose tables are `width: 100%` (3780) but tables outside prose have no width or overflow rule.
3. **Motion tokens ignore user preference** — `test_transition_tokens.py` enforces `--chirpui-duration-*` and `--chirpui-easing-*` token usage across the codebase, but there is no `@media (prefers-reduced-motion: reduce)` override at the root. 50+ animations run at full speed regardless of OS-level accessibility settings.
4. **No `color-scheme` declaration** — `:root` has light/dark theme tokens but no `color-scheme: light dark` property. Native scrollbars, form controls, date pickers, and autofill backgrounds fall back to system defaults that may not match the active theme — the worst offender is Chrome's yellow autofill on a dark-mode card.
5. **Anchor links land under sticky headers** — headings inside `.chirpui-prose` have no `scroll-margin-top`. Following an in-page hash link scrolls the target heading behind the app shell's sticky header. Users manually scroll back up every time.
6. **Scroll regions chain-scroll to the page** — `.chirpui-code-block` and `.chirpui-scroll-x` (Sprint 20) have no `overscroll-behavior`. Scrolling past a code block's boundary hijacks the page scroll — jarring on mobile, worse with trackpad inertia.
7. **Native form controls ignore brand color** — checkboxes, radios, and `<input type="range">` render with browser-default blue. `:root { accent-color: var(--chirpui-accent) }` is one line for a global brand-consistent fix.
8. **Typography still uses default wrapping** — headings can break awkwardly (one word on last line), paragraphs have ragged right edges. `text-wrap: balance` on headings and `pretty` on prose paragraphs is now widely supported and costs nothing.

### Evidence Table

| Finding | Source | Proposal Impact |
|---------|--------|-----------------|
| Raw `<img>` / `<svg>` / `<video>` / `<iframe>` / `<canvas>` have no base width cap | `chirpui.css` (no rule) | **FIXES** — Sprint 21 |
| `<pre>` / `<table>` only scroll/wrap inside `.chirpui-prose` | chirpui.css:3731, 3780 | **FIXES** — Sprint 22 |
| 50+ animations ignore `prefers-reduced-motion` | tests/test_transition_tokens.py (tokens enforced, preference not) | **FIXES** — Sprint 23 |
| No `color-scheme` on `:root` | themes/*.css (no declaration) | **FIXES** — Sprint 24 |
| No `accent-color` on `:root` | chirpui.css (no declaration) | **FIXES** — Sprint 24 |
| Headings lack `scroll-margin-top` under sticky shell | chirpui.css prose section | **FIXES** — Sprint 25 |
| Headings/prose use default wrapping | chirpui.css prose section | **FIXES** — Sprint 25 |
| `.chirpui-scroll-x`, `.chirpui-code-block` chain scroll | chirpui.css:3626, 1004 | **FIXES** — Sprint 26 |

---

## Invariants

1. **Only `chirpui.css` (base layer) changes** — no template edits, no new macros, no new filters. This is a pure reset/defaults sprint.
2. **No visual regression in the showcase** — every sprint ends with a showcase walk-through. If a change shifts a component's look, it's either intentional (documented) or reverted.
3. **All existing tests stay green** — `uv run poe ci` passes before and after each sprint.
4. **Each sprint ships independently** — one PR per sprint, each reviewable and revertable in isolation.
5. **Behavior is progressive-enhancement friendly** — `text-wrap`, `color-scheme`, `accent-color`, `overscroll-behavior` all degrade silently in older browsers. No polyfills.

---

## Target Architecture

No structural changes. All additions land in `chirpui.css` in a new (or existing) `/* base */` section near the top of the file, before the layout/component sections. New content:

```
chirpui.css:
  :root                     — color-scheme, accent-color
  *, ::before, ::after      — prefers-reduced-motion override
  img, svg, video, …        — global media reset
  :where(.chirpui-surface, .chirpui-card__body, .chirpui-callout)
                             :is(pre, table)
                            — pre/table containment outside prose
  :where(.chirpui-prose) :is(h1, h2, h3)
                            — scroll-margin-top + text-wrap: balance
  :where(.chirpui-prose) p  — text-wrap: pretty
  .chirpui-scroll-x,
  .chirpui-code-block       — overscroll-behavior: contain

docs/LAYOUT.md              — append "Base defaults" subsection
CLAUDE.md                   — Sprint 21–26 rows in sharp-edges table
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 20 | Container containment (surface/callout/field-input + utilities) | 2h | Low | ✅ **Landed** |
| 21 | Global media reset (img/svg/video/iframe/canvas/embed/object) | 1–2h | Medium | ✅ **Landed** |
| 22 | `<pre>`/`<table>` auto-containment outside prose | 1h | Low | ✅ **Landed** |
| 23 | `prefers-reduced-motion` global cap | 1h | Low | ✅ **Landed** |
| 24 | `color-scheme` + `accent-color` per theme | 2h | Low | ✅ **Landed** (color-scheme pre-existing; `:root { accent-color }` added) |
| 25 | Typography polish (`text-wrap`, `scroll-margin-top`) | 1–2h | Low | ✅ **Landed** (scroll-margin-top pre-existing on app-shell/navbar/site-header descendants; `text-wrap: pretty` added to prose `<p>`; `text-wrap: balance` on prose headings pre-existing) |
| 26 | `overscroll-behavior: contain` on scroll regions | 1h | Low | ✅ **Landed** |

---

## Sprint 21: Global Media Reset

**Problem.** Raw `<img>` inside a card body can overflow. `<svg>`, `<video>`, `<iframe>`, `<canvas>`, `<embed>`, `<object>` have no base treatment and also suffer from inline-baseline gaps (the 4px descender space that breaks flush layouts).

**Design decisions.**

- `display: block` + `max-width: 100%` is Tailwind preflight's approach. The risk is inline images in prose (e.g. emoji-as-image, inline icons) that *should* flow inline. Mitigation: scope `display: block` narrowly and leave `max-width: 100%` + `height: auto` on the rest.
- For `<img>` and `<video>` only, add `height: auto` — prevents intrinsic-height from conflicting with `max-width` scaling.
- For `<iframe>`, `<embed>`, `<object>` — these *never* want inline, so `display: block` is safe.
- For `<svg>` — leave `display` alone (inline SVG icons are common); add `max-width: 100%` as a safety net.
- Narrow the rule to `:where()` at zero specificity so authors can override with a single class.

**Concrete diff.**

```css
/* base media */
:where(img, video, canvas) {
    max-width: 100%;
    height: auto;
}

:where(iframe, embed, object) {
    display: block;
    max-width: 100%;
}

:where(svg) {
    max-width: 100%;
}
```

**Acceptance criteria.**
- `uv run poe ci` passes.
- Showcase renders identically for existing image-bearing components (card media, avatar, post-card media).
- A new test `test_media_reset.py` asserts the rule exists: `grep -E ':where\(img, video, canvas\)' src/chirp_ui/templates/chirpui.css` returns a match.
- Manual: drop a 2000px-wide `<img>` into a `.chirpui-card__body` in the showcase — it scales to the card width.

**Risks & mitigations.**
- **Risk:** an app relies on native `<img>` intrinsic width inside a narrow flex container — adding `max-width: 100%` changes sizing. **Mitigation:** `:where()` is zero-specificity; a single-class override wins. Document in LAYOUT.md § Base defaults.
- **Risk:** `<svg>` inside an inline icon usage breaks. **Mitigation:** we don't add `display: block` to SVG; inline SVGs keep their inline flow. `max-width: 100%` only applies when the SVG has no intrinsic width or an oversize one — rare for icons.

---

## Sprint 22: `<pre>` / `<table>` Auto-Containment Outside Prose

**Problem.** The `.chirpui-prose` scope handles code and tables correctly. Everywhere else, a `<pre>` inside a card/surface/callout blows out the cell. Developers currently have to know about `.chirpui-scroll-x` (Sprint 20) and wrap by hand.

**Design decisions.**

- Scope the rule to `.chirpui-card__body`, `.chirpui-surface`, `.chirpui-callout` (the containers most likely to host ad-hoc HTML blobs from user content). Skip `.chirpui-prose` (already handled).
- Use `:where(…)` to keep the rule at zero specificity so `.chirpui-scroll-x` and authored overrides still win.
- For tables, `display: block` + `overflow-x: auto` is the classic escape hatch (loses `<tr>`/`<td>` spanning but keeps the page unbroken). Alternative: wrap in a flex parent — but we can't do that without JS or templates. Accept the `display: block` tradeoff; document it.

**Concrete diff.**

```css
/* pre/table auto-containment outside prose */
:where(.chirpui-card__body, .chirpui-surface, .chirpui-callout) :is(pre, table) {
    max-width: 100%;
    overflow-x: auto;
}

:where(.chirpui-card__body, .chirpui-surface, .chirpui-callout) table {
    display: block;
}
```

**Acceptance criteria.**
- `uv run poe ci` passes.
- Manual: drop `<pre>print('x' * 500)</pre>` into `.chirpui-card__body` → scrolls horizontally, card width preserved.
- Manual: drop `<table>` with 10 columns into `.chirpui-surface` → scrolls, surface width preserved.
- The `.chirpui-prose` table treatment remains intact (no `display: block` inside prose).

**Risks & mitigations.**
- **Risk:** `display: block` on tables breaks `<colgroup>` / `<col>` styling that assumes `display: table`. **Mitigation:** documented; if needed, authors wrap the table in `.chirpui-scroll-x` (Sprint 20 utility) explicitly to get the scroll without the display change. Keep the `.chirpui-scroll-x` path as the escape hatch.
- **Risk:** prose-like content dropped into a card body now double-scrolls if it has its own prose class. **Mitigation:** `:where()` is zero specificity; `.chirpui-prose`'s own `pre` rule has higher specificity and wins.

---

## Sprint 23: `prefers-reduced-motion` Global Cap

**Problem.** 50+ animations (enforced by `test_transition_tokens.py`) use motion tokens but ignore OS-level accessibility preferences. A user with vestibular sensitivity sees full transitions even after setting *Reduce Motion* in their OS.

**Design decisions.**

- Apply at the root, not per-component. Tailwind-style: `*, ::before, ::after` gets `animation-duration: 0.01ms !important` and `transition-duration: 0.01ms !important` under the media query.
- Use `0.01ms` (not `0`) so events still fire (`animationend`, `transitionend`) — callers that depend on event timing still get notified.
- Scroll smooth → auto. Add `scroll-behavior: auto !important` to `html` under the same media query.
- **Exception list:** `.chirpui-streaming-block` and live regions may want to keep motion for visibility of state changes. Revisit if needed, not a blocker.

**Concrete diff.**

```css
@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

**Acceptance criteria.**
- `uv run poe ci` passes.
- A new test asserts the `@media (prefers-reduced-motion: reduce)` block exists: `grep -c 'prefers-reduced-motion: reduce' src/chirp_ui/templates/chirpui.css` returns ≥ 1.
- Manual: toggle *System Settings → Accessibility → Reduce motion* on; showcase transitions instant, no visible fade/slide.

**Risks & mitigations.**
- **Risk:** `!important` on animation/transition durations blocks authors who *want* motion even under reduced-motion preference. **Mitigation:** documented; authors wanting explicit motion wrap their rule in `@media (prefers-reduced-motion: no-preference) { ... }` or use `transform` without transition — both are recommended a11y patterns anyway.

---

## Sprint 24: `color-scheme` + `accent-color`

**Problem.** Native scrollbars, form controls, date pickers, and Chrome autofill don't know about the chirp-ui theme. Autofill highlights with yellow on dark cards. Range inputs are browser-default blue. Scrollbars in dark mode render light-on-light in some OS/browser combinations.

**Design decisions.**

- `color-scheme: light dark` on `:root` — tells the browser this app supports both, browser picks based on OS preference.
- Per-theme override: `[data-theme="dark"] { color-scheme: dark }`, `[data-theme="light"] { color-scheme: light }`. When `data-theme="system"` is active, inherit from `:root`.
- `accent-color: var(--chirpui-accent)` on `:root` — applies to checkboxes, radios, range, progress.
- Audit existing themes in `src/chirp_ui/templates/themes/` to confirm the per-theme override pattern is consistent.

**Concrete diff.**

```css
:root {
    color-scheme: light dark;
    accent-color: var(--chirpui-accent);
}

[data-theme="light"] { color-scheme: light; }
[data-theme="dark"]  { color-scheme: dark; }
/* data-theme="system" inherits from :root */
```

**Acceptance criteria.**
- `uv run poe ci` passes.
- Manual: dark-mode showcase → native scrollbars render dark, autofill background dark.
- Manual: a `<input type="range">` in the form showcase uses `--chirpui-accent` color for the track/thumb.
- Theme-switching test: toggle theme, verify `color-scheme` value changes via DevTools computed styles.

**Risks & mitigations.**
- **Risk:** `color-scheme: dark` darkens UA-styled form control backgrounds, which may conflict with `.chirpui-field__input` custom styling. **Mitigation:** chirp-ui's form controls override background explicitly (chirpui.css:7665) — `color-scheme` only affects UA defaults; authored styles still win.
- **Risk:** `accent-color` on `:root` cascades to every form control, including some that set their own accent via `--chirpui-checkbox-accent` (if any). **Mitigation:** audit for per-control accent tokens during sprint; promote them to CSS-var overrides on the specific selector.

---

## Sprint 25: Typography Polish

**Problem.** Headings can break with a single word orphaned on the last line ("this is my long heading / title" → "this is my long heading\ntitle"). Paragraphs have ragged right edges that modern wrap heuristics can improve. Anchor links land under the sticky app shell header.

**Design decisions.**

- `text-wrap: balance` on h1/h2/h3 (including component titles: `.chirpui-card__title`, `.chirpui-section-header__title`, etc.) — distributes text across lines more evenly.
- `text-wrap: pretty` on `.chirpui-prose p` and `.chirpui-surface__body` — better last-line handling.
- Both properties have widespread evergreen support (Chrome 114+, Firefox 121+, Safari 17.5+); fall back silently.
- `scroll-margin-top` on prose headings = app shell header height + a small buffer. Use a new token `--chirpui-scroll-anchor-offset` so it's tunable per-app.

**Concrete diff.**

```css
:root {
    --chirpui-scroll-anchor-offset: calc(var(--chirpui-app-shell-header-height, 4rem) + var(--chirpui-spacing));
}

:where(.chirpui-prose) :is(h1, h2, h3, h4, h5, h6),
:where(.chirpui-card__title, .chirpui-section-header__title,
       .chirpui-entity-header__title, .chirpui-page-header__title,
       .chirpui-surface__title) {
    text-wrap: balance;
}

:where(.chirpui-prose) p,
:where(.chirpui-surface__body, .chirpui-surface__lede) {
    text-wrap: pretty;
}

:where(.chirpui-prose) :is(h1, h2, h3, h4, h5, h6)[id] {
    scroll-margin-top: var(--chirpui-scroll-anchor-offset);
}
```

**Acceptance criteria.**
- `uv run poe ci` passes.
- Manual: showcase long-title card → heading no longer orphans last word.
- Manual: in a docs page with an anchor link, clicking the link scrolls so the heading sits below the sticky header with spacing.
- Grep confirms declarations exist.

**Risks & mitigations.**
- **Risk:** `text-wrap: balance` has a character-count ceiling in browsers (~6 lines), headings with unusually long text silently fall back to default. **Mitigation:** acceptable; the fallback is the current behavior.
- **Risk:** `--chirpui-app-shell-header-height` may not be defined in all apps. **Mitigation:** the `var(..., 4rem)` fallback handles this.

---

## Sprint 26: `overscroll-behavior: contain`

**Problem.** `.chirpui-code-block` and `.chirpui-scroll-x` let the browser chain-scroll into the page when the user reaches the scroll boundary. On trackpad/touch, this is jarring — scrolling a wide table sideways eventually kicks the page.

**Design decisions.**

- `overscroll-behavior: contain` on the scroll region only (not `auto` / `none`) — keeps elastic bounce within the region but blocks propagation to the page.
- Apply to `.chirpui-code-block`, `.chirpui-scroll-x`, and `.chirpui-app-shell__main--fill` scroll children.

**Concrete diff.**

```css
.chirpui-scroll-x,
.chirpui-code-block,
:where(.chirpui-prose) pre {
    overscroll-behavior: contain;
}
```

**Acceptance criteria.**
- `uv run poe ci` passes.
- Manual: on a trackpad, scroll a wide table inside `.chirpui-scroll-x` → at the boundary, the page does not scroll.
- Grep confirms property is present.

**Risks & mitigations.**
- **Risk:** negligible. `overscroll-behavior: contain` is a pure user-experience polish and has no visual impact.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Sprint |
|------|------------|--------|------------|--------|
| Global media reset breaks an existing inline-image pattern | Low | Medium | `:where()` zero-specificity lets authors override with a single class; showcase audit catches regressions | 21 |
| `display: block` on tables breaks `<colgroup>` styling | Low | Low | `.chirpui-scroll-x` wrap is the documented escape hatch; keep the utility for authored markup | 22 |
| `!important` on reduced-motion blocks intentional motion | Low | Low | Documented pattern: authors wrap in `@media (prefers-reduced-motion: no-preference)` | 23 |
| `color-scheme: dark` conflicts with custom form styles | Low | Low | chirp-ui form controls already override backgrounds; UA-default changes only affect unstyled native controls | 24 |
| `accent-color` cascades over per-control tokens | Medium | Low | Audit for existing `--chirpui-checkbox-accent`-style tokens during sprint; promote if found | 24 |
| `text-wrap: balance/pretty` character-count fallback | Low | None | Silent fallback to current wrapping is acceptable | 25 |
| Any sprint introduces a visual regression | Medium | Medium | Each sprint ends with a showcase walk-through; bail if anything shifts unintentionally | all |

---

## Success Metrics

| Metric | Current | After Sprint 23 | After Sprint 26 (complete) |
|--------|---------|-----------------|----------------------------|
| Base-element overflow bugs (img/svg/video/iframe/pre/table outside prose) | Unbounded — any author can punch past a card | 0 (pre/table + media handled) | 0 |
| Components honoring `prefers-reduced-motion` | 0 / 50+ animations | 50+ / 50+ (global cap) | 50+ / 50+ |
| Native-control theme parity (scrollbars, autofill, checkboxes, range) | System defaults | System defaults | Theme-matched |
| Anchor-link usability (heading lands below sticky header) | Broken (lands under header) | Broken | Fixed |
| Scroll chaining from code/tables to page | Always chains | Always chains | Contained |
| Showcase visual parity | — | 100% | 100% |
| `uv run poe ci` pass rate | 100% (1513 tests) | 100% | 100% |

---

## Out of Scope

- **Spacing utilities (`space-y-*`, `space-x-*`)** — chirp-ui uses `stack()` / `cluster()` primitives on purpose. Ad-hoc spacing utilities erode the composition story.
- **Utility CSS expansion** — Sprint 20 added `scroll-x`, `truncate`, `clamp-{2,3}`. This epic does not add more utilities.
- **Theme-aware `color-scheme` for custom themes beyond light/dark** — only the two canonical modes. Custom brand themes pick one.
- **Polyfills** — all features degrade silently in older browsers; no JS fallback.
- **`contain: layout/paint/content` on cards/surfaces** — render-perf optimization, flagged in the audit but deferred. Risks subtle z-index/positioning changes; not a blind win.
- **Print stylesheets** (`break-inside: avoid`) — niche; revisit if user demand surfaces.

---

## Open Questions

1. Should Sprint 21's media reset exclude `.chirpui-prose img` (which may already be handled explicitly)? **Action:** grep `.chirpui-prose img` during sprint; if a more specific rule exists, confirm it wins over `:where()`.
2. Should Sprint 24 introduce per-theme tokens for `accent-color` (e.g. `--chirpui-accent-focus`) or just use `--chirpui-accent` everywhere? **Action:** start with `--chirpui-accent`; split only if a showcase case needs it.
3. Should Sprint 25's `scroll-margin-top` apply to **all** `[id]` elements inside prose or only headings? **Action:** headings only in v1; expand if authors hit the gap.
4. Is there app shell height instability that makes a fixed `--chirpui-scroll-anchor-offset` wrong? **Action:** confirm the header-height token is stable across shell variants before Sprint 25.

---

## Notes

- Sprint 20 (container containment) is already on `lbliii/overflow-containment`. The follow-on sprints (21–26) can each ship as their own branch/PR off `main` once Sprint 20 merges.
- Estimated total: 8–12h across 6 small PRs. No sprint requires more than a single focused session.
- After Sprint 26 lands, add a Sprint 21–26 block to CLAUDE.md's *Sharp edges — what's been hardened* table.
