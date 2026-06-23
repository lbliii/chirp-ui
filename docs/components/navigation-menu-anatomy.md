# Navigation Menu Anatomy

**Status:** anatomy contract (experimental surface)
**Scope:** `navigation_menu`, `navigation_menu__trigger`, `navigation_menu__panel`, `navigation_menu__link`
**Runtime:** Alpine.js through `chirpui-alpine.js`

The navigation menu is site navigation with flyout submenus for nested links. It is
distinct from `menubar` application commands, `dropdown_menu` compact triggers, and
URL-backed `route_tabs`.

## Macro

Import from `chirpui/navigation_menu.html`:

```kida
{% from "chirpui/navigation_menu.html" import navigation_menu %}

{{ navigation_menu(label="Primary", items=[
  {"label": "Products", "children": [
    {"label": "Analytics", "href": "/products/analytics", "description": "Usage insights"},
    {"label": "Automation", "href": "/products/automation"},
  ]},
  {"label": "Pricing", "href": "/pricing"},
]) }}
```

## Rendered Contract

- root class: `chirpui-navigation-menu` with generated `id` and `aria-label`
- list class: `chirpui-navigation-menu__list` with `role="menubar"`
- item class: `chirpui-navigation-menu__item` with `--has-children` when nested
- trigger class: `chirpui-navigation-menu__trigger` for branches with children
- panel class: `chirpui-navigation-menu__panel` with `role="menu"`
- link classes: `navigation_menu__link`, `--top` for leaf top-level links
- Alpine controller: `x-data="chirpuiNavigationMenu()"` with `x-init="init()"`
- generated id: `x-id="['nav-panel']"`
- item count: `data-item-count`

Branch triggers bind `role="menuitem"`, `aria-haspopup="menu"`, bound
`aria-expanded`, bound `aria-controls`, `@click="toggle(index)"`, and
`@keydown="onTriggerKeydown($event, index)"`.

Submenus render with `x-show="openIndex === index"`, `x-cloak`, and
`x-transition`. Child links use `role="menuitem"`, `tabindex="-1"`, and
`route_link_attrs()` on `href`.

## Focus And Keyboard Behavior

Top-level branch triggers:

- Click toggles the flyout open or closed
- ArrowDown, Enter, or Space opens the flyout and focuses the first submenu link
- Escape closes the open flyout and returns focus to its trigger

Global dismiss:

- Escape on the root closes the open flyout
- Click outside closes the open flyout
- Focus leaving the open panel closes the flyout

Leaf top-level items render as plain links without a flyout panel.

## Mobile Fallback

At narrow widths the top-level list wraps instead of forcing horizontal page
overflow. Flyout panels stay in-flow under their trigger with floating elevation
and bounded inline size. Apps that need a drawer or tray fallback should compose
`drawer`, `sidebar`, and `nav_tree` rather than expecting the navigation menu
macro to collapse into a phone shell by itself.

## Boundary

Use `menubar` for horizontal application commands, `dropdown_menu` for compact
command triggers, `nav_tree` for docs sidebars, and `route_tabs` for URL-backed
subsection views.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered navigation menu family, not descriptor or
manifest metadata.

| Field | Navigation menu |
| --- | --- |
| Surface | `navigation_menu` site nav with flyout submenus for nested links. |
| Label | `experimental` rendered macro contract under the experimental `navigation-menu` component family. |
| Anatomy | `.chirpui-navigation-menu`, `.chirpui-navigation-menu__list`, `.chirpui-navigation-menu__trigger`, `.chirpui-navigation-menu__panel`, `.chirpui-navigation-menu__link`, generated `nav-panel` ids, `data-item-count`, trigger/panel refs. |
| Native semantics | List uses `role="menubar"`; branch triggers and submenu links use `menuitem`; flyouts use `role="menu"`. |
| Keyboard | Branch triggers open on ArrowDown/Enter/Space; Escape and outside click close; first submenu link receives focus on open. |
| Focus | Opening a flyout focuses the first submenu link in `$nextTick`; closing returns focus to the owning trigger. |
| Runtime | Requires `chirpuiNavigationMenu()` in `chirpui-alpine.js`, Alpine refs, `x-id`, `x-show`, `x-cloak`, `x-transition`, outside/focusin handlers. |
| Motion | Flyouts use `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. |
| Responsive and overflow | Top-level list wraps at narrow widths; panels use floating elevation with bounded inline size; browser gauntlet covers 320px without horizontal page bleed. |
| Security and escaping | Labels, descriptions, and hrefs render through template attribute helpers; child links use `route_link_attrs()`. |
| Performance | Open/close state is local to the navigation menu root; no page-global observers are part of the contract. |
| Proof | `tests/test_components.py` checks rendered navigation menu anatomy; `tests/browser/test_navigation_menu_gauntlet.py` checks submenu open, Escape/outside close, viewport containment, and 320px overflow. |
| Residual risk | Automated tests cover rendered semantics and open/close keyboard behavior, but no manual screen-reader or assistive-technology proof is claimed. Submenu ArrowUp/Down roving and typeahead search are not yet published. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy, branch/leaf modes, and ARIA roles.
- `tests/browser/test_navigation_menu_gauntlet.py` for submenu keyboard open, Escape/outside
  close, viewport containment, and narrow-width overflow checks.
