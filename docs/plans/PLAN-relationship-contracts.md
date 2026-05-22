# PLAN: Relationship Contracts Rollout

Status: in-flight
Date: 2026-05-21

## Status Block

- Reference contract: [RELATIONSHIP-CONTRACTS.md](../RELATIONSHIP-CONTRACTS.md)
- No new public macro parameters.
- No manifest schema change.
- CSS changes must stay owner-scoped and token-based.

This plan tracks the pass from isolated component styling to explicit
relationship ownership across ChirpUI primitives and components.

## Goal

Fresh app screens should not need bespoke spacing repairs for ordinary
composition. The parent primitive or component should own the relationship:
inset, sibling rhythm, attachment, grouping, separation, region placement,
responsive pressure, or local overflow.

## What We Learned

- Spacing failures repeated across catalog, operations, support, cards, layout,
  and forms.
- The durable fix is parent ownership, not page-local patching.
- Standalone compatibility can coexist with parent ownership: keep child
  margins for simple standalone use, trim them inside an owning parent.
- Browser proof matters because many relationship bugs are computed layout
  failures, not template failures.

## Current Accepted Slices

| Slice | Commit Theme | Contract |
|---|---|---|
| Workspace rhythm | workspace primitives | attached/group/stack/separated/inset rhythm tokens |
| Support shell inset | workspace shell | rail/content/inspector placement and inset rhythm |
| Framed content | card/surface/panel/callout | direct child margin trimming and internal flow |
| Action rows | command/filter/action strip | search/hints/actions wrapping and direct child rhythm |
| Stack/cluster | layout primitives | direct child margin trimming under primitive gap |
| Forms | form macro CSS | field/action/error-summary rhythm under form gap |
| Fieldsets | form field CSS | grouped form-control rhythm and child margin trimming |
| Headers | page/section/entity header CSS | title/meta attachment, action wrapping, long-title pressure |
| Search browse | search_header/resource_index CSS | search/header/filter/results rhythm and result feedback placement |
| Overlay regions | modal/drawer/tray/panel CSS | header/body/footer rhythm, margin trim, local long-token containment |
| Form internals | form field CSS | checkbox/radio/range/input-group/search-bar attachment and pressure |
| List and media rows | list/media/resource/workspace CSS | row separation, leading media/body/actions pressure, result card footer/body rhythm |

## Next 10 Tasks

1. Audit params-table, signature, DnD, sortable, and table row-action
   relationships.
2. Add relationship-specific browser probes for high-risk surfaces instead of
   only document overflow probes.
3. Remove first-party `chirpui-mt-*` / `chirpui-mb-*` usage when a component
   owner now exists.
4. Promote repeated accepted contracts into `docs/RELATIONSHIP-CONTRACTS.md`
   and keep `docs/INDEX.md` linked.
5. Defer descriptor or manifest projection until relationships repeat across
   enough owners to justify a public schema.
6. Mine `lbliii/emdashCSS` for parent-owned stack/spread/fit ideas, translating
   only the contract model into existing ChirpUI owners.
7. Keep checking first-party examples for relationship patches after each
   accepted owner lands.
8. Revisit specialized form controls such as star, thumbs, segmented, and file
   after common field internals prove stable.
9. Revisit overlay subvariants such as confirm and modal_overlay after native
   overlay regions prove stable.
10. Decide whether repeated pressure contracts deserve descriptor metadata or
   remain CSS/documentation-only.

## Parity Matrix

| Contract | API/CLI | Programmatic | Protocol | Schema/Types | Docs | Examples | Tests |
|---|---|---|---|---|---|---|---|
| Parent-owned rhythm | none | CSS behavior | rendered classes | none | relationship doc | forms/layout/support/catalog | unit + browser |
| Inset ownership | none | CSS behavior | component DOM | none | layout/primitive docs | cards/surfaces/workspaces | CSS + browser |
| Layout affinity | none | data attrs in HTML | HTML attrs | planned only | RFC + resolver guide | catalog/data/cards/workspaces | source scan + browser |
| Future manifest projection | not shipped | not shipped | not shipped | not shipped | not-now | none | manifest guard tests |

## Steward Notes

- Documentation steward: relationship guidance belongs in a canonical reference
  doc and must be linked from `docs/INDEX.md`.
- Planning steward: active rollout belongs in `docs/plans/` and should not
  imply a manifest or macro API change.
- Template/CSS steward: relationship fixes must edit source partials and
  regenerate CSS; no utility-class vocabulary.
- Test steward: browser proof is required for computed layout risks; unit CSS
  assertions are enough only for static selector ownership.
- Examples steward: first-party examples should stop teaching local margin
  patches once a component owns the relationship.

## Required Proof Per Slice

- Focused render or CSS tests naming the owner and relationship.
- Browser proof when the failure mode depends on computed layout, wrapping, or
  overflow.
- `uv run poe verify-generated` after generated CSS/docs changes.
- `uv run poe format-check`, relevant `ruff check`, and `git diff --check`.

## Not Now

- Public `relationship=` macro params.
- New descriptor fields.
- `chirpui-manifest@6` projection.
- Global `[data-chirpui-*]` relationship rules.
- New utility classes for margin, padding, flex, grid, or alignment.
