---
name: "chirp-ui Code/Pre Design Tokens"
overview: "Wire prose code and pre to design tokens; add code typography tokens; document code token system for theme overrides."
todos:
  - id: wire-prose
    content: "Wire prose code and pre to --chirpui-code-* tokens (replace --chirpui-bg-subtle)"
  - id: code-typography
    content: "Add --chirpui-code-font-family, --chirpui-code-font-size-inline, --chirpui-code-font-size-block, --chirpui-code-line-height"
  - id: block-tokens
    content: "Add --chirpui-pre-padding, --chirpui-pre-border (optional) for block-level customization"
  - id: docs
    content: "Document code tokens in TYPOGRAPHY.md or new docs/CODE-TOKENS.md"
isProject: false
---

# chirp-ui: Code/Pre Design Tokens

## Goal

Make `pre` and `code` styling fully token-driven so themes can override code appearance independently. Today prose `code` and `pre` bypass `--chirpui-code-*` tokens; code typography (font, size, line-height) is hardcoded. This plan aligns code with the design system and documents it.

---

## Current State

**Tokens exist** (lines 152–159 in chirpui.css):

- `--chirpui-code-bg`, `--chirpui-code-text` — base colors
- `--chirpui-code-type`, `--chirpui-code-type-bg` — type annotations
- `--chirpui-code-keyword`, `--chirpui-code-string`, `--chirpui-code-number` — syntax highlighting

**Prose bypasses them:**

- `:where(.chirpui-prose) code` uses `background: var(--chirpui-bg-subtle)` (no `--chirpui-code-bg`, no `--chirpui-code-text`)
- `:where(.chirpui-prose) pre` uses `background: var(--chirpui-bg-subtle)` (no `--chirpui-code-bg`)

**Explicit classes use tokens correctly:**

- `.chirpui-code` — uses `--chirpui-code-bg`, `--chirpui-code-text`
- `.chirpui-code-block` — uses `--chirpui-code-bg`

**Missing:**

- No `--chirpui-code-font-family` (monospace stack)
- No `--chirpui-code-font-size-inline` / `--chirpui-code-font-size-block`
- No `--chirpui-code-line-height`
- No `--chirpui-pre-padding`, `--chirpui-pre-border` for block-level tuning
- TYPOGRAPHY.md documents UI and Prose only; code tokens undocumented

---

## Proposed Token Structure

