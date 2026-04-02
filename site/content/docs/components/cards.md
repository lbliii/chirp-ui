---
title: Cards
description: card, glow_card, spotlight_card, index_card, config_card
draft: false
weight: 12
lang: en
type: doc
keywords: [chirp-ui, card, surface]
icon: cards
---

# Cards

Surface chrome for grouped content. Cards range from the headless `card()` macro (headers, footers, collapsible, variants) through opinionated domain cards (`post_card`, `video_card`, `channel_card`) to decorative effect cards (`glow_card`, `spotlight_card`). The `surface()` macro provides a plain background container without card framing.

## Quick reference

| Macro | Template | Purpose |
|-------|----------|---------|
| `card` | `card.html` | General-purpose card with optional header, footer, collapsible |
| `card_header` | `card.html` | Standalone card header |
| `card_media` | `card.html` | Standalone media container |
| `card_link` | `card.html` | Whole-card link for navigation grids |
| `card_main_link` | `card.html` | Partially linked card (independent top/footer links) |
| `resource_card` | `card.html` | Opinionated list/index card for app resources |
| `glow_card` | `glow_card.html` | Mouse-following radial glow (Alpine.js) |
| `spotlight_card` | `spotlight_card.html` | Auto-rotating spotlight glow (pure CSS) |
| `config_card` | `config_card.html` | Key-value settings card |
| `index_card` | `index_card.html` | Link card for index/listing pages |
| `post_card` | `post_card.html` | Social post card with avatar, media, actions |
| `channel_card` | `channel_card.html` | Channel card with avatar and subscriber count |
| `video_card` | `video_card.html` | Video thumbnail card with duration badge |
| `surface` | `surface.html` | Generic background container |

---

## card

```text
{% from "chirpui/card.html" import card %}
```

### Signature

```text
card(title=none, subtitle=none, footer=none, collapsible=false, open=false,
     variant="", icon=none, border_variant="", header_variant="", cls="",
     hoverable=false, attrs="", attrs_map=none)
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | str/none | `none` | Header title text. Omit for a headerless card. |
| `subtitle` | str/none | `none` | Muted subtitle below the title |
| `footer` | str/none | `none` | Footer content (rendered as-is) |
| `collapsible` | bool | `false` | Renders as `<details>` with `<summary>` header |
| `open` | bool | `false` | Initial open state when collapsible |
| `variant` | str | `""` | CSS variant modifier (e.g. `"feature"`) |
| `icon` | str/none | `none` | Icon passed through the `icon` filter |
| `border_variant` | str | `""` | Set to `"gradient"` for gradient border |
| `header_variant` | str | `""` | Set to `"gradient"` for gradient header |
| `hoverable` | bool | `false` | Adds `chirpui-card--hoverable` class |
| `cls` | str | `""` | Extra CSS classes |
| `attrs` | str | `""` | Extra HTML attributes (string) |
| `attrs_map` | dict/none | `none` | Extra HTML attributes (dict, e.g. `{"id": "my-card"}`) |

### Named slots

- **`header_actions`** -- actions area to the right of the header title
- **`media`** -- media block between header and body
- **`body_actions`** -- actions area inside the body
- **default** -- body content

### Examples

Basic card:

```text
{% call card(title="Dashboard") %}
    <p>Card body content.</p>
{% end %}
```

Card with icon, header actions, and media:

```text
{% call card(title="Settings", icon="gear", subtitle="App configuration") %}
    {% slot header_actions %}<button>Edit</button>{% end %}
    {% slot media %}<img src="/hero.jpg" alt="Hero">{% end %}
    <p>Body content goes here.</p>
{% end %}
```

Collapsible card:

```text
{% call card(title="Advanced", collapsible=true, open=false) %}
    <p>Hidden by default, click to expand.</p>
{% end %}
```

Card with attrs_map for htmx targeting:

```text
{% call card(title="Usage", attrs_map={"id": "usage-widget"}) %}
    <p>Stable id for hx-target="#usage-widget".</p>
{% end %}
```

---

## card_header

Standalone header for manual card composition.

```text
card_header(title, subtitle=none, icon=none, cls="")
```

The default slot receives header action content.

```text
{% call card_header(title="My Section", icon="star") %}
    <button>Action</button>
{% end %}
```

---

## card_media

Standalone media container.

```text
card_media(cls="")
```

```text
{% call card_media() %}
    <img src="/photo.jpg" alt="Photo">
{% end %}
```

---

## card_link

Whole-card `<a>` link for navigation/index grids.

```text
card_link(href, title, cls="")
```

### Named slots

- **`header_badge`** -- top-left chip or badge
- **`header_subtitle`** -- subtitle beneath the title
- **`footer`** -- footer below the body (e.g. tags)
- **default** -- body content

```text
{% call card_link(href="/docs/api", title="API Reference") %}
    {% slot header_badge %}<span class="chirpui-badge">New</span>{% end %}
    <p>Explore the full API surface.</p>
    {% slot footer %}<span>Python</span>{% end %}
{% end %}
```

---

## card_main_link

Partially linked card where top meta and footer remain independently interactive.

```text
card_main_link(href, title, cls="")
```

### Named slots

- **`top_meta`** -- content above the main link
- **`header_badge`**, **`header_subtitle`** -- inside the linked area
- **`footer`** -- independent footer area
- **default** -- body content

```text
{% call card_main_link(href="/projects/alpha", title="Project Alpha") %}
    {% slot top_meta %}<a href="/org/acme">acme</a>{% end %}
    <p>A cross-platform build tool.</p>
    {% slot footer %}<a href="/tags/rust">rust</a>{% end %}
{% end %}
```

---

## resource_card

Opinionated card for app resource lists and index pages. Combines top meta, badges, description, and footer into a single macro.

```text
resource_card(href, title, description=none, top_meta=none, top_meta_href=none,
              top_meta_title=none, cls="", link_mode="all")
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | str | required | Link target |
| `title` | str | required | Card title |
| `description` | str/none | `none` | Body description text |
| `top_meta` | str/none | `none` | Small text above the header (e.g. org name) |
| `top_meta_href` | str/none | `none` | Makes top meta a link (only in `link_mode="main"`) |
| `top_meta_title` | str/none | `none` | Title attribute for top meta |
| `link_mode` | str | `"all"` | `"all"` wraps entire card in `<a>`; `"main"` keeps top/footer independent |

