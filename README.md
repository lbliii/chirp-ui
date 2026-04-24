# ʘ chirp-ui

[![PyPI version](https://img.shields.io/pypi/v/chirp-ui.svg)](https://pypi.org/project/chirp-ui/)
[![Tests](https://github.com/lbliii/chirp-ui/actions/workflows/tests.yml/badge.svg)](https://github.com/lbliii/chirp-ui/actions/workflows/tests.yml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://pypi.org/project/chirp-ui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://pypi.org/project/chirp-ui/)

**Python-native UI components for Chirp and Kida apps.**

chirp-ui gives server-rendered Python apps a real component vocabulary:
Kida macros, typed variants and sizes, registry-cited CSS classes, design
tokens, htmx/Alpine interaction patterns, and an agent-groundable manifest.
No Node pipeline. No utility-class vocabulary. No mystery CSS strings that
your Python tests and tools cannot see.

## Quick Start

```bash
pip install chirp chirp-ui
```

```python
from chirp import App, AppConfig, use_chirp_ui

app = App(AppConfig(template_dir="templates", debug=True))
use_chirp_ui(app, prefix="/static")
```

```kida
{% from "chirpui/layout.html" import container, grid, block %}
{% from "chirpui/card.html" import card %}
{% from "chirpui/button.html" import btn %}

{% call container() %}
  {% call grid(cols=2) %}
    {% call block() %}
      {% call card(title="Pipeline", subtitle="Live status") %}
        <p>Builds, deploys, and background jobs in one swappable panel.</p>
        {{ btn("View details", href="/pipeline", variant="primary") }}
      {% endcall %}
    {% endcall %}
    {% call block() %}
      {% call card(title="Queue", subtitle="7 jobs waiting") %}
        <p>Rendered on the server, ready for htmx refreshes.</p>
      {% endcall %}
    {% endcall %}
  {% endcall %}
{% endcall %}
```

When you use Chirp, `use_chirp_ui(app)` registers the template loader, filters,
static assets, debug-aware strict validation, Alpine runtime support, and
Chirp-aware link/swap helpers. For standalone Kida usage, use
`chirp_ui.get_loader()` and serve the files from `chirp_ui.static_path()`.

## What It Is

chirp-ui is the optional companion design system for
[Chirp](https://github.com/lbliii/chirp), built on
[Kida](https://github.com/lbliii/kida). It is not the framework itself. It is
one opinionated way to build Chirp apps with a polished default UI, predictable
HTMX behavior, and components that stay inspectable from Python.

The central idea is simple: the component registry is the source of truth.
Macros, CSS, docs, validation, and the shipped manifest are projections of that
registry.

## Use chirp-ui For

| Surface | What chirp-ui gives you |
|---|---|
| Chirp apps | App shells, navigation, cards, forms, overlays, dashboard panels, and htmx-safe patterns |
| Admin screens | Fragment islands, confirm flows, polling, row actions, inline edit controls, and status displays |
| Data-heavy pages | Tables, pagination, metrics, timelines, trees, charts, descriptions, and resource indexes |
| Streaming UIs | SSE status, streaming blocks, copy buttons, model cards, suspense states, and retry affordances |
| Documentation | Page heroes, nav trees, params tables, signatures, code blocks, and index cards |
| Coding agents | `chirp_ui.manifest.build_manifest()` with real components, slots, params, classes, and tokens |

## Component Vocabulary

chirp-ui ships more than 300 registry-described components and primitives.

| Family | Examples |
|---|---|
| Layout | `container`, `stack`, `cluster`, `grid`, `frame`, `block`, `split_layout`, `app_shell`, `workspace_shell` |
| Controls | `btn`, `icon_btn`, `button_group`, `segmented_control`, `row_actions`, `theme_toggle`, `copy_btn` |
| Feedback | `alert`, `badge`, `toast`, `spinner`, `skeleton`, `progress`, `empty_state`, `callout` |
| Forms | `text_field`, `select_field`, `checkbox_field`, `toggle_field`, `file_field`, `date_field`, `wizard_form` |
| Navigation | `tabs`, `route_tabs`, `breadcrumbs`, `navbar`, `sidebar`, `nav_tree`, `pagination`, `stepper` |
| Data display | `table`, `metric_card`, `stat`, `timeline`, `tree_view`, `calendar`, `avatar`, `description_list` |
| Overlays | `modal`, `drawer`, `tray`, `popover`, `tooltip`, `command_palette` |
| Effects and ASCII | `shimmer_button`, `glow_card`, `aurora`, `ascii_card`, `ascii_table`, `ascii_spinner` |

Composition primitives are macros, not utilities. Reach for `stack()`,
`cluster()`, `grid()`, `frame()`, and `block()` instead of inventing spacing or
display classes.

## Registry And Manifest

The registry in `chirp_ui.components.COMPONENTS` describes every public block:
variants, sizes, modifiers, BEM elements, slots, composed children, emitted
classes, tokens, maturity, authoring hints, and runtime requirements.

```python
from chirp_ui import load_manifest
from chirp_ui.components import design_system_report

manifest = load_manifest()
card = manifest["components"]["card"]
print(card["params"])
print(card["slots"])

report = design_system_report()
print(report["stats"]["total_components"])  # 309
```

The shipped manifest schema is `chirpui-manifest@3`. It is available as:

| Surface | How to read it |
|---|---|
| Python API | `chirp_ui.load_manifest()` or `chirp_ui.manifest.build_manifest()` |
| CLI | `python -m chirp_ui.manifest --json` |
| Package data | `chirp_ui.MANIFEST_PATH` |
| Docs build | `site/public/chirpui.manifest.json` from `poe docs-build-all` |

This is the agent contract: downstream tools should cite the manifest instead
of guessing component names, slots, variants, or CSS classes.

## CSS Contract

chirp-ui CSS is generated from partials and guarded by registry parity tests.
Every shipped `chirpui-*` class must be cited by a registry entry, defined in
CSS, and reachable from the templates that emit it.

The cascade order is public API:

```css
@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility, app.overrides;
```

Put application overrides in `app.overrides` and use `--chirpui-*` custom
properties for theming. Do not fight the design system with specificity.

```css
:root {
  --chirpui-accent: #2563eb;
  --chirpui-container-max: 80rem;
  --chirpui-radius-lg: 0.75rem;
}

@layer app.overrides {
  .billing-panel {
    --chirpui-card-hover-border: color-mix(in oklab, var(--chirpui-accent) 35%, var(--chirpui-border));
  }
}
```

For token and override details, see
[TOKENS.md](docs/TOKENS.md),
[CSS-OVERRIDE-SURFACE.md](docs/CSS-OVERRIDE-SURFACE.md), and
[COMPONENT-OPTIONS.md](docs/COMPONENT-OPTIONS.md).

## Interactivity

chirp-ui stays server-rendered by default. Interactive components are htmx- and
Alpine-native where browser state is the right tool.

| Pattern | Components and docs |
|---|---|
| HTMX fragments | `fragment_island`, `poll_trigger`, `oob`, `infinite_scroll`, [HTMX-PATTERNS.md](docs/HTMX-PATTERNS.md) |
| Alpine behavior | `dropdown`, `modal`, `tray`, `tabs`, `theme_toggle`, `copy_btn`, [ALPINE-MAGICS.md](docs/ALPINE-MAGICS.md) |
| App shell swaps | `app_shell`, `shell_frame`, `route_tabs`, [SHELL-TABS-CONTRACT.md](docs/SHELL-TABS-CONTRACT.md) |
| High-state islands | `island_root`, `grid_state`, `wizard_state`, `upload_state`, [DND-FRAGMENT-ISLAND.md](docs/DND-FRAGMENT-ISLAND.md) |
| Streaming | `streaming_block`, `sse_status`, `model_card`, `copy_btn`, [HTMX-ADVANCEMENT.md](docs/HTMX-ADVANCEMENT.md) |

Named Alpine controllers live in `chirpui-alpine.js` and register through
`Alpine.safeData()`, so htmx swaps can initialize behavior safely. Component
templates do not ship inline `<script>` tags.

## Standalone Kida

You can use chirp-ui without Chirp by adding its loader to a Kida environment.

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

In standalone setups, register equivalent filters/globals and serve
`chirpui.css`, `chirpui.js`, `chirpui-alpine.js`, themes, and pattern assets
from `chirp_ui.static_path()`.

## Requirements

| Package | Requirement |
|---|---|
| Python | `>=3.14` |
| Kida | `kida-templates>=0.8.0` |
| Chirp | Optional, but recommended for `use_chirp_ui(app)` |
| Browser JS | Alpine 3.x for interactive components; auto-injected by Chirp integration |

chirp-ui declares free-threading support and avoids build/runtime dependencies
that rely on the GIL. The build pipeline is Python-native and CSS is assembled
from package partials.

## Showcase

```bash
git clone https://github.com/lbliii/chirp-ui.git
cd chirp-ui
pip install -e ".[showcase]"
python examples/component-showcase/app.py
```

Then open <http://localhost:8000>.

With the b-stack workspace:

```bash
cd /path/to/b-stack
uv sync
uv run python chirp-ui/examples/component-showcase/app.py
```

## Development

```bash
git clone https://github.com/lbliii/chirp-ui.git
cd chirp-ui
uv sync --group dev
uv run poe ci
```

| Task | Command |
|---|---|
| Run tests | `uv run pytest` or `uv run poe test` |
| Type check | `uv run ty check src/chirp_ui/` or `uv run poe ty` |
| Lint | `uv run ruff check .` or `uv run poe lint` |
| Build CSS | `uv run poe build-css` |
| Check manifest | `uv run poe build-manifest-check` |
| Full CI | `uv run poe ci` |
| Docs site and showcase | `uv sync --group docs` then `uv run poe docs-build-all` |

If you edit CSS, change `src/chirp_ui/templates/css/partials/*.css`, run
`uv run poe build-css`, and commit the generated `chirpui.css`.

If you edit a macro's public surface, update the registry entry and regenerate
the manifest/docs projections.

## Status

chirp-ui is pre-1.0 and shipped. Core principles are stable: Python-native
components, registry-cited CSS, no utility vocabulary, htmx/Alpine defaults,
and free-threading-ready tooling. Some variants, experimental effects, and
legacy compatibility classes can still move before 1.0.

## The Bengal Ecosystem

chirp-ui is part of a pure-Python stack built for Python 3.14t free-threading.

| | | | |
|--:|---|---|---|
| **ᓚᘏᗢ** | [Bengal](https://github.com/lbliii/bengal) | Static site generator | [Docs](https://lbliii.github.io/bengal/) |
| **∿∿** | [Purr](https://github.com/lbliii/purr) | Content runtime | - |
| **⌁⌁** | [Chirp](https://github.com/lbliii/chirp) | Web framework | [Docs](https://lbliii.github.io/chirp/) |
| **ʘ** | **chirp-ui** | Python-native UI components | [Docs](https://lbliii.github.io/chirp-ui/) |
| **=^..^=** | [Pounce](https://github.com/lbliii/pounce) | ASGI server | [Docs](https://lbliii.github.io/pounce/) |
| **)彡** | [Kida](https://github.com/lbliii/kida) | Component template engine | [Docs](https://lbliii.github.io/kida/) |
| **ฅᨐฅ** | [Patitas](https://github.com/lbliii/patitas) | Markdown parser | [Docs](https://lbliii.github.io/patitas/) |
| **⌾⌾⌾** | [Rosettes](https://github.com/lbliii/rosettes) | Syntax highlighter | [Docs](https://lbliii.github.io/rosettes/) |
| **ᓃ‿ᓃ** | [Milo](https://github.com/lbliii/milo-cli) | Terminal UI framework | [Docs](https://lbliii.github.io/milo-cli/) |

Python-native. Free-threading ready. No npm required.

## License

MIT
