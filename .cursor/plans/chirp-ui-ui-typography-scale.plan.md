---
name: "chirp-ui UI Typography Scale"
overview: "Introduce separate typography scales (size, family, weight) for UI components vs. document/prose, enabling independent tuning for dashboard density vs. content readability."
todos:
  - id: tokens
    content: "Add --chirpui-ui-* and --chirpui-prose-* tokens (size, family, weight)"
  - id: migrate
    content: "Migrate components from --chirpui-font-* to --chirpui-ui-*"
  - id: prose
    content: "Wire prose styles to --chirpui-prose-* (family, weight, size)"
  - id: docs
    content: "Document both scales in COMPONENT-OPTIONS or theme tokens"
isProject: false
---

# chirp-ui: UI Typography Scale

## Goal

Introduce a **UI/component typography scale** separate from the **document/prose scale**. Components (badges, chips, labels, card headers, buttons, form labels, meta text) use the UI scale; headings, paragraphs, lists use the prose scale. Enables independent tuning: dashboards get compact UI chrome; docs get readable body text.

---

## Current State

- Single scale: `--chirpui-font-xs` through `--chirpui-font-2xl`
- Components and prose both use these tokens
- No `font-family` or `font-weight` tokens — everything inherits from document
- Font weights hardcoded: `500` (badge, avatar), `600` (stat value, card header, unread count)
- No semantic distinction between "UI chip size" vs "body text size"
- Card header, page header, section header lack explicit font-size (inherit)

---

## Proposed Token Structure

### UI Scale (components)

**Font size**

| Token | Purpose | Default | Used by |
|-------|---------|---------|---------|
| `--chirpui-ui-xs` | Chip, badge, count, timestamp, meta | 0.75rem | badge, reaction-pill count, conversation time, unread count |
| `--chirpui-ui-sm` | Label, card header, button, list item title | clamp(0.8125rem, 1.5vw, 0.875rem) | badge, divider text, stat label, avatar, action bar, card header |
| `--chirpui-ui-base` | Modal title, section header, form label | clamp(0.9375rem, 2vw, 1rem) | card title, avatar-lg |
| `--chirpui-ui-lg` | Page header, hero title | clamp(1.0625rem, 2.5vw, 1.125rem) | stat value, action bar icon |
| `--chirpui-ui-xl` | Hero eyebrow, large stat | clamp(1.25rem, 3vw, 1.5rem) | stat icon |

**Font family & weight**

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-ui-font-family` | UI chrome (labels, badges, headers) | `ui-sans, system-ui, sans-serif` |
| `--chirpui-ui-font-weight-normal` | Body text in components | `400` |
| `--chirpui-ui-font-weight-medium` | Labels, badges, meta | `500` |
| `--chirpui-ui-font-weight-semibold` | Card headers, titles, stat values | `600` |
| `--chirpui-ui-font-weight-bold` | Page headers, emphasis | `700` |

### Prose Scale (document content)

**Font size**

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-prose-base` | Body text | clamp(0.9375rem, 2vw, 1rem) |
| `--chirpui-prose-sm` | Caption, footnote | clamp(0.8125rem, 1.5vw, 0.875rem) |
| `--chirpui-prose-lg` | Lead paragraph | clamp(1.0625rem, 2.5vw, 1.125rem) |
| `--chirpui-prose-xl` | h3 | clamp(1.25rem, 3vw, 1.5rem) |
| `--chirpui-prose-2xl` | h2 | clamp(1.5rem, 4vw, 1.75rem) |
| `--chirpui-prose-3xl` | h1 | clamp(1.75rem, 5vw, 2rem) |

**Font family & weight**

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-prose-font-family` | Document body, headings | `ui-sans, system-ui, sans-serif` (or serif stack for docs) |
| `--chirpui-prose-font-weight-normal` | Body, paragraphs | `400` |
| `--chirpui-prose-font-weight-medium` | Emphasis, lead | `500` |
| `--chirpui-prose-font-weight-heading` | h1–h6 | `600` |
| `--chirpui-prose-font-weight-bold` | Strong emphasis | `700` |

**Rationale**: UI often benefits from a crisp sans for labels and chrome; prose can use the same stack or a serif for long-form readability. Weights differ: UI labels use medium (500), card titles semibold (600); prose body uses normal (400), headings semibold (600). Themes override independently: e.g. `--chirpui-prose-font-family: Georgia, serif` for docs without touching UI.

**Alias strategy**: Keep `--chirpui-font-*` as aliases during migration. Phase 1: `--chirpui-ui-*` and `--chirpui-prose-*` both reference same values; Phase 2: allow themes to override UI and prose independently.

---

## Component → UI Token Mapping

### Size + weight

| Component | Element | Size | Weight |
|-----------|---------|------|--------|
| badge | .chirpui-badge | ui-sm | ui-medium |
| card | .chirpui-card__header | ui-sm | ui-semibold |
| card | .chirpui-card__title | ui-base | ui-semibold |
| stat | .chirpui-stat__value | ui-lg | ui-semibold |
| stat | .chirpui-stat__label | ui-sm | ui-medium |
| stat | .chirpui-stat__icon | ui-xl | ui-normal |
| avatar | .chirpui-avatar (md) | ui-sm | ui-medium |
| avatar | .chirpui-avatar--sm | ui-xs | ui-medium |
| avatar | .chirpui-avatar--lg | ui-base | ui-medium |
| divider | .chirpui-divider__text | ui-sm | ui-medium |
| action-bar | .chirpui-action-bar__icon | ui-lg | ui-normal |
| action-bar | .chirpui-action-bar__count | ui-sm | ui-medium |
| conversation-item | .chirpui-conversation-item__name | ui-sm | ui-semibold |
| conversation-item | .chirpui-conversation-item__time | ui-xs | ui-normal |
| conversation-item | .chirpui-conversation-item__preview | ui-sm | ui-normal |
| conversation-item | .chirpui-conversation-item__unread | ui-xs | ui-semibold |
| reaction-pill | .chirpui-reaction-pill__emoji | ui-sm | ui-normal |
| reaction-pill | .chirpui-reaction-pill__count | ui-xs | ui-medium |
| index-card | .chirpui-index-card__badge | ui-xs | ui-medium |
| model-card | .chirpui-model-card__badge | ui-xs | ui-medium |
| page-header | .chirpui-page-header__title | ui-lg or ui-xl | ui-bold |
| section-header | .chirpui-section-header__title | ui-base or ui-lg | ui-semibold |
| prose | .chirpui-prose | prose-base | prose-normal |
| prose | :where(.chirpui-prose) h1/h2/h3 | prose-3xl/2xl/xl | prose-heading |

---

## Utility Classes

Add UI utilities for ad-hoc component styling (size + family + weight):

```css
/* Size */
.chirpui-ui-xs   { font-size: var(--chirpui-ui-xs); }
.chirpui-ui-sm   { font-size: var(--chirpui-ui-sm); }
.chirpui-ui-base { font-size: var(--chirpui-ui-base); }
.chirpui-ui-lg   { font-size: var(--chirpui-ui-lg); }
.chirpui-ui-xl   { font-size: var(--chirpui-ui-xl); }

