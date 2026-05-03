# chirp-ui: Navigation Density Study

Status: study / backlog input
Date: 2026-05-03

## Goal

Study dense, high-utility navigation systems and translate the useful parts into
ChirpUI's registry-first vocabulary. The target is not to clone GitHub or any
other product chrome. The target is to identify which navigation contracts make
large applications feel fast, oriented, and safe without turning ChirpUI into a
utility-class or app-specific shell vocabulary.

## Working Definition

Dense navigation works when it separates these jobs instead of blending them
into one row:

| Job | User question | ChirpUI surface today |
|-----|---------------|-----------------------|
| Global identity | Where am I in the product? | `app_shell`, `navbar`, brand slots |
| Product / section movement | What major area can I switch to? | `primary_nav`, `sidebar`, `nav_tree` |
| Object context | Which repo/project/doc/workspace am I inside? | `breadcrumbs`, page header metadata |
| Local view switching | Which view of this object am I looking at? | `route_tabs`, `tabbed_page_layout` |
| Commands | What can I do right now? | `command_bar`, `action_strip`, `dropdown_menu`, `command_palette` |
| Status | What changed or needs attention? | badges, counters, notification actions |
| Overflow | What cannot fit, and where did it go? | partial: scroll strips, drawers/trays, dropdowns |

Dense navigation fails when these jobs are visually similar but semantically
different. A route link, a tab panel switch, a menu action, a search launcher,
and an account menu should not all be modeled as "nav items".

## GitHub Header Anatomy

The supplied GitHub header is a useful specimen because it packs many jobs into
a short vertical budget while keeping them separable:

- A global banner contains a top row and a local repository navigation row.
- Left-to-right scope generally moves from product/context to global utilities:
  menu, home, breadcrumbs/context, search, Copilot/create/issues/pulls/repos,
  notifications, user menu.
- Local repository navigation is a second row with `aria-label="Repository"` and
  `aria-current="page"` on the current route. This is route navigation, not a
  `tablist`.
- Search is presented as a command launcher, with a compact button, keyboard
  hint, modal/dialog machinery, suggestions, saved scopes, and feedback flows.
- Breadcrumbs support overflow. The visible breadcrumb trail is allowed to
  collapse into an overflow menu rather than forcing the header wider.
- Icon-only utilities carry accessible names through labels/tooltips. The visual
  density is high, but the accessible target names remain explicit.
- Responsive behavior is selective: some utilities hide at small/medium widths,
  search changes presentation, and the local nav remains horizontally navigable.

The important lesson for ChirpUI is architectural: dense navigation is layered
and contract-driven. It is not just small padding.

## External Benchmarks

### WAI-ARIA APG

- Disclosure navigation is usually a better semantic fit than ARIA `menu` for
  ordinary site navigation. APG explicitly warns that site navigation usually
  does not need full menubar/menu keyboard behavior. Source:
  <https://wai-website.netlify.app/aria/apg/patterns/disclosure/examples/disclosure-navigation/>
- Breadcrumbs should be a labelled navigation landmark, with the current page
  marked by `aria-current="page"` when represented by a link. Source:
  <https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/>
- True tabs are panel controls with `role="tablist"`, roving focus, arrow key
  behavior, and `aria-selected`. They are not the right semantic model for route
  navigation. Source: <https://www.w3.org/WAI/ARIA/apg/patterns/tabs/>

### GitHub Primer

- `UnderlineNav` is documented as navigation links for switching between related
  views without leaving the current context; its examples use repository views,
  counters, optional leading visuals, and `aria-current`. Source:
  <https://primer.style/product/components/underline-nav/>
- `NavList` is a vertical current-context navigation list, typically used as a
  sidebar, with grouping for longer lists. Source:
  <https://www.primer.style/product/components/nav-list/>
- `ActionList` is for interactive actions/options in a consistent vertical
  format, with space for icons, descriptions, side information, and rich visuals.
  Source: <https://primer.github.io/design/components/action-list/>