### Named slots

- **`badges`**, **`subtitle`**, **`footer`**, **default** (body extras)

```text
{{ resource_card(
    href="/projects/chirp",
    title="chirp",
    description="Web framework for Bengal.",
    top_meta="bengal-org",
    top_meta_href="/orgs/bengal",
    link_mode="main"
) }}
```

---

## glow_card

Mouse-following radial glow effect. Requires Alpine.js.

```text
{% from "chirpui/glow_card.html" import glow_card %}
```

```text
glow_card(variant="", cls="", attrs="", attrs_map=none)
```

**Variants:** `""` (default), `"accent"`, `"muted"`

```text
{% call glow_card(variant="accent") %}
    <h3>Feature Highlight</h3>
    <p>Hover to see the glow follow your cursor.</p>
{% end %}
```

---

## spotlight_card

Auto-rotating spotlight glow. Pure CSS, no JavaScript required.

```text
{% from "chirpui/spotlight_card.html" import spotlight_card %}
```

```text
spotlight_card(variant="", cls="", attrs="", attrs_map=none)
```

**Variants:** `""` (default), `"accent"`

```text
{% call spotlight_card(variant="accent") %}
    <h3>Highlighted</h3>
    <p>The spotlight rotates automatically.</p>
{% end %}
```

---

## config_card

Key-value card for settings and configuration display. Wraps `card()` and `description_list()`.

```text
{% from "chirpui/config_card.html" import config_card %}
```

```text
config_card(title, icon=none, items=none, cls="", attrs="", attrs_map=none)
```

Pass a list of item dicts to `items`. Each item has `term`, `detail`, and optional `type` (`"bool"`, `"url"`, `"number"`, `"unset"`).

```text
{{ config_card(title="Logs", icon="refresh", items=[
    {"term": "retention_days", "detail": "14", "type": "number"},
    {"term": "max_entries_per_day", "detail": "500", "type": "number"},
]) }}
```

```text
{{ config_card(title="ACP", icon="diamond", items=[
    {"term": "enabled", "detail": "Yes", "type": "bool"},
    {"term": "endpoint", "detail": "https://api.example.com", "type": "url"},
    {"term": "api_key", "detail": "(not set)", "type": "unset"},
]) }}
```

If `items` is omitted, the default slot is rendered instead.

---

## index_card

Link card for index and listing pages (API docs, module directories, command references).

```text
{% from "chirpui/index_card.html" import index_card %}
```

