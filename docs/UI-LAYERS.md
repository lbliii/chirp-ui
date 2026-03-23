# UI layers & terms

Authoritative site copy lives in **`site/content/docs/app-shell/ui-layers.md`**. This file is the same reference for repo-wide search (CLAUDE, IDE).

## Glossary

| Term | Meaning |
|------|---------|
| **App shell** | Persistent layout: `chirpui/app_shell_layout.html` (topbar, sidebar, `#main`). |
| **Page content** | `#page-content` — swapped on boosted navigation (`hx-select`). |
| **Page chrome** | Inside `#page-content`: tabs, headers, route toolbars. |
| **Shell actions** | `shell_actions_bar` in `#chirp-shell-actions`; Chirp `ShellActions`. |
| **Shell regions** | Stable ids for HTMX OOB: see `chirp.shell_regions` in Chirp. |
| **Surface chrome** | Component frame (card/panel/bento border and padding) — not the app shell. |

Do **not** use “chrome” alone for the global frame; say **app shell** or name the region.

## Chirp imports

```python
from chirp.shell_regions import (
    DOCUMENT_TITLE_ELEMENT_ID,
    SHELL_ACTIONS_TARGET,
    SHELL_ELEMENT_IDS,
)
```

## See also

- [LAYOUT-OVERFLOW.md](./LAYOUT-OVERFLOW.md)
- [COMPONENT-OPTIONS.md](./COMPONENT-OPTIONS.md) — panel / surface wording
