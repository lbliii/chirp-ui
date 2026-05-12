# Plan: Legacy Helper Cleanup Before 1.0

**Status**: complete
**Created**: 2026-05-12
**Target**: pre-1.0
**Estimated Effort**: 8-14h across 3-4 PRs
**Dependencies**:
[PLAN-primitive-vocabulary-hardening.md](PLAN-primitive-vocabulary-hardening.md),
[../PRIMITIVES.md](../PRIMITIVES.md),
[../PUBLIC-SURFACE-STABILIZATION.md](../PUBLIC-SURFACE-STABILIZATION.md),
[../VISUAL-AUDIT-SHOWCASE.md](../VISUAL-AUDIT-SHOWCASE.md)

---

## Goal

Reduce legacy helper usage in first-party Chirp UI examples, docs, and visual
proof pages without breaking existing consumers.

The cleanup is about teaching the right authoring model before 1.0:

- New Chirp UI examples should reach for components, layout primitives, and
  tokens first.
- Legacy helper classes should remain available as compatibility surface.
- The visual audit showcase should prove the current design system, not depend
  on old utility-like typography and spacing helpers.

---

## Non-Goals

- Do not delete public legacy helper classes in this phase.
- Do not add runtime warnings or CSS warnings for existing helper usage.
- Do not rewrite the full static showcase in one large pass.
- Do not remove narrow accessibility and containment helpers where the
  component contract still needs them.

---

## Current Inventory

The current legacy compatibility helper set is intentionally retained:

`clamp-2`, `clamp-3`, `display`, `focus-ring`, `font-2xl`, `font-base`,
`font-lg`, `font-medium`, `font-mono`, `font-sm`, `font-xl`, `font-xs`,
`list-reset`, `mb-md`, `measure-lg`, `measure-md`, `measure-sm`, `min-w-0`,
`mt-md`, `mt-sm`, `placeholder-inline`, `prose-lg`, `prose-sm`, `scroll-x`,
`text-muted`, `truncate`, `ui-base`, `ui-bold`, `ui-label`, `ui-lg`,
`ui-medium`, `ui-meta`, `ui-normal`, `ui-semibold`, `ui-sm`, `ui-title`,
`ui-xl`, `ui-xs`, `visually-hidden`.

### Helper Groups

| Group | Helpers | Direction |
|-------|---------|-----------|
| Spacing shorthands | `mt-sm`, `mt-md`, `mb-md` | Deprecate later; prefer `stack`, `flow`, slots, or component-owned rhythm. |
| Typography shorthands | `display`, `font-*`, `ui-*`, `text-muted`, `measure-*`, `prose-*` | Keep compatibility; prefer component slots, tokens, and `prose`. |
| Text and containment escapes | `truncate`, `clamp-*`, `scroll-x`, `min-w-0`, `placeholder-inline` | Keep compatibility; prefer component CSS or layout primitives first. |
| Accessibility/reset helpers | `visually-hidden`, `focus-ring`, `list-reset` | Keep; these stay narrow and explicit. |

---

## Safety Rules

1. **No public class removals before the breaking-change window.** Legacy
   helpers keep `maturity=legacy` and `authoring=compatibility`.
2. **No helper vocabulary growth.** Any new one-off typography or spacing helper
   needs an explicit design-system review.
3. **First-party examples should teach preferred primitives.** Compatibility
   helpers can appear only when they are the subject of the example or when a
   narrow accessibility/containment need remains.
4. **Generated docs stay aligned with the manifest.** The manifest remains the
   source of truth for preferred versus compatibility authoring paths.

---

## Phase 1: Make The Visual Audit Helper-Free

**Goal**: The design-system gap showcase should prove tokens, primitives, and
component surfaces without using legacy typography/spacing helpers in its own
audit chrome.

Files:

- `examples/design-system-gap-showcase/index.html`
- `tests/test_visual_audit_showcase.py`
- `tests/browser/test_visual_audit_showcase.py`

Tasks:

- Replace audit-page uses of `chirpui-ui-title`, `chirpui-ui-label`,
  `chirpui-ui-meta`, and `chirpui-text-muted` with local `audit-*` classes or
  existing component slots.
- Replace audit-page uses of `chirpui-scroll-x` with a local audit-only
  overflow wrapper.
- Keep `chirpui-visually-hidden` only if the underlying control component still
  requires it; otherwise prefer component-native hidden input handling.
- Add a test guard that fails if the audit page introduces non-allowed legacy
  helper classes.
- Keep the browser visual checks passing for token color, theme contrast, overlay
  alignment, logo spacing, and long command labels.

Acceptance:

- `examples/design-system-gap-showcase/index.html` has no legacy helper class
  usage except any explicitly allowlisted accessibility helper.
- `uv run pytest tests/test_visual_audit_showcase.py -q` passes.
- `uv run --group browser pytest tests/browser/test_visual_audit_showcase.py -q --timeout=30 --override-ini=addopts=` passes.

---

## Phase 2: Clean High-Visibility Showcase Templates

**Goal**: The dynamic component showcase should stop using old helper classes as
page-copy styling and spacing shortcuts.

Files to inspect first:

