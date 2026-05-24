# chirp-ui: Search Shell Contracts

Status: shipped
Date: 2026-05-21
Trigger: The component showcase catalog shell proved that Chirp UI can build
advanced HTMX/Alpine search surfaces, but also exposed missing contracts around
counts, responsive command surfaces, rails, dense results, and progressive
enhancement.

Depends on:

- [../PLAN-application-chrome-system.md](../PLAN-application-chrome-system.md)
- [../../HTMX-PATTERNS.md](../../components/htmx-patterns.md)
- [../../RESPONSIVE.md](../../fundamentals/responsive.md)
- [../../LAYOUT.md](../../fundamentals/layout.md)
- [../../DENSE-NAVIGATION-RECIPES.md](../../patterns/dense-navigation-recipes.md)
- [../../PUBLIC-SURFACE-STABILIZATION.md](../../safety/public-surface-stabilization.md)

## Goal

Turn the catalog-shell exercise into implementable contracts without
prematurely creating a mega-component or utility-class vocabulary.

This plan is recipe-first. Public macro promotion is allowed only after the
contract is proven in examples, docs, tests, and at least two repeated real
composition shapes.

## Execution Log

- 2026-05-21: Started the recipe-first execution slice. Added the canonical
  search-shell recipe doc, linked it from the documentation index, extended
  HTMX/responsive/verification guidance, and added render/browser proof for the
  component-showcase catalog shell. Public macro promotion remains not-now.
- 2026-05-21: Added a primitive-quality pass from the catalog-shell findings:
  command bars now provide a stronger default surface and direct search/hint
  wrapping behavior, badges use softer compact pill defaults, cards/resource
  cards get quieter dense spacing, and catalog rails align headers without
  stretched side rails.
- 2026-05-21: Started the layout-affinity rollout as a recipe-first prototype.
  Added `docs/decisions/layout-affinity.md`, marked the catalog shell command
  surface with `data-chirpui-role` / `data-chirpui-pressure` /
  `data-chirpui-affinity`, and taught `command_bar` to resolve those signals
  without adding public macro params or registry fields.
- 2026-05-21: Proved the second layout-affinity consumer on the
  component-showcase data filter toolbar. The shipped `filter_bar` composite now
  resolves the same parent-scoped recipe attributes as `command_bar`, with
  render, CSS, docs, and browser overflow proof across phone, tablet, and
  desktop widths.
- 2026-05-21: Added the third layout-affinity consumer in `card` internals.
  Card header content, actions, badges, top metadata, and footer metadata now
  expose readable role/pressure/affinity attributes, and card scoped CSS
  resolves those signals without adding macro parameters or registry fields.
- 2026-05-21: Captured descriptor/manifest readiness without changing public
  schema. The RFC now proposes separate `layout_resolver` and `layout_parts`
  projection shapes for a future manifest bump, and tests gate against
  accidental `chirpui-manifest@5` schema drift.
- 2026-05-21: Added an authoring vocabulary contract for emitted
  `data-chirpui-role`, `data-chirpui-pressure`, and `data-chirpui-affinity`
  values. Source-scanning tests now prevent undocumented layout-affinity tokens
  from entering templates while the contract is still recipe-first.

## Steward Notes

Consulted:

- Core Registry/API steward: requested, timed out.
- Template/CSS/Behavior steward: requested, timed out.
- Examples/Showcase steward: requested, timed out.
- Documentation/Published Site steward: requested, timed out.
- Test Contract steward: returned full signals.

Applied standing scoped guidance from all steward `AGENTS.md` files:

- Registry remains source of truth for promoted components.
- CSS partials and generated CSS move together for shipped components.
- Examples may teach recipes, but must not invent fake public APIs.
- Docs must distinguish shipped contracts from active plans.
- Tests should assert semantics and behavior, not broad snapshots.

## Task Backlog

### Task 1. Progressive Enhancement Contract

Type: contract documentation plus tests
Priority: P1
Promote to public macro API: no

Define the baseline rule for HTMX/Alpine recipes:

- Every enhanced control has a real `href` or `action`.
- Forms preserve submitted state without JavaScript.
- HTMX enhancement names the target boundary, selected fragment, URL behavior,
  and concurrency behavior.
