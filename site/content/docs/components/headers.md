---
title: Headers
description: page_header, section_header, entity_header, document_header, profile_header
draft: false
weight: 21
lang: en
type: doc
keywords: [chirp-ui, header, entity]
icon: text-align-left
---

# Headers

Header components provide title, metadata, breadcrumb, and action regions for pages, sections, entities, documents, profiles, and search-first layouts.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `layout.html` | `page_header`, `section_header`, `section_header_inline` | Page and section titles with breadcrumbs and action slots |
| `entity_header.html` | `entity_header` | Compact title + meta for entity detail pages |
| `document_header.html` | `document_header` | Document-oriented header with path, status, provenance |
| `profile_header.html` | `profile_header` | Cover image, avatar, bio, stats, action |
| `search_header.html` | `search_header` | Page title + prominent search bar + controls |
| `label_overline.html` | `label_overline` | Small-caps section label for cards and dense panels |

## page_header

Full-width page title with optional subtitle, meta line, breadcrumbs, and an actions slot.

```text
{% from "chirpui/layout.html" import page_header %}

{% call page_header("Users", subtitle="Manage team members", breadcrumb_items=[{"label": "Home", "href": "/"}]) %}
  {% slot actions %}
    {{ btn("Add user", variant="primary") }}
  {% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Page heading (renders as `<h1>`) |
| `subtitle` | `str` | `none` | Secondary text below title |
| `meta` | `str` | `none` | Muted meta line (rendered with `| safe`) |
| `breadcrumb_items` | `list` | `none` | Items for the breadcrumbs component |
| `variant` | `str` | `"default"` | Validated against `page_header` registry |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** `actions` -- right-aligned action buttons.

## section_header

Section-level heading with optional icon, subtitle, and action slot.

```text
{% from "chirpui/layout.html" import section_header %}

