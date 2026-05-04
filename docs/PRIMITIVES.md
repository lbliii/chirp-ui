# Primitive Vocabulary

ChirpUI primitives are named composition concepts, not one-off CSS utilities. Reach for these first when shaping a page. They keep layout decisions visible to Python, the registry, generated docs, and coding agents.

Use legacy helpers only for narrow compatibility cases such as truncation or local overflow. If a template starts to read like a list of CSS properties, reshape it around a primitive.

---

## Blessed Primitives

| Primitive | Use For | Prefer Over |
|-----------|---------|-------------|
| `stack()` | Vertical rhythm between siblings | margin helper chains |
| `cluster()` | Wrapping inline rows of chips, buttons, badges | ad hoc flex rows |
| `grid()` | Repeating cards/tiles that wrap | hand-written grid classes |
| `frame()` | Fixed page regions: hero, main/sidebar, two-column layouts | forcing `grid()` into page structure |
| `block()` | Items inside `grid()` that need spans | custom grid-column classes |
| `flow` | Simple flow rhythm wrapper | margin helper chains |
| `layer()` | Overlapping card/media decks | absolute-position piles |
| `container()` | Page/content width bounds | copied max-width wrappers |
| `actions` | Button/action rows when no macro owns the region | scattered button wrappers |
| `prose` | Long-form rendered content | per-element typography helpers |

`actions`, `flow`, and `prose` are CSS primitives today. The rest are Kida macros in `chirpui/layout.html`.

For product-site pages, use these primitives through the recipes in
[PRODUCT-PAGE-PATTERNS.md](PRODUCT-PAGE-PATTERNS.md). Those recipes show how
to compose hero, proof, lifecycle, customer story, and CTA sections without
adding utility classes or speculative component APIs.

For streaming, video, catalog, live-event, and media-plan page recipes, see
[MEDIA-SITE-PATTERNS.md](MEDIA-SITE-PATTERNS.md). Those recipes show how to
compose media pages from existing registry-cited primitives before adding any
new media-specific component surface.

For forum, Q&A, threaded discussion, moderation, and community page recipes, see
[FORUM-SITE-PATTERNS.md](FORUM-SITE-PATTERNS.md). Those recipes show how to
compose forum-shaped pages from existing registry-cited primitives before adding
any new forum-specific component surface.

The registry projects this boundary into the manifest as `authoring` metadata:
these blessed primitives are `preferred`, legacy helpers are `compatibility`,
and other public surfaces remain `available`.

To inspect that boundary from an installed package:

```bash
python -m chirp_ui find --authoring=preferred
python -m chirp_ui find --authoring=compatibility
```

Python tooling can use the same discovery layer:

```python
from chirp_ui.find import compatibility_components, preferred_components

preferred = preferred_components()
legacy_typography = compatibility_components(category="typography")
```

---

## Layout Examples

Import the layout macros once near the top of a template:

```kida
{% from "chirpui/layout.html" import container, stack, cluster, grid, frame, block, layer %}
```

### `stack()`

Default vertical rhythm:

```kida
{% call stack() %}
  {{ page_header("Deployments") }}
  {{ alert("Last deploy succeeded", variant="success") }}
  {{ table(rows) }}
{% end %}
```

Non-default gap:

```kida
{% call stack(gap="lg") %}
  {{ page_header("Settings") }}
  {% call section("Profile") %}...{% end %}
  {% call section("Security") %}...{% end %}
{% end %}
```

### `cluster()`

Default wrapping row:

```kida
{% call cluster() %}
  {{ badge("Active", variant="success") }}
  {{ badge("Owner") }}
  {{ badge("Production") }}
{% end %}
```

Compact chip row:

```kida
{% call cluster(gap="sm") %}
  {% for tag in tags %}
    {{ badge(tag, variant="muted") }}
  {% endfor %}
{% end %}
```

### `grid()`

Default responsive grid:

```kida
{% call grid() %}
  {% for project in projects %}
    {{ card(project.name, href=project.href) }}
  {% endfor %}
{% end %}
```

Fixed-track preset:

```kida
{% call grid(preset="bento-211", gap="lg", items="start") %}
  {% call block(span=2) %}{{ metric_grid(metrics) }}{% end %}
  {{ status_panel(system_status) }}
  {{ activity_panel(events) }}
{% end %}
```

### `frame()`

Balanced two-column region:

