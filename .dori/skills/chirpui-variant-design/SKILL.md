---
name: chirpui-variant-design
description: |
  Design the variant and size set for a new or extended chirp-ui component.
  Given a component name and product context, recommends which variants to expose,
  what the CSS modifiers should express, and produces the VARIANT_REGISTRY /
  SIZE_REGISTRY entries and a filled-in State × Variant table.
tags:
  - chirpui
  - variants
  - design-system
  - component
triggers:
  - "::chirpui-variant-design"
  - "::cvd"
  - "design chirpui variants"
  - "what variants should"
  - "chirpui variant"
inputs:
  - component: "Component name (e.g. stat-card, timeline, code-block)"
  - context: "Optional — product type (e.g. SaaS dashboard, developer tool, e-commerce)"
  - purpose: "Optional — what the component communicates (e.g. status, severity, identity)"
outputs:
  - recommendation: "Variant set rationale + registry entries + State × Variant table"
---

# chirpui Variant Design

Decide what variants and sizes a chirp-ui component should expose before writing
any code. A well-designed variant set is small, orthogonal, and tied to semantic
meaning — not visual preferences.

---

## Variant Design Principles

### 1. Variants express semantic meaning, not appearance

Good: `variant="error"` — means something went wrong
Bad: `variant="red"` — describes a color, not a concept

The CSS class `chirpui-alert--error` can be restyled per theme; `chirpui-alert--red`
cannot be restyled without breaking the API.

### 2. Keep the set small and exhaustive

Aim for 3–7 variants. If you need more, consider splitting the component.
Every variant must be meaningfully different from the others.

### 3. The first variant is the fallback

The first entry in the registry tuple is what invalid values fall back to.
Make it the safest, most neutral option (often `""`, `"default"`, or `"info"`).

### 4. Sizes are independent of variants

If the component needs size control, use `SIZE_REGISTRY` separately. Avoid
`variant="sm"` — that conflates two orthogonal concerns.

### 5. Don't expose every CSS possibility

Not every CSS modifier needs a variant. Use `modifier=` in `bem()` for one-off
states (e.g. `modifier="loading"`, `modifier="dismissible"`) — these don't go
in the registry.

---

## Product Context → Variant Guidance

Use the product context to calibrate which semantic dimensions matter most:

| Product type | High-value variant axes |
|---|---|
| SaaS / dashboard | status (info/success/warning/error), emphasis (default/muted/elevated) |
| Developer tool | semantic (info/warning/error/tip), kind (inline/block) |
| E-commerce | intent (primary/ghost/danger), urgency (default/sale/oos) |
| Content / blog | editorial (default/featured/callout) |
| Accessibility-critical (health, gov) | severity (info/caution/critical), tone (neutral/positive/negative) |
| AI / chat platform | role (default/user/assistant/system) |

---

## Decision Procedure

### Step 1 — Name the semantic axes

What does this component communicate? List the dimensions independently:
- **Status axis**: info, success, warning, error
- **Emphasis axis**: muted, default, elevated, accent
- **Role axis**: user, assistant, system

Usually one axis is primary. If two are needed, model them as `variant` + `modifier`.

### Step 2 — Check existing registry for consistency

Look at `VARIANT_REGISTRY` in `validation.py`. Reuse existing variant names where
the semantics match — e.g. if `alert` uses `("info", "success", "warning", "error")`,
a `toast` component should use the same names for the same meanings.

Inconsistent naming between similar components forces users to memorise two APIs.

### Step 3 — Apply the UUXPM anti-pattern filter

Before finalising, check against these common mistakes:

| Anti-pattern | Instead |
|---|---|
| Color-named variants (`red`, `blue`) | Semantic names (`error`, `primary`) |
| Appearance variants (`rounded`, `flat`) | Use CSS or modifier, not variant |
| Too many variants (>8) | Split the component or use modifiers |
| Duplicate semantics (`caution` + `warning`) | Pick one, document the alias |
| No default/fallback as first entry | Reorder so safest is first |

### Step 4 — Produce the registry entries

```python
# validation.py
VARIANT_REGISTRY = {
    ...
    "<name>": ("<default>", "<v2>", "<v3>"),
}

# Only add if the component has meaningful size differences
SIZE_REGISTRY = {
    ...
    "<name>": ("", "sm", "md", "lg"),
}
```

### Step 5 — Fill the State × Variant table

| State | default | `<v2>` | `<v3>` |
|-------|---------|--------|--------|
| Default | | | |
| Hover | | | |
| Active | | | |
| Disabled | opacity 50%, no pointer-events | same | same |
| Focus-visible | `--chirpui-focus-ring` outline | same | same |

---

## Output Format

```markdown
## Variant Design: <component>

### Context
<product type and purpose summary>

### Recommended variant set

| Variant | Semantic meaning | CSS modifier |
|---------|-----------------|--------------|
| (first) | fallback / neutral | chirpui-<name> |
| ... | ... | chirpui-<name>--... |

### Rationale
<why this set, what was considered and rejected>

### Registry entries

```python
"<name>": ("<default>", ...),
```

### State × Variant table
| State | default | ... |
|-------|---------|-----|
| Default | | |
| Hover | | |
| Disabled | opacity 50% | same |
| Focus-visible | focus-ring token | same |
```

---

## DORI Lifecycle

- `dori_begin(skill="chirpui-variant-design")`
- `dori_complete(files_reviewed="src/chirp_ui/validation.py", notes="...")`
