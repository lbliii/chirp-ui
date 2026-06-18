# AI Chat & Agent-UI Completeness — Saga Plan

## Goal & posture
Close the AI-chat *compositions* that chirp-ui currently leaves to the application layer, while explicitly **not** rebuilding the mechanisms we already lead on. The posture is MIDDLE-PATH and additive: project typed Python state into the existing form/config surface, give streaming a named event grammar, and ship the message-turn / composer / shortcut compositions on top — no new framework, no client build step, no rewrite of `message_bubble`/`streaming.html`/`app_shell`.

## Provenance
Derived from an audit of **open-webui** (a SvelteKit + Tailwind LLM chat UI) run **2026-06-18**, cross-checked against the chirp-ui working tree the same day. The audit's purpose was a capability diff, not a feature-copy: most of open-webui's surface is either already covered, intentionally out of scope, or cheaply re-expressible in our stack (server-rendered Kida macros, `Alpine.safeData` factories, htmx swaps/SSE, hand-authored `chirpui-*` CSS under `@layer`/`@scope`, typed stdlib Python helpers à la `grid_state.py`/`route_tabs.py`).

## What chirp-ui already matches/exceeds
chirp-ui ships a structurally strong chat surface today: `message_bubble` + `message_thread`, `streaming.html` (`streaming_bubble`/`streaming_block`/`copy_btn`/`model_card`/`load_sentinel`), `chat_input` + `composer_shell` + `chat_layout`, `conversation_list` + `conversation_item`, and `sse_status`. On the *hard* parts we are ahead of the audited target: the streaming region is `role=\"log\"` with `aria-relevant=\"additions text\"`; motion is capped under `prefers-reduced-motion` at the base layer; overlays use native `<dialog>`; Cmd+K is a real, single-authority palette. This saga therefore closes compositions, not mechanisms.

## Recommended Execution Order
Phase ordering across epics. Two cross-cutting bets go **first** because they have the broadest blast radius and unblock the rest:
- **Phase 1 — keystone + cheapest-broadest:** *Server-state projection* (schema-driven config forms + parameter overrides) is the keystone — it unblocks param-overrides *and* slash-command forms once a typed schema can project into `forms.html`/`config_row`/`slider`/`toggle_group`. *SSE event-vocabulary doctrine* is the cheapest, widest-reach change — a named terminal/error/heartbeat grammar so a dropped stream stops shimmering forever.
- **Phase 2 — turn surface + ergonomics:** *Message turn surface* (per-turn actions, meta, reasoning, tool-call, citations) rides on the projection + SSE grammar. *Shortcut catalog + guarded handler + a11y/theming polish* hardens keyboard ergonomics around the new surfaces.
- **Phase 3 — composer:** *Real composer* (auto-grow, IME-safe send, send/stop cancellation, attachments, suggestions) lands last, consuming the SSE cancellation grammar and the projected slash-command forms.

## Server-state projection — schema-driven config forms + parameter overrides

**Phase:** 1  ·  **Priority:** P1  ·  **Audit lessons:** A (typed-descriptor projection beats string-keyed forms) + H (parameter overrides need an inherit/override tri-state, not a second form).

### Why this is the keystone

This is the "Python vocabulary, not string vocabulary" bet applied to *server state*. Today a settings form for a model/agent config is hand-authored: a developer writes a `dataclass` (or a Pydantic model) on the server, persists it, and then *separately* hand-writes a Kida form with one `text_field`/`select_field` per attribute. The two surfaces drift the instant anyone adds a field, renames a choice, or changes a default. We already proved the fix twice — `route_tabs.tab_is_active` and `grid_state.sort_columns` are typed, stdlib-only, Chirp-agnostic helpers that *project* developer-authored declarations into render-ready rows the macro consumes but never derives. `config_schema.py` is the third instance of that exact pattern, this time for config forms. `project_fields()` is the direct analog of `sort_columns()`: the same `Field` list the server validates/persists against produces the rendered control, its widget, its value, and its choices — so they structurally cannot drift.

Secondary unlock: `project_fields` is also what the **slash-command fill-in-form recipe** needs — a slash command (`/summarize`, `/translate`) names a parameter schema; the recipe calls `project_fields(SCHEMA, prefilled)` and renders `config_form()` inline in the composer. We get that recipe for free once the projection exists.

### Verified source facts this section builds on

- `src/chirp_ui/grid_state.py` — frozen `@dataclass(frozen=True, slots=True)`, `__all__`, stdlib only (`collections.abc`, `dataclasses`, `urllib.parse`), `_coerce_column(raw)` accepts a `Column` **or** a `Mapping` for caller convenience, and projection functions (`sort_columns`) return a list of frozen projected dataclasses (`ColumnSort`) the macro reads field-by-field.
- `src/chirp_ui/__init__.py` — grid_state symbols are imported (lines 33–43) and listed in `__all__` (lines 59–96).
- `src/chirp_ui/filters.py` — `register_filters()` registers template globals under `if hasattr(app, "template_global"):` via `tg = cast(..., app.template_global)` then `tg("sort_columns")(sort_columns)` etc. (lines 939–968). New globals go here.
- `src/chirp_ui/templates/chirpui/forms.html` — the **real** field macro signatures (verified):
  - `text_field(name, value="", label=none, errors=none, type="text", required=false, placeholder="", hint=none, ...)`
  - `password_field(name="password", value="", label=none, errors=none, required=true, ..., autocomplete="current-password", ...)`
  - `textarea_field(name, value="", label=none, errors=none, rows=4, required=false, placeholder="", hint=none, ...)`
  - `select_field(name, options, selected="", label=none, errors=none, required=false, hint=none, ...)` — `options` is a list of dicts read via `opt.get("value", "")` / `opt.get("label", opt.get("value", ""))`.
  - `toggle_field(name, checked=false, label=none, errors=none, size="", variant="", label_inside=false)`
  - `range_field(name, value=50, min=0, max=100, step=1, label=none, errors=none, hint=none, show_value=false)`
  - `number_scale(name, min=0, max=10, selected=none, label=none, errors=none, required=false, hint=none, low_label="", high_label="")`
  - `radio_field(name, options, selected="", ...)`, `multi_select_field(name, options, selected=none, ...)`, `hidden_field(name, value="")` also available.
  - `form(action, method="get", ...)` auto-adds `hx-select="unset"` + `hx-disinherit` when htmx is detected; mutating forms reset on success.
- `src/chirp_ui/templates/chirpui/badge.html` — `badge(text, variant="primary", appearance="", tone="", icon=none, cls="", color=none, fill="subtle", href=none)`. Use for the lock badge.
- `src/chirp_ui/templates/chirpui/tooltip.html` — `tooltip(content=none, hint=none, position="top", block=false, cls="")`, used via `{% call tooltip("...") %}<trigger>{% end %}`. Use for the lock reason.
- `tests/test_grid_state.py` — no-render, no-Chirp, plain `pytest` asserting on the projected dataclasses (`assert parse_sort("name") == GridSort("name", "asc")`). This is the test template.
- `tests/conftest.py` (lines 26–35, 318–323) — globals registered on the `env` fixture via `e.add_global("sort_columns", sort_columns)`. Add `project_fields` there so macro render tests can call it.
- `tests/test_strict_undefined.py` — renders each dict-iterating component with an empty `{}` item; we add `config_form`/`param_field` cases here.
- Existing chat surface already present: `chat_input.html`, `chat_layout.html`, `message_bubble.html`, `message_thread.html`, `streaming.html`, `live_badge.html` — this epic adds the *config/params* layer those live alongside.

### Step 1 — `src/chirp_ui/config_schema.py` (new file)

Mirrors `grid_state.py` exactly: module docstring with a Chirp-route example, stdlib-only imports, `__all__`, frozen slotted dataclasses, `_coerce_field` dict-or-dataclass tolerance, and a single projection function.

```python
"""Typed config-schema → form-field projection for chirp-ui.

Deliberately modeled on :mod:`chirp_ui.grid_state` and
:mod:`chirp_ui.route_tabs`: stdlib + dataclasses only, no ``import chirp`` and
no ``import kida``. Fully unit-testable with plain pytest and ``ty``-checkable
without a render ("works without Chirp, better with Chirp").

A developer declares a config once as a list of :class:`Field`. The same list
the server validates/persists against is projected by :func:`project_fields`
into :class:`ProjectedField` rows that carry the resolved ``widget``, the
current ``value``, and render-ready ``choices``. The ``config_form`` macro
reads those props directly and never derives them — so persisted server config
and the rendered form cannot drift (the :func:`grid_state.sort_columns` analog
for forms).

Example (Chirp route)::

    from chirp_ui import Field, Widget, project_fields

    MODEL_SETTINGS = [
        Field("model", type="str", label="Model", default="gpt-4o",
              choices=(("gpt-4o", "GPT-4o"), ("claude", "Claude"))),
        Field("temperature", type="float", label="Temperature",
              default=0.7, min=0.0, max=2.0, step=0.1),
        Field("stream", type="bool", label="Stream responses", default=True),
        Field("api_key", type="str", label="API key", secret=True),
        Field("system_prompt", type="str", label="System prompt",
              widget=Widget.TEXTAREA, default=""),
    ]

    fields = project_fields(MODEL_SETTINGS, values=load_settings(user))
    # -> template: {{ config_form(fields, action="/settings", method="post") }}
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

__all__ = ["Field", "ProjectedField", "Widget", "project_fields"]

_SECRET_MASK = ""  # secrets never round-trip to the client; render an empty input


class Widget(str, Enum):
    """The render target a :class:`ProjectedField` dispatches to.

    Each value maps to an existing macro in ``forms.html`` (text_field,
    textarea_field, select_field, toggle_field, range_field, number_scale,
    password_field). ``str`` mixin so ``widget == "select"`` works in templates.
    """

    TEXT = "text"
    TEXTAREA = "textarea"
    SELECT = "select"
    TOGGLE = "toggle"
    RANGE = "range"
    NUMBER = "number"
    PASSWORD = "password"


@dataclass(frozen=True, slots=True)
class Field:
    """A single config attribute — the developer-authored input.

    ``name`` is the stable form key (matches the server attribute). ``type`` is
    the Python type hint as a string (``"str"``/``"int"``/``"float"``/``"bool"``)
    used for widget inference when ``widget`` is not set. ``choices`` are
    ``(value, label)`` pairs (static); ``options_callable`` supplies them lazily
    (e.g. a live model list) and wins over ``choices`` when set. ``secret=True``
    forces a password widget and never echoes the value back to the client.
    ``min``/``max``/``step`` drive range/number widgets.
    """

    name: str
    type: str = "str"
    label: str = ""
    default: Any = None
    description: str = ""
    choices: tuple[tuple[str, str], ...] = ()
    widget: "Widget | None" = None
    secret: bool = False
    options_callable: Callable[[], Sequence[tuple[str, str]]] | None = None
    min: float | None = None
    max: float | None = None
    step: float | None = None


@dataclass(frozen=True, slots=True)
class ProjectedField:
    """A field projected for rendering. The macro reads these props directly.

    ``widget`` is the resolved :class:`Widget` *value* (a plain str, so the
    template can ``{% if pf.widget == "select" %}``). ``choices`` is a tuple of
    ``{"value", "label"}`` dicts — exactly the shape ``select_field`` /
    ``radio_field`` / ``multi_select_field`` already iterate with
    ``opt.get("value")`` / ``opt.get("label")``. ``value`` is masked (empty) for
    secrets.
    """

    name: str
    widget: str
    label: str
    value: Any
    description: str
    choices: tuple[Mapping[str, str], ...]
    secret: bool
    min: float | None
    max: float | None
    step: float | None
    required: bool


def _infer_widget(f: Field) -> Widget:
    """Infer a widget from ``type``/``choices``/``secret`` when not explicit."""
    if f.secret:
        return Widget.PASSWORD
    if f.choices or f.options_callable:
        return Widget.SELECT
    if f.type == "bool":
        return Widget.TOGGLE
    if f.type in ("int", "float"):
        # bounded numeric -> slider; unbounded -> plain number input
        return Widget.RANGE if (f.min is not None and f.max is not None) else Widget.NUMBER
    return Widget.TEXT


def _coerce_field(raw: "Field | Mapping[str, Any]") -> Field:
    """Accept a :class:`Field` or a plain dict (caller convenience).

    Mirrors :func:`grid_state._coerce_column`. ``widget`` in a dict may be a
    :class:`Widget`, its string value, or ``None``.
    """
    if isinstance(raw, Field):
        return raw
    widget = raw.get("widget")
    if isinstance(widget, str):
        widget = Widget(widget)
    choices = tuple((str(v), str(l)) for v, l in raw.get("choices", ()))
    return Field(
        name=str(raw.get("name", "")),
        type=str(raw.get("type", "str")),
        label=str(raw.get("label", "")),
        default=raw.get("default"),
        description=str(raw.get("description", "")),
        choices=choices,
        widget=widget,
        secret=bool(raw.get("secret", False)),
        options_callable=raw.get("options_callable"),
        min=raw.get("min"),
        max=raw.get("max"),
        step=raw.get("step"),
    )


def project_fields(
    schema: Sequence["Field | Mapping[str, Any]"],
    values: Mapping[str, Any] | None = None,
) -> list[ProjectedField]:
    """Project ``schema`` into render-ready :class:`ProjectedField` rows.

    The :func:`grid_state.sort_columns` analog for forms. For each field it
    resolves the widget (explicit ``widget`` wins, else :func:`_infer_widget`),
    reads the current value from ``values`` (falling back to ``default``, masked
    to empty for secrets), and normalizes choices to ``{"value","label"}`` dicts
    so the existing ``select_field``/``radio_field`` macros consume them
    unchanged. The macro never recomputes any of this — the server schema and
    the rendered control are the same source of truth.
    """
    vals = values or {}
    out: list[ProjectedField] = []
    for raw in schema:
        f = _coerce_field(raw)
        widget = (f.widget or _infer_widget(f)).value
        raw_val = vals.get(f.name, f.default)
        value = _SECRET_MASK if f.secret else raw_val
        choices_src = f.options_callable() if f.options_callable else f.choices
        choices = tuple({"value": str(v), "label": str(label)} for v, label in choices_src)
        out.append(
            ProjectedField(
                name=f.name,
                widget=widget,
                label=f.label or f.name,
                value=value,
                description=f.description,
                choices=choices,
                secret=f.secret,
                min=f.min,
                max=f.max,
                step=f.step,
                required=(f.default is None and not f.secret),
            )
        )
    return out
```

Design notes:
- **Secrets never round-trip.** `value` is forced empty for `secret=True`. The server keeps the stored secret; an empty submitted value means "unchanged" (route-side concern, documented in the macro docstring).
- **`choices` shape is deliberately the existing one.** `select_field` already iterates `opt.get("value")`/`opt.get("label")`; emitting `{"value","label"}` dicts means zero new macro plumbing and strict-undefined safety (the keys are always present).
- **No `import chirp`/`import kida`** — keeps it `ty`-checkable and unit-testable headless, exactly like `grid_state.py`.

### Step 2 — exports + template-global registration

In `src/chirp_ui/__init__.py`, add the import block next to the grid_state one (after line 43):

```python
from chirp_ui.config_schema import (
    Field,
    ProjectedField,
    Widget,
    project_fields,
)
```

And add to `__all__` (keep the existing alphabetical-ish ordering):

```python
    "Field",
    "ProjectedField",
    "Widget",
    "project_fields",
```

In `src/chirp_ui/filters.py`, inside the existing `if hasattr(app, "template_global"):` block (right after the grid_state `tg(...)` calls, ~line 968), import and register the projection as a template global so routes don't have to:

```python
        from chirp_ui.config_schema import Field, Widget, project_fields

        # Config-form server-state projection — registered beside sort_columns
        # so config_form can render widget/value/choices it never derives.
        # See chirp_ui.config_schema.
        tg("project_fields")(project_fields)
        tg("config_field")(Field)      # `{{ config_field("temp", type="float", ...) }}`
        tg("Widget")(Widget)           # exposes Widget.SELECT etc. for inline schemas
```

(Registering `Field` under the name `config_field` lets a template author declare a schema inline without a Python module, paralleling how `parse_sort` is exposed for ad-hoc routes. `Widget` is exposed so `widget=Widget.TEXTAREA` works in a template-side schema.)

Mirror these `add_global` calls in **both** `env` fixtures in `tests/conftest.py` (the two blocks at lines ~318–323 and ~374–378):

```python
    from chirp_ui.config_schema import Field, Widget, project_fields
    e.add_global("project_fields", project_fields)
    e.add_global("config_field", Field)
    e.add_global("Widget", Widget)
```

Manifest note: adding a Python helper does not change `manifest.json`, but the new `config_form`/`param_field` *macros* do — run `uv run poe build-manifest` and commit `manifest.json` (template line-numbers drift on any template edit; `build-manifest-check` gates CI).

### Step 3 — `config_form()` in `forms.html`

Add at the end of `forms.html`. It dispatches on `ProjectedField.widget` to the **real existing macros** (no new field primitives). Strict-undefined safe: `project_fields` always emits every key, and choices dicts always carry `value`/`label`.

