# Static Showcase Legacy Helper Triage

**Status**: active inventory
**Updated**: 2026-05-12
**Scope**: `examples/static-showcase/index.html`

This report keeps the broad static catalog useful without letting it become the
source of truth for legacy helper authoring. The dynamic component showcase and
visual audit page remain the preferred proof surfaces for new design-system
behavior.

## Current Usage

After the page-chrome cleanup, the static showcase has 102 legacy helper class
uses, all of them `chirpui-visually-hidden`.

| Helper | Count | Classification | Decision |
|--------|-------|----------------|----------|
| `chirpui-visually-hidden` | 102 | component contract | Keep. These are native inputs inside segmented controls, toggles, ASCII controls, checkboxes, radios, tile buttons, knobs, and settings-row examples. |

## Cleaned Page Chrome

The following static-page styling has been moved to local `sc-*` classes:

- Header note copy.
- Label-overline explanatory copy.
- Safe region explanatory copy.
- Entity header meta examples.
- Settings-row labels and monospace detail examples.

## Follow-Up Rules

- Keep `chirpui-visually-hidden` where the component example needs a real native
  input and the component CSS expects the helper.
- Do not introduce typography or spacing helpers for static-page chrome.
- If a future static example needs a compatibility helper for demonstration, add
  a short note in this report that classifies it as `legacy example`.
- If `visually-hidden` becomes component-native later, update the count and
  migrate examples in the same PR.

## Verification

- `uv run pytest tests/test_static_showcase_legacy_helper_triage.py -q`
- `uv run poe check`