{% call section_header("Recent activity", icon="clock", variant="inline") %}
  {% slot actions %}
    {{ btn("View all", variant="ghost") }}
  {% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Section heading (`<h2>`) |
| `subtitle` | `str` | `none` | Shown below title (hidden when `variant="inline"`) |
| `icon` | `str` | `none` | Icon passed through `| icon` filter |
| `variant` | `str` | `"default"` | `"default"` or `"inline"` |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** `actions` -- trailing controls.

`section_header_inline` is a deprecated alias for `section_header(variant="inline")`.

## entity_header

Compact header for entity detail views (dashboards, settings pages).

```text
{% from "chirpui/entity_header.html" import entity_header %}

{% call entity_header(title="Chain: My Workflow", meta="3 steps - Updated 2h ago", icon="link") %}
  {% slot actions %}
    {{ btn("Edit", href="/chains/1/edit") }}
  {% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Entity name (`<h1>`) |
| `meta` | `str` | `none` | Muted detail line |
| `icon` | `str` | `none` | Leading icon |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** `actions` -- trailing action buttons.

## document_header

Document-oriented header for editor/viewer surfaces. Wraps `page_header` and adds detail fields for path, provenance, status, and arbitrary meta items.

```text
{% from "chirpui/document_header.html" import document_header %}

{% call document_header("README.md", path="docs/README.md", status="Draft", eyebrow="Documentation") %}
  {% slot actions %}<button type="button">Save</button>{% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Document title |
| `subtitle` | `str` | `none` | Forwarded to `page_header` |
| `meta` | `str` | `none` | Forwarded to `page_header` |
| `breadcrumb_items` | `list` | `none` | Forwarded to `page_header` |
| `eyebrow` | `str` | `none` | Small label above the title |
| `path` | `str` | `none` | File path shown as `<code>` |
| `provenance` | `str` | `none` | Origin/source detail |
| `status` | `str` | `none` | Status label |
| `meta_items` | `list` | `none` | Additional detail spans |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** `actions` -- forwarded to inner `page_header`.

## profile_header

Profile header with cover image, avatar, name, bio, stats, and action areas. Supports both named slots (Kida 0.3+, `use_slots=true`) and legacy sub-macros.

```text
{% from "chirpui/profile_header.html" import profile_header %}
{% from "chirpui/avatar.html" import avatar %}

{% call profile_header(name="Alice", cover_url="/cover.jpg", use_slots=true) %}
  {% slot avatar %}{{ avatar(initials="AC", alt="Alice", size="lg") }}{% end %}
  {% slot bio %}<p>Developer and designer</p>{% end %}
  {% slot stats %}{{ stat(value="1.2K", label="Followers") }}{% end %}
  {% slot action %}{{ btn("Follow", variant="primary") }}{% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | `none` | Display name (`<h1>`) |
| `cover_url` | `str` | `none` | Background cover image URL |
| `href` | `str` | `none` | Link wrapping the name |
| `cls` | `str` | `""` | Extra CSS classes |
| `use_slots` | `bool` | `false` | Use named slots instead of legacy sub-macros |

**Named slots:** `avatar`, `bio`, `stats`, `action`.

**Legacy sub-macros:** `profile_header_avatar`, `profile_header_info(name, href)`, `profile_header_stats`, `profile_header_action`.

## search_header

Page header combined with a prominent search bar and controls strip. Composes `page_header`, `search_bar`, and `action_strip`.

```text
{% from "chirpui/search_header.html" import search_header %}

{% call search_header("Skills", form_action="/skills", query=q, search_placeholder="Search skills...") %}
  {{ select("category", options=categories) }}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Page title |
| `form_action` | `str` | required | Form submit URL |
| `query` | `str` | `""` | Current search value |
| `search_name` | `str` | `"q"` | Input field name |
| `subtitle` | `str` | `none` | Forwarded to `page_header` |
| `meta` | `str` | `none` | Forwarded to `page_header` |
| `breadcrumb_items` | `list` | `none` | Forwarded to `page_header` |
| `form_method` | `str` | `"get"` | HTTP method |
| `form_attrs` | `str` | `""` | Extra form attributes string |
| `form_attrs_map` | `dict` | `none` | Extra form attributes map |
| `search_placeholder` | `str` | `"Search..."` | Input placeholder |
| `button_label` | `str` | `"Search"` | Submit button text |
| `button_icon` | `str` | `"⌕"` | Submit button icon |
| `surface_variant` | `str` | `"muted"` | Action strip surface |
| `density` | `str` | `"md"` | Action strip density |
| `wrap` | `str` | `"wrap"` | Flex wrap behavior |
| `sticky` | `bool` | `false` | Sticky positioning |
| `cls` | `str` | `""` | Extra CSS classes |

The default slot receives extra controls beside the search bar.

## label_overline

Small-caps overline label for cards, dense panels, and section headings.

```text
{% from "chirpui/label_overline.html" import label_overline %}

{{ label_overline("Configuration", section=true, tag="h3") }}
{{ label_overline("Sub-label") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | `str` | required | Label text |
| `section` | `bool` | `false` | Adds `--section` modifier for extra spacing |
| `tag` | `str` | `"span"` | HTML element (`span`, `h3`, `h4`, etc.) |
| `cls` | `str` | `""` | Extra CSS classes |

**CSS classes:** `chirpui-label-overline`, `chirpui-label-overline--section`, plus utility classes `chirpui-font-xs` and `chirpui-text-muted`.

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-page-header` | Page header wrapper |
| `chirpui-page-header__top` | Top row (title + actions) |
| `chirpui-page-header__actions` | Actions container |
| `chirpui-page-header__meta` | Meta line |
| `chirpui-section-header` | Section header wrapper |
| `chirpui-section-header--inline` | Inline variant |
| `chirpui-entity-header` | Entity header wrapper |
| `chirpui-entity-header__title` | Entity title |
| `chirpui-entity-header__actions` | Entity actions |
| `chirpui-document-header` | Document header wrapper |
| `chirpui-document-header__eyebrow` | Eyebrow label |
| `chirpui-document-header__path` | File path code block |
| `chirpui-document-header__status` | Status badge |
| `chirpui-profile-header` | Profile header wrapper |
| `chirpui-profile-header__cover` | Cover image |
| `chirpui-search-header` | Search header wrapper |
| `chirpui-label-overline` | Overline label |

## Layout notes

Headers include flex rules so title columns shrink safely. Pair with [Layout overflow](../guides/layout-overflow.md) for long titles.

## Related

- [Navigation](./navigation.md)
- [Layout](./layout.md)
