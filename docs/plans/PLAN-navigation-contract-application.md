# chirp-ui: Navigation Contract Application

Status: active plan
Date: 2026-05-03
Depends on: [PLAN-navigation-density-study.md](PLAN-navigation-density-study.md)

Progress:

- Phase 1 accepted: `docs/NAVIGATION.md` is the canonical repository guidance.
- Phase 2 accepted: component showcase includes a dense object-navigation example
  composed from existing primitives.
- Phase 3 accepted: `breadcrumbs(..., overflow="collapse", max_items=4)` ships
  opt-in middle-crumb overflow for deep path trails.
- Phases 4-6 remain not-now until a consuming app proves the need.

## Goal

Apply the navigation density study to ChirpUI in small, contract-first slices:

1. document the navigation decision model,
2. demonstrate dense navigation with existing primitives,
3. harden the highest-value existing primitives,
4. only then evaluate whether a new composite component is justified.

This plan intentionally does not start with a new dense-header component. The
first deliverable is a better navigation contract that reduces one-off chrome
and prevents route links, tab widgets, disclosures, command menus, and search
launchers from being modeled as the same thing.

## Affected Stewards

- Documentation: new canonical navigation guidance and site-published copy.
- Template/CSS/Behavior: examples and later macro/CSS hardening.
- Core Registry/API: descriptor, manifest, and generated docs only when public
  macro signatures or new components ship.
- Tests: render, strict-undefined, CSS contract, responsive/browser proof for
  accepted implementation changes.

## Target Contract

| User need | Blessed ChirpUI surface | Notes |
|-----------|-------------------------|-------|
| App/product identity | `app_shell`, `navbar`, brand slots | Persistent global context. |
| Broad app movement | `primary_nav`, `sidebar`, `nav_tree` | Product/section navigation, not commands. |
| Deep hierarchy | `nav_tree(branch_mode="linked")`, drawer/tray on phones | Avoid three-tier top bars. |
| Object/path context | `breadcrumbs`, page header metadata | Needs overflow guidance. |
| Local object views | `render_route_tabs` / `route_tabs` | Route links with `aria-current`, not `tablist`. |
| In-place panels | `tabs_panels`, `tabs` where panel semantics are satisfied | True tab widgets require tab ARIA/focus behavior. |
| Commands/actions | `command_bar`, `action_strip`, `dropdown_menu` | Command menus may use menu semantics; route nav should not. |
| Search/jump | `command_palette`, `command_palette_trigger` | Compact trigger, spacious overlay. |
| Attention/status | badges, counters, notification actions | Needs stable loading/layout guidance. |
| Overflow | scroll strip, drawer/tray, overflow menu, selective hide | Must be documented by layer. |

## Phase 1: Canonical Navigation Guidance

Create `docs/NAVIGATION.md` and publish or mirror the relevant content into the
site docs if the app-shell docs are the canonical site entrypoint.

Content:

- navigation layer model: global shell, sidebar/product nav, object context,
  route tabs, page toolbars, commands, status, overflow
- decision matrix mapping user need to component
- ARIA guidance:
  - route navigation uses links, labelled `nav`, and `aria-current`
  - true tabs use tablist/tab/tabpanel semantics
  - disclosure navigation should not be turned into ARIA menus
  - command menus are distinct from navigation disclosure
- responsive overflow policy:
  - keep context and primary action reachable
  - keep local route tabs horizontally scrollable
  - move broad/deep navigation into drawer/tray
  - collapse low-frequency utilities into overflow
  - hide only duplicate shortcuts
- examples of what not to do:
  - topbar with three navigation depths
  - dropdown menu roles for normal route links
  - route links modeled as tabs
  - utility-class escape hatches for density

Files:

- `docs/NAVIGATION.md`
- `docs/INDEX.md`
- likely `site/content/docs/app-shell/_index.md` or a new site docs page

Proof:

- `uv run poe build-docs-check`
- docs link check if/when one exists

Collateral:

- No generated component docs unless macro signatures change.
- No changelog fragment unless this ships as user-facing release content.

## Phase 2: Dense Navigation Example Using Existing Primitives

Add a copyable example before adding API. The example should show a dense object
navigation layout assembled from existing components:

- global/app row: brand, product menu trigger, command/search trigger, utility
  action group, account/user slot placeholder
- object context row: breadcrumbs, object title/meta, object actions
- local route row: route tabs with badges/counters
- mobile/responsive behavior: route tabs scroll; deep nav moves into drawer/tray;
  non-critical utilities collapse into an overflow action

Recommended location:

- `examples/component-showcase/templates/showcase/navigation.html` if the page
  remains readable
- otherwise a focused partial such as
  `examples/component-showcase/templates/showcase/_dense_navigation.html`

Constraints:

- Use `stack()`, `cluster()`, `grid()`, `frame()`, and `block()` composition
  primitives where possible.
- Do not add utility classes.
- Do not add inline scripts.
- Avoid public macro params until the example proves what is missing.

Proof:

- render/showcase tests that cover the example if existing patterns provide one
- browser responsive screenshots if CSS changes are needed
- `uv run poe build-docs-check`

Collateral:

- `docs/NAVIGATION.md` should cite the example.
- `site/content/docs/app-shell/_index.md` can link to it if site docs publish
  examples.

## Phase 3: Breadcrumb Overflow

Implement the first component hardening only after the guidance and example make
the desired behavior concrete.

Potential API:

```html
{{ breadcrumbs(items, overflow="collapse", max_items=4) }}
```

Open design questions:

- Should overflow be built into `breadcrumbs()` or offered as a separate
  `breadcrumbs_overflow()` macro to avoid expanding the stable macro too much?
- Should collapsed middle crumbs be a disclosure/list of links rather than an
  ARIA menu?
- How should the ordered-list semantics be preserved when middle items collapse?
- Which items are always visible: first/current, first/previous/current, or
  configurable?

Expected behavior:

- Preserve labelled `nav`.
- Preserve current-page state.
- Keep separators presentation-only.
- Avoid overflow on narrow headers.
- Work with strict undefined and minimal dicts.

Files if accepted:

- `src/chirp_ui/templates/chirpui/breadcrumbs.html`
- `src/chirp_ui/templates/css/partials/026_breadcrumbs.css`
- `src/chirp_ui/components.py`
- generated `src/chirp_ui/templates/chirpui.css`
- generated `src/chirp_ui/manifest.json` if descriptor projection changes
- generated `docs/COMPONENT-OPTIONS.md`
- examples and site docs

Proof:

- focused render tests for normal, collapsed, minimal, and current item states
- `tests/test_template_css_contract.py`
- `tests/test_registry_emits_parity.py`
- `tests/test_strict_undefined.py` if new dict access appears
- responsive browser coverage at phone/tablet/desktop if CSS changes
- `uv run poe build-docs-check`

Collateral:

- `docs/NAVIGATION.md`
- `docs/RESPONSIVE.md`
- examples/showcase
- changelog fragment if behavior ships

## Phase 4: Counter And Badge Stability

Define and, if needed, implement stable count behavior for nav contexts.

Scope:

- `route_tabs`
- `primary_nav`
- `sidebar_link`
- possibly `nav_tree` badges

Guidance:

- reserve stable inline space when a count is expected
- avoid multiple independent layout shifts from async counters
- support hidden/loading states without changing semantic labels incorrectly
- include accessible count text when visual badges are compact

Potential API ideas:

- `badge_loading`
- `badge_reserved`
- item-level `badge_label`

These are speculative until Phase 1 and Phase 2 expose a real need.

Proof:

- render tests for badge/counter states
- responsive/browser layout proof if CSS dimensions change
- generated docs/manifest checks for public params

Collateral:

- component docs
- `docs/NAVIGATION.md`
- examples/showcase
- changelog fragment if public behavior changes

## Phase 5: Command Launcher Placement

Clarify and improve the compact search/jump trigger story without building a
bespoke header search clone.

Scope:

- document where `command_palette_trigger` belongs in app chrome
- consider a dense trigger example with visible shortcut hint and accessible
  label
- avoid coupling command palette behavior to app shell layout

Potential implementation:

- example-only first
- later macro refinement if current trigger cannot express:
  - icon + placeholder
  - keyboard hint
  - compact/expanded responsive presentation

Proof:

- render tests if macro changes
- accessibility checks for accessible names
- browser checks if responsive CSS changes

Collateral:

- `ALPINE-MAGICS.md` only if behavior changes
- `COMPONENT-OPTIONS.md` if signature changes

## Phase 6: Evaluate A Composite

Only after two consuming examples or apps show the same shape, consider a
composite such as `object_chrome` or `dense_navigation_shell`.

Acceptance bar for a new component:

- two real consumers with matching structure
- clear slot contract for brand/context/search/utilities/local nav
- responsive overflow behavior that cannot be cleanly expressed by existing
  primitives
- descriptor, manifest, docs, examples, tests, and changelog ready in the same
  PR

Default decision: document composition rather than ship a composite.

## Parity Matrix

| Contract | API/CLI | Programmatic | Protocol | Schema/Types | Docs | Examples | Tests |
|----------|---------|--------------|----------|--------------|------|----------|-------|
| Navigation decision model | N/A | N/A | N/A | N/A | Phase 1 | Phase 2 | docs freshness |
| Dense object navigation example | N/A | N/A | N/A | N/A | Phase 1/2 | Phase 2 | render/browser if CSS changes |
| Breadcrumb overflow | macro params if accepted | descriptor/manifest | route links/HTMX attrs unchanged | item dict shape documented | Phase 3 | Phase 3 | render, strict, CSS, responsive |
| Counter stability | macro params if accepted | descriptor/manifest | async/OOB guidance | item badge fields | Phase 4 | Phase 4 | render/browser |
| Command launcher placement | possible macro params | descriptor/manifest if changed | dialog/Alpine unchanged unless refined | trigger params if changed | Phase 5 | Phase 5 | render/a11y/browser |
| Future composite | public macro | descriptor/manifest | shell/chrome swap ownership | slots/items | Phase 6 | Phase 6 | full component contract |

## Not Now

- Do not create a `github_header`, `mega_nav`, or product-specific clone.
- Do not add utility classes for dense spacing, visibility, or alignment.
- Do not change route tabs into ARIA tabs.
- Do not use ARIA menu roles for ordinary navigation disclosure.
- Do not add new macro params without a concrete example or implementation need.
- Do not touch generated `chirpui.css`, `manifest.json`, or generated docs by
  hand.

## Done Criteria

- Phase 1 is complete when `docs/NAVIGATION.md` is linked from `docs/INDEX.md`
  and site/app-shell docs point to the canonical guidance.
- Phase 2 is complete when a dense navigation example exists using current
  primitives and responsive behavior has been inspected.
- Later implementation phases are complete only when descriptors, CSS partials,
  generated CSS, manifest, generated docs, examples, tests, and changelog are
  updated as required by the touched public surface.
- Full CI target remains `uv run poe ci`; narrower PRs must state why narrower
  checks were sufficient.