```kida
{% call frame() %}
  {% call surface() %}Primary details{% end %}
  {% call surface(variant="muted") %}Secondary notes{% end %}
{% end %}
```

Hero/media region:

```kida
{% call frame(variant="hero", gap="lg") %}
  {% call stack(gap="sm") %}
    <h1>Release console</h1>
    <p>Ship, monitor, and roll back from one screen.</p>
  {% end %}
  {{ video_thumbnail(src="/preview.png", alt="Release console") }}
{% end %}
```

Left navigation shell:

```kida
{% call frame(variant="sidebar-start", gap="md") %}
  {% call sidebar(current_path="/work") %}…{% end %}
  {% call stack(gap="md") %}…workspace content…{% end %}
{% end %}
```

### `block()`

Default grid cell:

```kida
{% call grid(cols=3) %}
  {% for stat in stats %}
    {% call block() %}{{ metric_card(stat.value, stat.label) }}{% end %}
  {% endfor %}
{% end %}
```

Spanning cell:

```kida
{% call grid(cols=3) %}
  {% call block(span=2) %}{{ chart_panel(chart) }}{% end %}
  {% call block() %}{{ summary_panel(summary) }}{% end %}
{% end %}
```

### `flow`

Default flow wrapper:

```kida
<div class="chirpui-flow">
  <p>First paragraph.</p>
  <p>Second paragraph.</p>
</div>
```

Larger flow rhythm:

```kida
<div class="chirpui-flow chirpui-flow--lg">
  {{ page_header("Guide") }}
  <p>Longer explanatory content.</p>
</div>
```

### `layer()`

Default overlap deck:

```kida
{% call layer() %}
  {{ card("Plan") }}
  {{ card("Build") }}
  {{ card("Ship") }}
{% end %}
```

Centered, calmer deck:

```kida
{% call layer(direction="center", overlap="sm", angle="none", hover=false) %}
  {{ card("Draft") }}
  {{ card("Review") }}
  {{ card("Done") }}
{% end %}
```

### `container()`

Default content width:

```kida
{% call container() %}
  {{ page_header("Projects") }}
  {{ project_grid(projects) }}
{% end %}
```

Narrow content width:

```kida
{% call container(max_width="48rem") %}
  <article class="chirpui-prose">
    {{ sanitized_body_html | safe }}
  </article>
{% end %}
```

### `actions`

Default action row:

```kida
<div class="chirpui-actions">
  {{ btn("Cancel") }}
  {{ btn("Save", variant="primary") }}
</div>
```

Separated action row:

```kida
<div class="chirpui-actions chirpui-actions--between">
  {{ btn("Delete", variant="danger") }}
  {{ btn("Save", variant="primary") }}
</div>
```

When the action row belongs to a component region, prefer that component's slot first:

```kida
{% call section("Imports") %}
  {% slot actions %}{{ btn("Run import", variant="primary") }}{% end %}
  ...
{% end %}
```

### `prose`

Default long-form text:

```kida
<article class="chirpui-prose">
  {{ sanitized_body_html | safe }}
</article>
```

Prose with layout rhythm:

```kida
{% call stack(gap="lg", cls="chirpui-prose") %}
  <h1>{{ title }}</h1>
  {{ sanitized_body_html | safe }}
{% end %}
```

---

## Legacy Helpers

Legacy helpers remain available for compatibility, but they are not the growth path for new vocabulary:

- Typography shortcuts: `font-sm`, `font-lg`, `ui-title`, `text-muted`, and siblings.
- Spacing shortcuts: `mt-sm`, `mt-md`, `mb-md`.
- Text bounding helpers: `truncate`, `clamp-2`, `clamp-3`.
- Containment helpers: `scroll-x`, `min-w-0`.
- Accessibility/reset helpers: `visually-hidden`, `focus-ring`, `list-reset`.

Use them when they solve a narrow edge that a primitive cannot own. Do not add new stable helpers in this style without a design review; prefer a macro, token, or existing primitive.

---

## Decision Lens

Ask these in order:

1. Is this vertical rhythm? Use `stack()` or `flow`.
2. Is this an inline row that can wrap? Use `cluster()`.
3. Is this a repeating collection? Use `grid()` and `block()`.
4. Is this a fixed page region? Use `frame()`.
5. Is this long-form text? Use `prose`.
6. Is this only a tiny containment/a11y edge? A legacy helper may be fine.

If the answer sounds like a CSS property, pause. ChirpUI probably wants a concept, not another helper class.
