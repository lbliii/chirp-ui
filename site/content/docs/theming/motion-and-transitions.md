---
title: Motion and transitions
description: HTMX swap classes, view transitions, and motion tokens
draft: false
weight: 34
lang: en
type: doc
keywords: [chirp-ui, motion, htmx, view-transitions]
icon: wave-sine
---

# Motion and transitions

## HTMX swap classes

During swaps, HTMX adds:

| Class | When |
|-------|------|
| `htmx-swapping` | Outgoing content removing |
| `htmx-settling` | New content inserting |
| `htmx-added` | New nodes just added |

Style these with **`--chirpui-duration-*`** and **`--chirpui-easing-*`** — enforced by `test_transition_tokens.py` in the repo.

## View Transitions

When Chirp enables View Transitions, include **`chirpui-transitions.css`** after `chirpui.css`. It sets safe `view-transition-name` defaults and defines short fade animations for `page-content`, respecting **`prefers-reduced-motion`**.

See comments in `chirpui-transitions.css` for boost/OOB caveats.

## Related

- [Accessibility](../guides/accessibility.md)
- [Typography effects](../components/typography-effects.md)