```html
{# Schema-driven config form. `fields` is a list of ProjectedField (from
   chirp_ui.config_schema.project_fields) or plain dicts with the same shape.
   Dispatches each field to the matching forms.html macro by `.widget`.
   Pass `values=` only if you projected without values and want late binding;
   normally project on the server: project_fields(SCHEMA, values=stored).

   Usage (Chirp route already called project_fields):
       {{ config_form(fields, action="/settings", method="post") }}
#}
{% def config_form(fields, action="", method="post", submit_label="Save", errors=none, cls="") %}
{% call form(action, method=method, cls=("chirpui-config-form" ~ (" " ~ cls if cls else ""))) %}
    {% for f in fields %}
        {% set _name = f.get("name") if f is mapping else f.name %}
        {% set _widget = (f.get("widget", "text") if f is mapping else f.widget) %}
        {% set _label = (f.get("label", _name) if f is mapping else f.label) %}
        {% set _value = (f.get("value") if f is mapping else f.value) %}
        {% set _hint = (f.get("description", "") if f is mapping else f.description) %}
        {% set _choices = (f.get("choices", []) if f is mapping else f.choices) %}
        {% set _req = (f.get("required", false) if f is mapping else f.required) %}
        {% if _widget == "select" %}
            {{ select_field(_name, options=_choices, selected=_value, label=_label,
                            errors=errors, required=_req, hint=_hint) }}
        {% elif _widget == "toggle" %}
            {{ toggle_field(_name, checked=_value, label=_label, errors=errors) }}
        {% elif _widget == "range" %}
            {{ range_field(_name, value=_value,
                           min=(f.get("min", 0) if f is mapping else (f.min if f.min is not none else 0)),
                           max=(f.get("max", 100) if f is mapping else (f.max if f.max is not none else 100)),
                           step=(f.get("step", 1) if f is mapping else (f.step if f.step is not none else 1)),
                           label=_label, errors=errors, hint=_hint, show_value=true) }}
        {% elif _widget == "number" %}
            {{ text_field(_name, value=_value, label=_label, type="number",
                          errors=errors, required=_req, hint=_hint) }}
        {% elif _widget == "password" %}
            {{ password_field(_name, value="", label=_label, errors=errors,
                              required=_req, hint=_hint) }}
        {% elif _widget == "textarea" %}
            {{ textarea_field(_name, value=_value, label=_label, errors=errors,
                              required=_req, hint=_hint) }}
        {% else %}
            {{ text_field(_name, value=_value, label=_label, errors=errors,
                          required=_req, hint=_hint) }}
        {% end %}
    {% end %}
    {% call form_actions(align="end") %}
        {% from "chirpui/button.html" import btn %}
        {{ btn(submit_label, type="submit", variant="primary") }}
    {% end %}
{% end %}
{% end %}
```

Notes:
- `f is mapping` guard supports both `ProjectedField` (attribute access) and plain dicts (so a route that hand-builds dicts still works, and `test_strict_undefined.py` can pass `{}`-ish minimal dicts). The `.get(...)` form is the strict-undefined-safe path required by kida 0.7.0.
- Reuses `form()` (so htmx auto-isolation, reset-on-success, `hx-select="unset"` all come for free) and `form_actions()`/`btn()`.
- No new CSS strictly required (children reuse `.chirpui-field*`); add a thin `.chirpui-config-form` section to `css/partials/` only if grouping/spacing is needed, then `poe build-css`.

### Step 4 — `chirpui/param_override.html` (new): tri-state `param_field`, `advanced_params`, `locked`, `scope_indicator`

This is Lesson H. A parameter override is **not** the same as a config field: each param is tri-state — *inherit the model/agent default* (the value is `null`/absent) **or** *override with a custom value*. The control makes that explicit with a Default/Custom radio that toggles a nested value field via Alpine (factory registered in `chirpui-alpine.js`, never inline `<script>`).

```html
{#- chirp-ui: Parameter override controls
    Tri-state per-parameter override for AI chat/agent params. Each param either
    inherits a model/agent default (value = null/absent) or carries a custom
    override. Pairs with config_schema.project_fields for the inner control.

    Usage:
        from "chirpui/param_override.html" import param_field, advanced_params, scope_indicator

        {% call advanced_params() %}
            {{ param_field("temperature", value=0.9, default=0.7, widget="range",
                           min=0, max=2, step=0.1, label="Temperature") }}
            {{ param_field("model", value=none, default="gpt-4o", widget="select",
                           choices=models, label="Model",
                           locked=true, locked_reason="Set by your workspace admin") }}
        {% end %}
-#}

{# One overridable parameter. value=none -> inherit default; any value -> custom.
   locked=true renders the control disabled with a lock badge + reason tooltip. #}
{% def param_field(name, value=none, default=none, widget="text", label=none, choices=none,
                   min=0, max=100, step=1, errors=none, hint=none,
                   locked=false, locked_reason="") %}
{% set _label = label if label is not none else name %}
{% set _overridden = value is not none %}
<div class="chirpui-param" id="field-{{ name }}"
     x-data="chirpuiParamOverride({ overridden: {{ "true" if _overridden else "false" }} })">
    <div class="chirpui-param__head">
        <span class="chirpui-param__label">{{ _label }}</span>
        {% if locked %}
            {% from "chirpui/badge.html" import badge %}
            {% from "chirpui/tooltip.html" import tooltip %}
            {% call tooltip(locked_reason or "Locked", position="left") %}
                {{ badge("Locked", variant="muted", icon="lock") }}
            {% end %}
        {% end %}
    </div>
    <div class="chirpui-param__mode" role="radiogroup" aria-label="{{ _label }} source">
        <label class="chirpui-param__mode-opt">
            <input type="radio" name="{{ name }}__mode" value="default"
                   {% if not _overridden %}checked{% end %}
                   {% if locked %}disabled{% end %}
                   @change="overridden = false" x-model="modeDefault">
            <span>Default <span class="chirpui-param__default-val">{{ default }}</span></span>
        </label>
        <label class="chirpui-param__mode-opt">
            <input type="radio" name="{{ name }}__mode" value="custom"
                   {% if _overridden %}checked{% end %}
                   {% if locked %}disabled{% end %}
                   @change="overridden = true">
            <span>Custom</span>
        </label>
    </div>
    <div class="chirpui-param__custom" x-show="overridden" x-cloak>
        {% from "chirpui/forms.html" import text_field, select_field, range_field, toggle_field %}
        {% if widget == "select" %}
            {{ select_field(name, options=(choices or []), selected=(value or default),
                            label=none, errors=errors) }}
        {% elif widget == "range" %}
            {{ range_field(name, value=(value if value is not none else default),
                           min=min, max=max, step=step, label=none, errors=errors,
                           show_value=true) }}
        {% elif widget == "toggle" %}
            {{ toggle_field(name, checked=(value if value is not none else default),
                            label=none, errors=errors) }}
        {% else %}
            {{ text_field(name, value=(value if value is not none else default),
                          label=none, errors=errors) }}
        {% end %}
    </div>
    {% if hint %}<span class="chirpui-field__hint">{{ hint }}</span>{% end %}
</div>
{% end %}

{# Collapsible advanced-parameters disclosure. Wrap param_field calls. #}
{% def advanced_params(label="Advanced parameters", open=false, cls="") %}
<details class="chirpui-advanced-params{{ " " ~ cls if cls else "" }}"{% if open %} open{% end %}>
    <summary class="chirpui-advanced-params__summary">{{ label }}</summary>
    <div class="chirpui-advanced-params__body">
        {% slot %}
    </div>
</details>
{% end %}

{# Scope indicator — communicates whether a value is inherited or overridden.
   scope: "default" | "override". source labels the origin (e.g. "model", "chat"). #}
{% def scope_indicator(scope="default", source="", cls="") %}
{% set _override = scope == "override" %}
<span class="chirpui-scope-indicator chirpui-scope-indicator--{{ "override" if _override else "default" }}{{ " " ~ cls if cls else "" }}"
      role="status">
    <span class="chirpui-scope-indicator__dot" aria-hidden="true"></span>
    {% if _override %}
        Overridden{% if source %} for this {{ source }}{% end %}
    {% else %}
        Using {{ source or "model" }} default
    {% end %}
</span>
{% end %}
```

Alpine factory (add to `src/chirp_ui/templates/chirpui-alpine.js`, registered via `Alpine.safeData` — NO `<script>` in macros):

```javascript
// param-override: tri-state default/custom toggle. Idempotent (first-wins),
// htmx-safe via Alpine.safeData (re-binds on boosted swaps).
Alpine.safeData('chirpuiParamOverride', (cfg = {}) => ({
  overridden: !!cfg.overridden,
  get modeDefault() { return !this.overridden; },
}));
```

CSS: add a `/* param-override */` partial under `src/chirp_ui/templates/css/partials/` using the envelope convention (`@layer chirpui.component { @scope (.chirpui-param) to (.chirpui-param .chirpui-param) { ... } }`), plus `.chirpui-advanced-params` (style the `<details>`/`<summary>`) and `.chirpui-scope-indicator` (dot + muted/accent tone). Motion (the `<details>` open, the `x-show` reveal) must use `--chirpui-duration-*`/`--chirpui-easing-*` tokens (enforced by `test_transition_tokens.py`). Run `poe build-css` and commit `chirpui.css`. Add `x-cloak { display: none }` is already shipped; confirm via `test_template_css_contract.py` that every new class exists in `chirpui.css`.

A11y: lock uses a real `disabled` input + a visible `badge` + a `tooltip` carrying the reason (not just a `title`); the mode toggle is a labelled `role="radiogroup"`; `scope_indicator` is `role="status"`. The disclosure uses native `<details>`/`<summary>` (keyboard + SR free).

### Step 5 — tests

**`tests/test_config_schema.py`** — no-render, no-Chirp, plain pytest, mirroring `tests/test_grid_state.py`:

```python
"""Unit tests for chirp_ui.config_schema (AI chat saga, Phase 1).

No browser, no Chirp — the helper is stdlib + dataclasses only, mirroring
tests/test_grid_state.py. Locks the typed-projection contract config_form
renders from.
"""

import pytest
from chirp_ui.config_schema import Field, ProjectedField, Widget, project_fields


def test_explicit_widget_wins():
    pf = project_fields([Field("bio", type="str", widget=Widget.TEXTAREA)])[0]
    assert pf.widget == "textarea"


def test_infers_toggle_for_bool():
    assert project_fields([Field("stream", type="bool", default=True)])[0].widget == "toggle"


def test_infers_select_when_choices_present():
    f = Field("model", choices=(("a", "A"), ("b", "B")))
    pf = project_fields([f])[0]
    assert pf.widget == "select"
    assert pf.choices == ({"value": "a", "label": "A"}, {"value": "b", "label": "B"})


def test_bounded_numeric_is_range_unbounded_is_number():
    bounded = project_fields([Field("temp", type="float", min=0, max=2, step=0.1)])[0]
    unbounded = project_fields([Field("max_tokens", type="int")])[0]
    assert bounded.widget == "range"
    assert unbounded.widget == "number"


def test_value_pulled_from_values_then_default():
    fields = [Field("model", default="gpt-4o")]
    assert project_fields(fields, {"model": "claude"})[0].value == "claude"
    assert project_fields(fields, {})[0].value == "gpt-4o"


def test_secret_is_masked_and_forces_password():
    pf = project_fields([Field("api_key", secret=True)], {"api_key": "sk-real"})[0]
    assert pf.widget == "password"
    assert pf.value == ""  # never round-trips to the client


def test_options_callable_overrides_static_choices():
    pf = project_fields([Field("model", options_callable=lambda: [("x", "X")])])[0]
    assert pf.choices == ({"value": "x", "label": "X"},)


def test_accepts_plain_dict_like_coerce_column():
    pf = project_fields([{"name": "n", "type": "bool", "default": False}])[0]
    assert isinstance(pf, ProjectedField)
    assert pf.widget == "toggle"


def test_required_when_no_default_and_not_secret():
    assert project_fields([Field("q")])[0].required is True
    assert project_fields([Field("q", default="")])[0].required is False
    assert project_fields([Field("k", secret=True)])[0].required is False
```

**`tests/test_components.py`** — render tests using the `env` fixture (which now globals `project_fields`): assert `config_form(project_fields(SCHEMA, {...}))` emits the expected control classes (`chirpui-field__input` for text, a `<select>` for select, `.chirpui-toggle` for toggle, `type="range"` for range), and that a `secret` field renders an empty `type="password"` input. Add `param_field` render tests: default-mode emits an unchecked custom radio, override (value not none) checks custom, and `locked=true` emits `disabled` + the `Locked` badge + tooltip.

**`tests/test_strict_undefined.py`** — add `config_form` (passing a minimal projected dict `{"name": "x", "widget": "text"}` plus the `.get` defaults) and `param_field` (minimal `name` only) to the regression matrix so kida 0.7.0 strict-undefined breakage is caught.

**Manifest / CSS / contract gates:** after the new macros land, `uv run poe build-manifest` + `uv run poe build-css`, commit `manifest.json` + `chirpui.css`; `test_template_css_contract.py` and `test_description_coverage.py` (the doc-block on `param_override.html`) must pass. Run `make pre-pr`.

### Sequencing

1. `config_schema.py` + `test_config_schema.py` (pure Python; lands and is provable with zero template work — the keystone).
2. `__init__.py` exports + `filters.py` template-global registration + conftest globals.
3. `config_form()` in `forms.html` + render tests + strict-undefined cases.
4. `param_override.html` (`param_field`, `advanced_params`, `locked`, `scope_indicator`) + Alpine factory + CSS partial + render/a11y tests.
5. Wire `project_fields` into the slash-command fill-in-form recipe (follow-on recipe doc; the projection it needs already exists after step 1).

### Out of scope (explicit, to avoid advertising contracts we don't honor)

