# Standalone core — chirp-ui without Chirp

**Scope:** **Kida renders macros; chirp-ui supplies the design system.** This
guide covers chirp-ui loader/filters, static assets, Alpine bootstrap, and CSRF
bridges — not how to install Kida in your web framework. For that, start with
Kida 0.11's [framework tutorials](https://lbliii.github.io/kida/docs/tutorials/flask-integration/)
(Flask, [Django](https://lbliii.github.io/kida/docs/tutorials/django-integration/),
[Starlette/FastAPI](https://lbliii.github.io/kida/docs/tutorials/starlette-integration/))
and the [Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/)
(`render_block`, introspection). Overlap between the two doc sets is audited in
[kida-overlap-audit.md](kida-overlap-audit.md).

Use this guide when you want chirp-ui in **Flask, FastAPI, Django, or any other
Python web stack** without adopting the Chirp framework. The per-framework guides
([Flask](flask.md), [FastAPI](fastapi.md), [Django](django.md)) only cover
framework-specific glue; everything in this document is shared.

See also: [capability matrix](capability-matrix.md) — what Chirp gives you for
free vs what you hand-roll standalone, and the [upgrade pitch](capability-matrix.md#upgrade-pitch-why-chirp)
for when standalone seams outweigh the design-system win.

---

## What you need

| Package | Role |
|---|---|
| `chirp-ui` | Kida macros, filters, CSS/JS assets |
| `kida-templates` | Template engine (pulled in by `chirp-ui`) |
| Your web framework | Routes, request/response, static serving |
| Alpine.js 3.x (CDN) | Interactive components (dropdown, modal, theme toggle, …) |
| htmx (CDN, optional) | Fragment swaps, polling, SSE — only if you use those patterns |

**Hard dependency:** `kida-templates` only. `bengal-chirp` is optional and used
by the showcase, not by the library itself.

The test suite already renders every component against a bare Kida
`Environment` with zero Chirp installed (`tests/conftest.py`). The standalone
path works today — this doc makes the wiring explicit and CI-proven.

---

## Bare Kida bootstrap

You do **not** use your framework's native template engine for chirp-ui macros.
Render kida directly and return the HTML string from your view.

```python
from kida import ChoiceLoader, Environment, FileSystemLoader

import chirp_ui
from chirp_ui import get_loader, register_filters, static_path


class _KidaFilterApp:
    """Adapter so ``register_filters()`` works on a kida ``Environment``."""

    def __init__(self, env: Environment) -> None:
        self._env = env

    def template_filter(self, name: str | None = None):
        def decorator(fn):
            self._env.filters[name] = fn
            return fn

        return decorator

    def template_global(self, name: str | None = None):
        def decorator(fn):
            self._env.globals[name] = fn
            return fn

        return decorator


def make_chirpui_env(*, template_dir: str = "templates") -> Environment:
    """Kida environment with chirp-ui loader + filters registered."""
    env = Environment(
        loader=ChoiceLoader([
            FileSystemLoader(template_dir),
            get_loader(),
        ]),
        autoescape=True,
    )
    register_filters(_KidaFilterApp(env))
    # Bridge CSRF for ``form()`` — wire to your framework's token (see below).
    from kida.template import Markup

    env.globals["csrf_field"] = lambda: Markup(
        '<input type="hidden" name="_csrf_token" value="CHANGE-ME">'
    )
    return env
```

Import macros in your kida templates as usual:

```kida
{% from "chirpui/card.html" import card %}
{% from "chirpui/button.html" import btn %}

{% call card(title="Hello") %}
  <p>Rendered by kida, not Jinja/Django templates.</p>
  {{ btn("Continue", href="/next", variant="primary") }}
{% endcall %}
```

Optional: call `chirp_ui.register_colors({"brand": "#6366f1"})` once at startup
if you use semantic color names with `resolve_color`, `badge(..., color=...)`, or
`filter_chips`.

---

## Static assets

Serve everything under `chirp_ui.static_path()` at a URL prefix your templates
use (commonly `/static`):

| Asset | Required | Purpose |
|---|---|---|
| `chirpui.css` | yes | Component styles + design tokens |
| `chirpui-transitions.css` | yes | Motion tokens (loaded after base CSS) |
| `chirpui.js` | yes | Pre-paint theme/style init |
| `chirpui-alpine.js` | when using interactive macros | Shared Alpine controllers |
| `patterns/*.svg`, `themes/*` | optional | Texture/pattern tokens, theme packs |

`get_library_contract()` lists the canonical load order if you fingerprint or
bundle assets programmatically.

---

## Alpine loading contract *(the #1 footgun)*

Interactive macros (`theme_toggle`, `dropdown_menu`, `modal`, `tabs_panels`,
`copy_button`, …) emit `x-data="chirpuiXxx()"`. Those factories live in
`chirpui-alpine.js` and register through **`Alpine.safeData`** (or the
`_chirpAlpineData` queue shim below).

Get this wrong and **every interactive component is silently dead** — no console
error from the macros themselves. `chirpui-alpine.js` includes a self-check that
logs a loud warning when Alpine never initializes; still, wire the scripts
correctly up front.

### Script order

1. `chirpui.js` — pre-paint theme/style (in `<head>` or early `<body>`)
2. **`Alpine.safeData` shim** — inline `<script>` (see below)
3. `chirpui-alpine.js` — **before** Alpine core
4. Alpine plugins (Mask, Intersect, Focus) — optional but recommended for parity
   with Chirp
5. Alpine core — `defer`, URL **must** end in `/dist/cdn.min.js`

```html
<link rel="stylesheet" href="/static/chirpui.css">
<link rel="stylesheet" href="/static/chirpui-transitions.css">
<script src="/static/chirpui.js"></script>

<!-- safeData shim — copy verbatim; queues registrations until alpine:init -->
<script>
(function(){
  var q=[];
  window._chirpAlpineData=function(n,f){
    if(window.Alpine&&Alpine.version){Alpine.data(n,f);}else{q.push([n,f]);}
  };
  document.addEventListener("alpine:init",function(){
    Alpine.store("modals",{});
    Alpine.store("trays",{});
    Alpine.safeData=function(n,f){Alpine.data(n,f);};
    q.forEach(function(r){Alpine.data(r[0],r[1]);});q=[];
  });
})();
</script>

<script src="/static/chirpui-alpine.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.15.8/dist/cdn.min.js"></script>
```

The shim is the same inline bootstrap [Chirp injects](https://github.com/lbliii/chirp/blob/main/src/chirp/server/alpine.py)
via `use_chirp_ui(app)`. `chirpui-alpine.js` falls back to
`window._chirpAlpineData` when `Alpine.safeData` is not yet defined.

**CDN footgun:** a bare `alpinejs@3.x` URL (without `/dist/cdn.min.js`) resolves
to the CommonJS build and throws `ReferenceError: module is not defined` in the
browser.

Validate rendered HTML in dev with:

```python
from chirp_ui.alpine import check_alpine_runtime

result = check_alpine_runtime(html)
if not result.ok:
    raise RuntimeError(result.problems)
```

**CSP:** interactive macros require `script-src 'unsafe-eval'` with standard
Alpine (plus a nonce or `'unsafe-inline'` for the safeData shim). See
[csp.md](csp.md) for the full contract — a secure CSP without `'unsafe-eval'`
silently disables every Alpine component.

---

## CSS subset (ship only what you use)

The committed `chirpui.css` includes every component (~700KB unminified). For
standalone apps that import a handful of macros, emit a **manifest-driven
subset**:

```bash
python scripts/build_chirpui_css.py --components card,btn,badge,form,alert \
  -o static/chirpui.subset.css
```

Or from Python:

```python
from chirp_ui.css_subset import CssSubsetPlan

plan = CssSubsetPlan.for_components(["card", "btn", "badge"])
paths = plan.partial_paths  # foundation + utilities + matched partials
```

Foundation partials (tokens, reset, base, layout) and shared utilities are
always included. Load `chirpui-transitions.css` separately if you use motion
classes. The monolithic `chirpui.css` remains the canonical full bundle.

---

## htmx

chirp-ui macros assume htmx attributes (`hx-get`, `hx-swap`, …) work when you
emit them. Add the htmx `<script>` tag yourself — Chirp injects it via
`use_chirp_ui(app)`.

For app-shell layouts, read [HTMX-PATTERNS.md](../components/htmx-patterns.md)
and wire `build_hx_attrs` (registered by `register_filters`) for dict-style
`hx={}` params.

---

## CSRF

`form()` and field macros expect a **`csrf_field`** global that renders a hidden
input. Bridge it to your framework:

| Framework | Bridge |
|---|---|
| Flask + Flask-WTF | `lambda: Markup(f'<input type="hidden" name="csrf_token" value="{csrf_token()}">')` |
| Django | `lambda: Markup(f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">')` |
| FastAPI | Wire to `starlette-csrf` or your middleware token |

Your framework's CSRF **middleware still enforces** the token; chirp-ui only
emits the field.

---

## Island / primitive components

Macros that call `island_attrs()` or `primitive_attrs()` assume Chirp's island
runtime. Standalone you either:

- **Avoid** island-backed components, or
- **Stub** the globals (return empty/minimal `data-island` attrs):

```python
from kida.template import Markup

env.globals["island_attrs"] = lambda *a, **k: Markup("")
env.globals["primitive_attrs"] = lambda *a, **k: Markup("")
```

See `tests/conftest.py` for production-faithful stubs used in the component test
suite.

---

## OOB / SSE / suspense

Macros render the markup; **emitting** OOB swap fragments, SSE frames, and
suspense responses is your server code's job. Chirp provides helpers
(`Suspense`, streaming HTML, shell OOB targets) that standalone stacks reimplement
per route.

---

## Dev checklist

- [ ] `get_loader()` in a `ChoiceLoader` with your app templates
- [ ] `register_filters()` via the kida adapter (or `use_chirp_ui` on Chirp)
- [ ] Static mount for `static_path()` at the URL your templates expect
- [ ] `csrf_field` global bridged to your CSRF token
- [ ] `chirpui.css` + `chirpui-transitions.css` linked
- [ ] `chirpui.js` + safeData shim + `chirpui-alpine.js` + Alpine core (in order)
- [ ] `check_alpine_runtime(html)` passes in dev when using interactive macros
- [ ] Optional: `register_colors()` for semantic color names

---

## Next steps

| Guide | When |
|---|---|
| [capability-matrix.md](capability-matrix.md) | Honest feature comparison before you commit |
| [flask.md](flask.md) | Flask / WSGI glue |
| [fastapi.md](fastapi.md) | FastAPI / Starlette glue |
| [django.md](django.md) | Django glue (most hand-roll, largest upgrade payoff) |
| [csp.md](csp.md) | Content-Security-Policy contract for interactive macros |
| [kida-overlap-audit.md](kida-overlap-audit.md) | How chirp-ui guides relate to Kida 0.11 framework docs |

### See also (Kida engine)

| Kida doc | When |
|---|---|
| [Flask Integration](https://lbliii.github.io/kida/docs/tutorials/flask-integration/) | `init_kida`, `render_template`, `render_block` in Flask |
| [Django Integration](https://lbliii.github.io/kida/docs/tutorials/django-integration/) | `KidaTemplates` backend, `using="kida"` |
| [Starlette & FastAPI Integration](https://lbliii.github.io/kida/docs/tutorials/starlette-integration/) | `KidaTemplates`, `TemplateResponse` |
| [Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/) | Block rendering, introspection, composition |
| [`kida check` CLI](https://lbliii.github.io/kida/docs/reference/cli/#kida-check) | Template verification (`--strict`, `--format json\|sarif`) |

When the standalone seams feel heavy, [Chirp's `use_chirp_ui`](https://lbliii.github.io/chirp/docs/build-apps/ui-extensions/chirp-ui/)
and the [capability-matrix upgrade pitch](capability-matrix.md#upgrade-pitch-why-chirp)
describe what gets deleted — Chirp is the destination, not the requirement.