- Alpine is used only for local state that does not own server data.

Acceptance:

- `docs/components/htmx-patterns.md` names the rule and shows a good and bad example.
- Catalog shell markup follows the contract for search, hints, reset, rails,
  version filters, topic filters, and empty states.
- Render tests assert non-JS fallback paths exist.

Required proof:

- Targeted render tests for `href`, `action`, `method`, hidden state, `hx-target`,
  `hx-select`, and `hx-push-url`.
- Browser proof that a hint click and reset update the URL and visible results.

Collateral:

- `docs/components/htmx-patterns.md`
- `examples/component-showcase/templates/showcase/catalog_shell.html`
- `tests/test_data_integration.py`
- Browser test fixture if the behavior moves beyond smoke coverage.

Not now:

- Do not add a generic `search_shell()` macro in this task.

### Task 2. Scoped Count Contract

Type: contract documentation plus data/render tests
Priority: P2
Promote to public macro API: no

Define count scopes used in dense search shells:

- `visible`: count after current query, filters, and version.
- `filtered`: count after query and filters, before a local view split.
- `available`: count available if a facet is selected under current query.
- `total` or `corpus`: unfiltered source count.

Default rule: rails and workspace summaries use the same visible scope unless
the UI explicitly labels a different scope.

Acceptance:

- Catalog shell rails, family list, metrics, product cards, and coverage labels
  use consistent `docs`, `docset`, and `product` language.
- Singular/plural labels are correct.
- Count aria labels describe the same object as visible text.

Required proof:

- Tests for all-products latest counts, selected category counts, and query
  scoped counts.
- Tests for singular and plural labels.
- Browser proof for HTMX filter clicks if counts are updated dynamically.

Collateral:

- `docs/components/htmx-patterns.md` or a new search-shell recipe doc.
- `tests/test_data_integration.py`

Not now:

- Do not add a `CountScope` Python API until another component consumes it.

### Task 3. Responsive Command Surface

Type: recipe contract, possible later component variant
Priority: P2
Promote to public macro API: maybe later

Define a search-with-suggestions command surface that does not rely on
horizontal scrolling for normal controls.

Acceptance:

- Wide: search and suggestions sit in stable columns.
- Medium: controls stack in source order.
- Narrow: search button remains reachable; suggestion buttons wrap predictably.
- No document-level horizontal overflow at stress widths.
- Touch target sizing follows existing control-size contracts.

Required proof:

- CSS contract for the chosen breakpoint rules.
- Browser viewports: 320, 390, 768, 1024, 1280.
- Assertions: search input visible, submit visible, suggestions visible or
  intentionally collapsed, no horizontal overflow.

Collateral:

- `docs/fundamentals/responsive.md`
- `docs/fundamentals/layout.md`
- `examples/component-showcase/templates/base.html`
- `tests/test_responsive_contract.py`
- `tests/browser/` coverage if promoted beyond showcase-local CSS.

Not now:

- Do not add `command_bar(layout="search-suggestions")` until the recipe repeats.

### Task 4. Search Shell Recipe

Type: advanced recipe
Priority: P2
Promote to public macro API: no

Document and test the full recipe shape:

- Query form.
- Hidden state fields.
- Suggested searches.
- Facet rails.
- Version or scope filter.
- Results workspace.
- Empty state.
- Pending feedback.
- URL-preserving HTMX swaps.

Acceptance:

- Recipe is copyable without relying on unpublished classes as public API.
- The recipe states which classes are example-local versus registry-owned.
- The non-JS path and HTMX path share the same URL contract.

Required proof:

- Structural route tests for form, state inputs, rails, result cards, empty
  state, and HTMX target boundaries.
- Browser tests for typing, hint click, reset, rail click, and back/forward URL.

Collateral:

- New `docs/patterns/search-shell-recipes.md` or a section in `docs/components/htmx-patterns.md`.
- Showcase route and tests.
- Published site page only after the recipe settles.

Not now:

- Do not publish it as a first-class macro or manifest component.

### Task 5. Dense Result Item Primitive Evaluation

