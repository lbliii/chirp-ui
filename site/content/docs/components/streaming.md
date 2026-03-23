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

Templates in `chirpui/streaming.html` help LLM and SSE UIs: `streaming_block`, `streaming_bubble`, `model_card`, and helpers like `copy_btn`.

## Usage

Pair with htmx SSE or Chirp streaming responses; swap fragments into a stable container. Keep the scroll region in a flex child with `min-height: 0` when using [Vertical layout](../guides/vertical-layout.md).

## Related

- [Social and chat](./social-and-chat.md)
- [HTMX patterns](../guides/htmx-patterns.md)
