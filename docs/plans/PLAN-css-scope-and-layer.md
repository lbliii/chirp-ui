# EPIC — CSS as a projection of the Python registry

**Status:** residual backlog
**Drafted:** 2026-04-17
**Owner:** maintainers
**Category:** architecture (load-bearing for `docs/strategy/vision.md § CSS architecture as a registry projection`)

> Current note: the CSS concat pipeline, layer order, registry-emits parity,
> manifest projection, and first envelope conversions have shipped. This file
> now tracks the ongoing `@scope` conversion policy and future evidence-backed
> hardening batches.

## Thesis

CSS is a projection of the registry. Author CSS in partials, generate the
committed `chirpui.css`, keep cascade order public, and make registry/CSS parity
fail fast when either side drifts. The remaining work is not another rebuild of
the CSS pipeline; it is opportunistic conversion of legacy flat partials into
scoped component envelopes.

## Current State

| Surface | Status | Contract |
|---|---|---|
| CSS build | Shipped | `scripts/build_chirpui_css.py` concatenates author partials into generated `src/chirp_ui/templates/chirpui.css`. Edit partials, then run `poe build-css`. |
| Cascade layers | Shipped | Layer order is public API: `chirpui.reset`, `chirpui.token`, `chirpui.base`, `chirpui.component`, `chirpui.utility`, then app overrides. |
| Registry parity | Shipped | `ComponentDescriptor.emits`, `extra_emits`, and `trim_emits` define the class contract; `tests/test_registry_emits_parity.py` catches orphan CSS/classes. |
| Manifest projection | Shipped | `python -m chirp_ui.manifest --json` exposes the registry-visible surface for agents and downstream tooling. |
| `@scope` envelope | Residual | Converted partials use `@layer chirpui.component` plus a component-local `@scope`; legacy partials convert only when touched or when a bounded evidence-backed batch justifies it. |

## Invariants

- Generated `chirpui.css` is never hand-edited.
- No utility-class vocabulary is introduced to avoid a scoped conversion.
- Public BEM classes stay registry-cited, template-emitted intentionally, and
  defined in generated CSS.
- The build stays pure Python or subprocess-to-binary; no runtime dependency is
  added for CSS generation.
- Any scoped conversion ships with regenerated CSS, parity proof, and browser
  proof when selector behavior changes.

## Envelope Convention

```css
@layer chirpui.component {
  @scope (.chirpui-NAME) to (.chirpui-NAME .chirpui-NAME) {
    :scope { /* root */ }
    .chirpui-NAME__part { /* children */ }
    :scope.chirpui-NAME--modifier { /* variants */ }
  }
}
```

Use `045_card.css` as the reference shape. Use `:scope` for the component root,
nest modifiers from `:scope`, and update `extra_emits` only when a real emitted
class cannot be described by the descriptor grammar.

## Shipped Milestones

| Milestone | Result | Proof |
|---|---|---|
| Design lock-in | Layer names, partial paths, build API, and registry emit policy recorded. | `docs/decisions/css-registry-projection.md` |
| Build scaffold | Pure-Python concat pipeline and freshness checks exist. | `tests/test_chirpui_css_concat.py` |
| Partial extraction | Author CSS lives under `src/chirp_ui/templates/css/partials/`. | `poe build-css` |
| Cascade API | Consumer override surface is documented. | `docs/fundamentals/css-override-surface.md` |
| Registry parity | CSS classes and descriptor `emits` are symmetric. | `tests/test_registry_emits_parity.py` |
| Card pilot | A high-traffic component proved the envelope pattern. | `045_card.css`, browser card tests |
| Manifest | Registry facts are machine-readable for agents. | `src/chirp_ui/manifest.py`, `src/chirp_ui/manifest.json` |

## Residual Policy

Do not bulk-convert the remaining flat partials just to raise a percentage.
Convert a partial when one of these is true:

- the same PR already touches that component's CSS,
- a documented bleed risk has enough browser proof to justify a bounded batch,
- a new component is added and needs a scoped authoring model from the start.

Every conversion follows the same proof route: rewrite the partial, run
`poe build-css`, keep registry parity green, add or extend a browser test for
nested-instance bleed when selector semantics changed, and name the converted
partial in the PR.

## Migration status

The envelope convention is the default for new components and for any partial modified in an existing PR. Conversions do not need a dedicated PR — this is a flywheel, not a forced march.

## Steward Notes