Type: promotion evaluation
Priority: P2
Promote to public macro API: maybe after evidence

Evaluate whether the catalog result card should become a reusable dense result
item primitive.

Candidate anatomy:

- Eyebrow or family.
- Title link.
- Source/site metadata.
- Count or status slot.
- Summary.
- Coverage/meta row.
- Tags/topics slot.
- Nested links slot.

Acceptance:

- At least two recipes repeat the same anatomy.
- Existing `resource_card` cannot express the shape without awkward overrides.
- The primitive has clear slot ownership and no product-specific vocabulary.

Required proof if promoted:

- Component descriptor with emits and maturity.
- Kida macro with doc block and escaped attributes.
- CSS partial plus generated `chirpui.css`.
- Strict-undefined and slot render tests.
- Browser overflow and focus tests.
- Generated `COMPONENT-OPTIONS.md` and manifest freshness.

Collateral:

- `src/chirp_ui/components.py`
- `src/chirp_ui/templates/chirpui/<name>.html`
- `src/chirp_ui/templates/css/partials/<nnn>_<name>.css`
- `docs/COMPONENT-OPTIONS.md`
- Showcase examples and changelog fragment.

Not now:

- Do not promote from the catalog shell alone.

### Task 6. Facet Rail Contract

Type: recipe contract, possible later primitive
Priority: P2
Promote to public macro API: maybe later

Define the contract for rail-based facets:

- Link-native fallback.
- Active state.
- Count scope.
- All/reset item.
- Query-parameter retention.
- HTMX target and URL push behavior.
- Compact responsive fallback.

Acceptance:

- Category and family rails in the catalog shell follow the same active/count
  semantics.
- Rails expose real navigation labels and do not depend on visual ordinals.
- Mobile/tablet behavior is intentional: horizontal strip, stacked panel, tray,
  or another named fallback.

Required proof:

- Render tests for all item, active item, inactive item, counts, and hrefs.
- Browser tests for rail click, URL update, visible result update, and focus.
- CSS/browser proof for compact widths if the rail layout changes.

Collateral:

- Search-shell recipe docs.
- `docs/fundamentals/responsive.md` if a rail fallback rule is standardized.

Not now:

- Do not add `facet_rail()` until more than one shell repeats this exact rail
  anatomy.

### Task 7. Pending And Settling Feedback Primitive Evaluation

Type: behavior contract, possible later Alpine primitive
Priority: P2
Promote to public macro API: maybe later

Define an accessible async-region status pattern:

- Scoped pending boundary.
- `role="status"` and `aria-live`.
- HTMX `hx-indicator` wiring.
- Settle/error clearing.
- Reduced-motion behavior for visual settle animations.
- No global listener reactions to unrelated requests.

Acceptance:

- Catalog shell pending state is scoped and cannot stick after error.
- Status text is available to assistive tech.
- Visual feedback does not shift layout unexpectedly.

Required proof:

- Render tests for indicator ID, role, live region, and request targets.
- Browser tests for pending during request and cleared after settle/error.
- CSS contract for reduced motion.

Collateral:

- `docs/components/htmx-patterns.md`
- `docs/components/alpine-magics.md` if behavior becomes named Alpine data.
- `src/chirp_ui/alpine.py` only if runtime metadata is added.

Not now:

- Do not add a named Alpine controller until the behavior repeats.

### Task 8. Rail Header Contract

Type: recipe guidance
Priority: P3
Promote to public macro API: no

Define rail header anatomy for dense shells:

- Optional ordinal.
- Required text label.
- Relation to the rail `nav` aria label.
- Stacked compact layout by default.
- No orientation conveyed only by number.

Acceptance:

- Catalog shell category and family rail headers follow the anatomy.
- Documentation says when ordinals are useful and when to omit them.

Required proof:

- Render tests for label text and nav labels.
- CSS contract or browser proof if responsive rail header layout is shipped in
  a component CSS partial.

Collateral:

- Search-shell recipe docs.
- Possibly `docs/patterns/navigation.md` if rail guidance generalizes.

Not now:

- No `rail_header()` macro without repeated use.

### Task 9. Responsive Tier Guidance