### Carbon UI Shell

- Carbon treats the header as the highest navigation layer, with optional left
  and right panels designed to work together. It explicitly separates header
  identity/navigation/actions from the left panel's deeper product navigation.
  Source: <https://v10.carbondesignsystem.com/components/UI-shell-header/usage/>
- Carbon's header anatomy uses left-to-right scope: product-level items on the
  left, system-level controls in the middle, global utilities on the right.
  Source: <https://v10.carbondesignsystem.com/components/UI-shell-header/usage/>
- Carbon recommends a left panel when secondary navigation has more than five
  items or users switch secondary items frequently, and it discourages a third
  navigation tier inside that panel. Source:
  <https://v10.carbondesignsystem.com/components/UI-shell-left-panel/usage/>

## ChirpUI Current State

### Strong Existing Contracts

- `route_tabs` already makes the key semantic distinction: route-backed tabs are
  `nav` links with `aria-current`, not ARIA tabs.
- `SHELL-TABS-CONTRACT.md` defines shell, page content, and page chrome swap
  ownership. This is exactly the kind of contract dense navigation needs.
- `RESPONSIVE.md` already requires `route_tabs` and `primary_nav` to become
  horizontal scroll strips below `40rem`.
- `nav_tree` supports docs/admin/settings hierarchies and uses native
  `<details>` for disclosure-style branches.
- `breadcrumbs` uses a labelled `nav`, an ordered list, and current-page state.
- `dropdown_menu` and `command_palette` provide action/command surfaces that
  should not be confused with route navigation.

### Gaps Exposed By The Study

| Gap | Why it matters | Existing nearest surface |
|-----|----------------|--------------------------|
| No explicit dense header composition contract | Apps need guidance for arranging brand, object context, search, utilities, and local nav without inventing one-off chrome. | `app_shell`, `navbar`, `primary_nav`, `route_tabs` |
| Breadcrumb overflow is not a first-class pattern | Deep project paths need compact context without causing header overflow. | `breadcrumbs`, `dropdown_menu` |
| Search/command launcher placement is under-specified | Dense apps often need search as navigation and command execution, with keyboard hints. | `command_palette`, `command_palette_trigger` |
| Action menus vs disclosure navigation need clearer guidance | ARIA `menu` is appropriate for commands, but not for normal navigation lists. | `dropdown_menu`, `nav_tree`, `navbar_dropdown` |
| Counters/badges can cause layout shift | Primer calls out loading counters together to avoid multiple shifts; ChirpUI has badges but not a documented loading contract for nav counts. | `route_tabs`, `primary_nav`, `sidebar_link` |
| Responsive overflow policy is split across components | We have scroll strips and shell collapse, but not a hierarchy for "hide, scroll, move to drawer, move to overflow menu". | `RESPONSIVE.md`, component CSS |

## Design Principles For ChirpUI

1. **Model the job before the shape.**
   A horizontal row can be primary nav, route tabs, command actions, or status
   utilities. The component name and ARIA must follow the job.

2. **Keep route navigation link-native.**
   Use anchors, `nav`, labels, and `aria-current`. Reserve `role="tablist"` for
   panel widgets where focus movement and panel visibility are controlled in
   place.

3. **Prefer disclosure for navigation expansion.**
   Use native `<details>` or disclosure buttons for navigation sections. Use
   ARIA menu/menuitem only for command menus that behave like menus.

4. **Separate global chrome from object chrome.**
   A dense app can have a global shell row and a local object row. ChirpUI should
   document where breadcrumbs, route tabs, search, actions, and counters live.

5. **Overflow is a contract, not a breakpoint afterthought.**
   Every dense nav primitive needs an overflow strategy: scroll, collapse to
   drawer/tray, collapse to an overflow menu, hide low-priority utilities, or
   wrap only when wrapping remains readable.

