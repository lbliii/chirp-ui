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

### Anti-footgun: Target must be co-located with form

When forms live inside content that loads via HTMX (e.g. `hx-get` + `hx-swap="innerHTML"`):

- The `hx-target` element **must be in the same DOM subtree** as the form.
- If the target is in a sibling (e.g. `filters_panel`) and the form is in content that gets replaced by HTMX, the target may not exist when the form fires.
- **Fix:** Put the target div inside the same fragment that contains the mutating forms.

### fragment_island_with_result: Co-located mutation target

Use `fragment_island_with_result()` when the island content includes forms that target a result div. The macro renders the result div at the top of the island, guaranteeing it is in the same DOM subtree as the forms.

```html
{% from "chirpui/fragment_island.html" import fragment_island_with_result %}

{% call fragment_island_with_result("collections-results", "update-result",
    attrs='hx-get="/collections/status" hx-trigger="load, every 5m" hx-target="this" hx-swap="innerHTML"') %}
  {% include "collections/_status_summary.html" %}
{% end %}
```

Forms inside the included content use `hx-target="#update-result"`; the target is always present because it is rendered inside the same island.

| Param | Description |
|-------|-------------|
| `id` | **Required.** Stable root id for the island. |
| `mutation_result_id` | **Required.** Id for the result div. Forms use `hx-target="#mutation_result_id"`. |
| `hx_target`, `hx_swap`, `hx_select`, `cls`, `attrs` | Same as `fragment_island()`. |

---

## Forms inside boosted layouts

When a `<form>` with `hx-post` lives inside `#main`, it inherits that element’s `hx-select`. Layouts differ:

- **`chirp/layouts/boost.html`:** `hx-select="#page-content"`.
- **`chirpui/app_shell_layout.html` / `app_shell`:** `hx-select="#page-root"` (page templates must include `<div id="page-root">…</div>`).

Two inheritance traps apply:

### Trap 1: `hx-select` empties the swap

The form inherits the shell’s `hx-select` from `#main`. When the server returns a fragment without a matching wrapper (`#page-content` or `#page-root`, depending on layout), htmx filters the response, finds nothing, and swaps in empty content.

**`hx-disinherit="hx-select"` on the form is NOT sufficient** — it only prevents the form's *children* from inheriting `hx-select`. The form itself still inherits it.

**Fix:** Add `hx-select="unset"` directly on the form to override the inherited value:

```html
<form hx-post="/chat/message"
      hx-target="#composer-wrap"
      hx-swap="innerHTML"
      hx-select="unset"
      hx-disinherit="hx-select">
```

### Trap 2: View transitions flash the page

With `globalViewTransitions=true`, every htmx swap calls `document.startViewTransition()`. Even though `.chirpui-fragment-island` sets `view-transition-name: none` on the island element, the parent `#page-content` (which has `view-transition-name: page-content`) still animates — causing a visible fade/slide on every form submission.

**Fix:** Add `transition:false` to `hx-swap`:

```html
<form hx-swap="innerHTML transition:false" ...>
```

### Complete pattern

```html
<form hx-post="/endpoint"
      hx-target="#my-island"
      hx-swap="innerHTML transition:false"
      hx-select="unset"
      hx-disinherit="hx-select">
  <div id="my-island" class="chirpui-fragment-island"
       hx-disinherit="hx-select hx-target hx-swap">
    {% block my_fragment %}
      ...inputs and controls...
    {% end %}
  </div>
</form>
```

The server returns `Fragment("template.html", "my_fragment", ...)` and the swap replaces the island's inner content without inheriting the shell's selector or triggering page transitions.

---

## Sortable List Reorder (sortable_list + HTMX)

For chains, todo lists, setup targets: use `sortable_list` and `sortable_item` with a **hidden form** for reliable HTMX submission. Alpine 3 removed `$parent`, so use `dataset.draggingIdx` on the list element to pass the source index to the drop handler.

