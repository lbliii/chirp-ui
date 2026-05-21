# Workspace Shell Proof

Status: promotion proof
Date: 2026-05-21

The larger layout-affinity rollout is worth continuing only if it reduces
page-owned shell code while improving dense workspace defaults. The current
proof compares the operations baseline route with the same-data
`/operations-shell-workspace` route.

## Compared Surfaces

| Surface | Shell Owner | Inner Owner | Route |
|---|---|---|---|
| Operations baseline | page-owned `frame` + example grid | page-owned rail/card/inspector classes | `/operations-shell` |
| Operations workspace variant | `workspace_shell` | `filter_rail`, `metric_strip`, `result_collection`, `result_card`, `inspector_panel` | `/operations-shell-workspace` |
| Support workspace | `workspace_shell` | page-owned inner ticket/card classes | `/support-shell` |

## Proof Points

- The same operations data renders through both `/operations-shell` and
  `/operations-shell-workspace`.
- The workspace variant no longer uses the baseline page-owned shell class
  `ops-shell-workspace`.
- The workspace variant replaces page-owned rail/result/inspector shapes with
  registry-cited primitives.
- Browser tests cover no horizontal overflow at phone, tablet, and desktop
  widths.
- HTMX tests cover reactive search updates inside the workspace boundary.

## Promotion Decision

Promote `workspace_shell` plus the dense workspace primitives as the preferred
path for new serious app workspaces. Keep `/operations-shell` as the comparison
baseline until at least one more existing shell migrates to the dense primitives.

Do not promote layout-affinity fields into the manifest yet. The importable
`chirp_ui.layout_affinity` vocabulary is enough for tests and agents while the
schema remains stable.

## Next Migration Candidates

- Convert `/support-shell` inner ticket/rail/inspector shapes to dense
  workspace primitives.
- Convert the catalog shell rails/results only after deciding whether layered
  two-rail catalog navigation needs a specialized rail composition.
- Add a visual audit page that shows baseline, workspace shell, and dense
  primitive variants side by side.
