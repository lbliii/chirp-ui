# Epic: Primitive Vocabulary Hardening

**Status**: Active
**Created**: 2026-04-24
**Target**: pre-1.0
**Estimated Effort**: 10-16h across 4 PRs
**Dependencies**: Registry auto-category debt cleared; `chirpui-manifest@3`

---

## Why This Matters

ChirpUI's category bet is that UI is a Python-reachable vocabulary, not a bag of CSS strings. The registry now has no `category="auto"` descriptors and no active global emit reconciliation maps, which closes the biggest hidden drift source. The next risk is softer: historical CSS helpers can still teach agents and app developers the wrong mental model if they appear equivalent to composition primitives.

This phase makes the primitive surface explicit:

- **Blessed primitives** are named UI/layout concepts ChirpUI wants consumers to use directly: `stack`, `cluster`, `grid`, `frame`, `block`, `flow`, `layer`, `actions`, `container`, and `prose`.
- **Legacy helpers** are compatibility classes retained for existing templates and CSS, but not promoted as the authoring vocabulary: `mt-md`, `font-sm`, `text-muted`, `truncate`, `scroll-x`, `min-w-0`, and similar typography/spacing shorthands.
- **Specialized primitives** remain discoverable by category (`ascii`, `effect`, `feedback`, `control`) without becoming a utility-class expansion path.

The work is mostly documentation and guardrails. No classes are removed in this phase.

### Evidence

| Finding | Current State | Proposal Impact |
|---------|---------------|-----------------|
| Registry auto bucket is closed | `auto_category_components = 0` | Locks in the cleared debt |
| Legacy primitive surface exists | 39 `role="primitive"`, `maturity="legacy"` entries | Documents and ratchets it |
| Layout primitives are real product vocabulary | `stack`, `cluster`, `grid`, `frame`, `block`, `flow`, `layer`, `actions`, `container` are stable layout primitives | Elevates docs/examples |
| Typography helpers look utility-like | `font-sm`, `ui-lg`, `mt-md`, `text-muted`, etc. remain as CSS compatibility surface | Prevents accidental growth |
| Manifest is agent-facing | Generated docs and agents read categories, roles, maturity, authoring hints | Makes guidance machine-visible |

---

## Invariants

1. **No utility-class vocabulary growth.** New spacing/typography single-purpose helpers are not added as stable primitives. Use composition macros or tokens.
2. **No removals in this phase.** Legacy helpers stay available; the goal is signaling and guardrails.
3. **Registry stays source of truth.** Classification lives on `ComponentDescriptor`, and generated docs/manifest project it.
4. **Agents should prefer concepts over strings.** Docs and metadata should steer generated code toward macros/primitives, not raw helper classes.
5. **Authoring hints are descriptor-backed.** Preferred/compatibility signals live on `ComponentDescriptor` or derive from descriptor maturity; the manifest only projects them.

---

## Current Inventory

### Blessed Layout/Composition Primitives

These are the concepts ChirpUI should teach first:

| Primitive | Category | Maturity | Notes |
|-----------|----------|----------|-------|
| `actions` | layout | stable | Action-row composition primitive |
| `block` | layout | stable | Grid/frame item with spans |
| `cluster` | layout | stable | Inline wrapping group |
| `container` | layout | stable | Page/content width constraint |
| `flow` | layout | stable | Flow rhythm primitive |
| `frame` | layout | stable | Fixed-format layout tracks |
| `grid` | layout | stable | Responsive card/list grids |
| `layer` | layout | stable | Overlap/layering primitive |
| `stack` | layout | stable | Vertical rhythm primitive |
| `prose` | typography | stable | Long-form text rhythm |

### Legacy Compatibility Helpers

These are retained, but should not be the vocabulary agents reach for in new code:

`clamp-2`, `clamp-3`, `display`, `focus-ring`, `font-2xl`, `font-base`, `font-lg`, `font-medium`, `font-mono`, `font-sm`, `font-xl`, `font-xs`, `list-reset`, `mb-md`, `measure-lg`, `measure-md`, `measure-sm`, `min-w-0`, `mt-md`, `mt-sm`, `placeholder-inline`, `prose-lg`, `prose-sm`, `scroll-x`, `text-muted`, `truncate`, `ui-base`, `ui-bold`, `ui-label`, `ui-lg`, `ui-medium`, `ui-meta`, `ui-normal`, `ui-semibold`, `ui-sm`, `ui-title`, `ui-xl`, `ui-xs`, `visually-hidden`.

### Specialized Primitive Families

- `ascii`: ASCII/TUI companion primitives and rows/groups.
- `effect`: background, texture, and motion effect primitives.
- `feedback`: streaming/progress/status containers.
- `control`: grouped controls and toggles.

These are valid surfaces, but each family should be documented as a pattern, not expanded into arbitrary CSS knobs.

---

## Sprint Structure

| Sprint | Focus | Effort | Ships Independently? |
|--------|-------|--------|----------------------|
| 0 | Plan + CI ratchet for legacy growth | 1-2h | Yes |
| 1 | Document blessed layout primitives with examples | 3-4h | Yes |
| 2 | Add agent guidance in generated/reference docs | 2-3h | Yes |
| 3 | Review each legacy helper: keep legacy, promote, or deprecate later | 4-6h | Yes |

---

## Sprint 0: Plan + Ratchet

**Goal**: Make the boundary explicit and prevent accidental growth while the rest of the phase lands.