### Existing (keep, wire prose to them)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-code-bg` | Background for inline and block code | light-dark(#f1f5f9, #1e293b) |
| `--chirpui-code-text` | Foreground for code | light-dark(#334155, #cbd5e1) |
| `--chirpui-code-keyword` | Syntax: keywords | light-dark(#7c3aed, #a78bfa) |
| `--chirpui-code-string` | Syntax: strings | light-dark(#059669, #34d399) |
| `--chirpui-code-number` | Syntax: numbers | light-dark(#d97706, #fbbf24) |
| `--chirpui-code-type` | Syntax: types | var(--chirpui-info) |
| `--chirpui-code-type-bg` | Type annotation background | var(--chirpui-alert-info-bg) |

### New — Code typography

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-code-font-family` | Monospace stack for code | `ui-monospace, ui-serif, "Cascadia Code", "Fira Code", "JetBrains Mono", "SF Mono", Consolas, monospace` |
| `--chirpui-code-font-size-inline` | Inline `code` size | 0.9em (or `var(--chirpui-prose-sm)`) |
| `--chirpui-code-font-size-block` | Block `pre` size | var(--chirpui-prose-sm) |
| `--chirpui-code-line-height` | Line height for blocks | 1.6 |

### New — Block-level (optional)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-pre-padding` | Padding for `pre` / `.chirpui-code-block` | var(--chirpui-spacing) |
| `--chirpui-pre-border` | Optional border for code blocks | none (or 1px solid var(--chirpui-border)) |

### Inline code padding (existing pattern)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-code-padding-inline` | Horizontal padding for inline code | 0.15em 0.35em (keep as-is or tokenize) |

---

## Component → Token Mapping

| Selector | Uses |
|----------|------|
| `:where(.chirpui-prose) code` | `--chirpui-code-bg`, `--chirpui-code-text`, `--chirpui-code-font-family`, `--chirpui-code-font-size-inline` |
| `:where(.chirpui-prose) pre` | `--chirpui-code-bg`, `--chirpui-pre-padding`, `--chirpui-code-font-family`, `--chirpui-code-font-size-block`, `--chirpui-code-line-height` |
| `.chirpui-code` | Already uses `--chirpui-code-bg`, `--chirpui-code-text`; add font-family, font-size |
| `.chirpui-code-block` | Already uses `--chirpui-code-bg`; add `--chirpui-pre-padding`, font tokens |

---

## Implementation Phases

### Phase 1: Wire prose to existing tokens (no new tokens)

1. Update `:where(.chirpui-prose) code` to use `background: var(--chirpui-code-bg)`, `color: var(--chirpui-code-text)` instead of `--chirpui-bg-subtle`
2. Update `:where(.chirpui-prose) pre` to use `background: var(--chirpui-code-bg)` instead of `--chirpui-bg-subtle`
3. Ensure `:where(.chirpui-prose) pre code` inherits `color: var(--chirpui-code-text)` (or reset to it)

**Files**: `chirpui.css` (prose section ~1815–1866)

### Phase 2: Add code typography tokens

1. Add to `:root`:
   - `--chirpui-code-font-family`
   - `--chirpui-code-font-size-inline` (0.9em)
   - `--chirpui-code-font-size-block` (var(--chirpui-prose-sm))
   - `--chirpui-code-line-height` (1.6)
2. Apply to prose `code`, prose `pre`, `.chirpui-code`, `.chirpui-code-block`
3. Add `--chirpui-pre-padding` (var(--chirpui-spacing)) and use for `pre` and `.chirpui-code-block`

**Files**: `chirpui.css` (`:root` + prose + code-block rules)

### Phase 3: Documentation

1. Add "Code" section to `docs/TYPOGRAPHY.md` or create `docs/CODE-TOKENS.md`
2. Document all `--chirpui-code-*` and `--chirpui-pre-*` tokens with purpose and override examples
3. Add override example for monospace font, code block padding, etc.

**Files**: `docs/TYPOGRAPHY.md` or `docs/CODE-TOKENS.md`

---

## Backward Compatibility

- **Visual**: Switching prose `code`/`pre` from `--chirpui-bg-subtle` to `--chirpui-code-bg` is a no-op if themes haven't overridden either; defaults are similar (both slate grays)
- **Themes overriding `--chirpui-bg-subtle`**: Code will no longer follow that override; they must set `--chirpui-code-bg` for code-specific styling (intended)
- **New tokens**: All default to current behavior; no breaking changes

---

## Deliverables

| Item | File |
|------|------|
| Prose code/pre wired to tokens | chirpui.css |
| Code typography tokens | chirpui.css `:root` |
| Block tokens (pre-padding) | chirpui.css |
| Code token docs | docs/TYPOGRAPHY.md or docs/CODE-TOKENS.md |

---

## Open Questions

1. **Font-size-inline**: Use `0.9em` (relative to prose) or `var(--chirpui-prose-sm)` for consistency? Recommend `0.9em` to preserve current "slightly smaller than body" feel.
2. **--chirpui-pre-border**: Add as optional or skip? Recommend: skip initially; add if themes request it.
3. **Syntax highlighter integration**: Tokens `--chirpui-code-keyword`, `--chirpui-code-string`, `--chirpui-code-number` exist but may not be wired to `.hljs-*` or similar. Out of scope for this plan; document for future use.
4. **CODE-TOKENS.md vs TYPOGRAPHY.md**: Add a "Code" section to TYPOGRAPHY.md (keeps typography in one place) or create CODE-TOKENS.md (separate for code-specific tokens)? Recommend: add to TYPOGRAPHY.md since code is typography-adjacent.