- Cross-request override *persistence* (route concern; chirp-ui only projects + renders).
- Live validation of submitted overrides against `min`/`max` server-side (the macro emits the HTML constraints; enforcement is the route's job).
- Per-field conditional visibility ("show X only when Y") — deferred; `Field` stays flat in v1, matching `grid_state`'s "ship no no-op contract" discipline (cf. the deliberately-not-shipped `Column(frozen=…)`).

## Streaming & SSE event-vocabulary doctrine (no infinite shimmer)

**Phase:** 1 — **Priority:** P1 — **Labels:** epic, documentation, javascript, accessibility, robustness, architecture

### Why this is the highest ROI-per-hour item

chirp-ui already ships every streaming *primitive* a chat/agent UI needs, and is verifiably ahead of open-webui on the a11y axis. What is missing is the **doctrine** — the shared event vocabulary and the two invariants that turn "I wired SSE and it mostly works" into "dropped connections, tool calls, and reloads all behave predictably." open-webui's hardest streaming bugs are *rules*, not *code*; the one genuinely missing line of code is a terminal-done handler.

**Verified source facts (read before editing):**

- `src/chirp_ui/templates/chirpui/streaming.html`
  - `streaming_block(streaming=false, sse_swap_target=false, cls="")` renders `<div class="chirpui-streaming-block{... --active if streaming}">` with `role="log" aria-relevant="additions text"`, a `{% try %} {% slot %} ... {% fallback %}` boundary, and a `chirpui-streaming-block__cursor` span gated purely on the `--active` class.
  - `streaming_bubble(role="assistant", state="", streaming=true, sse_swap_target=false, sse_connect=none, sse_close="done", cls="")` puts `hx-ext="sse" sse-connect=... sse-close="{{ sse_close }}" hx-disinherit="hx-target hx-swap"` on the `<article>`; the **inner** block gets `sse-swap="fragment" hx-target="this" hx-swap="beforeend"` when `sse_connect or sse_swap_target`. `state="thinking"` adds `aria-busy="true"` to the article; `state="error"` adds `role="alert"`.
  - **Line 6 dangling import (confirmed):** `{% from "chirpui/streaming.html" import streaming_block, copy_btn, prose %}` imports `prose`, but **no `prose` macro is defined** in the file (`.chirpui-prose` is a CSS class only). This is a *separate standalone bug* filed by the saga agent — NOT in scope for this epic.
- `src/chirp_ui/templates/chirpui-alpine.js`
  - `chirpuiSseRetry` exists and only flips a `retrying` flag on `htmx:afterRequest` / `responseError` / `sendError` (button-local busy state). **There is NO handler anywhere that listens for an SSE close/error and clears `aria-busy` or removes `chirpui-streaming-block--active`.** Grep for `sseClose|sseError|sse:close|sse:error` returns nothing across `src/` and `docs/`. So a dropped EventSource leaves the shimmer + `aria-busy="true"` on forever. This is the infinite-shimmer bug.
- `src/chirp_ui/templates/css/partials/038_streaming-and-ai-components.css`
  - `.chirpui-streaming-block__cursor` blinks via `chirpui-cursor-blink` and is visually shown by `.chirpui-streaming-block--active`. The `@media (prefers-reduced-motion: reduce)` block already caps it (`animation: none`). So the shimmer is entirely class-driven — removing `--active` is the correct, CSS-respecting way to stop it.
- `src/chirp_ui/templates/chirpui/sse_status.html` — `sse_status(state)` (connected/disconnected/error dot+label, `role="status" aria-live="polite"`) and `sse_retry(url, ...)` (htmx retry button, `chirpuiSseRetry`).
- `src/chirp_ui/templates/chirpui/oob.html` — `oob_toast(message, variant)` for transient server-pushed toasts; `oob_fragment(id, swap)`.
- `#260` (verified body): adopts `role="log" aria-relevant="additions text"` + the `role="status"` `load_sentinel` — **live-region semantics only**. This epic is the orthogonal layer: *event vocabulary* + *terminal-done invariant*. Do not duplicate #260's a11y prose; link to it.

### Deliverable 1 — `docs/patterns/sse-events.md` (new pattern doc)

Format mirrors `docs/patterns/data-grid.md` (intro thesis paragraph, "See also" links, tables, fenced route+template prototypes). Full outline:

```markdown
# SSE Event Vocabulary & the Terminal-Done Rule

chirp-ui's streaming primitives are server-driven and unopinionated about wire
format on purpose — but a chat/agent UI built on raw `sse-swap` will drift unless
the server and client agree on (1) a stable set of **event names**, (2) which
macro/swap each event drives, and (3) two non-negotiable rules. This doc is that
contract. It does NOT replace the live-region a11y semantics in #260 — those say
*how appended content is announced*; this says *what each event means and when the
shimmer must stop*.

See also:
- [COMPONENT-OPTIONS.md § Streaming](../COMPONENT-OPTIONS.md)
- [COMPONENT-OPTIONS.md § SSE Status](../COMPONENT-OPTIONS.md)
- [HTMX-PATTERNS.md](../HTMX-PATTERNS.md)
- #260 — Live-region polish (role=log + load sentinel)

## The event table

The server emits named SSE events; each maps to one macro target + one htmx swap
strategy. Names are a *recommended canonical set* — the rules below are mandatory,
the names are a starting vocabulary you can extend.

| Event name        | Meaning                              | Target macro / element                              | htmx swap strategy                          | Persist on reload? |
|-------------------|--------------------------------------|-----------------------------------------------------|---------------------------------------------|--------------------|
| `token`           | One token / chunk of assistant text  | inner `streaming_block` (`sse-swap="token"`)        | `hx-swap="beforeend"` (append)              | **Yes** (replay full text) |
| `thinking-start`  | Model began reasoning                 | the `streaming_bubble` article                       | client sets `aria-busy="true"` + `--thinking`| No (transient state) |
| `thinking-stop`   | Reasoning finished, answer begins     | same article                                         | client clears `aria-busy` / `--thinking`     | No |
| `tool-call`       | Agent invoked a tool                  | a `streaming_block` / card appended to the turn      | `hx-swap="beforeend"` (new block)           | **Yes** (replay result) |
| `citation`        | A source/citation chip                | a citation list region (`sse-swap="citation"`)       | `hx-swap="beforeend"`                        | **Yes** |
| `error`           | Recoverable stream error              | `streaming_bubble(state="error")` + `sse_retry()`    | `hx-swap="beforeend"` then **terminal-done** | No (re-render on retry) |
| `done`            | Stream finished cleanly               | the block's lifecycle hook                           | **terminal-done** (Rule 1)                   | n/a (it IS the end) |
| `toast`           | Transient notice (rate limit, saved)  | `oob_toast(...)` into `#chirpui-toasts`              | `hx-swap-oob` (OOB)                          | **No** (ephemeral) |

> The `done` row is special: it is named via `sse-close="done"` on the macro
> (the default), which tells htmx's SSE extension to close the EventSource. See
> Rule 1.

## Rule 1 (NON-NEGOTIABLE) — every stream close is a terminal "done"

A dropped connection, a network error, a server crash, and a clean `done` event
are **indistinguishable to the user** and must all land on the same terminal
state: shimmer off, `aria-busy` cleared. htmx's SSE extension fires `htmx:sseClose`
when the EventSource closes (including `sse-close="done"`) and `htmx:sseError` on a
connection error. chirp-ui ships a tiny `chirpuiStreamLifecycle` Alpine factory
that listens for both and performs the terminal-done cleanup. Opt in by adding the
`x-data` hook to the SSE-connected block (the macro does this for you):

(then: the chirpuiStreamLifecycle code block — see Deliverable 2)

Without this, a dropped socket strands `chirpui-streaming-block--active` (infinite
blinking cursor) and `aria-busy="true"` (a screen reader stuck on "busy") forever —
the single most common open-webui-class streaming bug.

## Rule 2 (NON-NEGOTIABLE) — persist-vs-ephemeral

On reload the server re-renders the conversation from its own store. Decide per
event whether it is **persisted** (replayed on reload) or **ephemeral** (lives only
in the live stream):

- **Persist & replay:** `token` text (the assistant turn), `tool-call` results,
  `citation`s, the final assistant message. On reload these come back as ordinary
  server-rendered `streaming_bubble`s with `streaming=false` — no SSE, no shimmer.
- **Ephemeral (never replay):** `toast` (an `oob_toast` is a one-shot notice),
  `thinking-start`/`thinking-stop` (a live state, not content), and `sse_status`
  transitions (connection chrome). A reloaded page shows the *result*, not the
  reasoning animation.

The litmus test: *if the user reloads mid-answer, would they be confused to NOT see
this again?* If yes -> persist. If it's chrome/notice/animation -> ephemeral.

## Relationship to #260

#260 standardizes the **live-region semantics**: `role="log" aria-relevant="additions text"`
on append targets and the `role="status"` `load_sentinel`. Those ship today. This
doc is the orthogonal layer — **event vocabulary + the terminal-done invariant** —
and depends on #260's roles being present (the lifecycle handler clears the
`aria-busy` that those regions rely on). They are complementary; neither subsumes
the other.
```

### Deliverable 2 — Rule 1 implementation: `chirpuiStreamLifecycle` (the only new code)

Register in `src/chirp_ui/templates/chirpui-alpine.js`, immediately after the existing `register("chirpuiSseRetry", ...)` block (lines ~1181–1207). Uses `this.$root` (stable across child-checkbox-style rebinds, matching the `chirpuiGridSelection` convention already in the file) and unbinds in `destroy()`:

```javascript
    // Rule 1 (terminal-done): ANY stream close — a clean `done` event, a
    // connection error, or a dropped socket — must clear aria-busy and stop
    // the shimmer. htmx's SSE extension fires htmx:sseClose when the
    // EventSource closes (including via sse-close="done") and htmx:sseError on
    // a connection error. We listen for both (plus the kebab spellings htmx
    // also dispatches and the send-error siblings) and run cleanup exactly
    // once. The streaming block stays mounted across token appends
    // (hx-swap="beforeend"), so this attaches in init() scoped to this.$root
    // and detaches in destroy(); it never re-fires per token. Without it a
    // dropped connection strands chirpui-streaming-block--active (infinite
    // cursor) and aria-busy="true" (screen reader stuck on "busy") forever.
    register("chirpuiStreamLifecycle", function () {
        var EVENTS = [
            "htmx:sseClose", "htmx:sseError",
            "htmx:sse-close", "htmx:sse-error",
            "htmx:sendError", "htmx:send-error",
        ];
        return {
            done: false,
            init: function () {
                var self = this;
                this._finish = function () { self.finish(); };
                EVENTS.forEach(function (name) {
                    self.$root.addEventListener(name, self._finish);
                });
            },
            finish: function () {
                if (this.done) { return; }
                this.done = true;
                // Drop the shimmer (CSS-gated on --active) and release the
                // busy region(s). Clear on the block AND its enclosing bubble,
                // since streaming_bubble puts aria-busy on the <article>.
                this.$root.classList.remove("chirpui-streaming-block--active");
                this.$root.removeAttribute("aria-busy");
                var bubble = this.$root.closest(
                    ".chirpui-streaming-bubble, .chirpui-message-bubble"
                );
                if (bubble) { bubble.removeAttribute("aria-busy"); }
            },
            destroy: function () {
                var self = this;
                EVENTS.forEach(function (name) {
                    self.$root.removeEventListener(name, self._finish);
                });
            },
        };
    });
```

Notes:
- No `<script>` in any macro (per CLAUDE.md). The factory is registered via the existing `register()` idempotency-guarded path; the macro only emits the `x-data="chirpuiStreamLifecycle()"` attribute.
- `closest(".chirpui-streaming-bubble, .chirpui-message-bubble")` — `streaming_bubble` puts `aria-busy="true"` on the `<article class="chirpui-message-bubble ...">` (verified line 26), so we clear it there too.
- Reduced-motion is already handled in CSS; removing `--active` is the canonical "stop" and respects it.

### Deliverable 3 — wire the hook into the macros (`streaming.html`, exact edits)

The SSE-connected inner block must carry the `x-data`. Add it only on the SSE path so non-SSE static renders stay byte-identical. In `streaming_bubble` (line ~27–28), the inner block currently is:

```html
    <div class="chirpui-streaming-block{{ " chirpui-streaming-block--active" if streaming else "" }}"
         {% if sse_connect or sse_swap_target %}sse-swap="fragment" hx-target="this" hx-swap="beforeend" {% endif %}role="log" aria-relevant="additions text">
```

Exact edit — add the lifecycle `x-data` inside the same SSE-only conditional:

```html
    <div class="chirpui-streaming-block{{ " chirpui-streaming-block--active" if streaming else "" }}"
         {% if sse_connect or sse_swap_target %}x-data="chirpuiStreamLifecycle()" sse-swap="fragment" hx-target="this" hx-swap="beforeend" {% endif %}role="log" aria-relevant="additions text">
```

And in `streaming_block` (line ~47–49):

```html
<div class="chirpui-streaming-block{{ " chirpui-streaming-block--active" if streaming else "" }}{{ " " ~ cls if cls else "" }}"
     {% if sse_swap_target %}x-data="chirpuiStreamLifecycle()" sse-swap="fragment" hx-target="this" {% endif %}role="log"
     aria-relevant="additions text">
```

(Optional follow-up, out of this epic's required scope: thread the same hook into `model_card`'s `sse_streaming` block at line ~88. Note in the plan, don't ship unless trivial.)

Manifest note: editing `streaming.html` shifts line numbers, so `manifest.json` will drift — run `poe build-manifest` and commit (per `feedback_workspace_git_gotchas`). No template-CSS-contract risk: no new classes introduced (we only add an attribute and reuse `--active`).

### Deliverable 4 — Rule 2 doc (covered in Deliverable 1's `## Rule 2` section)

No code. Pure doctrine in `sse-events.md`. The persist/ephemeral table column and the litmus test are the artifact.

### Test approach

1. **Unit (`tests/test_components.py`)** — render `streaming_bubble(sse_connect="/x")` and `streaming_block(sse_swap_target=true)`; assert the inner block contains `x-data="chirpuiStreamLifecycle()"` and `role="log"` and `aria-relevant="additions text"`. Render `streaming_block(streaming=true)` *without* `sse_swap_target` and assert it does NOT carry the `x-data` (static path unchanged). Use `assert_element` per Sprint 18 convention.
2. **Strict-undefined guard** — no new dict-iterating component, so no `tests/test_strict_undefined.py` case needed.
3. **Browser regression (`tests/browser/test_streaming_terminal_done.py`, in `test-browser-chrome-check`)** — render an SSE-connected `streaming_bubble`, dispatch a synthetic `htmx:sseError` (and separately `htmx:sseClose`) on the block, then assert (a) `chirpui-streaming-block--active` is gone and (b) no ancestor still has `aria-busy="true"`. This is the proof that a dropped connection cannot strand an infinite shimmer. Mirrors the gauntlet style of `tests/browser/test_data_grid_gauntlet.py`.
4. **Docs contract** — `sse-events.md` linked from `docs/INDEX.md`; add a `### Streaming event vocabulary` cross-link in `docs/COMPONENT-OPTIONS.md § Streaming` pointing at the new pattern doc and #260.

### Sequencing

