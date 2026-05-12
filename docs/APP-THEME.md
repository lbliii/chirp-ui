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
and token explorer sections. The audit checklist lives in
[VISUAL-AUDIT-SHOWCASE.md](VISUAL-AUDIT-SHOWCASE.md).

When `chirp_ui.static_path()` is served at `/static`, the same file is available
as:

```html
<link rel="stylesheet" href="/static/chirpui.css">
<link rel="stylesheet" href="/static/themes/app-theme-starter.css">
```

## Ownership

- **Chirp-UI owns** the `--chirpui-*` token names, component classes, theme
  toggle behavior, and baseline defaults.
- **Chirp owns** project bootstrapping and static asset wiring.
- **The app owns** concrete brand values: color, typeface, shape, and any
  deliberate component-level overrides.

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
