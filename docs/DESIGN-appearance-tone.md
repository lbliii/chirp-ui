# DESIGN: Appearance And Tone

**Status:** decided for Sprint 2 pilot
**Created:** 2026-05-11
**Purpose:** translate Skeleton-style presets into Chirp-native macro and registry vocabulary.

## Decision

Chirp UI will model cross-component visual treatment with two descriptor-backed
axes:

- `appearance`: how a component is rendered.
- `tone`: what semantic intent or palette role it carries.

These axes are public macro parameters only where a component opts into them.
They are not utility classes, not free-form strings, and not aliases for
Skeleton class names.

## Candidate Vocabulary

Initial `appearance` values:

- `filled`
- `tonal`
- `outlined`
- `ghost`

Initial shared `tone` values:

- `neutral`
- `primary`
- `secondary`
- `success`
- `warning`
- `danger`
- `info`
- `surface`

`danger` is the shared destructive/action tone. `error` is not a shared tone.
Existing components that already expose `error` keep it as component-local
legacy compatibility until a migration is designed. New shared tone vocabulary
must not add both `danger` and `error`.

Current `error` compatibility inventory:

| Component | Existing surface | Sprint 2 policy |
|---|---|---|
| `alert` | `variant="error"` | Keep legacy variant; new shared tone uses `danger` only if `alert` joins the tone pilot. |
| `badge` | `variant="error"` | Keep legacy variant; do not add shared `tone="error"`. |
| `toast` | `variant="error"` | Out of Sprint 2 pilot unless selected later; keep legacy variant. |
| `status_indicator` | `variant="error"` | Keep legacy variant; do not add shared `tone="error"`. |
| `notification_dot` | `variant="error"` | Out of Sprint 2 pilot unless selected later; keep legacy variant. |
| `streaming_bubble` | `variant="error"` | Out of Sprint 2 pilot unless selected later; keep legacy variant. |

`aura(tone=...)` is an existing effect-local parameter with non-shared values.
It is not part of the shared semantic tone vocabulary until explicitly migrated.

## Registry Shape

Chosen descriptor shape for the Sprint 2 pilot:

```python
ComponentDescriptor(
    block="btn",
    appearances=("filled", "tonal", "outlined", "ghost"),
    tones=("neutral", "primary", "secondary", "success", "warning", "danger"),
)
```

Do not add a generic descriptor-axis model for the pilot. Reconsider generic
axes only after at least a third repeated axis proves the abstraction, and even
then keep stable manifest field names for public concepts.

## Rendering Contract

Macros validate `appearance` and `tone` through descriptor-derived registries.
Invalid values warn in strict mode and fall back to the component default.

Rendering maps to component-owned BEM modifiers and token aliases:

```html
<button class="chirpui-btn chirpui-btn--filled chirpui-btn--primary">
```

This is acceptable because the classes are owned by `btn`. These are not
acceptable:

```html
<button class="chirpui-appearance-filled chirpui-tone-primary">
<button class="preset-filled-primary">
```

No global `chirpui-tone-*`, `chirpui-preset-*`, spacing, color, or utility-like
class vocabulary is allowed.

`appearances` and `tones` must be first-class descriptor-owned emits. Normal
axis classes must be derived by `ComponentDescriptor.emits` as
`chirpui-{block}--{value}`, not hidden in `extra_emits`.

Legacy `variant` values may collide with new axis class names during migration
because both use component-owned BEM modifiers. Each pilot component must include
a variant-to-axis compatibility table before changing preferred examples.

New `tone="danger"` CSS should use `--chirpui-danger` token hooks. Existing
legacy `error` variants may continue to use `--chirpui-error` or
component-specific error aliases.

## Validation Contract

Implementation should add public validation/filter entry points:

- `validate_appearance_block()`
- `validate_tone_block()`

A private generic helper may share implementation behind those names.

The helper must use the same warning style as variant and size validation, with
messages that name the component, invalid value, allowed values, and fallback.

## Manifest Contract

If the axes ship publicly, bump the manifest schema and project the fields:

```json
{
  "components": {
    "btn": {
      "appearances": ["filled", "tonal", "outlined", "ghost"],
      "tones": ["neutral", "primary", "secondary", "success", "warning", "danger"]
    }
  }
}
```

Generated component options should include these fields beside variants and
sizes.

## Pilot Components

Current Sprint 2 pilot:

- `btn`
- `badge`
- `alert`
- `card`
- `surface`
- `field` / `text_field`

Do not add the axes to all components in one sweep.

## Required Proof

- Manifest schema and determinism tests.
- Validation tests for strict and non-strict invalid values.
- Template rendering tests for default and non-default axes.
- Registry emits parity and template/CSS contract tests.
- Dynamic showcase matrix with copyable macro examples.
- Generated `COMPONENT-OPTIONS.md` refresh.

## Stop-And-Ask Items

- Changing or expanding the shared `appearance` or `tone` vocabulary.
- Making `error` a shared tone instead of component-local compatibility.
- Removing an existing legacy `variant="error"` without a migration path.
- Removing or repurposing existing `variant` values.
- Adding descriptor fields or manifest schema fields.

## Non-Goals

- Tailwind/Skeleton class compatibility.
- Utility classes.
- Free-form theme color strings.
- Global preset classes.
