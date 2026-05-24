# Screen Entry Template

Status: recipe template
Date: 2026-05-23

Use this template when adding or upgrading a screen catalog entry. Screen
entries describe a complete product situation. They do not define public
macros, manifest fields, generated artifacts, or utility classes.

```markdown
# Screen: <Name>

Status: <planned recipe target | golden screen fixture>
Profile: `<atlas | sage | ember | signal candidate>`
Fixture route: `<route or not yet fixture-backed>`
Source template: `<source path or not yet fixture-backed>`
Proof: `<test path list or not yet fixture-backed>`

## Use When

Use this screen when a product needs:

- <job>,
- <job>,
- <job>.

Good fits include <specific product situations>.

## Do Not Use When

Do not use this screen for <near misses>. Use <other archetype> instead.

## Composition Map

| Job | Current Surface |
|---|---|
| Profile | `<profile>` token mood through screen metadata. |
| Shell | <app/site/workspace/flow shell ownership>. |
| Command or action surface | <components/primitives>. |
| Main content | <components/primitives>. |
| Secondary content | <components/primitives>. |
| State coverage | <components/primitives>. |

## Typography Role Map

Use the recipe-only role names from
`docs/decisions/typography-role-matrix.md`. These names do not authorize public
tokens or utility classes.

| Role | Screen Surface | Intent |
|---|---|---|
| `<role>` | <surface> | <why this type treatment exists>. |

## Data Shape

The fixture or recipe expects records with:

- <field>,
- <field>,
- <field>.

Use realistic long labels, mixed states, and enough metadata to prove the
screen is not decorative.

## Required States

- Populated state.
- Loading or pending state.
- Empty state.
- Warning or degraded state.
- Error or invalid state when the workflow can fail.
- Selected or focused state when the screen compares objects.

## Agent Guidance

When the user asks for <intent>, start from this screen before assembling
individual components.

Prefer this screen over <nearby archetype> when <decision rule>.

Use the `<profile>` profile unless <override rule>.

Do not invent utility classes for spacing, width, typography, or alignment.
Record repeated local CSS pressure as an extraction candidate instead.

## Proof Checklist

- Server route renders and exposes `data-screen-archetype="<slug>"` when
  fixture-backed.
- Browser proof covers 320, 390, 768, and 1280 widths with no document
  horizontal overflow when fixture-backed.
- Realistic data covers long labels and mixed state.
- Existing route or pattern remains available for baseline comparison.

## Extraction Candidates

Track, but do not promote yet:

- `<candidate>`

These need repeated independent screen evidence before public API work.
```

## Authoring Rules

- Keep the entry in product-situation language.
- Prefer existing macros, slots, primitives, and documented recipes over raw
  classes.
- Cite source templates and proof only when they exist.
- Label planned entries as planned recipe targets, not golden fixtures.
- Link promotion pressure to [promotion-ledger.md](promotion-ledger.md).
- Stop and ask before adding public vocabulary, macro signatures, token names,
  theme packs, manifest/schema data, or generated artifacts.