```text
index_card(href, title, description=none, badge=none, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | str | required | Link target |
| `title` | str | required | Card title |
| `description` | str/none | `none` | Short description below title |
| `badge` | str/none | `none` | Small badge label (e.g. `"function"`, `"class"`) |

```text
{{ index_card(href="/api/foo", title="foo", description="Does something.", badge="function") }}
{{ index_card(href="/docs/start", title="Getting Started", description="Quick start guide.") }}
```

---

## post_card

Social post card with avatar, author info, media, and action slots.

```text
{% from "chirpui/post_card.html" import post_card %}
```

```text
post_card(name=none, handle=none, time=none, href=none, cls="")
```

### Named slots

- **`avatar`** -- avatar element
- **`media`** -- media below body (images, embeds)
- **`actions`** -- action bar (likes, shares, etc.)
- **default** -- post body text

```text
{% call post_card(name="Alice", handle="@alice", time="2h ago") %}
    {% slot avatar %}{{ avatar(src="/alice.jpg", alt="Alice", size="md") }}{% end %}
    {% slot media %}<img src="/sunset.jpg" alt="Sunset">{% end %}
    {% slot actions %}{{ action_bar_item(icon="heart", label="Like", count=42) }}{% end %}
    <p>Check out this amazing sunset!</p>
{% end %}
```

Legacy macros `post_card_header`, `post_card_body`, `post_card_media`, and `post_card_actions` are still available for backward compatibility.

---

## channel_card

Channel card with avatar, subscriber count, and action slots.

```text
{% from "chirpui/channel_card.html" import channel_card %}
```

```text
channel_card(href, name, avatar_src=none, avatar_initials=none,
             subscribers=none, cls="", use_slots=false)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | str | required | Channel link |
| `name` | str | required | Channel name |
| `avatar_src` | str/none | `none` | Avatar image URL |
| `avatar_initials` | str/none | `none` | Fallback initials for avatar |
| `subscribers` | str/none | `none` | Subscriber count text (e.g. `"12.5K"`) |
| `use_slots` | bool | `false` | Enables `body` and `actions` named slots |

When `use_slots=false`, the default slot receives action content (e.g. a subscribe button). When `use_slots=true`, use named `body` and `actions` slots.

```text
{% call channel_card(href="/channel/dev", name="Dev Channel",
                     avatar_initials="DC", subscribers="12.5K") %}
    {{ btn("Subscribe", variant="primary") }}
{% end %}
```

---

## video_card

Video thumbnail card with duration badge, channel info, and view/date metadata.

```text
{% from "chirpui/video_card.html" import video_card %}
```

```text
video_card(href, thumbnail, duration, title, channel=none,
           channel_href=none, views=none, date=none, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | str | required | Video link |
| `thumbnail` | str | required | Thumbnail image URL |
| `duration` | str | required | Duration label (e.g. `"4:32"`) |
| `title` | str | required | Video title |
| `channel` | str/none | `none` | Channel name |
| `channel_href` | str/none | `none` | Channel link |
| `views` | str/none | `none` | View count text |
| `date` | str/none | `none` | Published date text |

Named slot **`actions`** receives overlay content on the thumbnail (e.g. a menu button).

```text
{% call video_card(href="/watch/1", thumbnail="/thumb.jpg", duration="4:32",
                   title="Building with Chirp", channel="Dev Channel",
                   channel_href="/channel/dev", views="1.2K", date="3 days ago") %}
    {% slot actions %}<button>...</button>{% end %}
{% end %}
```

---

## surface

Generic background container. Use when you need a styled region without card framing.

```text
{% from "chirpui/surface.html" import surface %}
```

```text
surface(variant="default", full_width=false, padding=true, cls="",
        style="", attrs="", attrs_map=none)
```

**Variants:** `default`, `muted`, `elevated`, `accent`, `gradient-subtle`, `gradient-accent`, `gradient-border`, `gradient-mesh`, `glass`, `frosted`, `smoke`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | str | `"default"` | Background variant |
| `full_width` | bool | `false` | Adds `chirpui-surface--full` for edge-to-edge |
| `padding` | bool | `true` | Set `false` for `chirpui-surface--no-padding` |
| `style` | str | `""` | Inline CSS (e.g. custom gradient overrides) |

```text
{% call surface(variant="muted") %}
    <p>Content on a muted background.</p>
{% end %}
```

```text
{% call surface(variant="elevated", full_width=true) %}
    <h2>Hero Section</h2>
    <p>Full-width elevated surface.</p>
{% end %}
```

---

## CSS classes

Root classes: `chirpui-card`, `chirpui-glow-card`, `chirpui-spotlight-card`, `chirpui-index-card`, `chirpui-config-card`, `chirpui-post-card`, `chirpui-channel-card`, `chirpui-video-card`, `chirpui-surface`, `chirpui-resource-card`.

## Related

- [Layout](./layout.md) -- `grid()` + `block()` for card grids
- [Theming](../theming/design-tokens.md) -- elevation and surface tokens
