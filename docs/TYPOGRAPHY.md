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
| `--chirpui-ui-font-family` | UI chrome | `ui-sans, system-ui, sans-serif` |
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
| `--chirpui-prose-font-family` | Document body, headings | `ui-sans, system-ui, sans-serif` |
| `--chirpui-prose-font-weight-normal` | Body, paragraphs | `400` |
| `--chirpui-prose-font-weight-medium` | Emphasis, lead | `500` |
| `--chirpui-prose-font-weight-heading` | h1–h6 | `600` |
| `--chirpui-prose-font-weight-bold` | Strong emphasis | `700` |

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
