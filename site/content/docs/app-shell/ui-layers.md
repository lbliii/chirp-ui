---
title: UI layers & terms
description: App shell, page chrome, surface chrome, and shell regions — one vocabulary
draft: false
weight: 39
lang: en
type: doc
keywords: [chirp-ui, app shell, chrome, glossary, OOB]
category: app-shell
---

# UI layers & terms

This page aligns with the **Chirp** guide: [UI layers & shell regions](https://lbliii.github.io/chirp/docs/guides/ui-layers/) (same concepts; Chirp owns the `chirp.shell_regions` constants).

## Quick glossary

| Term | Meaning |
|------|---------|
| **App shell** | Persistent layout from `chirpui/app_shell_layout.html` or `app_shell()` + `shell_outlet()`: topbar, sidebar, `#main` wrapper. Not replaced on navigation; `#page-content` inside `#main` swaps. |
| **Page content** | The document area: `#page-content` — what `hx-select` targets for boosted nav, provided by `app_shell_layout.html` or `shell_outlet()`. |
| **Page chrome** | Route-owned UI *inside* `#page-content`: titles, tabs, toolbars — not the global topbar. |
| **Shell actions** | `ShellActions` → `shell_actions_bar`, target `#chirp-shell-actions`. Route-scoped; updates via OOB. |
| **Shell regions** | Stable `id`s updated by `hx-swap-oob` (e.g. `chirp-shell-actions`, `chirpui-document-title`). |
| **Marketing site shell** | Full-page scroll layout: `site_shell()` + `site_header()` + `site_footer()`. Use for landing pages, docs homes, marketing sites. Counterpart to **app shell** — no sidebar, no fixed `#main`. |
| **Surface chrome** | Visual frame of a **component** (`surface`, `panel`, bento): border, padding, scroll — *not* the app shell. |
| **Navigation domain** | The author-facing boundary declared in Chirp `_layout.html` via `{# domain: name #}`. `swap_attrs()` uses shared domain ancestry to choose the right swap target. |

**Avoid:** using "chrome" alone for the whole app frame — say **app shell**, **site shell**, or **topbar/sidebar**.

## Chirp `mount_pages` layouts

Filesystem `_layout.html` files that extend `app_shell_layout` should declare `{# target: body #}`, an explicit **`{# domain: ... #}`**, and **`{# outlet: main #}`** so Chirp can:

- decide which links should boost together from shared domain ancestry
- match `HX-Target: #main` for intra-domain app-shell navigation
- return HTML that still includes `#page-content` for `hx-select`

Minimal pattern:

```html
{# target: body #}
{# domain: workspace #}
{# shell: workspace #}
{# outlet: main #}
{% extends "chirpui/app_shell_layout.html" %}
```

See the Chirp guide [Filesystem routing](https://lbliii.github.io/chirp/docs/routing/filesystem-routing/) for the routing-side contract.

## chirp-ui responsibilities

- **`app_shell_layout.html`** — Defines the shell DOM, registers no extra Python; pairs with Chirp’s `use_chirp_ui(app)`.
- **Shell coherence script** — Clears `#chirp-shell-actions` in `htmx:beforeSwap` when the response includes a shell-actions OOB, so users never see one frame of new page + stale actions (htmx runs primary swap before OOB).

## Related docs

- Repo: **`docs/UI-LAYERS.md`** (duplicate reference for editors)
- **`docs/LAYOUT-OVERFLOW.md`** — keeping the main column stable
- **`docs/COMPONENT-OPTIONS.md`** — components; distinguishes surface chrome from shell
