# Drag-Drop Primitives and Fragment Islands

ChirpUI provides HTMX-safe mutation regions and behavior-ready drag-drop primitives for row lists and kanban boards.

---

## Fragment Island (HTMX-safe mutation region)

**Problem**: App shells with `hx-boost` or broad `hx-select` (e.g. `#page-content`) can cause local mutations (add/delete/reorder) to fail: inherited selectors may yield empty selection or swap into the wrong region.

**Solution**: Wrap mutation regions with `fragment_island()` to isolate them from inherited HTMX attributes.

```html
{% from "chirpui/fragment_island.html" import fragment_island %}
{% from "chirpui/sortable_list.html" import sortable_list, sortable_item %}

{% call fragment_island("step-list") %}
{% call sortable_list(attrs='x-data="{ dragging: null }"') %}
  {% for step in steps %}
  {% call sortable_item(attrs='draggable="true" @dragstart="..." @drop="..."') %}
    ...item content...
  {% end %}
  {% end %}
{% end %}
{% end %}
```

### Parameters

| Param | Description |
|-------|-------------|
| `id` | **Required.** Stable root id for the swap target. Must match `hx-target="#id"` on mutating forms/buttons. |
| `hx_target` | Optional. Override default target (default: none; children inherit from parent). |
| `hx_swap` | Optional. Override swap strategy (e.g. `outerHTML`). |
| `hx_select` | Optional. Override response selector. |
| `cls` | Extra CSS classes. |
| `attrs` | Raw HTML attributes. |

The island applies `hx-disinherit="hx-select hx-target hx-swap"` so child mutations are not affected by shell attributes.

### Anti-footgun: Inherited HTMX attributes

When using `app_shell` or any layout with `hx-boost` or broad `hx-select`:

- **Always** use `fragment_island()` for regions that receive HTMX swaps (add/delete/reorder).
- **Or** add `hx-disinherit="hx-select"` (or equivalent) on the target element.
- Mutating forms/buttons must have explicit `hx-target`, `hx-swap`, and `hx-select` when they differ from the island.

---

## DnD Row Primitive (ordered lists)

For chains, todo lists, setup targets: use `dnd_list`, `dnd_item`, `dnd_handle`, `dnd_drop_indicator`.

```html
{% from "chirpui/dnd.html" import dnd_list, dnd_item, dnd_handle, dnd_drop_indicator %}

{% call dnd_list(attrs='x-data="{ dragging: null }"') %}
{% for item in items %}
{% call dnd_item(attrs='draggable="true"
    @dragstart="dragging = ' ~ loop.index0 ~ '"
    @dragover.prevent
    @dragenter="$el.classList.add(`chirpui-dnd__item--over`)"
    @dragleave="$el.classList.remove(`chirpui-dnd__item--over`)"
    @drop.prevent="...reorder logic..."') %}
  {{ dnd_handle() }}
  {{ dnd_drop_indicator() }}
  <div class="chirpui-dnd__content">{{ item.name }}</div>
{% end %}
{% end %}
{% end %}
```

### Parameters

| Macro | Params | Description |
|-------|--------|-------------|
| `dnd_list` | `cls`, `attrs` | Container. Use `attrs` for `x-data` and other Alpine/HTMX. |
| `dnd_item` | `cls`, `attrs` | Draggable row. Add `draggable="true"` and `@dragstart`, `@drop` etc. |
| `dnd_handle` | `cls`, `attrs` | Grip affordance (&#x2630;). |
| `dnd_drop_indicator` | `cls`, `attrs` | Visual drop indicator (optional). |

CSS classes for state: `chirpui-dnd__item--dragging`, `chirpui-dnd__item--over`.

---

## DnD Board Primitive (kanban)

For kanban columns with cross-column movement:

```html
{% from "chirpui/dnd.html" import dnd_board, dnd_column, dnd_card %}

{% call dnd_board() %}
{% for col in columns %}
{% call dnd_column(title=col.name, attrs='...drop zone attrs...') %}
  {% for card in col.cards %}
  {% call dnd_card(attrs='draggable="true" ...') %}
    {{ card.title }}
  {% end %}
  {% end %}
{% end %}
{% end %}
{% end %}
```

### Parameters

| Macro | Params | Description |
|-------|--------|-------------|
| `dnd_board` | `cls`, `attrs` | Horizontal scroll container. |
| `dnd_column` | `title`, `cls`, `attrs` | Column with header and body. Add `chirpui-dnd__column-body--over` for drop target. |
| `dnd_card` | `cls`, `attrs` | Draggable card. Use `chirpui-dnd__card--dragging` when dragging. |

---

## Tactile polish tokens

Override in your CSS:

```css
:root {
  --chirpui-dnd-lift-scale: 1.02;
  --chirpui-dnd-lift-offset-y: -4px;
  --chirpui-dnd-drag-opacity: 0.5;
  --chirpui-dnd-drop-indicator-color: var(--chirpui-accent);
  --chirpui-dnd-transition: 150ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

`prefers-reduced-motion: reduce` disables lift and transitions.

---

## Chirp debug guardrails

With Chirp debug mode (`app.debug=True`), the HTMX overlay warns when:

- **Empty hx-select**: Response has no element matching the selector.
- **Broad inherited target**: Mutating request inherits `#main` or `#page-content` without explicit `hx-target`.
- **Load-trigger targets #main**: `hx-trigger="load"` with inherited `hx-target="#main"` — the request will replace the page on load. Use `fragment_island` (which applies `hx-disinherit`) or explicit `hx-target="this"`.

Static contract checks suggest `fragment_island()` when mutation targets lack `hx-disinherit`.
