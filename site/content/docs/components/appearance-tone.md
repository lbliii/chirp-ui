---
title: Appearance and tone
description: Descriptor-backed visual preset axes for Chirp UI components
draft: false
weight: 22
lang: en
type: doc
keywords: [chirp-ui, appearance, tone, presets, components]
category: components
---

# Appearance and tone

Chirp UI components that opt into the preset pilot accept `appearance` and
`tone` as macro parameters. These values are descriptor-backed component
contracts, not utility classes.

```kida
{{ btn("Delete", appearance="outlined", tone="danger") }}
{{ badge("At risk", appearance="tonal", tone="warning") }}
{% call card(title="Review", appearance="outlined", tone="danger") %}...{% end %}
{% call surface(appearance="outlined", tone="primary") %}...{% end %}
{{ text_field("project", label="Project", appearance="outlined", tone="primary") }}
```

## Pilot components

The current pilot covers:

- `btn`
- `badge`
- `alert`
- `card`
- `surface`
- `field` / `text_field`

Use `danger` for shared destructive or high-risk intent. Do not use
`tone="error"`; existing `variant="error"` values remain component-local
compatibility where they already shipped.

## Canonical reference

The repository guide has the full vocabulary, migration map, validation
behavior, and compatibility policy:
[`docs/components/appearance-tone.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/components/appearance-tone.md?plain=1).

The component showcase also includes a live `/appearance-tone` page for copyable
examples across the pilot components.
