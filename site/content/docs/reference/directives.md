---
title: Directives
description: Every chirp-theme directive with its options and a rendered example
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-theme, directives, admonition, card, cards, child-cards, callout]
category: reference
---

# Directives

Directives are block-level containers you author with fenced `:::{name}` syntax.
Options are written as `:key: value` lines directly under the opening fence;
the block body (and any nested directives) goes below the options. Close the
block with a matching `:::` line.

```
:::{name} Optional title
:option: value

Body Markdown.
:::
```

The chirp-theme provides templates for four directives — `admonition`, `card`,
`cards`, and `child-cards` — each rendered with Chirp UI markup so authored
content matches the rest of the site. This page documents every one with its
options and a live rendered example.

| Directive | Purpose |
|-----------|---------|
| `admonition` | Semantic callouts: note, tip, warning, danger, … |
| `card` | A single linkable card |
| `cards` | A responsive grid of `card` blocks |
| `child-cards` | Auto-generated cards from child pages |

---

## admonition

The full semantic callout family. The directive name *is* the admonition type,
so you write `:::{note}`, `:::{tip}`, `:::{warning}`, and so on — there is no
literal `:::{admonition}` block. Each type maps to a Chirp UI `callout` variant
(`info`, `success`, `warning`, `error`, or `neutral`).

Supported types: `note`, `info`, `important`, `tip`, `success`, `warning`,
`caution`, `danger`, `error`, `example`, `seealso`.

| Option | Default | Description |
|--------|---------|-------------|
| *title* (after the type) | the capitalized type | Custom heading |
| `:class:` | — | Extra CSS class on the callout |
| *body* | — | Callout content (Markdown) |

```
:::{tip} Pro tip
Prefer the macro vocabulary over raw classes.
:::

:::{warning}
This changes shared workspace state.
:::
```

:::{tip} Pro tip
Prefer the macro vocabulary over raw classes — it keeps your content in sync with the registry.
:::

:::{note} A note
`note`, `info`, and `important` all render as the informational callout variant.
:::

:::{warning}
With no title, the type name becomes the heading.
:::

:::{danger} Irreversible
`danger` and `error` render as the error variant for high-risk actions.
:::

For the inline (non-block) equivalents, the `tip` / `warning` / `danger`
[shortcodes](/docs/reference/shortcodes/#tip-warning-danger) wrap the same callout markup.

---

## card

A single card. With `:link:` (or a title that resolves to a page), the whole
card becomes a link. Use it standalone, or nest it inside a `cards` grid.

| Option | Default | Description |
|--------|---------|-------------|
| *title* (after `card`) | — | Card heading |
| `:icon:` | — | Phosphor icon name shown in the header |
| `:link:` | — | URL or page reference; makes the card a link |
| `:description:` | — | Brief summary under the title |
| `:badge:` | — | Small badge text (e.g. `New`, `Beta`) |
| `:color:` | — | Accent color (`blue`, `green`, `red`, `yellow`, `orange`, `purple`, `gray`, `pink`, `indigo`, `teal`, `cyan`, `violet`) |
| `:image:` | — | Header image URL |
| `:layout:` | `default` | `default`, `horizontal`, `portrait`, or `compact` |
| `:class:` | — | Extra CSS class |
| *body* | — | Card content (Markdown) |

```
:::{card} Component reference
:icon: layers
:link: /docs/components/
:badge: Live
Browse every public macro with options and a rendered example.
:::
```

A single card is most useful inside a `cards` grid (below).

---

## cards

A responsive grid container for `card` blocks. Nest one `card` per cell.

| Option | Default | Description |
|--------|---------|-------------|
| `:columns:` | `auto` | `auto`, `1`–`6`, or a responsive ramp like `1-2-3` |
| `:gap:` | `medium` | `small`, `medium`, or `large` |
| `:style:` | `default` | `default`, `minimal`, or `bordered` |
| `:layout:` | `default` | Card layout applied to the grid |
| `:class:` | — | Extra CSS class |

```
:::{cards}
:columns: 2
:gap: medium

:::{card} Shortcodes
:icon: code
:link: /docs/reference/shortcodes/
Inline helpers for media, callouts, and live specimens.
:::{/card}

:::{card} Directives
:icon: layers
:link: /docs/reference/directives/
Block containers for admonitions and card grids.
:::{/card}

:::{/cards}
```

:::{cards}
:columns: 2
:gap: medium

:::{card} Shortcodes
:icon: code
:link: /docs/reference/shortcodes/
Inline `{{</* name */>}}` helpers for media, callouts, and live specimens.
:::{/card}

:::{card} Directives
:icon: layers
:link: /docs/reference/directives/
Block `:::{name}` containers for admonitions and card grids.
:::{/card}

:::{/cards}

---

## child-cards

Auto-generates a `cards` grid from the current page's children — handy on a
section `_index.md` so the landing page stays in sync as pages are added or
removed. Note the hyphenated name: `:::{child-cards}`.

| Option | Default | Description |
|--------|---------|-------------|
| `:columns:` | `auto` | Column layout (same values as `cards`) |
| `:gap:` | `medium` | `small`, `medium`, or `large` |
| `:include:` | `all` | `sections`, `pages`, or `all` |
| `:fields:` | `title, description` | Which child fields to pull into each card |
| `:layout:` | `default` | Card layout |
| `:style:` | `default` | `default`, `minimal`, or `bordered` |

```
:::{child-cards}
:columns: 3
:include: pages
:fields: title, description, icon
:::
```

When a section has no matching children, the directive renders a single muted
card with an explanatory message instead of crashing the page.

Looking for inline helpers instead? See the
[shortcodes reference](/docs/reference/shortcodes/).
