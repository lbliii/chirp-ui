# App Theme Layer

Chirp-UI gives apps a component vocabulary, baseline tokens, and the
`data-theme`/`data-style` runtime contract. It does not own an application's
brand palette. A fresh Chirp app should add one small token-only stylesheet
after `chirpui.css` so `theme_toggle()` has real app colors behind it on day
one.

The packaged starter lives at:

```text
src/chirp_ui/templates/themes/app-theme-starter.css
```

For a visual comparison of the starter profile against other token sets, open
`examples/design-system-gap-showcase/index.html` and review the theme gallery
and token explorer sections. The gallery includes the `default`,
`app-starter-light`, `app-starter-dark`, `holy-light`, and `chirp-theme`
profile IDs. The audit checklist lives in
[VISUAL-AUDIT-SHOWCASE.md](../patterns/visual-audit-showcase.md).

When `chirp_ui.static_path()` is served at `/static`, the same file is available
as:

```html
<link rel="stylesheet" href="/static/chirpui.css">
<link rel="stylesheet" href="/static/themes/app-theme-starter.css">
```

Sprint 3 also packages a small curated catalog:

| Name | Path | Best fit |
|---|---|---|
| Atlas | `/static/themes/atlas.css` | Cool operational SaaS and dashboards |
| Ember | `/static/themes/ember.css` | Warm editorial products and docs |
| Sage | `/static/themes/sage.css` | Low-glare review and planning tools |

These packs are discoverable through `chirp_ui.list_theme_packs()` and
`chirp_ui.get_library_contract().theme_packs`. They are token-only CSS
resources, not component skins.

The component showcase publishes the live matrix at `/theme-packs`, with each
pack rendered in isolated light, dark, and `system` preview frames.

## Ownership

- **Chirp-UI owns** the `--chirpui-*` token names, component classes, theme
  toggle behavior, and baseline defaults.
- **Chirp owns** project bootstrapping and static asset wiring.
- **The app owns** concrete brand values: color, typeface, shape, and any
  deliberate component-level overrides.
- **Theme packs own** curated starting values for `--chirpui-*` tokens only.

Keep app themes token-only by default. Do not introduce `chirpui-*` classes in
an app theme file, and do not create utility-class vocabulary to express brand
choices.

## Required Shape

Use a layer that loads after `chirpui.css`:

```css
@layer app.theme {
    :root {
        --chirpui-accent: oklch(0.58 0.16 248);
        --chirpui-radius-lg: 0.75rem;
    }

    [data-theme="light"] {
        color-scheme: light;
        --chirpui-bg: oklch(0.985 0.004 248);
        --chirpui-surface: oklch(1 0 0);
        --chirpui-text: oklch(0.22 0.028 248);
    }

    [data-theme="dark"] {
        color-scheme: dark;
        --chirpui-bg: oklch(0.18 0.024 248);
        --chirpui-surface: oklch(0.24 0.028 248);
        --chirpui-text: oklch(0.94 0.008 248);
    }
}
```

Handle `system` explicitly. Chirp-UI's pre-paint script sets
`data-theme="system"` when the user has not chosen a fixed mode, so app tokens
need media-query branches for that state:

```css
@media (prefers-color-scheme: dark) {
    @layer app.theme {
        [data-theme="system"] {
            color-scheme: dark;
            --chirpui-bg: oklch(0.18 0.024 248);
            --chirpui-surface: oklch(0.24 0.028 248);
            --chirpui-text: oklch(0.94 0.008 248);
        }
    }
}
```

## Starter Tokens

The starter covers the tokens most likely to make a fresh project feel
unfinished if they are missing:

- `--chirpui-bg`, `--chirpui-bg-subtle`
- `--chirpui-surface`, `--chirpui-surface-alt`,
  `--chirpui-surface-elevated`
- `--chirpui-border`
- `--chirpui-text`, `--chirpui-text-muted`
- `--chirpui-accent`, `--chirpui-accent-hover`,
  `--chirpui-accent-secondary`, `--chirpui-on-accent`
- `--chirpui-primary`, `--chirpui-success`, `--chirpui-warning`,
  `--chirpui-error`, `--chirpui-muted`
- alert background and border tokens
- typography family aliases
- common radius aliases

Add component-level rules only when a token cannot express the intent. Put
those rules in `@layer app.overrides`, after the token layer, so the split
between brand values and component overrides stays obvious.

## First Tokens To Override

Start with token jobs, not component selectors. The visual audit token explorer
uses the same grouping so an app author can compare changes without reading the
full reference first.

| Job | Override first | Controls |
| --- | --- | --- |
| Page | `--chirpui-bg`, `--chirpui-bg-subtle` | Canvas and page bands |
| Surface | `--chirpui-surface`, `--chirpui-surface-alt`, `--chirpui-border` | Cards, panels, inputs, table rows |
| Text | `--chirpui-text`, `--chirpui-text-muted` | Primary and secondary copy |
| Accent | `--chirpui-accent`, `--chirpui-accent-hover`, `--chirpui-on-accent` | Primary buttons, links, active UI |
| Semantic | `--chirpui-success`, `--chirpui-warning`, `--chirpui-error`, muted variants | Badges, alerts, validation, status |
| Focus | `--chirpui-focus-ring`, `--chirpui-state-focus-outline` | Keyboard and input focus states |
| Radius | `--chirpui-radius-sm`, `--chirpui-radius-md`, `--chirpui-radius-lg` | Shape across controls and surfaces |
| Elevation | `--chirpui-elevation-card-rest`, `--chirpui-elevation-floating`, `--chirpui-elevation-overlay` | Card, menu, and overlay depth |
| Typography | `--chirpui-ui-font-family`, `--chirpui-prose-font-family`, UI/prose scale tokens | Interface density and content reading |
| Motion | `--chirpui-motion-*`, `--chirpui-ease-*` | Transition timing and easing |

Avoid creating app-private token namespaces such as `--my-theme-card-border`
or `--chirp-theme-*` when a `--chirpui-*` token already carries the job. If a
component genuinely lacks a token hook, add a narrow rule in
`@layer app.overrides` and treat that rule as evidence for a future Chirp UI
token.

## Override Escalation Ladder

Use this order when a brand or product style does not look right yet:

| Step | Use | Stop when |
| --- | --- | --- |
| 1. Public token | A listed `--chirpui-*` token controls the job. | The visual audit profile shows the intended surface, state, or density. |
| 2. Semantic alias | Several components need the same role-specific value. | A semantic `--chirpui-*` alias can describe the job without naming one component. |
| 3. App override | One app has a deliberate local exception. | The rule lives in `@layer app.overrides` and targets the smallest component surface. |
| 4. Token proposal | The same exception repeats across apps or examples. | Open a Chirp UI token proposal with the override rule as evidence. |

Do not skip directly to component selectors for brand color, radius, spacing,
type, focus, or state color. Those are token jobs unless proven otherwise.

## Catalog Rules

Curated packs are intentionally constrained:

- They must define light, dark, and `system` branches.
- They may set cataloged `--chirpui-*` tokens only.
- They must not emit `.chirpui-*` selectors, utility classes, or component
  overrides.
- They are immutable package resources; export/write commands are deferred.

Use the Python API when a host needs to present a theme picker:

```python
import chirp_ui

for pack in chirp_ui.list_theme_packs():
    print(pack.name, pack.label, pack.path)
```
