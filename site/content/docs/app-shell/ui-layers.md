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
| **App shell** | Persistent layout from `chirpui/app_shell_layout.html`: topbar, sidebar, `#main`. Not replaced on navigation; boosted nav swaps the fragment matching `hx-select="#page-root"` into `#main`. |
| **Boosted fragment** | **`id="page-root"`** — required in page templates for `app_shell_layout` / `app_shell` (the `page_root` block name does not create this id). Chirp’s `layouts/boost.html` uses `hx-select="#page-content"` instead. |
| **Page content** | `#page-content` — inner wrapper in the layout around `{% block content %}`. |
| **Page chrome** | Route-owned UI in the main area: titles, tabs, toolbars — not the global topbar. |
| **Shell actions** | `ShellActions` → `shell_actions_bar`, target `#chirp-shell-actions`. Route-scoped; updates via OOB. |
| **Shell regions** | Stable `id`s updated by `hx-swap-oob` (e.g. `chirp-shell-actions`, `chirpui-document-title`). |
| **Surface chrome** | Visual frame of a **component** (`surface`, `panel`, bento): border, padding, scroll — *not* the app shell. |

**Avoid:** using “chrome” alone for the whole app frame — say **app shell** or **topbar/sidebar**.

## chirp-ui responsibilities

- **`app_shell_layout.html`** — Defines the shell DOM, registers no extra Python; pairs with Chirp’s `use_chirp_ui(app)`.
- **Shell coherence script** — Clears `#chirp-shell-actions` in `htmx:beforeSwap` when the response includes a shell-actions OOB, so users never see one frame of new page + stale actions (htmx runs primary swap before OOB).

## Related docs

- Repo: **`docs/UI-LAYERS.md`** (duplicate reference for editors)
- **`docs/LAYOUT-OVERFLOW.md`** — keeping the main column stable
- **`docs/COMPONENT-OPTIONS.md`** — components; distinguishes surface chrome from shell