- Consulted stewards: Core Registry and Python API; Template, CSS, and Behavior;
  Build Projection; Test Contract; Documentation.
- Contract touched: CSS partial authoring, cascade layer order, descriptor
  `emits`, generated CSS, manifest/docs projection, and agent-facing guidance.
- Accepted findings: keep this plan focused on residual `@scope` conversion and
  do not present shipped layer/emits work as still missing.
- Required proof: `uv run poe verify-generated`,
  `uv run pytest tests/test_chirpui_css_concat.py tests/test_registry_emits_parity.py tests/test_template_css_contract.py tests/test_transition_tokens.py -q`,
  plus browser proof for layout-sensitive envelope conversions.
- Collateral: update `docs/fundamentals/css-override-surface.md`, `docs/strategy/vision.md`, generated
  docs, examples, and changelog fragments only when the public CSS contract
  changes.
- Remaining risk: legacy flat partials remain until touched; this is accepted as
  incremental migration scope.

**Detection.** A partial is "converted" when its first non-comment token is `@layer chirpui.component` (the build's `_wrap_in_layer` treats that as authored layering). Audit:

```bash
# List converted partials
grep -lE '^@layer chirpui\.component' src/chirp_ui/templates/css/partials/*.css
```

**Current converted count:** 24 partials as of 2026-06-15.

Converted partials currently include:

- `011_media-object.css`
- `036_list.css`
- `039_surface.css`
- `041_callout.css`
- `045_card.css`
- `046_video-card.css`
- `047_channel-card.css`
- `052_modal.css`
- `053_drawer.css`
- `065_tray.css`
- `072_badge.css`
- `159_resource-card.css`
- `161_navigation-metadata-authoring.css`
- `162_logo-cloud.css`
- `163_story-card.css`
- `164_cta-band.css`
- `165_pattern-assets.css`
- `166_dense-navigation-primitives.css`
- `167_workspace-primitives.css`
- `168_maturity-primitives.css`
- `169_data-grid.css`
- `170_context-menu.css`
- `171_combobox.css`
- `172_date-picker.css`

**Legacy (flat, opportunistic conversion):** all other partials in
`src/chirp_ui/templates/css/partials/`. No global checklist is maintained —
the grep above is the source of truth when this count drifts.

**Epic closure signal.** The epic can close when:

1. The four mechanism invariants are green: concat build, layer declaration, registry–CSS parity, envelope-partial opt-out — all load-bearing in CI.
2. At least one high-traffic component (card) is in envelope form and has browser-test coverage of its variants.
3. The policy is documented in `CLAUDE.md § Key conventions` and new-component guidance points at card as the reference.

Percentage converted is not an epic gate — half-converted is a supported steady state.

### Hardening batch 1 — priority order

The opportunistic policy is the default, but a small bounded batch of deliberate conversions is justified when a partial carries documented bleed risk that organic touches may not reach for months. Batch 1 (planned 2026-04-20, see `docs/plans/done/PLAN-envelope-hardening-batch-1.md`) covered six conversions, ordered by intersecting bleed evidence with existing browser-test coverage:

| # | Partial | Bleed-risk justification | Browser test |
|---|---------|--------------------------|--------------|
| 1 | `065_tray.css` | Sharp-edge memory (`feedback_tray_shell_sharp_edges.md`); overlay panel that hosts other components. | `tests/browser/test_tray.py` (existing) |
| 2 | `053_drawer.css` | Overlay container; drawers commonly hold forms/lists where outer hover states could leak. | `tests/browser/test_drawer.py` (existing) |
| 3 | `052_modal.css` | Modal-in-modal is a real pattern (confirmation inside a settings modal). | `tests/browser/test_modals.py` (existing) |
| 4 | `039_surface.css` | Parent epic E2 cited `surface`-inside-`surface` as a live hazard. Highest-leverage conversion in this batch. | `tests/browser/test_surface.py` (new in this batch) |
| 5 | `041_callout.css` | Surface-shaped container often nested inside a `surface` or `card`; callout-in-callout pattern (notice → expandable detail) carries the same risk. | `tests/browser/test_callout.py` (new in this batch) |
| 6 | `046_video-card.css` + `047_channel-card.css` | Mirror `card`'s structure (border + radius + overflow-clip + hover) but live outside `.chirpui-card`'s `@scope`, so the pilot's bleed fix doesn't reach them. | `tests/browser/test_video_card_variants.py`, `tests/browser/test_channel_card_variants.py` (both new) |

After batch 1, opportunistic mode resumed for the remaining flat partials. **No further deliberate batch is planned**; future batches require their own justification document with evidence on par with this one.

### Next opportunistic queue

These flat partials are the highest-value conversions when touched for adjacent
work. The queue is not permission for a bulk migration; it is proof routing for
the next natural edits.

| Partial | Why next | Required proof |
|---|---|---|
| `071_button.css` | Buttons appear inside cards, command bars, forms, tables, modals, and nav chrome; hover/focus state bleed is high-impact. | Render tests for link/button modes, CSS contract tests, and browser focus/hover proof if selectors change. |
| `070_form-fields.css` | Fields nest inside surfaces, panels, modals, drawers, and inline-edit flows. | Form render tests plus browser focus/error/disabled proof for any selector rewrite. |
| `059_table.css` | Tables host badges, buttons, row actions, links, and dense records. | Table render tests plus browser proof for dense rows and nested controls. |
| `027_navbar.css` | Global nav contains links, dropdown triggers, badges, and responsive actions. | Navigation render tests plus browser proof for focus, dropdown, and mobile overflow behavior. |
| `029_sidebar.css` | Sidebar hosts route links, nested sections, counters, and app shell overflow. | App-shell/sidebar render tests plus browser proof for active/focus and overflow behavior. |
| `054_tabs.css` / `067_tabs-panels.css` | Tabs can be route navigation or true panels; active/focus styles are easy to over-broaden. | Tabs render tests plus browser proof for active state, focus, and panel ownership. |

### Per-PR conversion template

Every conversion (deliberate or opportunistic) follows the same five steps:

1. **Rewrite the partial** to the envelope form. Use `045_card.css` as the structural reference: open with `@layer chirpui.component { @scope (.chirpui-NAME) to (.chirpui-NAME .chirpui-NAME) { … } }`, use `:scope` for self-reference, nest `&.chirpui-NAME--modifier` for variants.
2. **Rebuild the monolith.** `poe build-css` regenerates `src/chirp_ui/templates/chirpui.css`. Commit the regenerated file with the partial change in the same PR.
3. **Run CI locally.** `poe ci` — must be green. The concat test (`tests/test_chirpui_css_concat.py`) and the registry-emits parity test (`tests/test_registry_emits_parity.py`) are the load-bearing gates.
4. **Add or extend a browser test.** If the component already has one under `tests/browser/`, extend it to cover a nested-instance bleed case if not already present. If not, add a new `tests/browser/test_<component>.py` following the pattern in `### Browser test: bleed case` below.
5. **PR description.** Cite this `Migration status` section, name the partial converted, and if part of a deliberate batch, link to the batch plan and the row in its priority-order table.

When the conversion consolidates a compound class the descriptor grammar can't express, update the component's `extra_emits` in `src/chirp_ui/components.py` in the same PR — the parity test will surface the gap if missed.

### Browser test: bleed case

Use `tests/browser/test_card_variants.py` as the reference for testing nested-instance bleed. The pattern:

1. Render two instances of the component nested inside each other (outer with one variant, inner with a different variant).
2. Hover or focus the outer instance.
3. Assert the inner instance's computed style for the bleed-prone property (commonly `border-color`, `box-shadow`, or `background`) matches the inner's declared value, **not** the outer's hover state.

Tests added in batch 1 (surface, callout, video-card, channel-card) all follow this template. The test should fail on the unconverted partial (proving it catches the bleed) and pass after conversion — if it passes on both, either the bleed wasn't actually present or the test isn't asserting the right property.

## Open items

- **S0 decision: layer namespace.** Recommend `chirpui.*`. Needs a second opinion before S3 ships.
- **S0 decision: partials directory.** Recommend `src/chirp_ui/templates/css/`. Needs sign-off before S2 ships.
- **S7 scope creep risk.** Don't let the manifest absorb "and also generate docs / and also generate the showcase" — that's a separate epic.

## Related

- `docs/strategy/vision.md § CSS architecture as a registry projection` — the *why* this epic exists
- `examples/css-scope-prototype/card.scope.css` — S5 starting point
- `CLAUDE.md § Sharp edges — what's been hardened` — the drift cost history (E3)
- `docs/decisions/css-registry-projection.md` — decision record for CSS as a
  registry projection
- root `AGENTS.md` Non-Negotiables — R6 / E7 free-threading constraint