6. **Counters and status should not move the nav repeatedly.**
   Count badges need stable dimensions or a loading policy so async updates do
   not reflow dense headers one badge at a time.

7. **Icon-only density requires explicit accessible names.**
   Tooltip text is not enough by itself. Icon buttons need `aria-label`,
   `aria-labelledby`, or visible/visually hidden text. Keyboard hints should be
   supplemental, not the only label.

8. **Command launchers belong in the chrome, command results belong in an overlay.**
   The header trigger can be compact; the search/command UI can be spacious,
   filterable, keyboard-driven, and modal/dialog-based.

## Candidate Backlog

### P1: Dense Navigation Contract Doc

Create a reference doc that names ChirpUI's blessed navigation layers:

- app shell/global row
- sidebar/product navigation
- object context row
- route tabs/local view navigation
- command/action row
- overflow/drawer policy

Required proof: docs-only unless examples change.
Collateral: `docs/INDEX.md`, `site/content/docs/app-shell/` if published.

### P1: Breadcrumb Overflow Pattern

Add a documented pattern, and possibly a macro option, for deep breadcrumb
trails:

- show first/current and collapse middle items into a disclosure/action-list
  style overflow
- preserve labelled `nav` and ordered-list semantics where feasible
- keep separators presentation-only

Required proof: render tests, strict-undefined fixture, responsive browser check.
Collateral: `COMPONENT-OPTIONS.md`, app-shell docs, examples.

### P1: Navigation Overflow Policy

Document a priority order for dense navigation at narrow widths:

1. Keep current context and primary action reachable.
2. Convert local route tabs to horizontal scroll.
3. Move broad/deep navigation into drawer/tray.
4. Collapse low-frequency utilities into overflow.
5. Hide only duplicate shortcuts whose destination remains reachable elsewhere.

Required proof: responsive docs update; browser tests only if CSS changes.
Collateral: `RESPONSIVE.md`, app-shell docs.

### P2: Header / Object Chrome Composite

Explore a macro or documented composition recipe for GitHub-like dense app
headers without creating an app-specific clone:

- brand/home
- product menu trigger
- object breadcrumbs
- search/command launcher
- utility icon group
- account slot
- optional local route nav row

This should likely start as documentation and examples before a new macro.

Required proof: showcase fixture, responsive browser screenshots if implemented.
Collateral: docs, examples, descriptor/manifest only if a new component ships.

### P2: Nav Counter Stability

Define badge/counter loading behavior for route tabs, primary nav, and sidebar
links:

- reserve stable inline space where practical
- allow hidden/loading count states
- recommend batching async count display

Required proof: render tests and browser layout regression if CSS changes.
Collateral: component docs and examples.

### P2: Action Menu vs Navigation Disclosure Guidance

Clarify when to use:

- `dropdown_menu`: commands/options
- `nav_tree`: hierarchy/disclosure navigation
- `navbar_dropdown`: simple grouped links, but avoid ARIA menu semantics unless
  keyboard/menu behavior is complete
- `command_palette`: search/jump/action overlay

Required proof: docs-only unless macro semantics change.
Collateral: `ALPINE-MAGICS.md`, `COMPONENT-OPTIONS.md`, examples.

## Not Now

- Do not add a new "mega nav" component before we have two real consuming apps
  with the same structure.
- Do not add utility spacing/visibility classes to make dense chrome easier.
- Do not retrofit ARIA `menu` roles onto normal navigation lists.
- Do not make GitHub's exact header structure a ChirpUI public API.

## Steward Notes

- Documentation steward: this study is planning guidance, not shipped contract.
- Template/CSS steward: any future implementation must edit partials, regenerate
  CSS, and preserve route-link vs tab-widget semantics.
- Registry/API steward: new components or macro params require descriptor,
  manifest, generated docs, and migration notes if public behavior changes.
- Tests steward: accepted implementation work needs render, strict undefined,
  responsive, and where relevant browser/focus proof.
