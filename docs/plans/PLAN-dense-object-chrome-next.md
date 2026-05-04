# chirp-ui: Dense Object Chrome Next

Status: active plan
Date: 2026-05-03
Depends on:

- [PLAN-navigation-density-study.md](PLAN-navigation-density-study.md)
- [PLAN-navigation-contract-application.md](PLAN-navigation-contract-application.md)
- [../NAVIGATION.md](../NAVIGATION.md)

## Goal

Turn the dense navigation work into buildable, reusable app patterns without
shipping a premature all-in-one header component.

The next work should make GitHub-like object pages easier to build:

- global product controls,
- object breadcrumbs and metadata,
- search or command launch,
- compact utility actions,
- local route tabs,
- stable counters and badges,
- responsive overflow behavior.

The target is a blessed ChirpUI composition path, not a `github_header()` clone.

## Progress

- Phase 1 accepted: the component showcase now includes project/repository and
  admin/settings dense object chrome recipes.
- Phase 2 accepted for `route_tabs` and `primary_nav`: item badges now support
  accessible labels, reserved count space, and loading placeholders.
- Phase 3 accepted: `command_palette_trigger()` supports compact dense-chrome
  options for icon, placeholder, shortcut, accessible label, and density.
- Phases 4-5 remain not-now until the recipes prove a repeated object header
  shape and responsive browser coverage is scheduled.

## Research Snapshot

Current primitives already cover most of the contract:

| Need | Current surface | Gap |
|------|-----------------|-----|
| Broad product navigation | `primary_nav` | Needs clearer dense examples and badge stability proof. |
| Object/path context | `breadcrumbs` | Middle-crumb collapse exists; object title/action composition still varies. |
| Local route-backed views | `route_tabs` | Uses link semantics; badge states are minimal. |
| Commands/actions | `command_bar`, `action_strip`, `dropdown_menu` | Recipes need to separate navigation links from commands. |
| Search/jump launch | `command_palette_trigger`, `command_palette` | Trigger is functional but not expressive enough for dense app chrome examples. |
| Compact counts | `inline_counter`, route/primary nav badges | No reserved/loading count contract yet. |
| Object headers | `entity_header`, `document_header`, `page_header` | No canonical dense object header recipe tying breadcrumbs, metadata, and actions together. |
| Responsive overflow | route tabs, primary nav, breadcrumbs | Needs browser proof for complete object chrome composition. |

## Non-Goals

- Do not add utility classes for dense spacing or hiding.
- Do not build a branded GitHub clone.
- Do not model route links as ARIA tabs.
- Do not turn normal navigation disclosure into ARIA menu items.
- Do not add a public `object_chrome()` or `workspace_header()` until at least
  two examples repeat the same structure and prove the missing API.

## Affected Stewards

- Documentation: recipes, examples, and plan/index clarity.
- Template/CSS/Behavior: command trigger, counters, route tab and nav badge
  states, responsive overflow.
- Core Registry/API: descriptors, manifest, generated options, and changelog
  only when macro signatures or emitted classes change.
- Tests: render tests, strict undefined coverage, CSS/registry parity, and
  browser/responsive proof for accepted implementation slices.

## Phase 1: Dense Object Recipes

Create two copyable examples before adding a composite API:

1. Project/repository object page:
   - global product row,
   - breadcrumb path,
   - object title and metadata,
   - primary action plus overflow actions,
   - route tabs with counters,
   - page-local toolbar.
2. Admin/settings object page:
   - global app context,
   - settings object breadcrumbs,
   - route tabs or sidebar distinction,
   - command/search trigger,
   - saved/dirty/status metadata.

Candidate locations:

- `examples/component-showcase/templates/showcase/navigation.html`
- a focused partial such as
  `examples/component-showcase/templates/showcase/_dense_object_chrome.html`
- published docs under `site/content/docs/app-shell/` if the site should expose
  the recipe.

Acceptance:

- Examples use composition primitives and existing components.
- Examples do not add public macro parameters.
- Docs explain which layer each control belongs to.
- Phone behavior keeps context, primary action, and route tabs reachable.

Proof:

- render/showcase test for the new examples,
- browser responsive screenshots if CSS changes are required,
- `uv run poe build-docs-check`.

## Phase 2: Stable Nav Counts

Define and implement the smallest stable count contract that real recipes need.

Candidate surfaces:

- `route_tabs` item badges,
- `primary_nav` item badges,
- `inline_counter` for object metadata rows.

Potential API, only if examples prove it:

- item-level `badge_label` for accessible count text,
- item-level `badge_reserved` or `badge_expected` for stable layout,
- item-level loading state when a count is expected but not loaded.

Acceptance:

- Visual count and accessible count are separable.
- Expected counts reserve stable inline space in dense navigation.
- Missing counts do not announce incorrect values.
- Existing `badge` item keys continue to work unchanged.

Proof:

- render tests for badge, empty, loading, reserved, and accessible-label states,
- `tests/test_strict_undefined.py` coverage for minimal tab/nav items,
- CSS parity and registry emits tests if new classes ship,
- responsive test for stable control sizing if CSS changes.

Collateral:

- `docs/NAVIGATION.md`,
- `docs/COMPONENT-OPTIONS.md` if signatures change,
- generated `src/chirp_ui/manifest.json` if descriptors change,
- changelog fragment for public behavior.

## Phase 3: Command Launcher Chrome

Improve the search/jump trigger story without binding command palette to a
specific app header.

Research questions:

- Should `command_palette_trigger()` support icon, placeholder, shortcut, and
  density arguments?
- Should the compact trigger use an accessible label that differs from visible
  placeholder text?
- Should shortcut hints be optional or slot-based?
- Can current Alpine dialog behavior support multiple launchers targeting one
  palette without additional API?

Potential implementation:

- example-only first using current trigger,
- then a narrow trigger enhancement if repeated examples need it.

Acceptance:

- Trigger has a clear accessible name.
- Shortcut hint is supplemental and can be hidden without changing meaning.
- Compact and wider trigger presentations do not change command palette
  behavior.
- No inline script tags; behavior stays in `chirpui-alpine.js`.

Proof:

- render tests for trigger variations if macro changes,
- browser command palette open/focus test if behavior changes,
- docs and generated options updates for public parameters.

## Phase 4: Object Header Recipe Or Composite

Only after Phases 1-3, decide whether ChirpUI needs a public dense object header
macro.

Decision criteria:

- At least two examples repeat the same title, metadata, breadcrumbs, actions,
  and local-route placement.
- Existing `entity_header`, `document_header`, `page_header`, `breadcrumbs`,
  and `action_strip` cannot express the structure cleanly.
- The proposed API has stable slot names and does not hide route/navigation
  semantics inside a generic "chrome" blob.

Potential API shape:

```html
{% call object_header(title, meta=..., breadcrumb_items=...) %}
  {% slot actions %}...{% end %}
  {% slot route_nav %}{{ route_tabs(...) }}{% end %}
{% end %}
```

Open questions:

- Should route tabs live inside the object header or immediately after it?
- Should breadcrumbs be a parameter or a slot?
- Should object metadata prefer strings, `inline_counter()`, or structured
  `meta_items`?
- How does this differ from `entity_header` enough to justify a new macro?

Acceptance:

- A composite ships only if it removes repeated boilerplate without reducing
  semantic clarity.
- Slots follow existing naming conventions: `actions`, `header_actions` only
  where the surrounding component pattern already expects it.
- Macro handles minimal inputs under strict undefined.
- Descriptor, manifest, docs, examples, CSS, and tests agree.

Proof:

- render tests for minimal, breadcrumbs, actions, route nav, and metadata states,
- CSS contract and registry emits parity,
- manifest and generated docs checks,
- browser responsive proof for object header plus route tabs,
- `uv run poe ci` or a documented narrower proof set.

## Phase 5: Responsive And Accessibility Gauntlet

Add browser coverage for one complete dense object page.

Coverage:

- desktop, tablet, and phone widths,
- route tabs scroll instead of wrapping into a tall block,
- breadcrumb overflow remains navigable,
- command trigger opens the palette and focuses search,
- overflow actions remain reachable,
- no horizontal page overflow outside intended scroll strips.

Proof:

- Playwright/browser test under `tests/browser/`,
- screenshots or artifact checks where existing browser tests already use them,
- responsive contract test updates for any CSS invariant added.

## Recommended Execution Order

1. Add the two recipe examples and docs links.
2. Harden count/badge semantics only where examples need it.
3. Improve `command_palette_trigger()` only if the examples cannot express the
   desired dense launcher.
4. Re-evaluate whether `entity_header` can be extended or whether a new
   `object_header` composite is justified.
5. Add browser responsive coverage for the complete dense object page.

## Not Now

- App-specific branded headers.
- User-configurable arbitrary slot maps.
- Async data loading protocol for counters.
- JavaScript-managed navigation overflow.
- Utility-class aliases for density, hiding, or alignment.
