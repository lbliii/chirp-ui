---
title: Avatars and media
description: avatar, avatar_stack, media_object, video_card, carousel
draft: false
weight: 23
lang: en
type: doc
keywords: [chirp-ui, avatar, media]
icon: user-circle
---

# Avatars and media

Components for user avatars, overlapping stacks, media object layouts, video thumbnails, carousels, and brand logos.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `avatar.html` | `avatar` | Circular image or initials with status ring |
| `avatar_stack.html` | `avatar_stack` | Overlapping avatar group with "+N" overflow |
| `media_object.html` | `media_object` | Classic media + body + actions layout |
| `video_thumbnail.html` | `video_thumbnail` | Image with play overlay, duration, progress |
| `carousel.html` | `carousel`, `carousel_slide` | CSS scroll-snap carousel |
| `logo.html` | `logo` | Brand mark with text, image, or both |

## avatar

Circular avatar with image, initials fallback, size variants, and optional status ring.

```text
{% from "chirpui/avatar.html" import avatar %}

{{ avatar(src="/img/user.jpg", alt="Alice") }}
{{ avatar(src="/img/user.jpg", alt="Alice", size="lg", status="online") }}
{{ avatar(initials="AB", alt="Alice Brown") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `src` | `str` | `none` | Image URL |
| `initials` | `str` | `none` | Fallback initials (used when `src` is empty) |
| `alt` | `str` | `""` | Accessible label |
| `size` | `str` | `"md"` | `"sm"`, `"md"`, `"lg"` |
| `status` | `str` | `none` | Status ring color (e.g. `"online"`, `"busy"`) |
| `cls` | `str` | `""` | Extra CSS classes |

When neither `src` nor `initials` is provided, a `"?"` placeholder renders.

## avatar_stack

Overlapping avatar group. Renders slot content (individual avatars) with optional "+N" overflow indicator.

```text
{% from "chirpui/avatar_stack.html" import avatar_stack %}
{% from "chirpui/avatar.html" import avatar %}

{% call avatar_stack(max_visible=3, total=5) %}
  {{ avatar(src="/a.jpg", alt="Alice", size="sm") }}
  {{ avatar(src="/b.jpg", alt="Bob", size="sm") }}
  {{ avatar(src="/c.jpg", alt="Carol", size="sm") }}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `max_visible` | `int` | `4` | Number of visible avatars |
| `total` | `int` | `none` | Total count (shows "+N" when `total > max_visible`) |
| `cls` | `str` | `""` | Extra CSS classes |

## media_object

Classic media + body + actions row. Supports named slots (Kida 0.3+, `use_slots=true`) or legacy sub-macros.

```text
{% from "chirpui/media_object.html" import media_object %}

{% call media_object(align="start", use_slots=true) %}
  {% slot media %}<img src="/thumb.jpg" alt="Preview">{% end %}
  <h3>Title</h3>
  <p>Description text.</p>
  {% slot actions %}<button>Action</button>{% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `align` | `str` | `"start"` | Vertical alignment (`"start"`, `"center"`, etc.) |
| `cls` | `str` | `""` | Extra CSS classes |
| `use_slots` | `bool` | `false` | Use named slots vs legacy sub-macros |

**Named slots:** `media`, default (body), `actions`.

**Legacy sub-macros:** `media_object_media`, `media_object_body`, `media_object_actions` -- each accepts `cls` and a default slot.

## video_thumbnail

Image with play button overlay, duration badge, and optional progress bar for watched percentage.

```text
{% from "chirpui/video_thumbnail.html" import video_thumbnail %}

{{ video_thumbnail(href="/watch/1", src="/thumb.jpg", alt="Video title", duration="4:32") }}
{{ video_thumbnail(src="/thumb.jpg", duration="4:32", watched_pct=75) }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | `str` | `none` | Link URL (renders as `<a>`; `<figure>` otherwise) |
| `src` | `str` | `""` | Thumbnail image URL |
| `alt` | `str` | `""` | Image alt text |
| `duration` | `str` | `none` | Duration badge text (e.g. `"4:32"`) |
| `watched_pct` | `int` | `none` | Progress bar width percentage (0-100) |
| `cls` | `str` | `""` | Extra CSS classes |

## carousel / carousel_slide

Horizontal scroll-snap carousel. CSS-only with native touch swipe. Optional dot navigation.

```text
{% from "chirpui/carousel.html" import carousel, carousel_slide %}

{% call carousel(variant="compact", slide_count=3, show_dots=true) %}
  {% call carousel_slide(1) %}
    <div class="chirpui-card">Slide 1</div>
  {% end %}
  {% call carousel_slide(2) %}
    <div class="chirpui-card">Slide 2</div>
  {% end %}
  {% call carousel_slide(3) %}
    <div class="chirpui-card">Slide 3</div>
  {% end %}
{% end %}
```

### carousel params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | `str` | `"compact"` | `"compact"` (card strip) or `"page"` (hero, one per viewport) |
| `slide_count` | `int` | `0` | Total slides (for dot navigation) |
| `show_dots` | `bool` | `false` | Show dot navigation below |
| `cls` | `str` | `""` | Extra CSS classes |

### carousel_slide params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `int/str` | required | Slide identifier (used for anchor links) |
| `cls` | `str` | `""` | Extra CSS classes |

## logo

Reusable brand mark with text, image, or both. Supports link wrapping, size, and alignment variants.

```text
{% from "chirpui/logo.html" import logo %}

{{ logo(text="ChirpUI", variant="text") }}
{{ logo(image_src="/static/logo.svg", image_alt="ChirpUI", variant="image") }}
{{ logo(text="ChirpUI", image_src="/static/logo.svg", href="/", variant="both", size="lg") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | `str` | `""` | Brand text |
| `image_src` | `str` | `""` | Logo image URL |
| `image_alt` | `str` | `""` | Image alt text |
| `href` | `str` | `none` | Link URL (renders as `<a>`) |
| `variant` | `str` | `"both"` | `"text"`, `"image"`, `"both"` |
| `size` | `str` | `"md"` | `"sm"`, `"md"`, `"lg"` |
| `align` | `str` | `"center"` | `"start"`, `"center"`, `"end"` |
| `cls` | `str` | `""` | Extra CSS classes |

When `variant="image"` with no `image_alt`, the `text` value is used as a visually hidden accessible fallback.

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-avatar` | Avatar wrapper |
| `chirpui-avatar--sm/md/lg` | Size variants |
| `chirpui-avatar--online/busy` | Status ring |
| `chirpui-avatar__img` | Avatar image |
| `chirpui-avatar__initials` | Initials fallback |
| `chirpui-avatar-stack` | Stack wrapper |
| `chirpui-avatar-stack__more` | "+N" overflow |
| `chirpui-media-object` | Media object wrapper |
| `chirpui-media-object--align-start/center` | Alignment |
| `chirpui-video-thumbnail` | Video thumbnail wrapper |
| `chirpui-video-thumbnail__play` | Play button overlay |
| `chirpui-video-thumbnail__duration` | Duration badge |
| `chirpui-video-thumbnail__progress` | Watch progress bar |
| `chirpui-carousel` | Carousel wrapper |
| `chirpui-carousel--compact/page` | Carousel variant |
| `chirpui-carousel__track` | Scroll track |
| `chirpui-carousel__slide` | Individual slide |
| `chirpui-carousel__dots` | Dot navigation |
| `chirpui-logo` | Logo wrapper |
| `chirpui-logo--text/image/both` | Display variant |
| `chirpui-logo--sm/md/lg` | Size variant |

## Related

- [Cards](./cards.md)