Type: docs plus test helper
Priority: P3
Promote to public macro API: no

Define named responsive test tiers for dense app shells:

- Phone narrow: 320.
- Phone common: 390.
- Tablet: 768.
- Laptop: 1024.
- Desktop: 1280.

Acceptance:

- Docs explain when CSS-string tests are enough and when browser proof is
  required.
- Browser helpers can run a shell recipe through the tier matrix.
- Catalog/search shell recipes use the matrix.

Required proof:

- Test helper or shared constants for the viewport matrix.
- At least one browser test using the matrix for a dense shell.
- Docs link from responsive guidance to verification guidance.

Collateral:

- `docs/fundamentals/responsive.md`
- `docs/safety/verification.md`
- `tests/browser/` helper or fixture.

Not now:

- Do not block every component change on the full matrix; use it for
  layout-sensitive shells and promoted responsive primitives.

### Task 10. Docs Browser / Catalog Shell Advanced Recipe

Type: durable advanced recipe
Priority: P2
Promote to public macro API: no

Graduate the catalog shell from ad hoc showcase experiment to a durable
advanced recipe after the preceding contracts are documented and tested.

Acceptance:

- The recipe has stable dummy data, no vendor-specific names, and clear scope.
- It demonstrates layered rails, search, facets, result cards, counts,
  responsive behavior, and progressive enhancement.
- It is cited by docs as an advanced composition, not a public macro.

Required proof:

- Targeted structure tests; no whole-template snapshots.
- Browser smoke for search, category, family, version, reset, and responsive
  widths.
- No stale classes, missing CSS, or generated-output drift.

Collateral:

- `examples/component-showcase/`
- `docs/patterns/search-shell-recipes.md` or equivalent canonical recipe doc.
- `site/content/` only when ready to publish.

Not now:

- No `catalog_shell()` component.
- No manifest entry for the full shell recipe.

## Parity Matrix

| Contract | API/CLI | Programmatic | Protocol | Schema/Types | Docs | Examples | Tests |
|---|---|---|---|---|---|---|---|
| Progressive enhancement | No public API | Recipe conventions | HTMX attributes, fallback links/forms | None | Required | Required | Render + browser |
| Scoped counts | No public API initially | Context/data helper optional later | URL/query scope | None initially | Required | Required | Render + browser |
| Responsive command surface | Maybe later macro param | Existing `command_bar` first | None | Descriptor only if promoted | Required | Required | CSS + browser |
| Search shell recipe | No macro | Example route/context | HTMX URL/fragment contract | None | Required | Required | Render + browser |
| Dense result item | Maybe component later | Macro slots if promoted | None | Descriptor if promoted | Required if promoted | Required | Render + CSS + browser |
| Facet rail | Maybe component later | Macro slots if promoted | HTMX URL parity | Descriptor if promoted | Required | Required | Render + browser |
| Pending feedback | Maybe Alpine primitive later | Runtime metadata if promoted | HTMX lifecycle | Alpine metadata if promoted | Required | Required | Render + browser |
| Rail header | No macro initially | Recipe anatomy | None | None | Required | Required | Render/CSS |
| Responsive tiers | No API | Test helper constants | None | None | Required | Optional | Browser matrix |
| Catalog shell recipe | No macro | Showcase route/context | HTMX fragment contract | None | Required | Required | Render + browser |

## Not Now

- No new runtime dependency.
- No manifest schema change.
- No public import.
- No mega-shell macro.
- No utility-class vocabulary.
- No broad visual snapshots as the main proof.
- No generated `chirpui.css` edits without CSS partial changes.

## Suggested Execution Order

1. Task 1: progressive enhancement contract.
2. Task 2: scoped count contract.
3. Task 3: responsive command surface.
4. Task 4: search shell recipe.
5. Task 9: responsive tier guidance and browser helper.
6. Task 10: durable catalog shell recipe.
7. Task 6: facet rail contract.
8. Task 7: pending/settling feedback evaluation.
9. Task 8: rail header guidance.
10. Task 5: dense result item primitive evaluation.

This order protects user-visible correctness and responsive behavior before
adding public component surface area.
