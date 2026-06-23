# PLAN: Component Maturity Gap Sweep

Status: active plan
Date: 2026-05-27
Trigger: Homepage and competitive-library review showed that Chirp UI has broad
component coverage, but several common UI-library primitives are missing,
under-surfaced, or named in ways that make the library feel less mature than it
is.
Progress: Phase 1 foundation primitives are implemented. Phase 2 has started
with the low-risk `slider`, `scroll_area`, and `item` primitives, plus the
`data_table` composite and the control-selection guide that documents native
select, dropdown-select, date input, slider, and record-table boundaries before
behavior-heavy work begins. The new primitives now have live docs specimens and
component-showcase coverage on `/forms`, `/ui`, and `/data`. The existing
`dropdown_select(...)` macro is now exposed as the `dropdown-select` registry
and manifest entry so the combobox-like surface is discoverable without adding a
duplicate `combobox(...)` API. Context-menu anatomy is now drafted as a
source-only design contract and implementation gate; no public context-menu
macro or classes are shipped yet.

## Mission

Close maturity gaps that would make a serious Python app team doubt Chirp UI as
an application UI library.

This is not a shadcn/ui parity project. Chirp UI should keep its server-rendered,
Python-inspectable contract. The goal is to cover the expected jobs-to-be-done
with Chirp-native components, names, docs, tests, and examples.

## Steward Notes

- Core Registry And Python API: new component descriptors, generated manifest,
  and component-option docs.
- Template, CSS, And Behavior: macro contracts, escaped attributes, scoped CSS,
  and Alpine behavior only where repeated browser behavior requires it.
- Test Contract: render, strict-undefined, generated-output, browser, and
  accessibility proof.
- Planning: keep this plan active until the matrix is implemented or each item
  is explicitly deferred.

## Non-Goals

- Do not clone shadcn/Radix APIs or React composition names mechanically.
- Do not add utility-class vocabulary.
- Do not add a dependency for a primitive unless repeated behavior proves the
  need and a free-threading note exists.
- Do not promote prototype layout-affinity vocabulary into manifest schema.
- Do not ship behavior-heavy components without browser proof.

## Gap Matrix

| Priority | Gap | Chirp UI Direction | Scope | Required Proof |
|---|---|---|---|---|
| P1 | `toggle_group` | First-class grouped toggle buttons for single or multiple selection. | New macro, CSS, descriptor, render tests, strict-undefined test, docs/demo. | Render tests for single/multiple/vertical/disabled; CSS/manifest/docs generated checks. |
| P1 | `combobox` | Promote existing dropdown-select anatomy into a discoverable component docs/API surface. | Docs, descriptor audit, examples, browser keyboard proof. | Dropdown/select anatomy tests plus docs contract. |
| P1 | `context_menu` | Menu opened from right-click/keyboard with native focus model where possible and Alpine only for positioning/state. Anatomy is drafted; implementation remains gated. | Behavior design, macro, Alpine factory, browser tests. | Keyboard, contextmenu event, Escape/outside close, overflow containment. |
| P1 | `menubar` / `navigation_menu` | App/site navigation menu distinct from dropdown and route tabs. | Macro family, keyboard model, anatomy docs. | Roving focus, submenu behavior, responsive proof. |
| P1 | `data_table` | Opinionated composition over table, filters, pagination, empty state, bulk actions, and density. | Composite macro and docs, not a grid engine. | Sorting/filter controls render, no horizontal overflow, empty/loading states. |
| P1 | `date_picker` | Documented date input + popover calendar path; stay native-first initially. | Macro or pattern docs depending on proof. | Date field parity, popover/calendar browser proof if interactive. |
| P1 | `slider` | First-class range input wrapper over existing `range_field`. | Alias/wrapper, docs, tests. | Native range semantics and value output. |
| P1 | `kbd` | Inline keyboard key primitive. | New macro, CSS, descriptor, tests. | Render and escaping tests. |
| P1 | `separator` | Semantic/decorative horizontal and vertical separator. | New macro, CSS, descriptor, tests. | Role/orientation tests. |
| P1 | `aspect_ratio` | Fixed-ratio media/content frame. | New macro, CSS, descriptor, tests. | Slot containment and CSS class parity. |
| P1 | `label` | Standalone label primitive for custom controls and compact forms. | New macro, CSS, descriptor, tests. | `for`, required mark, hint rendering. |
| P2 | `hover_card` | Delayed hover/focus preview card. | Behavior design before API. | Hover/focus/blur browser proof, reduced-motion consideration. |
| P2 | `input_otp` | Grouped one-time-code input fields. | Macro + optional Alpine enhancement. | Paste/backspace/focus browser proof if enhanced. |
| P2 | `resizable` | Split-pane/resizable region primitive. | Behavior-heavy; design with app shell/sidebar constraints. | Pointer/keyboard resize proof, persistence decision. |
| P2 | `scroll_area` | Styled scroll container with edge affordance, not custom scrollbars by default. | Macro + CSS. | Overflow containment proof. |
| P2 | native select docs | Surface `select_field` and dropdown-select differences clearly. | Docs/examples. | Docs contract and existing render tests. |
| P2 | item/list-item primitive | Reusable item row anatomy for lists, menus, command surfaces, and resource rows. | Macro family after auditing existing row/card components. | Render tests and no duplicated row vocabulary. |

## Implementation Phases

### Phase 1: Foundation Primitives

Ship low-risk primitives that unlock docs and showcase composition:

- `kbd`
- `separator`
- `aspect_ratio`
- `label`
- `toggle_group`

Acceptance:

- Templates escape user content by default.
- CSS lives in partials and regenerated `chirpui.css`.
- Descriptors own emitted classes.
- Render and strict-undefined tests pass.
- Generated manifest and component docs are fresh.

### Phase 2: Surface Existing Capability

Make existing capabilities discoverable before inventing replacements:

- item/list-item row anatomy
- scroll area containment primitive
- combobox/dropdown-select docs and component entry
- native select guidance
- slider wrapper over `range_field`
- date picker pattern decision
- data table composition from table/filter/resource-index pieces
- `context_menu` shipped in 0.11 with browser gauntlet and stable promotion in Wave 1 contract hardening

Acceptance:

- Docs tell users which component to choose.
- Existing render/browser proof is cited or extended.
- No duplicate component names where an existing macro already owns the job.

### Phase 3: Behavior-Heavy Components

Design and implement components that need real browser behavior:

- context menu
- menubar/navigation menu
- hover card
- input OTP
- resizable
- scroll area if custom affordance is needed

Acceptance:

- Accessibility anatomy docs exist before promotion to stable.
- Browser tests cover keyboard, focus, dismissal, viewport containment, and
  reduced-motion where relevant.
- Alpine behavior is named and covered by runtime detection tests.

## Next Slice

Remaining work should move from low-risk primitives into behavior-heavy
surfaces only when the contract is small enough to prove:

1. Draft menubar/navigation-menu anatomy separately from dropdown menu and route
   tabs so app/site navigation does not blur into command menus.
2. `context_menu` is shipped and promoted to stable after the browser gauntlet
   and anatomy doc landed in Wave 1 contract hardening.
3. Keep `hover_card` and `resizable` deferred until browser
   behavior and accessibility proof can be added in the same slice.
   `input_otp` promoted to stable in Wave 1 contract hardening.

## Not Now

- Full Radix parity.
- React-compatible APIs.
- Data-grid engine features such as virtual rows, column resizing, or remote
  query adapters.
- Component-specific theme skins.
