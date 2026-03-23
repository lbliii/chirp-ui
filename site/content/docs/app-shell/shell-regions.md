---
title: Shell regions
description: Sidebar, navbar, main, and shell actions
draft: false
weight: 41
lang: en
type: doc
keywords: [chirp-ui, app-shell, sidebar]
icon: sidebar
---

# Shell regions

The app shell divides the viewport into predictable regions:

- **Brand / sidebar** — navigation, `shell_brand_link`, `shell_boosted_link`.
- **Navbar** (optional top bar) — `navbar`, `command_bar`.
- **Main** — `#main` / `.chirpui-app-shell__main` scrollport for page content.
- **Shell actions** — `shell_actions`, `shell_frame` for global actions.

Layouts live in **`chirpui/app_shell_layout.html`**, **`app_shell.html`**, **`workspace_shell.html`**, etc.

## UI layers

See [UI layers](./ui-layers.md) for **app shell** vs **page chrome** vs **surface chrome** vocabulary.

## HTMX targets

Fragment IDs (`#page-content`, OOB regions) are documented in the main [App shell](./_index.md) page — keep targets stable across full loads and boosted navigation.

## Related

- [OOB updates](./oob-updates.md)
- [Vertical layout](../guides/vertical-layout.md)
