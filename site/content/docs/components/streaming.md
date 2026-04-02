---
title: Streaming
description: streaming_block, model_card, and SSE-friendly chat UI
draft: false
weight: 28
lang: en
type: doc
keywords: [chirp-ui, streaming, sse]
icon: broadcast
---

# Streaming

Components for LLM chat UIs, SSE-driven content, copy buttons, model comparison cards, and infinite scroll. Designed to work with htmx SSE extensions and Chirp streaming responses.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `streaming.html` | `streaming_bubble`, `streaming_block`, `copy_btn`, `model_card` | Chat bubbles, streaming blocks, copy buttons, model cards |
| `infinite_scroll.html` | `infinite_scroll` | htmx-triggered infinite scroll container |

## streaming_bubble

Chat message bubble with SSE streaming support. Renders as an `<article>` with a role label and optional SSE connection.

```text
{% from "chirpui/streaming.html" import streaming_bubble %}

{% call streaming_bubble(role="assistant", streaming=true, sse_connect="/api/chat/stream", sse_close="done") %}
  Thinking...
{% end %}

{% call streaming_bubble(role="user", streaming=false) %}
  What is the meaning of life?
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `role` | `str` | `"assistant"` | Message role (validated against `message_bubble` registry) |
| `streaming` | `bool` | `true` | Show blinking cursor |
| `sse_swap_target` | `bool` | `false` | Enable `sse-swap="fragment"` on inner block |
| `sse_connect` | `str` | `none` | SSE endpoint URL (enables `hx-ext="sse"`) |
| `sse_close` | `str` | `"done"` | SSE event name that closes the connection |
| `cls` | `str` | `""` | Extra CSS classes |

When `sse_connect` is set, the bubble renders with `hx-ext="sse"`, `sse-connect`, `sse-close`, and `hx-disinherit="hx-target hx-swap"`. The inner streaming block receives `sse-swap="fragment"` for appending fragments.

## streaming_block

Generic streaming content area without the chat bubble wrapper. Useful for non-chat streaming UIs.

```text
{% from "chirpui/streaming.html" import streaming_block %}

{% call streaming_block(streaming=true) %}
  Loading results...
{% end %}

{% call streaming_block(sse_swap_target=true) %}
  {# Fragments appended here via SSE #}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `streaming` | `bool` | `false` | Show blinking cursor |
| `sse_swap_target` | `bool` | `false` | Enable `sse-swap="fragment"` and `hx-target="this"` |
| `cls` | `str` | `""` | Extra CSS classes |

## copy_btn

Copy-to-clipboard button using Alpine.js. Shows "Copied!" feedback for 1.5 seconds.

```text
{% from "chirpui/streaming.html" import copy_btn %}

{{ copy_btn(label="Copy", copy_text=answer_text) }}
{{ copy_btn(label="Copy code", copy_text=code_snippet, cls="chirpui-mt-sm") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `label` | `str` | `"Copy"` | Button label |
| `copy_text` | `str` | `""` | Text to copy (HTML-escaped in `data-copy-text`) |
| `cls` | `str` | `""` | Extra CSS classes |

Uses `navigator.clipboard.writeText` with Alpine.js `x-data` for state.

## model_card

Card for comparing LLM model responses. Wraps content in a card with header, optional badge, footer, and SSE streaming support.

```text
{% from "chirpui/streaming.html" import model_card %}

{% call model_card("GPT-4", badge="Latest", sse_connect="/api/model/gpt4", sse_streaming=true) %}
  {# Response streams in here #}
{% end %}

{% call model_card("Claude", footer="Latency: 1.2s") %}
  <div class="chirpui-prose">{{ response | safe }}</div>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Model name in header |
| `badge` | `str` | `none` | Badge text next to title |
| `footer` | `str` | `none` | Footer content |
| `cls` | `str` | `""` | Extra CSS classes |
| `sse_connect` | `str` | `none` | SSE endpoint (enables `hx-ext="sse"`) |
| `sse_close` | `str` | `"done"` | SSE close event name |
| `sse_streaming` | `bool` | `false` | Enable streaming block with cursor inside body |

When `sse_streaming=true`, the card body contains a `streaming_block--active` div with `sse-swap="fragment"`.

## infinite_scroll

htmx-powered infinite scroll container. Loads more content when the element is revealed in the viewport.

```text
{% from "chirpui/infinite_scroll.html" import infinite_scroll %}

{% call infinite_scroll(load_url="/feed?page=2", target="this", swap="beforeend") %}
  {# Existing items here #}
  {% for item in items %}
    {{ feed_card(item) }}
  {% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `load_url` | `str` | required | URL to fetch next page |
| `target` | `str` | `"this"` | htmx target for appended content |
| `swap` | `str` | `"beforeend"` | htmx swap strategy |
| `loading_html` | `str` | `none` | Custom loading indicator HTML |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** Default slot for existing content. `loading` slot for custom skeleton (used when `loading_html` is not set).

Uses `hx-trigger="revealed"` to fire when scrolled into view.

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-message-bubble` | Chat bubble wrapper |
| `chirpui-message-bubble--assistant/user` | Role variants |
| `chirpui-streaming-block` | Streaming content area |
| `chirpui-streaming-block--active` | Active streaming (cursor visible) |
| `chirpui-streaming-block__cursor` | Blinking cursor |
| `chirpui-copy-btn` | Copy button |
| `chirpui-copy-btn__label` | Default label |
| `chirpui-copy-btn__done` | "Copied!" feedback |
| `chirpui-model-card` | Model card wrapper |
| `chirpui-model-card__header` | Card header |
| `chirpui-model-card__badge` | Model badge |
| `chirpui-model-card__body` | Card body |
| `chirpui-model-card__footer` | Card footer |
| `chirpui-infinite-scroll` | Scroll container |
| `chirpui-infinite-scroll__loading` | Loading indicator |

## Usage notes

- Pair streaming components with htmx SSE or Chirp streaming responses.
- Swap fragments into a stable container.
- Keep the scroll region in a flex child with `min-height: 0` when using [Vertical layout](../guides/vertical-layout.md).

## Related

- [Social and chat](./social-and-chat.md)
- [HTMX patterns](../guides/htmx-patterns.md)
