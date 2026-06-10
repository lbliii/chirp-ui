---
title: Shortcodes
description: Every chirp-theme shortcode with its parameters and a rendered example
draft: false
weight: 10
lang: en
type: doc
keywords: [chirp-theme, shortcodes, component_specimen, tip, warning, danger, figure, gallery, img, audio, details, highlight, blockquote, ref, relref, param]
category: reference
---

# Shortcodes

Shortcodes are inline helpers you call from Markdown with the
`{{</* name args */>}}` syntax. Each maps to a template in the theme's
`shortcodes/` directory and renders with Chirp UI markup. Arguments are
`key="value"` pairs (some shortcodes also accept a leading positional value);
paired shortcodes wrap inner content between an opening and a `{{</* /name */>}}`
closing tag.

This page documents every shipped shortcode with its parameters and a live
rendered example.

| Shortcode | Purpose |
|-----------|---------|
| `component_specimen` | Render a live Chirp UI component inside prose |
| `tip` / `warning` / `danger` | Inline semantic callouts |
| `figure` | Captioned, optionally linked image |
| `img` | Bare image (use inside `gallery`) |
| `gallery` | Responsive image grid |
| `audio` | Audio player card |
| `details` | Collapsible disclosure (accordion item) |
| `highlight` | Language-tagged code block |
| `blockquote` | Cited pull-quote |
| `ref` / `relref` | Link to another page by source path |
| `param` | Echo a config or front-matter value |

---

## component_specimen

Renders a live, in-page demo of a Chirp UI component. This is the live-demo
mechanism the components catalog uses, so a reader can see real rendered output
without leaving the site or running a local app.

The shortcode demos a curated set of primitives (`toggle_group`, `slider`,
`scroll_area`, `item`, `data_table`, `kbd`, `separator`, `aspect_ratio`,
`label`). For any other `name`, it renders the inner content you provide as the
preview body.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `name` | yes | — | Component key (also accepted as the first positional arg) |
| `title` | no | `name` | Heading shown above the preview |
| `description` | no | — | One-line caption under the title |
| *inner* | no | — | Fallback preview body for unknown `name` values |

```
{{</* component_specimen name="item" title="Item" description="Reusable row anatomy for lists and menus." */>}}
```

{{< component_specimen name="item" title="Item" description="Reusable row anatomy for lists and menus." >}}

For the full catalog of components with options and live specimens, see the
[component reference](/docs/components/).

---

## tip / warning / danger

Inline semantic callouts. Each is a paired shortcode whose inner Markdown
becomes the callout body, rendered with the Chirp UI `callout` macro
(`success`, `warning`, and `error` variants respectively).

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `title` | no | `Tip` / `Warning` / `Danger` | Callout heading |
| *inner* | yes | — | Callout body (Markdown) |

```
{{</* tip title="Pro tip" */>}}
Prefer the macro vocabulary over raw classes.
{{</* /tip */>}}
```

{{< tip title="Pro tip" >}}
Prefer the macro vocabulary over raw classes — it keeps your content in sync with the registry.
{{< /tip >}}

{{< warning >}}
This action changes shared workspace state.
{{< /warning >}}

{{< danger >}}
Deleting a project removes every environment and cannot be undone.
{{< /danger >}}

For the complete semantic admonition family (note, hint, caution, …) as a block
directive, see [directives — admonition](./directives/#admonition).

---

## figure

A captioned, optionally linked image rendered inside a Chirp UI card.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `src` | yes | — | Image URL |
| `alt` | no | — | Alternative text |
| `caption` | no | — | Caption text under the image |
| `link` | no | — | Wrap the image in a link to this URL |

```
{{</* figure src="/img/diagram.png" alt="Request flow" caption="Figure 1. Request flow." link="/docs/architecture/" */>}}
```

The image loads lazily; the caption renders as a muted, small `figcaption`.

---

## img

A bare lazy-loaded `<img>`. Use it inside `gallery` (it reads the parent
gallery's `class`) or anywhere you want a plain image without the card chrome.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `src` | yes | — | Image URL |
| `alt` | no | — | Alternative text |
| `class` | no | — | Extra class (inherited from a parent `gallery`) |

```
{{</* img src="/img/screen-1.png" alt="Dashboard" */>}}
```

---

## gallery

A responsive 3-column image grid. Wrap one or more `img` shortcodes inside it.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `class` | no | — | Extra class added to the grid |
| *inner* | yes | — | One or more `img` shortcodes |

```
{{</* gallery */>}}
{{</* img src="/img/a.png" alt="A" */>}}
{{</* img src="/img/b.png" alt="B" */>}}
{{</* img src="/img/c.png" alt="C" */>}}
{{</* /gallery */>}}
```

---

## audio

An audio player rendered inside a Chirp UI card.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `src` | yes | — | Audio file URL |
| `title` | no | — | Caption shown above the player |
| `preload` | no | `metadata` | Native `<audio>` preload hint (`none`, `metadata`, `auto`) |

```
{{</* audio src="/audio/episode-1.mp3" title="Episode 1" */>}}
```

---

## details

A collapsible disclosure rendered with the Chirp UI `accordion_item` macro.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `summary` | no | `Details` | Disclosure label (also accepted as the first positional arg) |
| `open` | no | `false` | Start expanded |
| *inner* | yes | — | Disclosure body (Markdown) |

```
{{</* details summary="Show the full configuration" open="false" */>}}
The body Markdown renders inside the disclosure.
{{</* /details */>}}
```

{{< details summary="Show the full configuration" >}}
The body Markdown renders inside the disclosure. Click the summary to toggle it.
{{< /details >}}

---

## highlight

A language-tagged code block. The inner content renders verbatim inside a
`chirpui-code-block`.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `lang` | no | — | Language class (also accepted as the first positional arg) |
| *inner* | yes | — | Code to display |

```
{{</* highlight lang="python" */>}}
print("hello")
{{</* /highlight */>}}
```

For most code, a fenced Markdown block is simpler. Reach for `highlight` when you
need to drive the language tag from a shortcode argument.

---

## blockquote

A cited pull-quote rendered as a neutral Chirp UI callout.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `author` | no | — | Attribution shown when `cite` is absent |
| `cite` | no | — | Cited source (rendered in a `<cite>`) |
| *inner* | yes | — | Quote body (Markdown) |

```
{{</* blockquote cite="The chirp-ui thesis" */>}}
The registry is the one bet.
{{</* /blockquote */>}}
```

{{< blockquote cite="The chirp-ui thesis" >}}
The registry is the one bet — a Python vocabulary, not a string vocabulary.
{{< /blockquote >}}

---

## ref / relref

Resolve a link to another page by its source path at build time. `ref` resolves
against the site root; `relref` resolves relative to the current page. If the
target moves, the build fails loudly instead of shipping a dead link.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `path` | yes | — | Source path of the target page (also accepted as the first positional arg) |
| `text` | no | the path | Link text (also accepted as `label`) |

```
{{</* ref path="docs/components/_index.md" text="the component catalog" */>}}
{{</* relref "controls.md" text="control selection" */>}}
```

---

## param

Echo a value from site config (preferred) or the current page's front matter
into prose. Useful for keeping version numbers and shared values in one place.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `key` | yes | — | Config or front-matter key (also accepted as the first positional arg) |

```
The current version is {{</* param "version" */>}}.
```

Looking for block-level containers instead? See the
[directives reference](./directives/).