/* Weight (shorthand for components) */
.chirpui-ui-normal   { font-weight: var(--chirpui-ui-font-weight-normal); }
.chirpui-ui-medium   { font-weight: var(--chirpui-ui-font-weight-medium); }
.chirpui-ui-semibold { font-weight: var(--chirpui-ui-font-weight-semibold); }
.chirpui-ui-bold     { font-weight: var(--chirpui-ui-font-weight-bold); }

/* Full stack — applies family + size + weight for a role */
.chirpui-ui-label   { font-family: var(--chirpui-ui-font-family); font-size: var(--chirpui-ui-sm); font-weight: var(--chirpui-ui-font-weight-medium); }
.chirpui-ui-title   { font-family: var(--chirpui-ui-font-family); font-size: var(--chirpui-ui-base); font-weight: var(--chirpui-ui-font-weight-semibold); }
.chirpui-ui-meta    { font-family: var(--chirpui-ui-font-family); font-size: var(--chirpui-ui-xs); font-weight: var(--chirpui-ui-font-weight-normal); }
```

Components use `font-family: var(--chirpui-ui-font-family)` (or prose) so themes can override. Keep `.chirpui-font-*` as aliases to `--chirpui-font-*` (which map to prose) for backward compatibility.

---

## Implementation Phases

### Phase 1: Add tokens, no breaking changes

1. Add `--chirpui-ui-xs` … `--chirpui-ui-xl` to `:root`, defaulting to current `--chirpui-font-*` values
2. Add `--chirpui-ui-font-family` and `--chirpui-ui-font-weight-*` (normal, medium, semibold, bold)
3. Add `--chirpui-prose-base` … `--chirpui-prose-3xl` (alias to font scale)
4. Add `--chirpui-prose-font-family` and `--chirpui-prose-font-weight-*`
5. Migrate components to use `--chirpui-ui-*` (size + family + weight) instead of `--chirpui-font-*`
6. Add explicit font-size + weight to card header, page header, section header

**Files**: `chirpui.css` (tokens + component rules)

### Phase 2: Prose scale usage

1. Update `.chirpui-prose` and `:where(.chirpui-prose) h1/h2/h3` to use `--chirpui-prose-*`
2. Add `.chirpui-prose-sm`, `.chirpui-prose-lg` utilities if needed

### Phase 3: Theme token docs

1. Update `docs/PLAN-theme-tokens.md` or create `docs/TYPOGRAPHY.md` with both scales
2. Document override pattern: themes set `--chirpui-ui-sm` for denser/looser UI without touching prose

---

## Backward Compatibility

- **Existing themes**: If they override `--chirpui-font-sm`, etc., those still affect prose. UI scale starts as alias; themes can override `--chirpui-ui-*` for component-specific tuning
- **Breaking change**: None if we keep `--chirpui-font-*` and have `--chirpui-ui-*` default to them. Themes opt in to independent UI tuning by setting `--chirpui-ui-*`

---

## Deliverables

| Item | File |
|------|------|
| Tokens | chirpui.css `:root` |
| Component migrations | chirpui.css (component rules) |
| Utility classes | chirpui.css |
| Docs | docs/PLAN-theme-tokens.md or docs/TYPOGRAPHY.md |

---

## Open Questions

1. **Alias vs. copy**: Should `--chirpui-ui-sm` default to `var(--chirpui-font-sm)` (alias) or duplicate the value? Alias = one place to change; copy = can diverge later without breaking
2. **Page/section header**: Add new tokens `--chirpui-ui-page-title` and `--chirpui-ui-section-title` for semantic override, or use ui-lg/ui-base?
3. **Form labels**: Currently no explicit size. Add `--chirpui-ui-label` → ui-sm?
4. **Font-family default**: Same stack for UI and prose (`ui-sans, system-ui, sans-serif`), or prose default to serif for docs? Recommend: same by default; themes opt in to serif prose
5. **Mono for code**: Add `--chirpui-code-font-family` (ui-monospace, monospace) for `<code>` / syntax? Separate from UI/prose
