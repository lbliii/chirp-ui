# chirp-ui

**HTML over the wire, CSS without apology.**

A love letter to the web platform — reusable [Kida](https://github.com/lbliii/kida) components for [Chirp](https://github.com/lbliii/chirp). Gorgeous by default. Server-rendered fragments. Zero JavaScript for layout. Unapologetically modern CSS.

## Philosophy

chirp-ui celebrates what the web can do when you lean into it:

- **HTML over the wire** — Components render as blocks for htmx swaps, SSE streams, and view transitions. The server is the source of truth.
- **CSS as the design language** — Modern features (`:has()`, `aspect-ratio`, `clamp()`, `text-wrap: balance`) used where they add value.
- **Gorgeous by default** — Beautiful out of the box. Override `--chirpui-*` custom properties to customize.
- **Pushing the limits** — Container queries, fluid typography, intrinsic layouts. First impression: *"This is what the web can do?"*

## Install

```bash
pip install chirp-ui
```

When used with Chirp, components are auto-detected — no configuration needed.

## Component Showcase

Spin up a demo to browse all components:

```bash
pip install chirp chirp-ui
python examples/component-showcase/app.py
```

Open http://localhost:8000

## Quick Start

```html
{% from "chirpui/layout.html" import container, grid, block %}
{% from "chirpui/card.html" import card %}

{% call container() %}
    {% call grid(cols=2) %}
        {% call block() %}
            {% call card(title="Hello") %}
                <p>Card one.</p>
            {% end %}
        {% end %}
        {% call block() %}
            {% call card(title="World") %}
                <p>Card two.</p>
            {% end %}
        {% end %}
    {% end %}
{% end %}
```

Include the CSS in your base template. Serve assets from the package (recommended):

```python
from chirp.middleware.static import StaticFiles
import chirp_ui
app.add_middleware(StaticFiles(
    directory=str(chirp_ui.static_path()),
    prefix="/static"
))
```

Then in your base template:

```html
<link rel="stylesheet" href="/static/chirpui.css">
```

## Typography utilities

Use `--chirpui-*` tokens via utility classes:

| Class | Purpose |
|-------|---------|
| `chirpui-font-xs`, `chirpui-font-sm`, `chirpui-font-base`, `chirpui-font-lg`, `chirpui-font-xl`, `chirpui-font-2xl` | Font size |
| `chirpui-text-muted` | Muted text color |

## Layout

Tetris-inspired block system for responsive desktop-to-mobile layouts:

| Macro | Purpose |
|-------|---------|
| `container` | Max-width wrapper, centered. `max_width`, `padding` params. |
| `grid` | Auto-fit responsive grid. `cols` (2, 3, 4) for tighter columns. |
| `stack` | Vertical flex with gap. `gap` ("sm", "lg") for spacing. |
| `block` | Grid child. `span` (1, 2, 3, "full") for column span. |

```html
{% from "chirpui/layout.html" import container, grid, stack, block %}

{% call container() %}
    {% call stack() %}
        <h1>Title</h1>
        {% call grid(cols=3) %}
            {% call block() %}...{% end %}
            {% call block(span=2) %}...{% end %}
        {% end %}
    {% end %}
{% end %}
```

## Components

### Layout
| Component | Import | Features |
|-----------|--------|----------|
| **container** | `chirpui/layout.html` | Max-width, centered, responsive padding |
| **grid** | `chirpui/layout.html` | Auto-fit grid, cols 2–4 |
| **stack** | `chirpui/layout.html` | Vertical stack with gap |
| **block** | `chirpui/layout.html` | Grid child with span |

### UI
| Component | Import | Features |
|-----------|--------|----------|
| **card** | `chirpui/card.html` | Header, body (slot), footer, collapsible |
| **modal** | `chirpui/modal.html` | Dialog-based, trigger, close |
| **tabs** | `chirpui/tabs.html` | htmx tab switching |
| **dropdown** | `chirpui/dropdown.html` | Native `<details>`-based |
| **toast** | `chirpui/toast.html` | htmx OOB notifications |
| **table** | `chirpui/table.html` | Headers, row helper, sortable |
| **pagination** | `chirpui/pagination.html` | htmx page navigation |
| **alert** | `chirpui/alert.html` | Info, success, warning, error |
| **forms** | `chirpui/forms.html` | Field macros with error display |
| **badge** | `chirpui/badge.html` | Status indicators with icons |
| **spinner** | `chirpui/spinner.html` | Loading animations |
| **empty** | `chirpui/empty.html` | Empty state placeholders |
| **skeleton** | `chirpui/skeleton.html` | Loading placeholders with shimmer |
| **progress** | `chirpui/progress.html` | Progress bars |
| **status** | `chirpui/status.html` | Status indicators |

### Streaming & AI
| Component | Import | Features |
|-----------|--------|----------|
| **streaming_block** | `chirpui/streaming.html` | SSE content wrapper, cursor, aria-live |
| **copy_btn** | `chirpui/streaming.html` | Copy button with `data-copy-text` |
| **model_card** | `chirpui/streaming.html` | Card for LLM model comparison |

## Theming

chirp-ui ships with a gorgeous default: warm light mode, automatic dark mode via `prefers-color-scheme`. Override any `--chirpui-*` variable:

```css
:root {
    --chirpui-accent: #7c3aed;
    --chirpui-container-max: 80rem;
}
```

### Holy Light (optional)

WoW Blood Elf–inspired theme:

```html
<link rel="stylesheet" href="/static/chirpui.css">
<link rel="stylesheet" href="/static/themes/holy-light.css">
```

### Theme toggle

chirp-ui uses `prefers-color-scheme` by default. For manual light/dark switching, set `data-theme="light"` or `data-theme="dark"` on `<html>`. Example script:

```html
<script>
(function(){
  function apply(){ var t=localStorage.getItem('theme'); if(t) document.documentElement.dataset.theme=t; }
  function toggle(){
    var next=document.documentElement.dataset.theme==='dark'?'light':'dark';
    document.documentElement.dataset.theme=next;
    localStorage.setItem('theme',next);
  }
  document.addEventListener('DOMContentLoaded',apply);
  document.addEventListener('click',function(e){ if(e.target.closest('.theme-toggle')){ e.preventDefault(); toggle(); } });
})();
</script>
```

Add `class="theme-toggle"` to your toggle button. Ensure your CSS respects `[data-theme="light"]` and `[data-theme="dark"]` on `:root`.

## Animation and View Transitions

chirp-ui uses CSS-only motion: consistent timing, entrance/exit animations, and micro-feedback on interaction. All animations respect `prefers-reduced-motion: reduce`.

### Motion tokens

| Token | Value | Use |
|-------|-------|-----|
| `--chirpui-transition-fast` | 100ms | Micro-feedback (button press) |
| `--chirpui-transition` | 150ms | Default transitions |
| `--chirpui-transition-slow` | 250ms | Entrances, toggles |
| `--chirpui-ease-out` | cubic-bezier | Entrances |
| `--chirpui-ease-in-out` | cubic-bezier | Toggles |
| `--chirpui-ease-spring` | cubic-bezier | Playful feedback |

### Animation utilities

Opt-in classes for elements (work best with `@starting-style` or View Transitions):

- `chirpui-animate-fade-in` — opacity 0→1
- `chirpui-animate-slide-up` — translateY(8px)→0
- `chirpui-animate-scale-in` — scale(0.98)→1

### View Transitions (htmx swaps)

Enable Chirp's View Transitions for automatic htmx swap animations:

```python
from chirp import AppConfig
app = AppConfig(view_transitions=True)
```

Use `hx-swap="... transition:true"` for View Transitions on specific swaps. Override `::view-transition-old(root)` and `::view-transition-new(root)` in your CSS for custom effects.

Optional chirp-ui polish (slide-up + fade):

```html
<link rel="stylesheet" href="/static/chirpui.css">
<link rel="stylesheet" href="/static/chirpui-transitions.css">
```

### Component micro-feedback

- **Buttons** — Use `chirpui-btn` and `chirpui-btn--primary` for hover lift, active press, focus ring
- **Modal** — Entrance: scale + fade via `@starting-style`
- **Dropdown** — Menu entrance: opacity + translateY
- **Forms** — Error fields get a subtle shake when `.chirpui-field--error` is applied

### Skeleton loading

```html
{% from "chirpui/skeleton.html" import skeleton %}
{{ skeleton() }}
{{ skeleton(width="200px", height="2rem") }}
```

## SSE Patterns

For htmx SSE with streaming content:

- **streaming_block** — Use `sse_swap_target=true` to add `sse-swap="fragment" hx-target="this"` on the inner div. The slot is the placeholder; SSE fragments replace it.
- **model_card** — Use `sse_connect=url`, `sse_streaming=true` for LLM comparison UIs. Renders the full card with SSE wiring. See Chirp LLM playground.
- **hx-disinherit** — Use `hx-disinherit="hx-target hx-swap"` on the `sse-connect` element for isolated swaps when multiple SSE streams share a parent.
- **sse-close** — Set `sse-close="done"` (or your event name) so htmx closes the connection when the server sends that event.
- **copy_btn** — Returns HTML; use `{{ copy_btn(label="Copy", copy_text=text) }}`. When used inside htmx-swapped content, enable event delegation (e.g. `AppConfig(delegation=True)` in Chirp) so the copy handler works on dynamically inserted buttons.

Canonical examples: Chirp [RAG demo](https://github.com/lbliii/chirp/tree/main/examples/rag_demo) and [LLM playground](https://github.com/lbliii/chirp/tree/main/examples/llm_playground).

## Design Principles

- **Gorgeous by default** — Full visual design out of the box
- **htmx-native** — Interactive components use htmx or native HTML
- **Composable** — `{% slot %}` for content injection, components nest freely
- **Customizable** — Override `--chirpui-*` for colors, spacing, typography

## Manual Registration (without Chirp)

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

## Requirements

- Python >= 3.14
- kida-templates >= 0.1.2

## License

MIT