- `examples/component-showcase/templates/showcase/navigation.html`
- `examples/component-showcase/templates/showcase/dashboard.html`
- `examples/component-showcase/templates/showcase/islands.html`
- `examples/component-showcase/templates/showcase/ui.html`
- Other `examples/component-showcase/templates/showcase/*.html` files with
  repeated `chirpui-text-muted chirpui-font-sm` or spacing shorthand usage.

Tasks:

- Introduce or reuse local showcase page classes for descriptive copy, captions,
  and section rhythm.
- Replace repeated `chirpui-text-muted chirpui-font-sm` page-copy styling with
  showcase-local classes.
- Replace `chirpui-mt-sm`, `chirpui-mt-md`, and `chirpui-mb-md` with `stack`,
  `flow`, component slots, or local showcase CSS.
- Leave legacy helpers in examples only when the section is explicitly showing
  that helper or when the component API still emits the helper internally.

Acceptance:

- High-visibility showcase templates no longer teach spacing shorthands.
- Repeated page-copy styling is local showcase chrome, not legacy helper usage.
- Existing showcase route, manifest, and browser tests still pass.

---

## Phase 3: Triage The Static Showcase

**Goal**: Keep the static showcase useful as a broad catalog while preventing it
from becoming the main source of legacy-helper guidance.

Files:

- `examples/static-showcase/index.html`

Tasks:

- Add a usage report for legacy helper classes in the static page.
- Classify each use as one of:
  - **component contract**: the component itself needs the helper class.
  - **showcase chrome**: replace with local static-showcase CSS.
  - **legacy example**: keep only if the section is explicitly documenting the
    helper.
- Prioritize replacing showcase chrome uses before touching component examples.
- Do not attempt a full rewrite unless the report shows a small bounded diff.

Acceptance:

- Static showcase helper usage is documented and intentionally scoped.
- Page chrome no longer relies on spacing shorthands or typography helpers where
  local CSS is simpler.
- Component examples are not damaged while cleaning page-level styling.

---

## Phase 4: Documentation And Deprecation Policy

**Goal**: Make the compatibility stance explicit for humans and agents.

Files:

- `docs/PRIMITIVES.md`
- `docs/ANTI-FOOTGUNS.md`
- `docs/COMPONENT-OPTIONS.md`
- `docs/PUBLIC-SURFACE-STABILIZATION.md`
- `docs/ROADMAP-pre-1.0.md`
- `tests/test_manifest.py`

Tasks:

- Add a short "deprecate later" note for spacing shorthands.
- Keep typography helpers documented as compatibility, not preferred authoring.
- Keep `visually-hidden`, `focus-ring`, and `list-reset` positioned as narrow
  accessibility/reset helpers.
- Ensure `find --authoring preferred` and `find --authoring compatibility`
  continue to match the docs.
- Maintain the manifest ratchet that prevents unreviewed utility-like helper
  growth.

Acceptance:

- No generated docs present legacy helpers as the preferred path.
- Every helper still has a keep/deprecate-later disposition.
- `uv run poe verify-generated` passes.
- `uv run poe check` passes.

---

## Phase 5: Pre-1.0 Decision Gate

**Goal**: Decide what happens to the old helper classes at the 1.0 boundary.

Decision options:

- **Alias indefinitely**: keep the helper in CSS and manifest as compatibility.
- **Docs-only deprecation**: keep the class, stop showing it in preferred docs.
- **1.0 breaking removal**: remove only with an explicit migration guide and
  release-note callout.

Initial recommendations:

| Helpers | Recommendation |
|---------|----------------|
| `mt-sm`, `mt-md`, `mb-md` | Docs-only deprecation now; consider 1.0 removal only if first-party usage is gone. |
| `font-*`, `ui-*`, `text-muted` | Keep compatibility; reduce first-party page-chrome usage before deciding on removal. |
| `truncate`, `clamp-*`, `scroll-x`, `min-w-0`, `placeholder-inline` | Keep compatibility unless component-native alternatives fully cover the use cases. |
| `visually-hidden`, `focus-ring`, `list-reset` | Keep. These are narrow enough to remain useful and low-risk. |

Acceptance:

- A 1.0 helper decision table exists in `docs/PUBLIC-SURFACE-STABILIZATION.md`.
- Any removal candidate has a migration path and first-party usage count.

---

## Verification Checklist

- `uv run pytest tests/test_visual_audit_showcase.py -q`
- `uv run --group browser pytest tests/browser/test_visual_audit_showcase.py -q --timeout=30 --override-ini=addopts=`
- `uv run pytest tests/test_manifest.py tests/test_find_cli.py -q`
- `uv run poe verify-generated`
- `uv run poe check`

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-05-12 | Initial cleanup plan | Captures the follow-up from the Skeleton-inspired design-system audit and separates safe first-party cleanup from public compatibility removals. |
| 2026-05-12 | Phases 1-5 executed | Visual audit, high-visibility showcase templates, static showcase inventory, docs policy, and 1.0 decision gate now have committed proof and tests. |
| 2026-05-12 | Archived to done | The plan now records shipped work; residual legacy-helper policy lives in `PUBLIC-SURFACE-STABILIZATION.md` and `PLAN-primitive-vocabulary-hardening.md`. |
