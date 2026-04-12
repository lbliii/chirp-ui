# Provide / Consume Context Keys

Context keys used by chirp-ui's `{% provide %}` / `consume()` system for
parent-to-child state flow across slot boundaries (requires kida >= 0.3.4).

## Rules

1. **Underscore prefix** — all keys start with `_` to signal internal chirp-ui
   context, not user data.
2. **Explicit params always win** — `consume()` is a fallback only. The canonical
   consumer pattern is:
   ```jinja2
   {% set _variant = (variant if variant else consume("_surface_variant", "")) | validate_variant(...) %}
   ```
3. **Safe defaults** — every `consume()` call includes a fallback so components
   render correctly standalone (no parent context required).
4. **Namespaced** — keys use `_<scope>_<property>` to avoid collision between
   unrelated providers (e.g. `_bar_surface` vs `_surface_variant`).

## Key Registry

| Key | Type | Default | Provider(s) | Consumer(s) | Since |
|-----|------|---------|-------------|-------------|-------|
| `_hero_variant` | `str` | `""` | `hero_effects()` | `particle_bg`, `meteor`, `spotlight_card`, `symbol_rain`, `holy_light`, `rune_field`, `constellation` | 0.2.6 |
| `_table_align` | `list[str] \| None` | `None` | `table()` | `row()` | 0.2.6 |
| `_bar_surface` | `str` | `"default"` | `command_bar()`, `filter_bar()` | *(future bar children)* | 0.2.6 |
| `_bar_density` | `str` | `"sm"` | `command_bar()`, `filter_bar()` | `btn`, `icon_btn` | 0.2.6 |
| `_surface_variant` | `str` | `""` | `surface()`, `section()` (via surface), `panel()` (via surface) | `badge`, `divider`, `alert`, `timeline`, `callout`, `status_indicator`, `settings_row_list` | 0.3.0 |
| `_card_variant` | `str` | `""` | `card()` | `badge`, `divider`, `alert`, `settings_row_list` | 0.3.0 |
| `_accordion_name` | `str` | `"accordion"` | `accordion()` | `accordion_item()` | 0.3.0 |
| `_form_density` | `str` | `""` | `form()` | `field_wrapper()` | 0.3.0 |
| `_nav_current_path` | `str` | `""` | `sidebar()`, `navbar()` | `sidebar_link`, `navbar_link`, `navbar_dropdown` | 0.3.0 |
| `_streaming_role` | `str` | `"assistant"` | `streaming_bubble(role=...)` | `copy_btn`, `model_card` | 0.3.0 |
| `_sse_state` | `str` | `""` | *(manual provide)* | `sse_retry` | 0.3.0 |
| `_suspense_busy` | `str` | `"true"` | `suspense_group()` | `suspense_slot` | 0.3.0 |

## Consumer Pattern

```jinja2
{# Standard: check explicit param first, fall back to consume, then validate #}
{% set _variant = (variant if variant else consume("_surface_variant", "")) | validate_variant(...) %}

{# Name coordination: explicit param wins, otherwise consume from parent #}
{% set _name = name if name != "accordion" else consume("_accordion_name", "accordion") %}

{# Path context: consume from parent, fall back to global template variable #}
{% set _cp = consume("_nav_current_path", "") or (current_path | default("")) %}

{# Streaming role: inherit from streaming_bubble parent #}
{% set _role = consume("_streaming_role", "assistant") %}

{# SSE state: manual provide — auto-disable retry when connected #}
{% set _parent_state = consume("_sse_state", "") %}
{% if _parent_state == "connected" %} disabled aria-disabled="true"{% end %}

{# Suspense busy: detect whether inside an active group #}
{% set _busy = consume("_suspense_busy", "false") %}

{# Surface-aware theming: add --on-<surface> CSS modifier for visual adaptation #}
{% set _surface = consume("_surface_variant", "") %}
{% set _on_surface = " chirpui-timeline--on-" ~ _surface if _surface and _surface != "default" else "" %}
```

## Testing Pattern

Every provide/consume pair requires three test cases:

1. **Standalone** — component renders with sensible defaults, no `{% provide %}`:
   ```python
   def test_child_standalone(self, env):
       html = env.from_string('{% from "chirpui/X.html" import X %}{{ X() }}').render()
       # assert sensible default behavior
   ```

2. **Consumes from parent** — `{% provide %}` wrapper flows value to child:
   ```python
   def test_child_consumes_from_parent(self, env):
       html = env.from_string(
           '{% from "chirpui/X.html" import X %}'
           '{% provide _key = "value" %}{{ X() }}{% end %}'
       ).render()
       # assert child reflects provided value
   ```

3. **Explicit overrides provide** — explicit param beats consumed value:
   ```python
   def test_explicit_overrides_provide(self, env):
       html = env.from_string(
           '{% from "chirpui/X.html" import X %}'
           '{% provide _key = "value" %}{{ X(param="other") }}{% end %}'
       ).render()
       # assert child uses "other", not "value"
   ```
