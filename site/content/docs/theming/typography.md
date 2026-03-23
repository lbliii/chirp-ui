---
title: Typography
description: UI vs prose scales, weights, and overrides
draft: false
weight: 32
lang: en
type: doc
keywords: [chirp-ui, typography, prose]
icon: text-t
---

# Typography

chirp-ui uses two scales:

- **UI** — components (badges, cards, stats, headers).
- **Prose** — document content inside `.chirpui-prose`.

## UI scale

| Token | Role |
|-------|------|
| `--chirpui-ui-xs` | Chips, meta, timestamps |
| `--chirpui-ui-sm` | Labels, list titles |
| `--chirpui-ui-base` | Modal title, form labels |
| `--chirpui-ui-lg` | Page header, stat value |
| `--chirpui-ui-xl` | Hero eyebrow, large icons |

Weights: `--chirpui-ui-font-weight-normal` through `bold`.

## Prose scale

`--chirpui-prose-base` through `--chirpui-prose-5xl` for body → display headings. `--chirpui-prose-max-width` defaults to **65ch**.

## Override example

Denser dashboards without changing prose:

```css
:root {
  --chirpui-ui-sm: 0.8125rem;
  --chirpui-ui-xs: 0.6875rem;
}
```

Full tables: [TYPOGRAPHY.md](https://github.com/lbliii/chirp-ui/blob/main/docs/TYPOGRAPHY.md).

## Related

- [Design tokens](./design-tokens.md)