1. Author `docs/patterns/sse-events.md` (table + Rule 1 + Rule 2 + #260 note) — pure docs, unblocks reviewers on the doctrine.
2. Add `chirpuiStreamLifecycle` to `chirpui-alpine.js` (Deliverable 2).
3. Wire the `x-data` hook into `streaming.html` (Deliverable 3); run `poe build-manifest`.
4. Add unit assertions + the browser regression (Test approach 1 & 3).
5. Cross-link from `COMPONENT-OPTIONS.md` and `INDEX.md`.
6. Run `make pre-pr` (full `poe ci` + docs-chrome browser smoke).

### Explicitly out of scope (filed separately by the saga)

- The dangling `prose` import on `streaming.html:6` — confirmed bug, separate standalone fix.
- Any new wire-format/SSE-transport opinion in Chirp itself — this epic is chirp-ui doctrine + the one client-side terminal-done handler only.

## Message turn surface — actions, meta, reasoning, tool-call, citations

**Saga:** AI Chat & Agent-UI Completeness · **Phase:** 2 · **Priority:** P1

### Problem (verified against source)

`src/chirp_ui/templates/chirpui/message_bubble.html` is a bare `<article>` with exactly one default slot:

```html
{% def message_bubble(align="left", role="default", status=none, cls="") %}
{% set role_valid = role | validate_variant_block("message_bubble", default="default") %}
...
<article class="chirpui-message-bubble{{ align_class }}{{ role_class }}{{ status_class }}{{ " " ~ cls if cls else "" }}">
    {% slot %}
</article>
{% end %}
```

It renders a message but ships none of the chrome a real chat/agent turn needs: per-message actions, provenance meta, reasoning/tool-call disclosure, agentic step timelines, or citation UI. This epic adds those compositions on top of primitives that already exist — extending, never greenfielding. Lessons B (compose, don't reinvent) + C (server-state-driven, one Alpine factory per concern).

### Primitives already in the repo (read & confirmed)

| Primitive | File | Signature / hooks used |
|---|---|---|
| `action_bar` / `action_bar_item` | `action_bar.html` | `action_bar(cls)` → `<nav role="toolbar">`; `action_bar_item(icon, label, count=none, href=none, active=false, cls)` |
| `collapse` | `collapse.html` | `collapse(trigger, open=false, cls)` → `<details>`; slots: `header_actions`, default; classes `.chirpui-collapse__trigger`, `__content` |
| `confirm_dialog` / `confirm_trigger` | `confirm.html` | `confirm_dialog(id, title, message=none, confirm_label, cancel_label, variant, confirm_url, confirm_method="POST", hx_target, hx_swap, ...)`; native `<dialog closedby="any">`; `confirm_method == "DELETE"` emits `hx-delete` |
| `modal` | `modal.html` | `modal(id, title=none, size="md", cls)`; slots `header_actions`, `footer`, default; `<dialog closedby="any">` |
| `avatar_stack` | `avatar_stack.html` | `.chirpui-avatar-stack`, `.chirpui-avatar-stack__more` (the overflow `+N` pill we reuse) |
| `description_list` | `description_list.html` | `description_list(items=[{term, detail, type?, icon?}], variant, ...)`; already `.get()`-guarded for strict-undefined |
| `spinner` / `spinner_thinking` | `spinner.html` | `spinner(size="md")`, `spinner_thinking(size="md")` → `role="status"` |
| `icon_btn` | `icon_btn.html` | `icon_btn(icon, variant="", size="", href=none, aria_label="", ...)` |
| `tooltip` | `tooltip.html` | `tooltip(content=none, hint=none, position="top", block=false)`; `data-tooltip` + `role="tooltip"` bubble |
| `label_overline` | `label_overline.html` | `label_overline(text, section=false, tag="span")` for small-caps section labels |
| `chirpuiCopy` (Alpine) | `chirpui-alpine.js` ~L1118 | `resolveText()` returns **only** `this.$el.dataset.copyText \|\| this.$el.previousElementSibling?.textContent`. **No strip selector** — content-aware copy MUST pass an explicit `data-copy-text`. |
| Shimmer tokens | `002_reset.css` L314-316 | `--chirpui-shimmer-from/via/to` (color-mix over `--chirpui-border`/`--chirpui-surface`) |
| Shimmer keyframe | `089_effects-foundation.css` L19 | `@keyframes chirpui-shimmer { 0% { transform: translateX(-100%) } 100% { transform: translateX(100%) } }` |
| Helper registration | `filters.py` L939-968 | `if hasattr(app, "template_global"): tg = cast(...); tg("name")(fn)`; helpers imported from `chirp_ui.grid_state` / `chirp_ui.route_tabs`, exported in `__init__.__all__` |
| `status_timeline` | docs only | Documented **Candidate** (Agent Run Monitor; `docs/screens/agent-run-monitor.md`, `docs/decisions/composition-taxonomy-inventory.md`, `docs/screens/promotion-ledger.md`). This epic promotes it to a shipped macro. |

### Sequencing (build order)

1. **`message_bubble` `actions` slot** (1-line additive change — unblocks everything).
2. **`message_actions`** + content-aware copy + destructive-delete-with-confirm.
3. **`message_meta`** (provenance row).
4. **Reasoning / tool-call disclosure** (`reasoning.html`) — FIRST among the disclosure work; makes streaming legible.
5. **`status_timeline` promotion**.
6. **Citations** (`citations.html` + `build_text_fragment_url`) — LAST; depends on the meta row + URL helper.

---

### 1. `message_bubble` gains an `actions` slot

Exact edit to `src/chirp_ui/templates/chirpui/message_bubble.html` — render `actions` after the default slot, still inside the `<article>`. Additive; existing single-slot callers are byte-identical (empty `actions` slot renders nothing).

```html
<article class="chirpui-message-bubble{{ align_class }}{{ role_class }}{{ status_class }}{{ " " ~ cls if cls else "" }}">
    {% slot %}
    {% slot actions %}
</article>
```

Update the doc-block `Usage:` to show `{% fill actions %}{{ message_actions(...) }}{% end %}`.

---

### 2. `message_actions` — new `chirpui/message_actions.html`

Composes `action_bar`/`action_bar_item`; never re-implements toolbar chrome. Reveal-on-`:focus-within` (and hover) so the bar is quiet until the turn is engaged; `data-last` keeps the last turn's bar always visible (the common "act on the latest answer" case). Horizontal overflow is contained by the existing `.chirpui-scroll-x` utility so long action rows never widen the bubble.

```html
{#- chirp-ui: Message actions
    Per-message toolbar for a chat/agent turn. Composes action_bar.
    Content-aware copy reads data-copy-text (chirpuiCopy has no strip selector).
    Destructive delete confirms by default; Shift-click bypasses the dialog.

    Usage:
        {% from "chirpui/message_actions.html" import message_actions %}
        {% call message_actions(is_last=true, copy_text=raw_markdown,
                                can_delete=true, delete_url="/m/42", delete_target="#m-42") %}
            {{ action_bar_item(icon="up", label="Good answer") }}
            {{ action_bar_item(icon="refresh", label="Regenerate") }}
        {% end %}
-#}
{% from "chirpui/action_bar.html" import action_bar, action_bar_item %}
{% from "chirpui/confirm.html" import confirm_dialog %}

{% def message_actions(is_last=false, can_delete=false, copy_text="", delete_url=none,
                       delete_target=none, confirm_id="chirpui-msg-del", cls="") %}
<div class="chirpui-message-actions{{ " chirpui-message-actions--last" if is_last else "" }}{{ " " ~ cls if cls else "" }}"
     {% if is_last %}data-last{% end %}>
  <div class="chirpui-scroll-x">
    {% call action_bar() %}
      <button type="button" class="chirpui-action-bar__item" aria-label="Copy message" title="Copy"
              x-data="chirpuiCopy()" data-copy-text="{{ copy_text | e }}" @click="copy()">
        <span class="chirpui-action-bar__icon" x-text="copied ? '✓' : '⧉'">⧉</span>
      </button>
      {% slot %}
      {% if can_delete %}
      <button type="button" class="chirpui-action-bar__item chirpui-action-bar__item--danger"
              aria-label="Delete message" title="Delete (Shift-click to skip confirm)"
              x-data
              @click="$event.shiftKey
                       ? $el.closest('form')?.requestSubmit()
                       : document.getElementById('{{ confirm_id }}')?.showModal()">
        <span class="chirpui-action-bar__icon">🗑</span>
      </button>
      {% end %}
    {% end %}
  </div>
  {% if can_delete and delete_url %}
  {{ confirm_dialog(confirm_id, title="Delete message?", message="This cannot be undone.",
                    confirm_label="Delete", variant="danger",
                    confirm_url=delete_url, confirm_method="DELETE",
                    hx_target=delete_target, hx_swap="outerHTML") }}
  {% end %}
</div>
{% end %}
```

Notes:
- **Content-aware copy**: `chirpuiCopy` (verified ~L1118) resolves text from `dataset.copyText` first; `previousElementSibling.textContent` is the only fallback and would grab rendered HTML text, not the source markdown. So we pass `data-copy-text="{{ copy_text | e }}"` explicitly — the server hands over the raw/markdown source it already has. No new factory; no `<script>` in the macro.
- **Destructive delete confirms by default**: the trash button opens the reused `confirm_dialog` (native `<dialog>.showModal()`). `@click.shift` (`$event.shiftKey`) bypasses straight to submitting the wrapping form — the power-user escape hatch. `x-data` (bare) is required so `@click` binds without a factory.
- **`can_delete` gate**: server authority. When false, neither the button nor the dialog render — no client-side hiding of a live affordance.
- **`confirm_method="DELETE"`** drives `confirm.html`'s `hx-delete` branch (verified at `confirm.html` L48). When the caller wires `delete_target`, the dialog's confirm form does the htmx swap; otherwise it falls back to a native `method="DELETE"` form.
- The `id_suffix`-style duplicate-id risk (two bars in a thread) is handled by the caller passing a unique `confirm_id` per message; default is fine for single-bubble fixtures/tests.

CSS — new partial `src/chirp_ui/templates/css/partials/0XX_message-actions.css` (envelope convention per CLAUDE.md):

```css
@layer chirpui.component {
  @scope (.chirpui-message-actions) to (.chirpui-message-actions .chirpui-message-actions) {
    :scope {
      opacity: 0;
      transition: opacity var(--chirpui-duration-fast) var(--chirpui-ease-standard);
    }
    /* reveal when the turn is engaged */
    .chirpui-message-bubble:hover > & ,
    .chirpui-message-bubble:focus-within > & ,
    :scope:focus-within { opacity: 1; }
    /* the latest turn keeps its bar visible */
    &[data-last] { opacity: 1; }

    .chirpui-action-bar__item--danger { color: var(--chirpui-danger); }
  }
}
@media (prefers-reduced-motion: reduce) {
  .chirpui-message-actions { transition: none; }
}
```

---

### 3. `message_meta` — new `chirpui/message_meta.html`

Provenance row: model name + timestamp inline; token-usage detail tucked behind an `icon_btn` + `tooltip` so the common case stays calm. `usage` is a caller dict — **strict-undefined hostile** — so every field is `.get()`-guarded and `| default("")`-rendered.

```html
{#- chirp-ui: Message meta
    Provenance row for an assistant turn: model, timestamp, optional token usage.
    usage is a caller dict; fields are .get()-guarded for strict-undefined (kida 0.7.0).

    Usage:
        {% from "chirpui/message_meta.html" import message_meta %}
        {{ message_meta("claude-opus-4-8", "2:34 PM",
                        usage={"input": 1820, "output": 412, "total": 2232}) }}
-#}
{% from "chirpui/icon_btn.html" import icon_btn %}
{% from "chirpui/tooltip.html" import tooltip %}
{% from "chirpui/label_overline.html" import label_overline %}

{% def message_meta(model, timestamp=none, usage=none, cls="") %}
<div class="chirpui-message-meta{{ " " ~ cls if cls else "" }}">
  <span class="chirpui-message-meta__model">{{ label_overline(model) }}</span>
  {% if timestamp %}<time class="chirpui-message-meta__time">{{ timestamp }}</time>{% end %}
  {% if usage %}
  {% call tooltip(position="top") %}
    <span class="chirpui-message-meta__usage" role="img"
          aria-label="Token usage: {{ usage.get('input') | default('0') }} in, {{ usage.get('output') | default('0') }} out">
      {{ icon_btn("ℹ", variant="ghost", size="sm", aria_label="Token usage details") }}
    </span>
  {% end %}
  <span class="chirpui-message-meta__usage-detail chirpui-visually-hidden">
    {% if usage.get("input") is not none %}in {{ usage.input }} · {% end %}
    {% if usage.get("output") is not none %}out {{ usage.output }} · {% end %}
    {% if usage.get("total") is not none %}total {{ usage.total }}{% end %}
  </span>
  {% end %}
</div>
{% end %}
```

Strict-undefined contract:
- Guards use `{% if usage.get("input") is not none %}`; inside the guard body `{{ usage.input }}` is safe (key proven present), matching the codebase pattern.
- The `aria-label` uses `usage.get('input') | default('0')` (unguarded access → must default).
- `message_meta(model="...", usage={})` renders the model + time only — no crash. (Regression case added.)

CSS partial: small flex row, `--chirpui-font-xs`, `--chirpui-text-muted`; tooltip + visually-hidden detail already exist as utilities. Envelope-wrapped.

---

### 4. Reasoning + tool-call disclosure — new `chirpui/reasoning.html`

Both sit over `collapse` (`<details>/<summary>`). Reasoning shows a shimmering "Thinking…" label while pending (server toggles `done`), then a static "Thought for…" label. Tool-call renders name + status pill, `args` via `description_list`, optional `result` + `files`.

```html
{#- chirp-ui: Reasoning + tool-call disclosure
    reasoning_block: collapsible chain-of-thought; shimmers while pending.
    tool_call_card: collapsible tool invocation with args/result/files.
    Both compose collapse.html. args is a caller dict-list (description_list, .get()-guarded).

    Usage:
        {% from "chirpui/reasoning.html" import reasoning_block, tool_call_card %}
        {% call reasoning_block(label_pending="Thinking…", label_done="Thought for 4s", done=true) %}
            <p>First I checked the schema…</p>
        {% end %}
        {{ tool_call_card("search_docs", status="done",
                          args=[{"term": "query", "detail": "css scope"}],
                          result="3 matches", files=["docs/CSS.md"]) }}
-#}
{% from "chirpui/collapse.html" import collapse %}
{% from "chirpui/description_list.html" import description_list %}
{% from "chirpui/spinner.html" import spinner_thinking %}

{% def reasoning_block(label_pending="Thinking…", label_done="Reasoning", done=false, open=false, cls="") %}
{% set _label = label_done if done else label_pending %}
<div class="chirpui-reasoning{{ " chirpui-reasoning--pending" if not done else "" }}{{ " " ~ cls if cls else "" }}">
  {% call collapse(trigger=_label, open=open) %}
    {% slot %}
  {% end %}
  {% if not done %}
  <span class="chirpui-reasoning__shimmer" aria-hidden="true"></span>
  {% end %}
</div>
{% end %}

{% def tool_call_card(name, status="pending", args=none, result=none, files=none, cls="") %}
{% set _status = status | validate_variant(("pending","running","done","error"), "pending") %}
<div class="chirpui-tool-call chirpui-tool-call--{{ _status }}{{ " " ~ cls if cls else "" }}">
  {% set _trigger %}
    {% if _status in ("pending", "running") %}{{ spinner_thinking(size="sm") }}{% end %}
    <span class="chirpui-tool-call__name">{{ name }}</span>
    <span class="chirpui-tool-call__status" aria-label="Status: {{ _status }}">{{ _status }}</span>
  {% end %}
  {% call collapse(trigger=_trigger) %}
    {% if args %}{{ description_list(items=args, variant="horizontal", compact=true) }}{% end %}
    {% if result %}<div class="chirpui-tool-call__result chirpui-rendered-content">{{ result }}</div>{% end %}
    {% if files %}
    <ul class="chirpui-tool-call__files">
      {% for f in files %}<li class="chirpui-tool-call__file">{{ f }}</li>{% end %}
    </ul>
    {% end %}
  {% end %}
</div>
{% end %}
```

Notes:
- `collapse`'s `trigger` is rendered as `{{ trigger }}` inside `<summary>` — passing a captured `{% set _trigger %}…{% end %}` block of safe markup is the established way to get a rich summary. (If kida's `{% set %}`-capture is unavailable in this version, fall back to a plain string trigger and render the spinner/status as `header_actions` slot fill — both are supported by `collapse`.)
- `args` flows straight into `description_list(items=…)`, which is already `.get()`-guarded; we never index `args` ourselves.
- `result` wraps in `.chirpui-rendered-content` (escaping decisions stay with the caller, per that macro's contract).
- Status vocabulary `pending/running/done/error` added to `VARIANT_REGISTRY` under a `tool_call` block (so `validate_variant` falls back to `pending`, never errors).

CSS partial — shimmer reuses the existing keyframe + tokens (no new keyframe):

```css
@layer chirpui.component {
  @scope (.chirpui-reasoning) to (.chirpui-reasoning .chirpui-reasoning) {
    :scope { position: relative; }
    .chirpui-reasoning__shimmer {
      position: absolute; inset: 0; pointer-events: none; overflow: hidden;
      border-radius: var(--chirpui-radius-md);
    }
    .chirpui-reasoning__shimmer::after {
      content: ""; position: absolute; inset: 0;
      background: linear-gradient(90deg,
        var(--chirpui-shimmer-from),
        var(--chirpui-shimmer-via),
        var(--chirpui-shimmer-to));
      animation: chirpui-shimmer 2s var(--chirpui-ease-standard) infinite;
    }
  }
}
@media (prefers-reduced-motion: reduce) {
  .chirpui-reasoning__shimmer::after { animation: none; }
}
```

(`--chirpui-shimmer-from/via/to` confirmed at `002_reset.css` L314-316; `@keyframes chirpui-shimmer` confirmed at `089_effects-foundation.css` L19. We reuse, not redefine.)

Tool-call status pill CSS uses existing variant tokens (`--chirpui-success`, `--chirpui-danger`, `--chirpui-accent`, muted) keyed off `&.chirpui-tool-call--done` etc.

---

### 5. Promote `status_timeline` — new `chirpui/status_timeline.html`

Promotes the documented Candidate (Agent Run Monitor). Server-state-driven: each step's `done` and `count` come from the server; the macro renders, never computes. `query_chips` is an optional caller list (strict-undefined guarded).

```html
{#- chirp-ui: Status timeline
    Vertical agentic step list: each step has an action type, label, done state,
    optional query chips and a result count. Server owns step state.

    Usage:
        {% from "chirpui/status_timeline.html" import status_timeline, status_step %}
        {% call status_timeline() %}
            {{ status_step(action_type="search", label="Searched docs", done=true,
                           query_chips=["css scope", "@layer"], count=12) }}
            {{ status_step(action_type="read", label="Reading results", done=false) }}
        {% end %}
-#}
{% from "chirpui/label_overline.html" import label_overline %}

{% def status_timeline(cls="") %}
<ol class="chirpui-status-timeline{{ " " ~ cls if cls else "" }}" role="list">
  {% slot %}
</ol>
{% end %}

{% def status_step(action_type, label, done=false, query_chips=none, count=none, cls="") %}
<li class="chirpui-status-step chirpui-status-step--{{ action_type }}{{ " chirpui-status-step--done" if done else " chirpui-status-step--active" }}{{ " " ~ cls if cls else "" }}"
    {% if not done %}aria-busy="true"{% end %}>
  <span class="chirpui-status-step__marker" aria-hidden="true">{{ "✓" if done else "•" }}</span>
  <div class="chirpui-status-step__body">
    <span class="chirpui-status-step__label">{{ label }}
      {% if count is not none %}<span class="chirpui-status-step__count">{{ count }}</span>{% end %}
    </span>
    {% if query_chips %}
    <span class="chirpui-status-step__chips">
      {% for chip in query_chips %}<span class="chirpui-chip chirpui-chip--sm">{{ chip }}</span>{% end %}
    </span>
    {% end %}
  </div>
</li>
{% end %}
```

Strict-undefined: `query_chips` and `count` default to `none`; `{% if query_chips %}` / `{% if count is not none %}` guard. `status_step(action_type="x", label="y")` renders with no chips/count — regression case added. `action_type` becomes a BEM modifier (caller-controlled enum like `search`/`read`/`run`/`write`); kept as a free string (CSS only styles the known set, unknowns render unstyled rather than error). Add the known `action_type` set to docs, not the registry (it's an open vocabulary).

CSS partial: connector line via `:scope` + `::before` on `__marker`, active step uses `--chirpui-accent`, done uses `--chirpui-success`; envelope-wrapped. Reuse `.chirpui-chip` if present, else add `.chirpui-chip--sm` to the chip partial.

---

### 6. Citations — new `chirpui/citations.html` + `chirp_ui/text_fragment.py`

Inline numbered citation chip, a sources summary that **reuses `avatar_stack` overflow CSS**, a citation modal over `modal`, and a pure-URL Python helper for `#:~:text=` deep links.

#### 6a. `build_text_fragment_url` — new `src/chirp_ui/text_fragment.py`

Chirp-agnostic, stdlib-only (matches `route_tabs.py` / `grid_state.py` posture). Produces a [Text Fragment](https://wicg.github.io/scroll-to-text-fragment/) deep link so a citation jumps to and highlights the exact quoted chunk.

```python
"""Text-fragment deep-link helper for chirp-ui citation UI.

Pure-URL, stdlib-only (Chirp-agnostic, like route_tabs / grid_state).
Builds ``#:~:text=`` scroll-to-text-fragment links.
"""

from urllib.parse import quote


def build_text_fragment_url(href: str, chunk: str | None = None) -> str:
    """Return ``href`` with a text-fragment so the browser scrolls to/highlights ``chunk``.

    >>> build_text_fragment_url("https://x.test/doc", "exact quote")
    'https://x.test/doc#:~:text=exact%20quote'

    No chunk -> href unchanged. An existing ``#fragment`` is preserved and the
    text directive is appended with the ``:~:`` delimiter per the spec.
    Percent-encodes ``-`` , ``,`` and ``&`` because they are text-directive
    syntax characters.
    """
    if not chunk:
        return href
    encoded = quote(chunk, safe="").replace("-", "%2D")
    directive = f"text={encoded}"
    if "#" in href:
        base, frag = href.split("#", 1)
        if ":~:" in frag:
            return f"{href}&{directive}"
        return f"{base}#{frag}:~:{directive}"
    return f"{href}#:~:{directive}"
```

Wiring:
- Export in `src/chirp_ui/__init__.py`: import alongside the grid_state block and add `"build_text_fragment_url"` to `__all__`.
- Register as a template global in `filters.py` inside the existing `if hasattr(app, "template_global"):` block:
  ```python
  from chirp_ui.text_fragment import build_text_fragment_url
  tg("build_text_fragment_url")(build_text_fragment_url)
  ```

#### 6b. `citations.html`

```html
{#- chirp-ui: Citations
    citation_chip: inline numbered <sup><a> linking to a source (text-fragment aware).
    sources_summary: compact stacked source pills (reuses avatar_stack overflow CSS).
    citation_modal: full source detail over modal.html.

    Usage:
        {% from "chirpui/citations.html" import citation_chip, sources_summary, citation_modal %}
        {{ citation_chip(index=1, title="Scope spec", href="https://x.test/doc",
                         source_id="src-1") }}
        {{ sources_summary(sources=[{"id": "src-1", "title": "Scope spec",
                                     "href": "https://x.test/doc", "relevance": "high"}]) }}
-#}
{% from "chirpui/modal.html" import modal %}

{% def citation_chip(index, title, href, source_id="", chunk=none, cls="") %}
{% set _href = build_text_fragment_url(href, chunk) if chunk else href %}
<sup class="chirpui-citation{{ " " ~ cls if cls else "" }}">
  <a class="chirpui-citation__link" href="{{ _href }}"
     {% if source_id %}data-source-id="{{ source_id }}"{% end %}
     aria-label="Citation {{ index }}: {{ title }}" title="{{ title }}"
     target="_blank" rel="noopener">{{ index }}</a>
</sup>
{% end %}

{% def sources_summary(sources, max_visible=4, label="Sources", cls="") %}
{% set _total = sources | length %}
<div class="chirpui-sources-summary{{ " " ~ cls if cls else "" }}" aria-label="{{ label }}">
  <span class="chirpui-avatar-stack chirpui-sources-summary__stack">
    {% for s in sources %}
    {% if loop.index <= max_visible %}
    <a class="chirpui-sources-summary__chip{{ " chirpui-relevance--" ~ s.relevance if s.get("relevance") in ("high","med","low") else "" }}"
       href="{{ s.href | default("#") }}" title="{{ s.get("title") | default("") }}"
       data-source-id="{{ s.get("id") | default("") }}">
      <span class="chirpui-sources-summary__index">{{ loop.index }}</span>
    </a>
    {% end %}
    {% end %}
    {% if _total > max_visible %}
    <span class="chirpui-avatar-stack__more">+{{ _total - max_visible }}</span>
    {% end %}
  </span>
</div>
{% end %}

{% def citation_modal(source, cls="") %}
{% set _id = "citation-" ~ (source.get("id") | default("src")) %}
{% call modal(_id, title=source.get("title") | default("Source"), size="md", cls=cls) %}
  <div class="chirpui-prose">
    {% if source.get("href") %}
    <p><a href="{{ source.href }}" target="_blank" rel="noopener">{{ source.href }}</a></p>
    {% end %}
    {% if source.get("excerpt") %}<blockquote>{{ source.excerpt }}</blockquote>{% end %}
    {% slot %}
  </div>
{% end %}
{% end %}
```

Notes:
- **`sources_summary` reuses `avatar_stack`**: it puts the chips inside a `.chirpui-avatar-stack` container and reuses `.chirpui-avatar-stack__more` for the `+N` overflow pill (verified hooks). No new overflow logic.
- **Strict-undefined**: `sources` items are caller dicts → all access via `.get()` + `| default()`; the relevance class only applies when `s.get("relevance")` is in the allowed set.
- **`build_text_fragment_url`** is called as a template global only when `chunk` is provided.
- **Relevance ramp** — add to a citations CSS partial:
  ```css
  @layer chirpui.component {
    .chirpui-relevance--high { --chirpui-relevance: var(--chirpui-success); }
    .chirpui-relevance--med  { --chirpui-relevance: var(--chirpui-accent); }
    .chirpui-relevance--low  { --chirpui-relevance: var(--chirpui-text-muted); }
    .chirpui-sources-summary__chip { border-color: var(--chirpui-relevance, var(--chirpui-border)); }
  }
  ```

---

### Validation-registry edits (`src/chirp_ui/validation.py`)

- `VARIANT_REGISTRY`: add a `"tool_call"` block → `("pending", "running", "done", "error")`, default `"pending"`. (Used by `tool_call_card`.)
- No new `SIZE_REGISTRY` entries (`spinner_thinking`/`icon_btn` reuse existing sizes).
- `message_bubble` block already exists (`validate_variant_block("message_bubble", ...)`); no change.

### Manifest / freshness

- Each new `.html` starts with a `{#- chirp-ui: Title … -#}` doc-block (enforced by `test_description_coverage.py`).
- After template edits, regenerate: `uv run poe build-manifest` (manifest line numbers drift on any template line shift — memory `feedback_workspace_git_gotchas`). CSS is concat-from-partials: add partials under `css/partials/`, run `uv run poe build-css`, commit both `chirpui.css` and the partials.

### Test approach

`tests/test_components.py` (render + structural via `assert_element`):
- `message_bubble` with a filled `actions` slot renders the slot content inside `<article>`; empty `actions` is byte-identical to today.
- `message_actions`: copy button carries `data-copy-text`; danger button present only when `can_delete=true`; `confirm_dialog` rendered only when `can_delete and delete_url`; `confirm_method="DELETE"` reaches the dialog.
- `message_meta`: model + timestamp render; usage tooltip + `aria-label` present when `usage` truthy; absent when not.
- `reasoning_block`: `--pending` class + `__shimmer` present when `done=false`, absent when `done=true`; default slot content inside `.chirpui-collapse__content`.
- `tool_call_card`: status pill reflects `status`; `description_list` rendered from `args`; `files` list rendered; invalid status falls back to `pending` (validate_variant).
- `status_timeline`/`status_step`: `--done`/`--active` modifier; `aria-busy="true"` only when not done; chips + count render when provided.
- `citation_chip`: `<sup>` + `<a aria-label="Citation N: …">`; `href` rewritten with `#:~:text=` when `chunk` passed.
- `sources_summary`: reuses `.chirpui-avatar-stack` + `.chirpui-avatar-stack__more` `+N`; relevance class applied only for allowed values.
- `citation_modal`: `modal` with `.chirpui-prose` body.

`tests/test_strict_undefined.py` (regression — render each dict-iterating component with an empty `{}` item / empty inputs):
- `message_meta(model="m", usage={})` → no crash.
- `tool_call_card("t", args=[{}], files=[])` → no crash (args row renders empty term/detail via description_list's existing guards).
- `status_step(action_type="x", label="y")` (no `query_chips`, no `count`) → no crash.
- `sources_summary(sources=[{}])` → no crash (all `.get()` access defaults).

`tests/test_transition_tokens.py` / `test_template_css_contract.py`: every new class exists in `chirpui.css`; all animations use `--chirpui-duration-*` / `--chirpui-ease-*` tokens (shimmer reuses `chirpui-shimmer` + `--chirpui-ease-standard`).

New Python helper test `tests/test_text_fragment.py`:
- `build_text_fragment_url("h", None) == "h"`; chunk encodes spaces/`-`; existing `#frag` preserved (`#frag:~:text=…`); a second directive appends with `&`.

Browser/a11y smoke (`tests/browser/`, non-blocking): `message_actions` reveal on `:focus-within`, Shift-click delete bypass, citation chip focus + text-fragment navigation, reasoning shimmer respects `prefers-reduced-motion`. axe pass on a fixture composing all six pieces in a `message_thread`.

### Docs

- `docs/COMPONENT-OPTIONS.md`: add a "Message turn surface" subsection documenting all new macros + the `message_bubble` `actions` slot.
- `docs/screens/agent-run-monitor.md` + `docs/decisions/composition-taxonomy-inventory.md` + `docs/screens/promotion-ledger.md`: flip `status_timeline` from Candidate → shipped, cite this epic.
- Showcase fixture in `examples/component-showcase`: a full assistant turn (bubble + meta + reasoning + tool-call + citations + actions) so the promotion has proof.

## Shortcut catalog + guarded handler + a11y/theming polish

**Phase:** 2 · **Priority:** P2 (catalog/handler tasks P1; OLED + extra unit coverage P2)

### Why this epic (lessons F + I)

- **Lesson F — the modal that lies.** open-webui #17015: a keyboard-shortcut help modal listed bindings that the handler had since renamed/removed, so users pressed advertised keys and nothing happened. Root cause: two sources of truth (a hand-written modal table + a separate switch in JS). Fix: **one declarative catalog** (`shortcuts.py`) that the modal renders from *and* the handler dispatches from. The catalog cannot drift from itself.
- **Lesson I — the shortcut that fires into your text.** open-webui's Cmd+Shift+S-style global shortcuts fired while the user was typing in the composer, mangling input or triggering destructive actions. Fix: an **input-context guard** — a non-allowlisted shortcut early-returns when `document.activeElement` is a text field; only an explicit allowlist (Escape, focus-composer/send into the composer) is permitted to run there.
- Plus two cheap polish items verified as *missing today*: there is **zero** `env(safe-area-inset)` and **zero** `viewport-fit` anywhere in `src/chirp_ui/templates/chirpui.css` or the partials (`grep` confirmed exit 1), so a sticky composer is clipped behind the home indicator on notched phones; and there is no near-black OLED theme.

**Triage order: safe-area before OLED.** Safe-area is a *correctness* fix (clipped composer = unreachable send button on a phone). OLED is *taste*. Ship the catalog + handler + safe-area first; OLED last.

### Verified source facts (read before implementing)

- `kbd.html` exports `{% def kbd(keys, size="", cls="", attrs_map=none) %}` — accepts a scalar or iterable, renders `<kbd class="chirpui-kbd">` with one `<span class="chirpui-kbd__key">` per key. The modal reuses this; do **not** hand-roll `<kbd>`.
- `command_palette.html` is the native-`<dialog>` reference: `<dialog id=... x-ref="dialog" closedby="any">`, opened via `dialog.showModal()` in the `chirpuiCommandPalette` factory; `closedby="any"` gives Escape/backdrop close for free. Mirror this exactly for the help modal.
- `theme_toggle.html` → `chirpuiThemeToggle` factory (chirpui-alpine.js:1209): `order = ["system", "light", "dark"]`, `icons = { light:"○", dark:"●", system:"◐" }`, persists via `writeDocumentPreference("data-theme", "chirpui-theme", value)`. Pre-paint boot is a single inline IIFE in `app_shell_layout.html:76`.
- Helpers in chirpui-alpine.js: `register(name, factory)` (idempotent, first-wins, line 206); `readDocumentPreference(attr, fallback)` (line 47); `writeDocumentPreference(attr, storageKey, value)` (line 51); `safeSetItem` warns on failure. New factories register via `register(...)` like every sibling.
- Global registration pattern (`filters.py:939`): inside `if hasattr(app, "template_global"):`, `tg = cast(..., app.template_global)` then `tg("name")(fn)` — exactly how `tab_is_active`, `sort_columns` are wired. Test parity in `tests/conftest.py` via `e.add_global("name", fn)` (lines 318–325).
- Dark tokens live in `002_reset.css`: `:root` defines `--chirpui-surface: light-dark(#ffffff, #1e293b)`, `--chirpui-bg: light-dark(#f8fafc, #0f172a)`, `--chirpui-surface-alt: light-dark(#f8fafc, #334155)` (and an oklch upgrade under `@supports`). `[data-theme="dark"]` only overrides *semantic* colors (primary/success/…), not bg/surface — those come from `light-dark()` + `color-scheme`. OLED therefore overrides the three base tokens directly.
- `068_data-theme-support.css` today is **only** `color-scheme` rules for light/dark/system (21 lines, ends at L21). The OLED block is appended here.
- `083_app-shell.css`: topbar is `position: sticky; top: 0` (L64), `.chirpui-app-shell__main` has `padding: var(--chirpui-spacing-lg)` (L316). `018_chat-input.css` has no sticky dock and no safe-area today.

---

### Prototype 1 — `src/chirp_ui/shortcuts.py` (the single source of truth)

Chirp-agnostic, stdlib-only, structured like `route_tabs.py` / `grid_state.py`. Exported in `__init__.__all__`, registered as template globals.

```python
"""Declarative keyboard-shortcut catalog for chirp-ui.

The catalog is the single source of truth: ``shortcuts_help.html`` renders the
help modal from it, and the ``chirpuiShortcuts`` Alpine factory dispatches from
the same data (serialized via :func:`shortcuts_json`). This makes the open-webui
#17015 class of bug structurally impossible — the modal cannot advertise a
binding the handler does not run, because both read one list.

Chirp-agnostic and stdlib-only, like ``route_tabs.py`` and ``grid_state.py``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Shortcut:
    """One keyboard shortcut.

    ``keys`` are *display* tokens rendered via ``kbd()`` in the modal (e.g.
    ``("⌘", "K")``). The handler matches on ``mod`` (ctrlKey||metaKey, unified),
    ``shift``, and ``event_key()``. ``allow_in_input`` opts a shortcut past the
    input-context guard (Escape, focus-composer, composer send) — everything
    else early-returns when focus is in a text field.
    """

    id: str
    keys: tuple[str, ...]
    label: str
    action: str
    category: str = "General"
    mod: bool = False
    shift: bool = False
    key: str = ""
    allow_in_input: bool = False

    def event_key(self) -> str:
        """The ``event.key`` to match, lowercased. Defaults to the last display token."""
        return (self.key or self.keys[-1]).lower()


DEFAULT_SHORTCUTS: tuple[Shortcut, ...] = (
    Shortcut("help", ("?",), "Show keyboard shortcuts", "open-help", "General", key="?"),
    Shortcut("palette", ("⌘", "K"), "Open command palette", "open-palette", "General", mod=True, key="k"),
    Shortcut("focus-composer", ("/",), "Focus the message composer", "focus-composer", "Chat", key="/"),
    Shortcut("send", ("⌘", "↵"), "Send message", "send", "Chat", mod=True, key="enter", allow_in_input=True),
    Shortcut("escape", ("Esc",), "Close / cancel", "escape", "General", key="escape", allow_in_input=True),
)


def shortcuts_by_category(
    shortcuts: tuple[Shortcut, ...] = DEFAULT_SHORTCUTS,
) -> dict[str, list[Shortcut]]:
    """Group shortcuts by category for the help modal, preserving insertion order."""
    grouped: dict[str, list[Shortcut]] = {}
    for sc in shortcuts:
        grouped.setdefault(sc.category, []).append(sc)
    return grouped


def shortcuts_json(shortcuts: tuple[Shortcut, ...] = DEFAULT_SHORTCUTS) -> str:
    """Serialize the catalog for the ``chirpuiShortcuts`` Alpine factory.

    Only the handler-relevant fields are emitted (display ``keys`` stay
    server-side for the modal). Embedded in a ``<script type="application/json">``
    so the handler reads the same data the modal rendered from.
    """
    return json.dumps(
        [
            {
                "id": s.id,
                "action": s.action,
                "mod": s.mod,
                "shift": s.shift,
                "key": s.event_key(),
                "allowInInput": s.allow_in_input,
            }
            for s in shortcuts
        ]
    )
```

**Exact edit — `src/chirp_ui/__init__.py`.** Add to the import block alongside the other helper imports, and add the three names to `__all__`:

```python
from chirp_ui.shortcuts import (
    DEFAULT_SHORTCUTS,
    Shortcut,
    shortcuts_by_category,
    shortcuts_json,
)
# ... in __all__ = [ ... ]:
    "Shortcut",
    "DEFAULT_SHORTCUTS",
    "shortcuts_by_category",
    "shortcuts_json",
```

**Exact edit — `src/chirp_ui/filters.py`** (inside the existing `if hasattr(app, "template_global"):` block, right after `tg("sort_query")(sort_query)`):

```python
        from chirp_ui.shortcuts import shortcuts_by_category, shortcuts_json
        # Keyboard-shortcut catalog (#<epic>) — registered beside tab_is_active so
        # shortcuts_help.html and the chirpuiShortcuts handler render/dispatch from
        # one source. Cannot drift (open-webui #17015).
        tg("shortcuts_by_category")(shortcuts_by_category)
        tg("shortcuts_json")(shortcuts_json)
```

**Exact edit — `tests/conftest.py`** (beside the existing `e.add_global(...)` lines ~318–325):

```python
from chirp_ui.shortcuts import shortcuts_by_category, shortcuts_json
# ...
    e.add_global("shortcuts_by_category", shortcuts_by_category)
    e.add_global("shortcuts_json", shortcuts_json)
```

---

### Prototype 2 — `src/chirp_ui/templates/chirpui/shortcuts_help.html`

Native `<dialog closedby="any">` like `command_palette` (Escape + backdrop close free). Rows render from `shortcuts_by_category()`; keys via `kbd()`. The catalog JSON for the handler is emitted once here so the modal and handler share one payload. Strict-undefined safe (we own the `Shortcut` objects, not caller dicts, so attribute access is fine — but the doc-block + `test_strict_undefined` case still applies because the macro iterates the grouped mapping).

```html
{#- chirp-ui: Keyboard shortcuts help
    A modal listing all keyboard shortcuts, rendered from the declarative
    shortcuts.py catalog. The same catalog drives the chirpuiShortcuts handler
    (via shortcuts_json), so the modal can never advertise a binding the handler
    does not run (open-webui #17015).

    Usage:
        from "chirpui/shortcuts_help.html" import shortcuts_help, shortcuts_help_trigger
        {{ shortcuts_help_trigger() }}
        {{ shortcuts_help() }}   {# place once near </body> #}
-#}

{% from "chirpui/kbd.html" import kbd %}

{% def shortcuts_help(id="shortcuts-help", title="Keyboard shortcuts") %}
{#- Host element carries the global handler. The catalog JSON is the single
    payload the handler reads — identical data to what the modal rows render. -#}
<div x-data="chirpuiShortcuts()" x-init="init()" data-shortcuts-host>
    <script type="application/json" x-ref="catalog">{{ shortcuts_json() | safe }}</script>
    <dialog id="{{ id }}" x-ref="dialog" class="chirpui-shortcuts-help" closedby="any"
            aria-labelledby="{{ id }}-title">
        <div class="chirpui-shortcuts-help__inner">
            <header class="chirpui-shortcuts-help__header">
                <h2 id="{{ id }}-title" class="chirpui-shortcuts-help__title">{{ title }}</h2>
                <button type="button" class="chirpui-shortcuts-help__close"
                        aria-label="Close" @click="$refs.dialog.close()">×</button>
            </header>
            {% for category, items in shortcuts_by_category().items() %}
            <section class="chirpui-shortcuts-help__group">
                <h3 class="chirpui-shortcuts-help__category">{{ category }}</h3>
                <dl class="chirpui-shortcuts-help__list">
                    {% for sc in items %}
                    <div class="chirpui-shortcuts-help__row" data-shortcut-id="{{ sc.id }}">
                        <dt class="chirpui-shortcuts-help__label">{{ sc.label }}</dt>
                        <dd class="chirpui-shortcuts-help__keys">{{ kbd(sc.keys, size="sm") }}</dd>
                    </div>
                    {% end %}
                </dl>
            </section>
            {% end %}
        </div>
    </dialog>
</div>
{% end %}

{% def shortcuts_help_trigger(target="shortcuts-help", label="Keyboard shortcuts", cls="") %}
<button type="button"
        class="chirpui-btn chirpui-btn--ghost chirpui-btn--sm chirpui-shortcuts-help-trigger{{ " " ~ cls if cls else "" }}"
        x-data="chirpuiDialogTarget()" data-dialog-target="{{ target }}"
        @click="open()" aria-label="{{ label }}">
    {{ kbd("?", size="sm") }}
</button>
{% end %}
```

Note: `kbd(sc.keys, ...)` passes the `tuple` — `kbd()` already handles iterables (`keys is iterable and keys is not string`). `chirpuiDialogTarget` is the existing trigger factory (chirpui-alpine.js:1255), reused so the trigger and command-palette trigger behave identically.

---

### Prototype 3 — `chirpuiShortcuts` Alpine factory (append to `chirpui-alpine.js` via `register(...)`)

The **input-context guard** is the load-bearing part: a non-allowlisted shortcut early-returns when `document.activeElement` is a text field. The handler reads the catalog from the `<script type="application/json">` the modal emitted — one payload, no second source.

```javascript
    // Keyboard-shortcut handler (#<epic>). Reads the declarative catalog from a
    // <script type="application/json"> (emitted by shortcuts_help.html from the
    // SAME shortcuts.py data the modal rows render from), so the help modal can
    // never advertise a binding the handler does not run (open-webui #17015).
    //
    // Input-context guard: a shortcut early-returns when focus is in a text field
    // UNLESS it is allowlisted (allowInInput) — this kills open-webui's
    // Cmd+Shift+S-fires-into-the-composer footgun. Allowlisted today: Escape and
    // the composer send (which is *meant* to run while the composer is focused).
    register("chirpuiShortcuts", function () {
        return {
            _shortcuts: [],
            init: function () {
                var raw = this.$refs.catalog ? this.$refs.catalog.textContent : "[]";
                try {
                    this._shortcuts = JSON.parse(raw) || [];
                } catch (e) {
                    this._shortcuts = [];
                    console.warn("chirp-ui: invalid shortcuts catalog JSON:", e.message);
                }
                var self = this;
                this._onKey = function (ev) { self._handle(ev); };
                document.addEventListener("keydown", this._onKey);
            },
            destroy: function () {
                if (this._onKey) {
                    document.removeEventListener("keydown", this._onKey);
                }
            },
            // True when focus is in a text-entry context that a shortcut must not
            // hijack. contentEditable is a string ("true"/"false"/"inherit").
            _inInput: function () {
                var el = document.activeElement;
                if (!el) { return false; }
                var tag = el.tagName;
                if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") {
                    return true;
                }
                return el.isContentEditable === true;
            },
            _handle: function (ev) {
                // Unify Ctrl (Win/Linux) and Cmd (mac) into one "mod" concept.
                var mod = ev.ctrlKey || ev.metaKey;
                var key = (ev.key || "").toLowerCase();
                var inInput = this._inInput();
                for (var i = 0; i < this._shortcuts.length; i++) {
                    var sc = this._shortcuts[i];
                    if (sc.key !== key) { continue; }
                    if (Boolean(sc.mod) !== mod) { continue; }
                    if (Boolean(sc.shift) !== ev.shiftKey) { continue; }
                    // THE GUARD: skip non-allowlisted shortcuts while typing.
                    if (inInput && !sc.allowInInput) { return; }
                    ev.preventDefault();
                    if (sc.action === "open-help") {
                        this._openDialog();
                    } else {
                        // Server/page code listens for chirpui:shortcut:<action>.
                        document.dispatchEvent(
                            new CustomEvent("chirpui:shortcut:" + sc.action, {
                                bubbles: true,
                                detail: { id: sc.id },
                            })
                        );
                    }
                    return;
                }
            },
            _openDialog: function () {
                var d = this.$refs.dialog;
                if (d && typeof d.showModal === "function" && !d.open) {
                    d.showModal();
                }
            },
        };
    });
```

Design notes:
- `mod` unification (`ctrlKey || metaKey`) means the catalog declares `mod: true` once and it works cross-platform — no per-OS branching.
- The guard returns on the **matched** shortcut: a match that's blocked in an input doesn't fall through to a different shortcut with the same key. (Catalog has no such collision today, but the early `return` is the safe contract.)
- `open-help` is handled in-factory (it owns the dialog); every other action dispatches a `chirpui:shortcut:<action>` `CustomEvent` so app/page code wires behavior (focus composer, send, close active overlay) without the factory knowing about chat internals.

---

### Prototype 4 — `env(safe-area-inset)` padding (correctness fix, ships before OLED)

Today: `grep "safe-area-inset\\|viewport-fit"` over `chirpui.css` and every partial returns **nothing** (exit 1). On a notched phone with a sticky composer, the send button sits under the home indicator. `max()` makes this a no-op when the inset is `0` (every non-notched device / desktop), so it is always safe to ship unconditionally.

**Exact edit — `src/chirp_ui/templates/css/partials/018_chat-input.css`.** Add a sticky-dock modifier (the composer mounted at the bottom of a fill-mode chat panel) carrying the bottom inset:

```css
/* Sticky composer dock — when the chat-input is pinned to the bottom of a
   fill-mode panel, pad past the home indicator on notched phones. max() is a
   no-op off-notch (env() resolves to 0), so this is unconditionally safe.
   Requires <meta name="viewport" content="...,viewport-fit=cover"> for env()
   to resolve to nonzero on iOS Safari — without it the insets are always 0. */
.chirpui-chat-input--dock {
    position: sticky;
    bottom: 0;
    z-index: var(--chirpui-z-sticky);
    background: var(--chirpui-surface);
    padding-block-end: max(var(--chirpui-spacing), env(safe-area-inset-bottom));
}
```

**Exact edit — `src/chirp_ui/templates/css/partials/083_app-shell.css`.** Pad the sticky topbar's inline edges and `main`'s bottom for landscape notches + the home indicator. Append to the existing `.chirpui-app-shell__topbar` and `.chirpui-app-shell__main` rules (do not change existing declarations — add these):

```css
/* Safe-area: keep topbar content clear of landscape notches; keep the last row
   of main content above the home indicator. max() is a no-op off-notch. */
.chirpui-app-shell__topbar {
    padding-inline: max(var(--chirpui-spacing), env(safe-area-inset-left))
                    max(var(--chirpui-spacing), env(safe-area-inset-right));
}
.chirpui-app-shell__main {
    padding-block-end: max(var(--chirpui-spacing-lg), env(safe-area-inset-bottom));
}
```

**Docs note (add to `docs/COMPONENT-OPTIONS.md` chat section and the chat-layout doc):** `env(safe-area-inset-*)` only resolves to a nonzero value when the page sets `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`. Without `viewport-fit=cover` the insets are `0` and the `max()` falls back to the base spacing token — correct, just not notch-aware. App authors own the `<meta>` tag (it's not in `app_shell_layout.html` because it changes scroll/zoom behavior app-wide); document the recommended value.

---

### Prototype 5 — OLED theme (additive, ships last)

`[data-theme="oled"]` overrides only the three base surface tokens to near-black, derived from the *existing dark tokens* via `color-mix` toward black — so it tracks any future dark-token retune instead of hardcoding hex. Appended to `068_data-theme-support.css` (today only `color-scheme` rules).

**Exact edit — `src/chirp_ui/templates/css/partials/068_data-theme-support.css`** (append; also add the `color-scheme` rule so native controls render dark):

```css
[data-theme="oled"] {
    color-scheme: dark;
    /* Near-black surfaces for OLED power savings + deep contrast. Derived from
       the existing dark tokens (002_reset.css) by mixing toward black, so OLED
       follows any dark-palette retune instead of pinning literal hex. Only the
       three base surface tokens change; all semantic colors inherit from dark. */
    --chirpui-bg: color-mix(in oklab, var(--chirpui-bg) 12%, black);
    --chirpui-surface: color-mix(in oklab, var(--chirpui-surface) 30%, black);
    --chirpui-surface-alt: color-mix(in oklab, var(--chirpui-surface-alt) 30%, black);
}
```

Note: `[data-theme="oled"]` does not get the `light-dark()` machinery, so it must set `color-scheme: dark` itself (mirrors how `[data-theme="dark"]` relies on `color-scheme`). The mixed-from tokens reference the dark values because `color-scheme: dark` makes `light-dark()` resolve to its dark arm before the mix.

**Exact edit — `chirpui-alpine.js`, `chirpuiThemeToggle` factory (L1216–1221).** Add `"oled"` to the cycle after `"dark"` and add its glyph:

```javascript
    register("chirpuiThemeToggle", function () {
        return {
            theme: "system",
            icons: { light: "○", dark: "●", system: "◐", oled: "⬤" },
            init: function () {
                this.theme = readDocumentPreference("data-theme", "system");
            },
            cycle: function () {
                var order = ["system", "light", "dark", "oled"];
                var index = (order.indexOf(this.theme) + 1) % order.length;
                this.theme = order[index];
                writeDocumentPreference("data-theme", "chirpui-theme", this.theme);
            },
        };
    });
```

Also update the `aria-label` in `theme_toggle.html` (L17) to `"Toggle theme (light, dark, oled, system)"`.

**Exact edit — pre-paint boot script, `app_shell_layout.html:76`.** The boot reads any stored value and applies it; today it accepts anything (defaulting to `"system"`). To harden against a stale/garbage value while accepting `"oled"`, constrain to the known set:

```html
<script nonce="{{ csp_nonce() }}">
(function(){var T=["system","light","dark","oled"];var t=localStorage.getItem("chirpui-theme");if(T.indexOf(t)<0){t="system";}var s=localStorage.getItem("chirpui-style")||"default";document.documentElement.setAttribute("data-theme",t);document.documentElement.setAttribute("data-style",s);})();
</script>
```

---

### CSS for the help modal (new partial `src/chirp_ui/templates/css/partials/0NN_shortcuts-help.css`)

Use the envelope convention (default for new components): `@layer chirpui.component { @scope (.chirpui-shortcuts-help) to (.chirpui-shortcuts-help .chirpui-shortcuts-help) { … } }`. Motion via `--chirpui-duration-*`/`--chirpui-easing-*` tokens only (enforced by `test_transition_tokens.py`). Mirror `command_palette`'s `<dialog>`/`::backdrop` styling. Register a numbered partial; run `poe build-css` to regenerate `chirpui.css` and commit both (concat gate `poe build-css-check`).

```css
@layer chirpui.component {
    @scope (.chirpui-shortcuts-help) to (.chirpui-shortcuts-help .chirpui-shortcuts-help) {
        :scope {
            margin: auto;
            max-inline-size: min(32rem, 92vw);
            padding: 0;
            border: 1px solid var(--chirpui-border);
            border-radius: var(--chirpui-radius);
            background: var(--chirpui-surface);
            color: var(--chirpui-text);
            box-shadow: var(--chirpui-elevation-overlay);
        }
        :scope::backdrop { background: var(--chirpui-smoke-bg); }
        .chirpui-shortcuts-help__inner { padding: var(--chirpui-spacing-lg); }
        .chirpui-shortcuts-help__header {
            display: flex; align-items: center; justify-content: space-between;
            margin-block-end: var(--chirpui-spacing);
        }
        .chirpui-shortcuts-help__list {
            display: grid; grid-template-columns: 1fr auto;
            gap: var(--chirpui-spacing-xs) var(--chirpui-spacing);
            margin: 0;
        }
        .chirpui-shortcuts-help__row { display: contents; }
        .chirpui-shortcuts-help__category {
            margin-block: var(--chirpui-spacing) var(--chirpui-spacing-xs);
            font-size: var(--chirpui-font-xs); text-transform: uppercase;
            letter-spacing: 0.05em; color: var(--chirpui-text-muted);
        }
        .chirpui-shortcuts-help__keys { justify-self: end; }
    }
}
```

(Reuse `--chirpui-smoke-bg` / `--chirpui-elevation-overlay` — both already used by drawer/modal partials.)

---

### Test approach

1. **`tests/test_shortcuts.py` (unit, P2)** — catalog↔modal parity, the core anti-regression for lesson F:
   - `shortcuts_by_category(DEFAULT_SHORTCUTS)` groups every shortcut; assert no shortcut is dropped (`sum(len(v)) == len(DEFAULT_SHORTCUTS)`).
   - Render `shortcuts_help()` via the `env` fixture; assert one `data-shortcut-id="<id>"` row exists for **every** `Shortcut.id` and **no** orphan rows (count rows == count catalog).
   - `json.loads(shortcuts_json())` round-trips; every entry has `key`/`action`; `allowInInput` is `True` only for `escape` + `send`.
   - `Shortcut.event_key()` lowercases and falls back to last display token.
2. **`tests/test_strict_undefined.py` (P2)** — add a `shortcuts_help` case (it iterates the grouped mapping). Renders cleanly because we own the `Shortcut` objects, but the suite requires every dict/iterating component to have a case.
3. **`tests/test_css_syntax.py` + `tests/test_template_css_contract.py`** — auto-cover the new `.chirpui-shortcuts-help*` classes (contract test fails if a class in the template is missing from `chirpui.css`); `test_transition_tokens.py` enforces motion tokens.
4. **`tests/browser/test_shortcuts_gauntlet.py` (P1, gauntlet style — in `test-browser-chrome-check`)**, mirroring `test_command_palette.py`:
   - **Guard, the lesson-I assertion:** focus a `<textarea>`, press the `focus-composer` key (`/`, not allowlisted) → assert the `chirpui:shortcut:focus-composer` event did **not** fire (install a `window` listener that flips a flag; assert flag stays false) and the textarea value is unchanged char-by-char.
   - **Allowlist passes:** with the same textarea focused, press `Escape` (allowlisted) → assert the active dialog closes / `chirpui:shortcut:escape` fires.
   - **Help opens + parity:** press `?` outside an input → assert `#shortcuts-help` `dialog.open === true`; assert the set of `[data-shortcut-id]` rows equals the set of ids in the embedded `<script type=application/json>` catalog (modal can't lie).
   - **Cross-platform mod:** `Meta+k` and `Control+k` both dispatch `open-palette`.
5. **OLED browser smoke (P2)** — set `data-theme="oled"`, assert computed `--chirpui-bg` is darker than the dark value (compare luminance) and `color-scheme` is `dark`; cycle the toggle through 4 states back to `system`.
6. **Manifest freshness** — adding `shortcuts_help.html` shifts manifest linenos; run `poe build-manifest` and commit `manifest.json` (CI `poe build-manifest-check`). The doc-block header satisfies `test_description_coverage.py`.

### Sequencing (within the epic)

1. `shortcuts.py` + `__init__` export + `filters.py`/`conftest.py` globals + `tests/test_shortcuts.py` (no UI yet — catalog is the foundation).
2. `shortcuts_help.html` + the CSS partial + `poe build-css`/`build-manifest`.
3. `chirpuiShortcuts` factory in `chirpui-alpine.js` + `tests/browser/test_shortcuts_gauntlet.py` (the guard proof).
4. Safe-area CSS (`018`, `083`) + docs note — **correctness, ship before OLED**.
5. OLED (`068` block + toggle cycle + boot accepted-values) + OLED smoke — **last, taste**.

### Out of scope (follow-ups)

- Per-app shortcut customization / rebinding UI (catalog is static in v1).
- Wiring `chirpui:shortcut:send` / `focus-composer` into a concrete chat composer macro (the handler dispatches the events; app code listens). A showcase recipe demonstrates the wiring.
- `viewport-fit=cover` `<meta>` injection — left to the app author (documented, not auto-added, because it changes app-wide zoom/scroll behavior).

## Real composer — auto-grow, IME-safe send, send/stop cancellation, attachments, suggestions

**Phase:** 3 · **Priority:** P1 · **Lessons:** D (composer is a correctness gap, not a feature wishlist) + E (stop must abort the upstream task, not just close the listener).

### Problem statement (verified against source)

`src/chirp_ui/templates/chirpui/chat_input.html` is, in full, a `<form method="post">` wrapping one `<textarea>` plus an optional footer slot. It has **zero** `x-data`, **zero** `@keydown`, and **zero** attach/char-count markup — yet its doc-block (lines 1–13) claims *"Composer with optional attach button, character count."* The macro renders neither. Consequences:

- A user pressing **Enter** does nothing (textarea inserts a newline); there is no client submit path. The only way to send is a real `<button type="submit">` the *caller* must supply in the footer slot. This is a correctness bug for a "chat input".
- `src/chirp_ui/templates/css/partials/018_chat-input.css` line 28 sets `resize: none` on `.chirpui-chat-input__field`, so the textarea is fixed-height and cannot grow.
- `src/chirp_ui/templates/islands/upload_state.js` **fakes** upload progress with `window.setInterval(..., 120)` incrementing 15% per tick (lines 41–53) — it never talks to a server.
- There is no `file_item` macro anywhere (`grep "def file_item"` → empty); no attachment chip; no `disabled_reason` convention; no suggestion-chips macro. `tooltip()` exists (`chirpui/tooltip.html`, signature `tooltip(content=none, hint=none, position="top", block=false, cls="")`).
- The SSE swap idiom already in the codebase (`streaming.html`) is `sse-swap="fragment" hx-target="this" hx-swap="beforeend"` on a `hx-ext="sse" sse-connect=…` ancestor — attachment status will reuse this same pattern.
- Icons render through the `| icon` filter (`icon_btn.html`: `{{ icon | icon }}`). Buttons: `btn(label, variant=…, icon=…, hx=…, …)` and `icon_btn(icon, variant=…, aria_label=…, hx=…)`.

This epic turns `chat_input` into a real composer. We **keep the `chat_input` name as a thin back-compat alias** (callers exist) and add a richer `composer()` macro in the same file; the new behavior is opt-in via params so existing renders stay byte-stable unless they pass the new flags.

---

### Deliverable 1 — Auto-grow textarea (EXACT CSS edit, both halves required)

Two edits to `src/chirp_ui/templates/css/partials/018_chat-input.css`. **Both are required**: removing `resize: none` alone leaves a fixed-height box with a manual drag handle (worse UX); adding `field-sizing` alone is overridden in older engines and `resize: none` would still pin the height where `field-sizing` is unsupported. Together: auto-grow where supported, natural resize fallback elsewhere, no manual handle.

**Edit A — remove the resize pin (line ~28).** Current block:

```css
.chirpui-chat-input__field {
    flex: 1;
    padding: var(--chirpui-spacing-sm) var(--chirpui-spacing);
    border: 1px solid var(--chirpui-border);
    border-radius: var(--chirpui-radius-sm);
    font: inherit;
    background: var(--chirpui-surface);
    color: var(--chirpui-text);
    resize: none;                                   /* ← DELETE this line */
    transition: border-color var(--chirpui-transition);
}
```

After (replace `resize: none;` with a vertical-only fallback so the box stays well-behaved on no-`field-sizing` engines):

```css
.chirpui-chat-input__field {
    flex: 1;
    padding: var(--chirpui-spacing-sm) var(--chirpui-spacing);
    border: 1px solid var(--chirpui-border);
    border-radius: var(--chirpui-radius-sm);
    font: inherit;
    background: var(--chirpui-surface);
    color: var(--chirpui-text);
    resize: vertical;          /* fallback handle only where field-sizing is absent */
    transition: border-color var(--chirpui-transition);
}
```

**Edit B — add the auto-grow `@supports` block**, mirroring the *existing* proven pattern in `src/chirp_ui/templates/css/partials/070_form-fields.css` lines 123–128:

```css
/* existing pattern in 070_form-fields.css — copy its shape exactly */
@supports (field-sizing: content) {
    textarea.chirpui-field__input {
        field-sizing: content;
        min-height: 3lh;
    }
}
```

Append to `018_chat-input.css` (after the `.chirpui-chat-input__field:disabled` rules, before the `__footer` rule or at end of file):

```css
/* Auto-grow: the composer textarea sizes to its content (Chromium 123+).
   Mirrors textarea.chirpui-field__input in 070_form-fields.css. Where
   field-sizing is unsupported, `resize: vertical` (above) is the fallback. */
@supports (field-sizing: content) {
    .chirpui-chat-input__field {
        field-sizing: content;
        resize: none;          /* auto-grow makes the manual handle redundant */
        min-height: 3lh;
        max-height: 40vh;      /* cap growth; overflow scrolls */
        overflow-y: auto;
    }
}
```

`018_chat-input.css` is a flat (legacy) partial. Per the **opportunistic envelope conversion** rule in `CLAUDE.md`, since this PR touches it, also wrap it in the standard envelope in the same PR:

```css
@layer chirpui.component {
  @scope (.chirpui-chat-input) to (.chirpui-chat-input .chirpui-chat-input) {
    /* …existing rules, using :scope for self-reference… */
  }
}
```

After CSS edits: `uv run poe build-css` then commit the regenerated `src/chirp_ui/templates/chirpui.css` (the build is concat-from-partials; `poe build-css-check` gates CI on staleness).

---

### Deliverable 2 — `chirpuiComposer` Alpine factory + IME-safe send (rewritten macro)

**2a. Factory** — add to `src/chirp_ui/templates/chirpui-alpine.js` via the existing `register("name", factory)` call (place it beside `register("chirpuiGridSelection", …)` near the end of the IIFE; do **not** add a `<script>` tag anywhere). It follows the file's conventions: `this.$root` (not `$el`) for the component root, `this.$refs` for children, listeners registered in `init()` and removed in `destroy()`.

```js
register("chirpuiComposer", function () {
    return {
        value: "",
        generating: false,   // SSE in flight → button shows "Stop"
        uploadPending: false, // any attachment still uploading/processing
        files: 0,            // count of ready+pending attachments
        _composing: false,
        _compositionEndedAt: 0,
        sendKey: "enter",    // "enter" | "mod-enter"
        init: function () {
            this.sendKey = this.$root.dataset.sendKey || "enter";
            this.value = this.$refs.field ? this.$refs.field.value : "";
            // Attachment chips report their status by dispatching
            // chirpui:attachment-changed on the composer root after each
            // OOB swap (see Deliverable 4). Recompute pending/count from
            // the DOM so the send/stop button stays honest across swaps.
            var self = this;
            this._onAttach = function () { self.syncAttachments(); };
            this.$root.addEventListener("chirpui:attachment-changed", this._onAttach);
            this.syncAttachments();
            // SSE "done" closes generation: the streaming bubble dispatches a
            // chirpui:generation-done event (Chirp wires this on sse-close).
            this._onDone = function () { self.generating = false; };
            this.$root.addEventListener("chirpui:generation-done", this._onDone);
        },
        destroy: function () {
            this.$root.removeEventListener("chirpui:attachment-changed", this._onAttach);
            this.$root.removeEventListener("chirpui:generation-done", this._onDone);
        },
        syncAttachments: function () {
            var chips = this.$root.querySelectorAll(".chirpui-attachment-chip");
            var pending = this.$root.querySelectorAll(
                '.chirpui-attachment-chip[data-status="uploading"],' +
                '.chirpui-attachment-chip[data-status="processing"]'
            );
            this.files = chips.length;
            this.uploadPending = pending.length > 0;
        },
        get canSend() {
            return !this.uploadPending && (this.value.trim() !== "" || this.files > 0);
        },
        onCompositionStart: function () { this._composing = true; },
        onCompositionEnd: function () {
            this._composing = false;
            this._compositionEndedAt = Date.now();
        },
        // IME-safe Enter handling. Four guards, in order:
        //  1. Shift+Enter is always a newline.
        //  2. send_key="mod-enter" requires Cmd/Ctrl.
        //  3. e.isComposing — spec signal that this Enter commits a CJK
        //     candidate (do NOT send).
        //  4. keyCode 229 + a <500ms-old compositionend — Safari/Firefox
        //     flip isComposing false on the commit keydown, so the spec
        //     guard misses; the time window + legacy 229 keyCode close it.
        onEnter: function (e) {
            if (e.shiftKey) return;
            if (this.sendKey === "mod-enter" && !(e.metaKey || e.ctrlKey)) return;
            if (e.isComposing || e.keyCode === 229) return;
            if (Date.now() - this._compositionEndedAt < 500) return;
            if (!this.canSend) return;
            e.preventDefault();
            this.send();
        },
        send: function () {
            var form = this.$refs.field.closest("form");
            if (form) { form.requestSubmit(); }  // honors hx-post + validation
        },
        stop: function () {
            // The Stop button itself carries hx-post to the abort endpoint
            // (Deliverable 3). This handler only flips local state; the
            // server abort is the load-bearing half.
            this.generating = false;
        },
        // htmx:beforeRequest on the send button sets generating=true so the
        // button morphs to Stop while the SSE stream runs.
        onSend: function () { this.generating = true; },
    };
});
```

**2b. Rewritten macro** — `src/chirp_ui/templates/chirpui/chat_input.html`. Keep `chat_input(...)` as a back-compat alias that forwards to a new `composer(...)`. New params: `send_key`, `stop_action`, `attach`, `name`, `maxlength`, plus htmx pass-through (`hx`, `hx_post`, `hx_target`, `hx_swap`). The macro uses `build_hx_attrs(...) | html_attrs` per convention and emits `hx-boost="false"` on any interactive control that has an `hx_target` (boost-aware components rule).

```jinja
{#- chirp-ui: Chat Input / Composer
    A working chat composer: auto-grow textarea, IME-safe Enter-to-send
    (send_key 'enter' | 'mod-enter'), a send/stop toggle bound to live
    upload + generation state, an optional attach control, and slots for
    attachment chips and suggestion chips.

    Server contract: form `hx-post`s the message; `stop_action` MUST be an
    endpoint that ABORTS the upstream generation task (not merely close the
    SSE listener). See docs/patterns/ai-chat.md.

    Usage:
        {% from "chirpui/chat_input.html" import composer %}
        {% call composer(action="/send", name="message", send_key="enter",
                         stop_action="/abort", hx_target="#thread",
                         hx_swap="beforeend") %}
            {% slot attachments %}{% end %}
            {% slot suggestions %}{% end %}
        {% end %}
-#}

{% def composer(action="", name="message", placeholder="Type a message...",
                rows=2, maxlength=none, send_key="enter", stop_action="",
                attach=false, send_label="Send", stop_label="Stop",
                hx=none, hx_post=none, hx_target=none, hx_swap=none, cls="") %}
{% set _send_key = send_key | validate_variant(("enter", "mod-enter"), "enter") %}
{% set _post = hx_post or action %}
{% set _form_hx = build_hx_attrs(hx=hx, hx_post=_post, hx_target=hx_target,
                                 hx_swap=(hx_swap or "beforeend")) %}
<form class="chirpui-chat-input chirpui-composer{{ " " ~ cls if cls else "" }}"
      x-data="chirpuiComposer()"
      data-send-key="{{ _send_key }}"
      @composition-start.window="onCompositionStart()"
      action="{{ action }}" method="post"
      {{ _form_hx | html_attrs }}
      @htmx:before-request="onSend()">
    <div class="chirpui-composer__attachments" x-show="files > 0" x-cloak>
        {% slot attachments %}
    </div>
    <div class="chirpui-chat-input__composer">
        {% if attach %}
        <input type="file" multiple class="chirpui-composer__file" x-ref="file"
               name="{{ name }}_files" aria-label="Attach files"
               @change="syncAttachments()">
        {% end %}
        <textarea class="chirpui-chat-input__field chirpui-composer__field"
            name="{{ name }}" rows="{{ rows }}"
            x-ref="field" x-model="value"
            placeholder="{{ placeholder }}"
            {% if maxlength %}maxlength="{{ maxlength }}"{% end %}
            @compositionstart="onCompositionStart()"
            @compositionend="onCompositionEnd()"
            @keydown.enter="onEnter($event)"
            aria-label="{{ placeholder }}"></textarea>
    </div>
    <div class="chirpui-composer__suggestions">{% slot suggestions %}</div>
    <footer class="chirpui-chat-input__footer">
        {% slot %}
        {{ composer_send_stop(send_label=send_label, stop_label=stop_label,
                              stop_action=stop_action,
                              hx_target=hx_target) }}
    </footer>
</form>
{% end %}

{#- Back-compat: the old bare-form signature forwards to composer(). Renders
    identically when no new params are passed EXCEPT it is now interactive. -#}
{% def chat_input(action="", name="message", placeholder="Type a message...",
                  rows=2, maxlength=none, cls="") %}
{% call composer(action=action, name=name, placeholder=placeholder,
                 rows=rows, maxlength=maxlength, cls=cls) %}
    {% if caller is defined %}{% slot %}{% end %}
{% end %}
{% end %}
```

Note on `@keydown.enter`: Alpine's `.enter` modifier matches `event.key === "Enter"`. We pass `$event` to `onEnter` so the factory can inspect `isComposing`/`keyCode`/modifiers; we do **not** use `.prevent` on the binding because we only `preventDefault()` when we actually send (Shift+Enter and IME commits must keep their default newline/commit behavior).

---

### Deliverable 3 — Send/Stop toggle + the LOAD-BEARING server cancellation contract

**3a. The toggle macro** — ONE button that swaps icon/label/hx-attrs on the Alpine `generating` flag. `:disabled` is bound to `(value empty && no files) || uploadPending` via the factory's `canSend` getter. New macro in the same file:

```jinja
{% def composer_send_stop(send_label="Send", stop_label="Stop", stop_action="",
                          send_disabled_reason="Type a message or attach a file",
                          hx_target=none) %}
{# Send variant: real submit; disabled-says-why via tooltip when !canSend. #}
<span class="chirpui-tooltip chirpui-tooltip--top" data-chirpui-tooltip
      x-show="!generating"
      :data-tooltip="canSend ? '' : '{{ send_disabled_reason | e }}'">
    <button type="submit"
            class="chirpui-btn chirpui-btn--primary chirpui-composer__send"
            :disabled="!canSend"
            :aria-disabled="!canSend"
            aria-label="{{ send_label }}">
        <span class="chirpui-btn__icon" aria-hidden="true">{{ "send" | icon }}</span>
        <span class="chirpui-btn__label">{{ send_label }}</span>
    </button>
</span>
{# Stop variant: NOT a submit — POSTs the abort endpoint. -#}
<button type="button"
        class="chirpui-btn chirpui-btn--danger chirpui-composer__stop"
        x-show="generating" x-cloak
        @click="stop()"
        {{ build_hx_attrs(hx_post=stop_action, hx_target=hx_target,
                          hx_swap="none") | html_attrs }}
        hx-boost="false" hx-select="unset" hx-disinherit="hx-select"
        aria-label="{{ stop_label }}">
    <span class="chirpui-btn__icon" aria-hidden="true">{{ "stop" | icon }}</span>
    <span class="chirpui-btn__label">{{ stop_label }}</span>
</button>
{% end %}
```

`x-show` keeps both buttons in the DOM and toggles visibility — simpler and swap-safe than morphing one element's attributes (htmx won't fight an `x-bind` on a swapped node). The Stop button carries `hx-select="unset"`/`hx-disinherit` so a boost-inherited select can't strip its response, and `hx-boost="false"` per the boost-aware rule.

**3b. The cancellation contract (the actual deliverable, documented in `docs/patterns/ai-chat.md`).** This is the Lesson-E point: a Stop button that only closes the htmx SSE listener client-side is a **lie** — the upstream model keeps generating, burning tokens/GPU, and a reconnect resumes a stream the user "stopped" (this is exactly open-webui #1166 and #20018). The contract chirp-ui documents and the macro is shaped around:

```
Stop MUST do TWO things, server-authoritative:
  1. Client: stop() flips `generating=false` and the htmx-driven SSE
     element is removed/closed (visual stop).
  2. Server: the Stop button hx-POSTs `stop_action` (e.g. POST /chat/{id}/abort)
     which MUST cancel the in-flight generation task — e.g. cancel the
     asyncio Task / set an abort Event the generator checks each token /
     call the provider SDK's cancel — BEFORE the response returns.

If only (1) happens, the model keeps producing tokens and a page reload or
SSE reconnect resumes the "stopped" answer. chirp-ui ships the UI; the app
owns the abort endpoint. The macro REQUIRES `stop_action` to be non-empty
when generation is possible, and the docs state the endpoint contract.
```

Document a reference Chirp handler sketch (Chirp-agnostic prose + one snippet) so adopters can't miss it:

```python
# Reference only — app-owned. The point is the task is actually cancelled.
@app.post("/chat/{chat_id}/abort")
async def abort(chat_id: str):
    task = GENERATIONS.pop(chat_id, None)
    if task is not None:
        task.cancel()          # the generator coroutine raises CancelledError
    return Response(status_code=204)   # hx-swap="none"; UI already toggled
```

`done`/SSE-close flips `generating` back to false: the streaming bubble (`streaming.html`, `sse_close="done"`) dispatches `chirpui:generation-done` which the factory's `_onDone` listener catches.

---

### Deliverable 4 — `file_item.html`: attachment chips with REAL OOB-driven status

**4a. New macro file** `src/chirp_ui/templates/chirpui/file_item.html` (doc-block first per the add-a-component rule). Provides `attachment_chip()` (the chip) and `file_item()` (alias / list-row form). Each chip is **id-addressable** (`id="attachment-{id}"`) so the server can OOB-swap its status; status (`uploading`|`processing`|`ready`|`error`) drives a doc-icon→spinner swap and is exposed as `data-status` (consumed by `chirpuiComposer.syncAttachments`). Dismiss is a group-hover icon button; a preview opens an Alpine modal.

```jinja
{#- chirp-ui: File item / attachment chip
    Id-addressable attachment chip for the composer. Status (uploading /
    processing / ready / error) is server-authoritative and delivered by
    OOB swaps targeting #attachment-{id} (NO fake client timers — see
    docs/patterns/ai-chat.md). Doc-icon morphs to a spinner while pending.
-#}

{% def attachment_chip(id, name, status="uploading", size=none, href=none,
                       preview_url=none, dismiss_url=none, cls="") %}
{% set _status = status | validate_variant(
    ("uploading", "processing", "ready", "error"), "uploading") %}
{% set _pending = _status in ("uploading", "processing") %}
<span class="chirpui-attachment-chip chirpui-attachment-chip--{{ _status }}{{ " " ~ cls if cls else "" }}"
      id="attachment-{{ id }}"
      data-status="{{ _status }}"
      x-init="$root.dispatchEvent(new CustomEvent('chirpui:attachment-changed', {bubbles:true}))"
      {% if _status == "error" %}role="alert"{% end %}>
    <span class="chirpui-attachment-chip__icon" aria-hidden="true">
        {% if _pending %}<span class="chirpui-spinner chirpui-spinner--sm"></span>
        {% elif _status == "error" %}{{ "alert" | icon }}
        {% else %}{{ "file" | icon }}{% end %}
    </span>
    {% if preview_url %}
    <button type="button" class="chirpui-attachment-chip__name"
            x-data="chirpuiDialogTarget()" data-target="attachment-preview-{{ id }}"
            @click="open()">{{ name }}</button>
    {% else %}
    <span class="chirpui-attachment-chip__name">{{ name }}</span>
    {% end %}
    {% if size %}<span class="chirpui-attachment-chip__size">{{ size }}</span>{% end %}
    {% if dismiss_url %}
    <button type="button" class="chirpui-attachment-chip__dismiss"
            aria-label="Remove {{ name }}"
            {{ build_hx_attrs(hx_post=dismiss_url, hx_target="#attachment-" ~ id,
                              hx_swap="outerHTML") | html_attrs }}
            hx-boost="false">{{ "x" | icon }}</button>
    {% end %}
</span>
{% end %}

{# file_item: list-row presentation of the same data (e.g. activity rail). #}
{% def file_item(id, name, status="ready", size=none, href=none, cls="") %}
{{ attachment_chip(id=id, name=name, status=status, size=size, href=href,
                   cls="chirpui-attachment-chip--row " ~ cls) }}
{% end %}
```

The status fragment the server OOB-swaps is just `attachment_chip(..., status="ready")` re-rendered inside `oob_fragment` (`oob.html`) targeting `#attachment-{id}` — same `outerHTML` swap the dismiss button uses. The `x-init` dispatch on every render is what keeps `chirpuiComposer.uploadPending`/`files` honest after each swap (mirrors how `chirpuiGridSelection` reseeds on `htmx:afterSettle`).

**4b. Replace the fake timer.** `src/chirp_ui/templates/islands/upload_state.js` currently fakes progress (lines 41–53: `setInterval` bumping `percent += 15`). Rewrite `mount()` to do a real upload and let **server OOB swaps** drive each chip's status — the island no longer owns the `percent` lie:

```js
// upload_state.js — real upload; status comes from the server, not a timer.
const run = async () => {
  const files = input?.files ? Array.from(input.files) : [];
  if (!files.length) {
    setAction(payload, api, "upload", "error", { reason: "no_files" });
    return;
  }
  start?.setAttribute("disabled", "disabled");
  for (const file of files) {
    const body = new FormData();
    body.append("file", file);
    // The endpoint returns an OOB fragment that swaps #attachment-{id}
    // to its server-authoritative status (uploading→processing→ready/error).
    // htmx (or fetch+htmx.swap) applies it; no client-side percent fiction.
    const res = await fetch(endpoint, { method: "POST", body });
    const html = await res.text();
    window.htmx?.swap("body", html, { swapStyle: "none" }); // OOB-only payload
  }
  start?.removeAttribute("disabled");
};
```

(If true byte-progress is wanted, use `XMLHttpRequest.upload.onprogress` to drive a real `<progress>` — but the *status lifecycle* must remain server-authoritative.) Update `tests` and `docs/patterns/ai-chat.md` to state the island no longer fabricates progress.

**4c. CSS** — new partial `src/chirp_ui/templates/css/partials/174_attachment-chip.css` (next free number after `173_nav-pill.css`), authored in the envelope form. Chip layout, the doc-icon→spinner state via `[data-status]`, `--dragover` not here, group-hover dismiss reveal:

```css
@layer chirpui.component {
  @scope (.chirpui-attachment-chip) {
    :scope {
      display: inline-flex; align-items: center; gap: var(--chirpui-spacing-2xs);
      max-width: 100%; min-width: 0;
      padding: var(--chirpui-spacing-2xs) var(--chirpui-spacing-xs);
      border: 1px solid var(--chirpui-border);
      border-radius: var(--chirpui-radius-pill);
      background: var(--chirpui-surface);
    }
    .chirpui-attachment-chip__name {
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }
    .chirpui-attachment-chip__dismiss { opacity: 0; transition: opacity var(--chirpui-transition); }
    :scope:hover .chirpui-attachment-chip__dismiss,
    :scope:focus-within .chirpui-attachment-chip__dismiss { opacity: 1; }
    &.chirpui-attachment-chip--error { border-color: var(--chirpui-alert-error-border); }
  }
}
```

---

### Deliverable 5 — `@paste`/`@dragover`/`@drop` (P2, sequence AFTER chips)

Add paste/drop to the `chirpuiComposer` factory and bind on the composer `<form>`. Large paste → a `.txt` attachment (so a 5k-line paste doesn't blow out the textarea / the prompt); drop adds files; a `.chirpui-composer--dragover` class toggles a drop overlay.

```js
// add to chirpuiComposer:
LARGE_PASTE_CHARS: 2000,
onPaste: function (e) {
    var text = (e.clipboardData || window.clipboardData).getData("text");
    if (text && text.length > this.LARGE_PASTE_CHARS) {
        e.preventDefault();
        var file = new File([text], "pasted.txt", { type: "text/plain" });
        this.addFiles([file]);   // pushes onto the <input type=file> + triggers upload
    }
},
onDragOver: function (e) { e.preventDefault(); this.dragover = true; },
onDragLeave: function () { this.dragover = false; },
onDrop: function (e) {
    e.preventDefault(); this.dragover = false;
    this.addFiles(Array.from(e.dataTransfer.files));
},
addFiles: function (files) {
    var dt = new DataTransfer();
    var input = this.$refs.file;
    if (input && input.files) {
        Array.prototype.forEach.call(input.files, function (f) { dt.items.add(f); });
    }
    files.forEach(function (f) { dt.items.add(f); });
    if (input) { input.files = dt.files; input.dispatchEvent(new Event("change")); }
},
```

Macro bindings on the `<form>`: `@paste="onPaste($event)" @dragover="onDragOver($event)" @dragleave="onDragLeave()" @drop="onDrop($event)" :class="{'chirpui-composer--dragover': dragover}"`. Add a drop overlay element gated by `x-show="dragover"` + the `.chirpui-composer--dragover` overlay CSS in `018_chat-input.css`.

---

### Deliverable 6 — "Disabled-says-why" convention (P2, cross-cutting)

Establish: any disabled interactive control may accept a `disabled_reason` param; when disabled, it wraps in `tooltip()` (`chirpui/tooltip.html`) so the reason is discoverable. Already applied to send/stop in Deliverable 3 (the `:data-tooltip` binding). Document the convention in `docs/COMPONENT-OPTIONS.md` and `CLAUDE.md § Key conventions`, and roll it into the highest-traffic disabled controls (`btn`, `icon_btn`) as a follow-up param (out of scope to retrofit all here — the convention + the composer application is the deliverable). The tooltip text must be on a non-disabled wrapper because disabled elements don't fire pointer events for hover tooltips — hence the `<span class="chirpui-tooltip">` wrapper around the disabled `<button>` in Deliverable 3.

---

### Deliverable 7 — `follow_ups.html`: `suggestion_chips()` (P1, sequence BEFORE paste/drop)

New macro file `src/chirp_ui/templates/chirpui/follow_ups.html` providing `suggestion_chips()` built over `chip_group`/`chip` (`chirpui/chip_group.html`). `mode='prefill'` writes the suggestion into the composer textarea (focus, don't send); `mode='send'` submits immediately. Usable in the `chat_layout` empty-state slot AND as a post-stream OOB swap (the server appends follow-ups after the stream completes by OOB-swapping a `#follow-ups` target).

```jinja
{#- chirp-ui: Follow-up / suggestion chips
    Suggestion chips for chat empty-states and post-stream follow-ups.
    mode='prefill' fills the composer (focus, no send); mode='send' submits.
    Dedupe by stable key so an OOB refresh never double-renders a suggestion.
-#}

{% from "chirpui/chip_group.html" import chip_group %}

{% def suggestion_chips(suggestions, mode="prefill", target=".chirpui-composer",
                        label="Suggestions", id="follow-ups", cls="") %}
{% set _mode = mode | validate_variant(("prefill", "send"), "prefill") %}
{# Dedupe on a stable key: explicit item.key, else the prompt text. Strict
   undefined is on (kida 0.7.0) — guard with .get() and default(). #}
{% set _seen = [] %}
<div class="chirpui-follow-ups{{ " " ~ cls if cls else "" }}" id="{{ id }}">
  {% call chip_group(label=label) %}
    {% for item in suggestions %}
      {% set _key = item.get("key") or item.get("prompt") or "" %}
      {% if _key and _key not in _seen %}
        {% set _ = _seen.append(_key) %}
        <button type="button"
                class="chirpui-chip chirpui-chip--suggestion"
                data-prompt="{{ item.get('prompt') | default('') | e }}"
                @click="
                  $dispatch('chirpui:suggestion', {prompt: $el.dataset.prompt, mode: '{{ _mode }}'});
                  const c = document.querySelector('{{ target }}');
                  if (c && c.__x) { /* prefill via composer factory below */ }
                ">
          {{ item.get("label") or item.get("prompt") | default("") }}
        </button>
      {% end %}
    {% end %}
  {% end %}
</div>
{% end %}
```

Wire into the composer: the `chirpuiComposer` factory listens for `chirpui:suggestion` on `window` and either prefills (`this.value = detail.prompt; this.$refs.field.focus()`) or prefills+sends (`this.value = detail.prompt; this.send()`). Add to the factory `init()`:

```js
this._onSuggestion = function (e) {
    var d = e.detail || {};
    self.value = d.prompt || "";
    if (self.$refs.field) { self.$refs.field.value = self.value; self.$refs.field.focus(); }
    if (d.mode === "send" && self.canSend) { self.send(); }
};
window.addEventListener("chirpui:suggestion", this._onSuggestion);
```
(remove in `destroy()`).

**Dedupe + stable-key** (documented): each suggestion is a dict `{"label": str, "prompt": str, "key": str?}`. The dedupe key is `item.key` if present else `item.prompt`; rendering skips any repeated key. This makes a post-stream OOB refresh of `#follow-ups` idempotent — re-sending the same suggestion set never double-renders, and the stable key lets the server diff/replace cleanly. Guarded with `.get()` + `| default("")` because strict-undefined is on (kida 0.7.0).

`chat_layout` empty-state usage: place `{{ suggestion_chips(starter_prompts, mode="prefill") }}` inside the `messages` slot when the thread is empty; post-stream, the server OOB-swaps `#follow-ups`.

---

### Sequencing

1. **D1 (auto-grow CSS)** — smallest, independently shippable, no JS. Land first.
2. **D2 (factory + IME-safe send)** — the core correctness fix. Depends on D1 only cosmetically.
3. **D3 (send/stop + cancellation contract)** — depends on D2's `generating`/`canSend`. Ships with the `docs/patterns/ai-chat.md` contract; the doc is a blocking part of the deliverable, not optional.
4. **D7 (suggestion chips)** — depends on D2 (consumes `chirpuiComposer`). **Sequence BEFORE D5.**
5. **D4 (attachment chips + real upload)** — depends on D2 (`syncAttachments`/`uploadPending`). Replaces the `upload_state.js` fake timer.
6. **D5 (paste/drop)** — depends on D4 (`addFiles` pushes onto the file input). **After chips.**
7. **D6 (disabled-says-why)** — convention doc + send/stop application lands with D3; broader retrofit is a follow-up.

---

### Test approach

- **Render tests** (`tests/test_components.py`): `composer(...)` renders `x-data="chirpuiComposer()"`, the textarea has `@keydown.enter`, `@compositionstart`, `@compositionend`; `data-send-key` reflects `send_key`; `composer_send_stop` renders both a `type="submit"` send and a `type="button"` stop with `hx-post` to `stop_action`; `chat_input(...)` back-compat alias still renders a `<form>`. Use `assert_element` (Sprint 18 helper) for structure, not class-only string checks.
- **Strict-undefined regression** (`tests/test_strict_undefined.py`): add a case rendering `suggestion_chips([{}])` and `attachment_chip` with minimal dict items — must not raise under `strict_undefined=True`. This is required by the dict-iterating-component rule in `CLAUDE.md`.
- **CSS contract** (`test_template_css_contract.py`): every new class (`chirpui-composer`, `chirpui-composer__field`, `chirpui-composer__send`, `chirpui-composer__stop`, `chirpui-attachment-chip`, `chirpui-attachment-chip__*`, `chirpui-follow-ups`, `chirpui-chip--suggestion`, `chirpui-composer--dragover`) must exist in `chirpui.css` (regenerate via `poe build-css`).
- **Motion tokens** (`test_transition_tokens.py`): the new chip/dragover transitions must use `--chirpui-transition`/`--chirpui-duration-*`/`--chirpui-easing-*`, not raw values.
- **CSS build freshness**: `poe build-css-check` after every partial edit; commit regenerated `chirpui.css`.
- **Manifest freshness**: template line shifts drift `manifest.json` line numbers — run `poe build-manifest` and commit (per `feedback_workspace_git_gotchas`).
- **Description coverage** (`test_description_coverage.py`): `file_item.html` and `follow_ups.html` must start with a `{#- chirp-ui: … -#}` doc-block.
- **JS unit / lint**: `chirpuiComposer`, the rewritten `upload_state.js`, and the new factory must pass the JS gate in `poe ci`.
- **Browser gauntlet** (`tests/browser/`, in `test-browser-chrome-check`): a `test_composer_gauntlet.py` proving (a) Enter sends, Shift+Enter newlines, mod-enter mode requires Cmd/Ctrl; (b) an IME compositionend within 500ms of Enter does NOT send (CJK regression); (c) the textarea auto-grows; (d) send→stop morph on `generating`; (e) a disabled send exposes its `disabled_reason` tooltip; (f) an attachment chip's status updates via OOB swap (not a timer) and toggles `uploadPending`; (g) a suggestion chip prefills the composer; (h) re-OOB-ing the same follow-up set does not duplicate chips (dedupe).
- **Public-surface maturity**: ship `composer`/`attachment_chip`/`suggestion_chips` as `experimental` initially; promoting to `stable` requires the promote-to-stable collateral (manifest test + showcase proof) per the stable-composition-wrapper rule.

### Showcase

Add a composer recipe to `examples/component-showcase` (deployed to Railway): a working chat page using `chat_layout` + `composer` with a real (stubbed) abort endpoint demonstrating the cancellation contract, attachment chips with server-driven status, and post-stream follow-up chips. This is the proof artifact referenced by the maturity promotion.

## Explicitly NOT worth copying
These open-webui capabilities were evaluated in the 2026-06-18 audit and deliberately left out — either out of scope for a server-rendered macro library, already solved by our stack, or a maintenance liability with poor payoff.

| Capability (open-webui) | Why we are NOT copying it |
|---|---|
| Pyodide in-browser Python | In-browser interpreter is an app concern, not a UI macro; massive payload, no fit for a server-rendered library. |
| Client-side virtualization (custom list windowing) | We swap server fragments via htmx + `load_sentinel`; windowing belongs to the app's data layer, not the component layer. |
| TTS / voice (speech in/out) | Device/permissions/provider concern; no server-rendered surface to own; out of scope. |
| jsPDF / client PDF export | Heavy client lib for a niche export; server-side export is the app's job. |
| svelte-i18n runtime i18n | Framework-coupled; our strings are author-controlled in templates; no runtime i18n engine to import. |
| PWA manifest / service worker | Deployment/app concern, not a component-library responsibility. |
| Socket.IO + global client store | We standardize on htmx SSE + per-component Alpine factories; a global socket store fights our single-authority-Alpine and server-state model. |
| Caret-anchored trigger menus (popover at text cursor) | Caret-position popovers are fragile and high-maintenance; slash-commands route through projected forms (see backlog) instead of caret menus. |

## Lower-priority / needs design
Backlog beyond the five epics — valuable but either cheap follow-ons once the keystones land, or still needing design before they earn an epic.

- **Branch / sibling navigation** (regenerate-and-switch between alternate turn versions) — needs a data-model design for turn lineage before UI.
- **Slash-command form recipe** — essentially *free* once schema-driven config projection lands; document it as a recipe rather than a new mechanism.
- **Structured feedback flow** (thumbs + reason capture + tagging) — needs the per-turn actions surface from the message-turn epic first.
- **`model_picker` composite + multi-model compare** — composite over existing primitives; defer until the turn surface stabilizes the per-turn meta slot.
- **Code-block chrome** (language label + copy + collapse) — extends `rendered_content()`/`.chirpui-prose`; taste-floor, sequence after composer.
- **Code-exec OUTPUT layout** (stdout/stderr/result panes) — needs a layout spec; pairs with code-block chrome.
- **Artifacts sandboxed iframe + CSP doctrine** — security design (sandbox attrs + CSP) must precede any iframe-hosting macro.
- **High-contrast axis** — additive theming axis; sequence after the a11y/theming polish epic.
- **Real RTL** (logical-property sweep + bidi-safe affordances) — broad CSS audit; needs its own scoping pass.
