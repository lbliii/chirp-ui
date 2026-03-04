# chirp-ui Typography

chirp-ui uses two typography scales: **UI** (components) and **Prose** (document content). Override tokens independently to tune dashboard density vs. content readability.

---

## UI Scale (components)

Used by badges, cards, stats, avatars, labels, meta text, page/section headers.

### Size

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-ui-xs` | Chip, badge count, timestamp, meta | 0.75rem |
| `--chirpui-ui-sm` | Label, card header, button, list item title | clamp(0.8125rem, 1.5vw, 0.875rem) |
| `--chirpui-ui-base` | Modal title, section header, form label | clamp(0.9375rem, 2vw, 1rem) |
| `--chirpui-ui-lg` | Page header, stat value | clamp(1.0625rem, 2.5vw, 1.125rem) |
| `--chirpui-ui-xl` | Hero eyebrow, large stat icon | clamp(1.25rem, 3vw, 1.5rem) |

### Family & weight

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-ui-font-family` | UI chrome | `ui-sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` |
| `--chirpui-ui-font-weight-normal` | Body text in components | `400` |
| `--chirpui-ui-font-weight-medium` | Labels, badges, meta | `500` |
| `--chirpui-ui-font-weight-semibold` | Card headers, titles | `600` |
| `--chirpui-ui-font-weight-bold` | Page headers | `700` |

---

## Prose Scale (document content)

Used by `.chirpui-prose`, headings, paragraphs, captions.

### Size

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-prose-base` | Body text | clamp(0.9375rem, 2vw, 1rem) |
| `--chirpui-prose-sm` | Caption, footnote | clamp(0.8125rem, 1.5vw, 0.875rem) |
| `--chirpui-prose-lg` | Lead paragraph | clamp(1.0625rem, 2.5vw, 1.125rem) |
| `--chirpui-prose-xl` | h3 | clamp(1.25rem, 3vw, 1.5rem) |
| `--chirpui-prose-2xl` | h2 | clamp(1.5rem, 4vw, 1.75rem) |
| `--chirpui-prose-3xl` | h1 | clamp(1.75rem, 5vw, 2rem) |

### Family & weight

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-prose-font-family` | Document body, headings | `ui-sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` |
| `--chirpui-prose-font-weight-normal` | Body, paragraphs | `400` |
| `--chirpui-prose-font-weight-medium` | Emphasis, lead | `500` |
| `--chirpui-prose-font-weight-heading` | h1–h6 | `600` |
| `--chirpui-prose-font-weight-bold` | Strong emphasis | `700` |

### Prose spacing (vertical rhythm)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-prose-spacing` | Paragraph, list, pre, blockquote margins | 0.5em |
| `--chirpui-prose-spacing-heading` | Heading top/bottom margins | 0.75em |

---

## Override examples

Denser UI without touching prose:

```css
:root {
    --chirpui-ui-sm: 0.8125rem;
    --chirpui-ui-xs: 0.6875rem;
}
```

Serif prose for docs:

```css
:root {
    --chirpui-prose-font-family: Georgia, "Times New Roman", serif;
}
```

Custom font stack for both:

```css
:root {
    --chirpui-ui-font-family: "Inter", ui-sans, system-ui, sans-serif;
    --chirpui-prose-font-family: "Inter", ui-sans, system-ui, sans-serif;
}
```

Looser prose (e.g. long-form articles):

```css
:root {
    --chirpui-prose-spacing: 0.75em;
    --chirpui-prose-spacing-heading: 1em;
}
```

---

## Utility classes

| Class | Applies |
|-------|---------|
| `.chirpui-ui-xs` … `.chirpui-ui-xl` | Font size |
| `.chirpui-ui-normal` … `.chirpui-ui-bold` | Font weight |
| `.chirpui-ui-label` | Family + sm + medium |
| `.chirpui-ui-title` | Family + base + semibold |
| `.chirpui-ui-meta` | Family + xs + normal |
| `.chirpui-prose-sm`, `.chirpui-prose-lg` | Prose font size |

---

## Component mapping

| Component | Element | Size | Weight |
|-----------|---------|------|--------|
| badge | .chirpui-badge | ui-sm | medium |
| card | .chirpui-card__header | ui-sm | semibold |
| card | .chirpui-card__title | ui-base | semibold |
| stat | .chirpui-stat__value | ui-lg | semibold |
| stat | .chirpui-stat__label | ui-sm | medium |
| avatar | .chirpui-avatar | ui-sm | medium |
| page-header | h1 | ui-lg | bold |
| section-header | h2 | ui-base | semibold |
| prose | .chirpui-prose | prose-base | normal |
| prose | h1/h2/h3 | prose-3xl/2xl/xl | heading |

**Layout combos**:

- **Prose + stack**: When `chirpui-prose` is combined with `chirpui-stack` (e.g. in card bodies), prose uses block layout so margins collapse conventionally. Stack gap is disabled to avoid doubled spacing.
- **Prose in grid**: Use `chirpui-block chirpui-prose` or ensure prose is a grid child for overflow handling (long code blocks, pre-wrap).
- **Prose + grid (as grid)**: Avoid — prose should not be the grid container.

---

## Code Scale (inline and block code)

Used by `code`, `pre`, `.chirpui-code`, `.chirpui-code-block`. Override for docs, API references, or syntax-heavy content.

### Typography

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-code-font-family` | Monospace stack | `ui-monospace, ui-serif, "Cascadia Code", "Fira Code", "JetBrains Mono", "SF Mono", Consolas, monospace` |
| `--chirpui-code-font-size-inline` | Inline `code` size | 0.9em |
| `--chirpui-code-font-size-block` | Block `pre` size | var(--chirpui-prose-sm) |
| `--chirpui-code-line-height` | Line height for blocks | 1.6 |

### Colors

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-code-bg` | Background for inline and block code | light-dark(#f1f5f9, #1e293b) |
| `--chirpui-code-text` | Foreground for code | light-dark(#334155, #cbd5e1) |
| `--chirpui-code-keyword` | Syntax: keywords | light-dark(#7c3aed, #a78bfa) |
| `--chirpui-code-string` | Syntax: strings | light-dark(#059669, #34d399) |
| `--chirpui-code-number` | Syntax: numbers | light-dark(#d97706, #fbbf24) |
| `--chirpui-code-type` | Syntax: types | var(--chirpui-info) |
| `--chirpui-code-type-bg` | Type annotation background | var(--chirpui-alert-info-bg) |

### Block layout

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-pre-padding` | Padding for `pre` and `.chirpui-code-block` | var(--chirpui-spacing) |

### Override examples

Custom monospace font:

```css
:root {
    --chirpui-code-font-family: "IBM Plex Mono", ui-monospace, monospace;
}
```

Smaller inline code:

```css
:root {
    --chirpui-code-font-size-inline: 0.85em;
    --chirpui-code-font-size-block: 0.8125rem;
}
```

Darker code blocks:

```css
:root {
    --chirpui-code-bg: light-dark(#e2e8f0, #334155);
}
