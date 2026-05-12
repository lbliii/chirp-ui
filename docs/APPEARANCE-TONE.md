# Appearance And Tone

`appearance` and `tone` are descriptor-backed macro parameters for components
that opt into the visual preset pilot.

- `appearance` describes treatment: `filled`, `tonal`, `outlined`, `ghost`.
- `tone` describes semantic intent: `neutral`, `primary`, `secondary`,
  `success`, `warning`, `danger`, `info`, `surface`, depending on component.

They are not utility classes and should be passed as macro params:

```html
{{ btn("Delete", appearance="outlined", tone="danger") }}
{{ badge("At risk", appearance="tonal", tone="warning") }}
{% call card(title="Review", appearance="outlined", tone="danger") %}...{% end %}
{% call surface(appearance="outlined", tone="primary") %}...{% end %}
```

Do not write global tone or preset classes by hand:

```html
<!-- Avoid -->
<button class="chirpui-tone-danger chirpui-appearance-outlined">
```

## Pilot Components

The first public pilot covers:

| Component | Appearances | Tones |
|---|---|---|
| `btn` | `filled`, `tonal`, `outlined`, `ghost` | `neutral`, `primary`, `secondary`, `success`, `warning`, `danger` |
| `badge` | `filled`, `tonal`, `outlined` | `neutral`, `primary`, `success`, `warning`, `danger`, `info` |
| `alert` | `filled`, `tonal`, `outlined` | `info`, `success`, `warning`, `danger` |
| `card` | `filled`, `tonal`, `outlined`, `ghost` | `neutral`, `primary`, `secondary`, `success`, `warning`, `danger`, `info` |
| `surface` | `filled`, `tonal`, `outlined`, `ghost` | `surface`, `neutral`, `primary`, `secondary`, `success`, `warning`, `danger`, `info` |
| `field` / `text_field` | `filled`, `tonal`, `outlined`, `ghost` | `neutral`, `primary`, `success`, `warning`, `danger`, `info` |

## Migration Map

Legacy `variant` values keep working. New examples should prefer
`appearance`/`tone` when the value clearly belongs to one of those axes.

| Component | Old form | Preferred form | Status |
|---|---|---|---|
| `btn` | `variant="primary"` | `tone="primary"` or keep variant during migration | Compatible |
| `btn` | `variant="secondary"` | `tone="secondary"` | Compatible |
| `btn` | `variant="ghost"` | `appearance="ghost"` | Compatible |
| `btn` | `variant="danger"` | `tone="danger"` | Compatible |
| `btn` | `variant="success"` | `tone="success"` | Compatible |
| `btn` | `variant="warning"` | `tone="warning"` | Compatible |
| `card` | `variant="glass"` | Keep variant for glass treatment; use `appearance`/`tone` for preset surface intent | Compatible |
| `badge` | `variant="error"` | Keep `variant="error"` until component migration; do not use `tone="error"` | Legacy compatibility |
| `alert` | `variant="error"` | Keep `variant="error"` until component migration; use `tone="danger"` for new destructive tone demos | Legacy compatibility |
| `field` | `variant/state="error"` | Keep validation error state; use `tone="danger"` only for intentional non-error emphasis | State, not tone |

`danger` is the shared destructive/action tone. `error` is not a shared tone.
Existing `variant="error"` values remain component-local compatibility where
already shipped.

## Validation

Invalid `appearance` and `tone` values warn in normal mode and raise in strict
mode, using the same validation path as variants and sizes. Invalid values do
not emit classes.