**Key patterns:**
- Hidden form with `hx-post`, `hx-target`, `hx-select`, `hx-swap` — ensures correct form encoding and fragment extraction
- `dataset.draggingIdx` on the list — stores source index across Alpine scopes (no `$parent`)
- Per-item `overCount` — prevents drop-indicator flicker when hovering over child elements
- `@dragend` on the list — cleans up state when drag is cancelled (dropped outside)

```html
{% from "chirpui/sortable_list.html" import sortable_list, sortable_item %}

<div id="step-list">
<form id="reorder-form" method="post" action="/chains/{{ chain_id }}/reorder"
      hx-post="/chains/{{ chain_id }}/reorder" hx-target="#step-list" hx-select="#step-list" hx-swap="outerHTML"
      style="display:none">
  <input type="hidden" name="from_idx" value="">
  <input type="hidden" name="to_idx" value="">
</form>
{% call sortable_list(attrs='x-data
    @dragend="delete $el.dataset.draggingIdx; $el.querySelectorAll(\'.chirpui-sortable__item--dragging, .chirpui-sortable__item--over\').forEach(el => el.classList.remove(\'chirpui-sortable__item--dragging\', \'chirpui-sortable__item--over\'))"') %}
{% for step in steps %}
{% call sortable_item(attrs='x-data="{ overCount: 0 }" draggable="true"
    @dragstart="$el.closest(\'.chirpui-sortable\').dataset.draggingIdx = \'' ~ loop.index0 ~ '\'; $el.classList.add(\'chirpui-sortable__item--dragging\')"
    @dragover.prevent
    @dragenter="overCount++; if (overCount === 1) $el.classList.add(\'chirpui-sortable__item--over\')"
    @dragleave="overCount--; if (overCount === 0) $el.classList.remove(\'chirpui-sortable__item--over\')"
    @drop.prevent="overCount = 0; $el.classList.remove(\'chirpui-sortable__item--over\');
        const list = $el.closest(\'.chirpui-sortable\');
        const form = document.getElementById(\'reorder-form\');
        if (form) { form.elements[\'from_idx\'].value = list.dataset.draggingIdx; form.elements[\'to_idx\'].value = \'' ~ loop.index0 ~ '\'; htmx.trigger(form, \'submit\'); }"') %}
  <span class="chirpui-sortable__handle">&#x2630;</span>
  <div class="chirpui-sortable__content">{{ step.name }}</div>
{% end %}
{% end %}
{% end %}
</div>
```

**Backend:** Return `Fragment("chains/_step_list.html", "step_list", chain=updated, chain_id=name)` so the response contains `#step-list`. Use `hx-select="#step-list"` to extract it when the response is a full page.

### Anti-footgun: Alpine 3 and $parent

Alpine 3 removed `$parent`. Do not use `$parent.dragging` — it will throw. Use `$el.closest('.chirpui-sortable').dataset.draggingIdx` instead.

### Anti-footgun: htmx.ajax values vs form submission

`htmx.ajax(..., {values: {...}})` can fail to send form-encoded data correctly in some setups. Prefer a hidden form + `htmx.trigger(form, 'submit')` for reliable reorder requests.

---

## DnD Row Primitive (ordered lists)

For richer row styling (handle, drop indicator): use `dnd_list`, `dnd_item`, `dnd_handle`, `dnd_drop_indicator`. Apply the same Alpine patterns as above (dataset for source index, per-item overCount, form submission).

```html
{% from "chirpui/dnd.html" import dnd_list, dnd_item, dnd_handle, dnd_drop_indicator %}

{% call dnd_list(attrs='x-data') %}
{% for item in items %}
{% call dnd_item(attrs='x-data="{ overCount: 0 }" draggable="true"
    @dragstart="$el.closest(\'.chirpui-dnd\').dataset.draggingIdx = \'' ~ loop.index0 ~ '\'; $el.classList.add(\'chirpui-dnd__item--dragging\')"
    @dragover.prevent
    @dragenter="overCount++; if (overCount === 1) $el.classList.add(\'chirpui-dnd__item--over\')"
    @dragleave="overCount--; if (overCount === 0) $el.classList.remove(\'chirpui-dnd__item--over\')"
    @drop.prevent="...form submit..."') %}
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
