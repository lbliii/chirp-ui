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
    widget: Widget | None = None
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
        return Widget.RANGE if (f.min is not None and f.max is not None) else Widget.NUMBER
    return Widget.TEXT


def _coerce_field(raw: Field | Mapping[str, Any]) -> Field:
    """Accept a :class:`Field` or a plain dict (caller convenience).

    Mirrors :func:`grid_state._coerce_column`. ``widget`` in a dict may be a
    :class:`Widget`, its string value, or ``None``.
    """
    if isinstance(raw, Field):
        return raw
    widget = raw.get("widget")
    if isinstance(widget, str):
        widget = Widget(widget)
    choices = tuple((str(v), str(label)) for v, label in raw.get("choices", ()))
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
    schema: Sequence[Field | Mapping[str, Any]],
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