Tasks:

- Add this plan.
- Link it from `docs/INDEX.md`.
- Add manifest tests that:
  - `category="auto"` remains zero.
  - the known utility-like legacy primitive set does not grow silently.
  - blessed primitives remain stable primitives.

Acceptance:

- `uv run pytest tests/test_manifest.py tests/test_registry_emits_parity.py -q` passes.
- `uv run poe build-manifest-check` and `uv run poe build-docs-check` pass.

Progress:

- Added manifest tests that pin the blessed primitive set and require the utility-like legacy primitive set to be reviewed before it grows.

---

## Sprint 1: Blessed Primitive Docs

**Goal**: Make the intended authoring vocabulary obvious to humans and agents.

Tasks:

- Add a guide section to `docs/COMPOSITION.md` or a new `docs/PRIMITIVES.md`.
- Show common recipes with `stack`, `cluster`, `grid`, `frame`, `block`, `actions`, and `prose`.
- Prefer macro examples over raw class examples.
- Cross-link from `LAYOUT.md`, `COMPOSITION.md`, and `COMPONENT-OPTIONS.md` intro text if needed.

Acceptance:

- Docs include one default and one non-default example for each blessed layout primitive.
- No new macro parameters or classes.

Progress:

- Added `docs/PRIMITIVES.md` with examples for stable macro primitives and CSS primitives.
- Linked the guide from `docs/INDEX.md`, `docs/LAYOUT.md`, and `docs/COMPOSITION.md`.

---

## Sprint 2: Agent Guidance

**Goal**: Make generated docs/manifest consumers pick the right primitive first.

Tasks:

- Add concise language to generated/reference docs: "Prefer composition primitives over legacy helpers."
- Add an additive manifest `authoring` hint once docs prove the boundary: `preferred`, `available`, `compatibility`, or `internal`.
- Update `docs/ANTI-FOOTGUNS.md` with the utility-helper boundary.

Acceptance:

- An agent reading `COMPONENT-OPTIONS.md` and `COMPOSITION.md` sees stable composition primitives before legacy helpers.
- No utility-style helper is presented as a recommended primitive.

Progress:

- Added primitive-first guidance to `docs/COMPONENT-OPTIONS.md`.
- Added the utility-helper boundary to `docs/ANTI-FOOTGUNS.md`.
- Added descriptor-backed `authoring` hints to the manifest and generated component reference.

---

## Sprint 3: Legacy Review

**Goal**: Decide what each compatibility helper should become before 1.0.

Tasks:

- Create a small table with each legacy helper and decision:
  - **keep legacy**: compatibility surface, no promotion.
  - **promote**: make it a named concept with docs and rationale.
  - **deprecate later**: add a future deprecation note, but do not remove now.
- Flag any helper used by templates or docs in surprising ways.

Acceptance:

- Every current legacy primitive has a decision.
- Any deprecation path is documented but not enforced unless separately approved.

### Legacy Helper Decisions

| Helpers | Decision | Rationale |
|---------|----------|-----------|
| `clamp-2`, `clamp-3`, `truncate` | keep legacy | Narrow text-bounding escape hatches for constrained cells; useful, but not a composition vocabulary. |
| `focus-ring`, `visually-hidden`, `list-reset` | keep legacy | Accessibility/reset helpers with clear single-purpose behavior; do not promote as authoring primitives. |
| `min-w-0`, `scroll-x`, `placeholder-inline` | keep legacy | Containment/migration helpers for overflow and placeholder layouts; prefer component CSS or layout primitives first. |
| `mt-sm`, `mt-md`, `mb-md` | deprecate later | Spacing shorthands compete directly with `stack()`, `flow`, slots, and component-owned rhythm. Keep for compatibility until a deprecation policy is approved. |
| `display`, `text-muted`, `font-xs`, `font-sm`, `font-base`, `font-lg`, `font-xl`, `font-2xl`, `font-medium`, `font-mono` | keep legacy | Typography compatibility surface; prefer component slots, `prose`, and tokenized component CSS for new work. |
| `measure-sm`, `measure-md`, `measure-lg`, `prose-sm`, `prose-lg` | keep legacy | Prose/measure modifiers are useful but should remain scoped to long-form content, not general layout. |
| `ui-xs`, `ui-sm`, `ui-base`, `ui-lg`, `ui-xl`, `ui-title`, `ui-label`, `ui-meta`, `ui-normal`, `ui-medium`, `ui-semibold`, `ui-bold` | keep legacy | Older text-style classes retained for existing templates; future promotion should happen as named component or typography concepts, not as utility expansion. |

Progress:

- Documented every current legacy primitive with an initial keep/deprecate-later decision.
- No removals or warnings are introduced in this phase.

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-24 | Initial plan | Follow-on to clearing registry auto-category debt; prevents legacy helper drift from becoming a second vocabulary |
| 2026-04-24 | Added docs, guidance, and legacy-helper decisions | Makes the primitive boundary visible to humans and agents without removing compatibility classes |
| 2026-04-24 | Added manifest `authoring` hints | Gives coding agents a machine-readable preferred/compatibility signal without growing CSS vocabulary |
| 2026-04-24 | Added `find --authoring` discovery | Lets humans and agents query preferred primitives or compatibility helpers without parsing JSON manually |
| 2026-04-24 | Added Python authoring helpers | Lets downstream tooling query preferred/compatibility entries without hand-filtering the manifest |
