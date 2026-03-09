# chirp-ui

[![PyPI version](https://img.shields.io/pypi/v/chirp-ui.svg)](https://pypi.org/project/chirp-ui/)
[![Tests](https://github.com/lbliii/chirp-ui/actions/workflows/tests.yml/badge.svg)](https://github.com/lbliii/chirp-ui/actions/workflows/tests.yml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://pypi.org/project/chirp-ui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://pypi.org/project/chirp-ui/)

**An optional, opinionated UI layer for Chirp — gorgeous by default, htmx-native.**

```python
pip install chirp chirp-ui
```

```html
{% from "chirpui/layout.html" import container, grid, block %}
{% from "chirpui/card.html" import card %}

{% call container() %}
    {% call grid(cols=2) %}
        {% call block() %}{% call card(title="Hello") %}<p>Card one.</p>{% end %}{% end %}
        {% call block() %}{% call card(title="World") %}<p>Card two.</p>{% end %}{% end %}
    {% end %}
{% end %}
```

---

## What is chirp-ui?

chirp-ui is an optional companion design system for [Chirp](https://github.com/lbliii/chirp). It provides [Kida](https://github.com/lbliii/kida) template macros — cards, modals, forms, layouts — that render as HTML. It is one polished, opinionated way to build Chirp apps, not the framework itself and not the only way to use Chirp. Use it with htmx for swaps, SSE for streaming, and View Transitions for polish. No client-side framework required for layout.

**What's good about it:**

- **Gorgeous by default** — Full visual design out of the box. Override `--chirpui-*` CSS variables to customize.
- **htmx-native** — Interactive components use htmx or Alpine.js. Dropdown, modal, tray, tabs, theme toggle, copy button use Alpine for declarative behavior.
- **Composable** — `{% slot %}` for content injection. Components nest freely.
- **Modern CSS** — `:has()`, container queries, fluid typography, `prefers-color-scheme` dark mode.

---

## Installation

```bash
# pip
pip install chirp-ui

# uv
uv add chirp-ui
```

Requires Python 3.14+. When used with Chirp, components are auto-detected — no configuration needed.

You do not need `chirp-ui` to use Chirp. Use it when you want the companion component library, default design language, and app-shell patterns.

---

## Quick Start

| Step | Action |
|------|--------|
| 1 | Install Chirp and chirp-ui if you want the companion UI layer: `pip install chirp chirp-ui` |
| 2 | Serve static assets from the package (CSS, themes) |
| 3 | Import macros in templates: `{% from "chirpui/card.html" import card %}` |
| 4 | Include CSS: `<link rel="stylesheet" href="/static/chirpui.css">` |
| 5 | For interactive components (dropdown, modal, tray, tabs, theme toggle): use `chirpui/app_shell_layout.html` or `chirpui/app_layout.html` — both include Alpine.js |

**Serve assets:**

```python
from chirp.middleware.static import StaticFiles
import chirp_ui

app.add_middleware(StaticFiles(
    directory=str(chirp_ui.static_path()),
    prefix="/static"
))
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Layout** | container, grid, stack, block, page_header, section_header, divider, breadcrumbs, navbar, navbar_end, navbar_dropdown, sidebar, hero, surface, callout |
| **UI** | card, card_header, modal, drawer, tabs, accordion, dropdown, popover, toast, table, pagination, alert, button_group, island_root, state primitives |
| **Forms** | text_field, password_field, textarea_field, select_field, checkbox_field, toggle_field, radio_field, file_field, date_field, csrf_hidden, form_actions, login_form, signup_form |
| **Data display** | badge, spinner, skeleton, progress, description_list, timeline, tree_view, calendar |
| **Dashboard** | inline_edit_field, row_actions, status_with_hint, entity_header, confirm_dialog — [DASHBOARD-MATURITY-CONTRACT](docs/DASHBOARD-MATURITY-CONTRACT.md) |
| **Docs** | page_hero, nav_tree, params_table, signature, index_card — framework-agnostic docs components |
| **Streaming** | streaming_block, copy_btn, model_card — for htmx SSE and LLM UIs |
| **Theming** | `--chirpui-*` CSS variables, dark mode, optional Holy Light theme |
| **Component options** | [COMPONENT-OPTIONS.md](docs/COMPONENT-OPTIONS.md) — valid variants, sizes, strict mode |

---

## Usage

<details>
<summary><strong>Component Showcase</strong> — Browse all components</summary>

```bash
pip install chirp chirp-ui
python examples/component-showcase/app.py
```

Open http://localhost:8000

</details>

<details>
<summary><strong>Theming</strong> — Override CSS variables</summary>

chirp-ui uses `prefers-color-scheme` for dark mode. Override any `--chirpui-*` variable. Base colors drive derived states (hover, active, light, muted) via `color-mix()`:

```css
:root {
    --chirpui-accent: #7c3aed;
    --chirpui-container-max: 80rem;
    /* Optional: tune shade ratios for all colors */
    --chirpui-shade-hover: 85%;
    --chirpui-shade-muted: 15%;
}
```

Advanced tokens: HTTP methods (`--chirpui-method-get`, etc.), code syntax (`--chirpui-code-keyword`, etc.), example/admonition (`--chirpui-alert-example-*`). Full token reference: [PLAN-theme-tokens.md](docs/PLAN-theme-tokens.md).

For manual light/dark toggle, set `data-theme="light"` or `data-theme="dark"` on `<html>`.

Optional theme: `<link rel="stylesheet" href="/static/themes/holy-light.css">`

</details>

<details>
<summary><strong>Manual registration</strong> — Use with Kida without Chirp</summary>

```python
from kida import ChoiceLoader, Environment, FileSystemLoader
from chirp_ui import get_loader

env = Environment(
    loader=ChoiceLoader([
        FileSystemLoader("templates"),
        get_loader(),
    ])
)
```

Call `chirp_ui.register_filters(app)` if using Chirp for form/field helpers.

</details>

<details>
<summary><strong>Islands (framework-agnostic)</strong> — Isolate high-state widgets</summary>

chirp-ui stays server-rendered by default. For complex client-state widgets
(editors, canvases, advanced grids), mount isolated islands on dedicated roots.

```html
{% from "chirpui/islands.html" import island_root %}

{% call island_root("editor", props={"doc_id": doc.id}, mount_id="editor-root") %}
<p>Fallback editor UI (SSR) if JavaScript is unavailable.</p>
{% end %}
```

In Chirp, enable runtime lifecycle hooks:

```python
from chirp import App, AppConfig

app = App(AppConfig(islands=True, islands_contract_strict=True))
```

Lifecycle events emitted in the browser:
- `chirp:island:mount`
- `chirp:island:unmount`
- `chirp:island:remount`
- `chirp:island:state`
- `chirp:island:action`
- `chirp:island:error`

For no-build defaults, use primitive wrappers from `chirpui/state_primitives.html`:

```html
{% from "chirpui/state_primitives.html" import grid_state, wizard_state, upload_state %}

{% call grid_state("team_grid", ["name", "role"], mount_id="grid-root") %}
...
{% end %}
```

Included no-build primitives:
- `state_sync`
- `action_queue`
- `draft_store`
- `error_boundary`
- `grid_state`
- `wizard_state`
- `upload_state`

</details>

<details>
<summary><strong>SSE and streaming</strong> — htmx + Server-Sent Events</summary>

- **streaming_block** — Use `sse_swap_target=true` for htmx SSE fragment swaps.
- **model_card** — Use `sse_connect=url`, `sse_streaming=true` for LLM comparison UIs.
- **copy_btn** — Copy button with `data-copy-text`. Enable `AppConfig(delegation=True)` for dynamically inserted buttons.

See Chirp [RAG demo](https://github.com/lbliii/chirp/tree/main/examples/rag_demo) and [LLM playground](https://github.com/lbliii/chirp/tree/main/examples/llm_playground).

</details>

<details>
<summary><strong>Alpine Magics & Events</strong></summary>

chirp-ui uses Alpine.js magics for accessibility and cross-component communication:

| Magic | Use |
|-------|-----|
| `$el` | Current element (e.g. `$el.dataset.label`, `$el.value`) |
| `$refs` | DOM refs for focus management (dropdown trigger/panel) |
| `$store` | Global state (`modals`, `trays`) for overlay components |
| `$id` | Unique IDs for ARIA (dropdown, tabs) |
| `$watch` | Reactive sync (theme/style select) |
| `$dispatch` | Custom events for app-level handling |
| `$nextTick` | Post-render focus (dropdown_select) |

**Custom events** — Listen for `chirpui:*` events on `document` or a parent:

| Event | When | Detail |
|-------|------|--------|
| `chirpui:dropdown-selected` | Dropdown item clicked | `{ label, href? }` or `{ label, action? }` or `{ label, value? }` |
| `chirpui:tab-changed` | Tab clicked | `{ tab }` |
| `chirpui:tray-closed` | Tray backdrop/close clicked | `{ id }` |
| `chirpui:modal-closed` | Modal backdrop/close clicked | `{ id }` |

Example: run HTMX or analytics when a dropdown item is selected:

```javascript
document.addEventListener('chirpui:dropdown-selected', (e) => {
  if (e.detail.action) htmx.ajax('POST', '/api/action', { values: { action: e.detail.action } });
});
```

Full reference: [docs/ALPINE-MAGICS.md](docs/ALPINE-MAGICS.md)

</details>

<details>
<summary><strong>Icons and ergonomics</strong></summary>

Many components support Unicode icons via the `icon` param:

```html
{% from "chirpui/alert.html" import alert %}
{% from "chirpui/card.html" import card %}
{% from "chirpui/button.html" import btn %}
{% from "chirpui/callout.html" import callout %}

{% call alert(variant="warning", icon="⚠", title="Heads up") %}Body text{% end %}
{% call card(title="Feature", subtitle="Optional subtitle", icon="◆") %}Content{% end %}
{{ btn("Save", icon="✓") }}
{% call callout(icon="💡", title="Tip") %}Use Unicode for icons.{% end %}
```

For animated icons, use `ascii_icon()` in the component slot. For custom headers with actions, use the `header_actions` named slot (Kida 0.3+):

```html
{% from "chirpui/card.html" import card %}
{% call card(title="Settings", icon="⚙") %}
{% slot header_actions %}
<button class="chirpui-btn chirpui-btn--ghost">⋯</button>
{% end %}
<p>Body content.</p>
{% end %}
```

`empty_state` supports `action_label` and `action_href` for a primary CTA button.

</details>

---

## Key Ideas

- **HTML over the wire.** Components render as blocks for htmx swaps, SSE streams, and View Transitions. The server is the source of truth.
- **Companion, not core.** `chirp-ui` is an optional layer on top of Chirp, not a requirement for using the framework.
- **CSS as the design language.** Modern features (`:has()`, `aspect-ratio`, `clamp()`) used where they add value. All animations respect `prefers-reduced-motion`.
- **Composable.** `{% slot %}` for content injection. Components nest freely. No wrapper classes.
- **Minimal dependency.** `kida-templates` only. Chirp optional for auto-registration.

---

## Requirements

- Python >= 3.14
- kida-templates >= 0.2.6

**Interactive components** (dropdown, modal, tray, tabs, theme toggle, copy button) require [Alpine.js](https://alpinejs.dev/) 3.x. The `chirpui/app_shell_layout.html` and `chirpui/app_layout.html` layouts include Alpine via CDN. For custom layouts, add Alpine before using these components.

---

## Development

```bash
git clone https://github.com/lbliii/chirp-ui.git
cd chirp-ui
uv sync --group dev
pytest
```

| Task | Command |
|------|---------|
| Run tests | `uv run pytest` or `poe test` |
| Type check | `uv run ty check src/chirp_ui/` or `poe ty` |
| Lint | `uv run ruff check .` or `poe lint` |
| Full CI | `poe ci` |

---

## The Bengal Ecosystem

A structured reactive stack written in pure Python for 3.14t free-threading. Chirp is the framework; `chirp-ui` is one optional UI layer built on top of it.

| | | | |
|--:|---|---|---|
| **ᓚᘏᗢ** | [Bengal](https://github.com/lbliii/bengal) | Static site generator | [Docs](https://lbliii.github.io/bengal/) |
| **∿∿** | [Purr](https://github.com/lbliii/purr) | Content runtime | — |
| **⌁⌁** | [Chirp](https://github.com/lbliii/chirp) | Web framework | [Docs](https://lbliii.github.io/chirp/) |
| **ʘ** | **chirp-ui** | Optional companion UI layer ← You are here | — |
| **=^..^=** | [Pounce](https://github.com/lbliii/pounce) | ASGI server | [Docs](https://lbliii.github.io/pounce/) |
| **)彡** | [Kida](https://github.com/lbliii/kida) | Template engine | [Docs](https://lbliii.github.io/kida/) |
| **ฅᨐฅ** | [Patitas](https://github.com/lbliii/patitas) | Markdown parser | [Docs](https://lbliii.github.io/patitas/) |
| **⌾⌾⌾** | [Rosettes](https://github.com/lbliii/rosettes) | Syntax highlighter | [Docs](https://lbliii.github.io/rosettes/) |

Python-native. Free-threading ready. No npm required.

---

## License

MIT
