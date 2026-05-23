# Layout Affinity Resolver Authoring

Status: prototype authoring guide
Date: 2026-05-21
Canonical contract: [DESIGN-layout-affinity.md](DESIGN-layout-affinity.md)
Rollout plan: [PLAN-layout-affinity-rollout.md](plans/done/PLAN-layout-affinity-rollout.md)

## Status Block

- Prototype recipe attributes.
- Not yet descriptor API.
- Not yet manifest contract.
- Allowed only where documented parent resolvers consume them.

This guide explains how to add or change a layout-affinity resolver without
turning `data-chirpui-role`, `data-chirpui-pressure`, and
`data-chirpui-affinity` into utility classes. It is written for maintainers and
agentic developers editing Chirp UI itself.

## Resolver Rule

A layout-affinity resolver is a parent-owned contract. Children may declare
intent; the parent decides whether and how to resolve it.

The parent must name one of these shapes:

- `layout_resolver`: a parent primitive or component consumes intent from a
  bounded set of children.
- `layout_parts`: a component emits and resolves its own internal parts.

Those names are design targets only. They are not descriptor fields, macro
parameters, manifest keys, or public Python API until a schema-bump plan lands;
in short, they are not descriptor fields, macro parameters, manifest keys, or
public Python API today.

## When To Add A Resolver

Add a resolver only when all of these are true:

- A repeated real surface has the same layout decision, such as search taking
  remaining width or actions staying compact.
- A single parent owns the decision at a clear boundary.
- The behavior can be expressed with documented role, pressure, and affinity
  tokens.
- The CSS can be scoped to direct children or named component-owned parts.
- Browser proof can demonstrate no horizontal overflow and stable containment.

Do not add a resolver for one-off spacing, raw x/y placement, margin tweaks,
visual styling, or generic `stack` / `cluster` child behavior.

## Authoring Steps

1. Pick the parent owner.
   Name the resolver in the source RFC and rollout plan before writing CSS.
   Use the macro or component name app authors already recognize, such as
   `command_bar`, `filter_bar`, `card`, or `frame`.

2. Pick the scope.
   Use `direct-children` for action-strip style parents and explicit
   component-owned part classes for internal component anatomy. Do not resolve
   arbitrary descendants.

3. Use only documented vocabulary.
   Source templates may emit only values listed in
   `tests/layout_affinity_contract.py`. New values require a docs update,
   source-scan coverage, resolver CSS, and browser proof.

4. Emit attributes at the ownership boundary.
   Recipe templates may mark children supplied to a documented parent resolver.
   Component macros may emit attributes on their own internal parts. Avoid
   asking app authors to wrap children in extra styling containers.

5. Write CSS in the owning partial.
   Edit the source partial under `src/chirp_ui/templates/css/partials/`, then
   regenerate `src/chirp_ui/templates/chirpui.css`. Never hand-edit generated
   CSS.

6. Prove selector boundaries.
   Add positive tests for the resolver selectors and negative tests that reject
   broad descendant selectors.

7. Prove browser behavior.
   Add or update Playwright coverage for stress phone, phone, tablet, and
   desktop widths when the behavior depends on actual layout.

8. Publish collateral.
   Update the RFC, site bridge, source map, examples, and recipe docs that teach
   the resolver. Keep status language visible before examples.

## Selector Contract

Good selectors start from the owning parent and stop at the owned boundary:

```css
:where(.chirpui-command-bar, .chirpui-filter-bar)
    .chirpui-action-strip__inner
    > [data-chirpui-pressure~="flex"] {
    min-inline-size: 0;
}

.chirpui-card__header-actions[data-chirpui-affinity~="end"] {
    margin-inline-start: auto;
}
```

Bad selectors make every descendant look eligible:

```css
/* Do not resolve arbitrary descendants. */
.chirpui-command-bar [data-chirpui-pressure~="flex"] {}
.chirpui-card :scope [data-chirpui-pressure~="compress"] {}
.chirpui-stack > [data-chirpui-affinity~="fill"] {}
```

The bad patterns either leak into slotted content, affect nested components, or
turn low-level primitives into utility-class containers.

## Current Resolver Matrix

| Resolver | Scope | CSS owner | Required browser proof |
|---|---|---|---|
| `command_bar` | direct children of `.chirpui-action-strip__inner` | `014_action-containers.css` | catalog shell command surface |
| `filter_bar` | direct children of `.chirpui-action-strip__inner` | `014_action-containers.css` | data filter toolbar |
| `card` | component-owned header, badge, metadata, and footer parts | `045_card.css` | cards showcase |
| `frame` | direct rail/nav/content children | `004_layout.css` | layout affinity showcase |
| `workspace_shell` | component-owned sidebar/content/inspector parts | `005_workbench.css` | support shell payoff page |

`stack` and `cluster` are intentionally absent from this matrix. They can host
copyable prototype markup, but they do not resolve generic child pressure or
affinity.

## Required Proof

Every accepted resolver change needs focused proof:

- `tests/docs_contracts/test_layout_affinity_docs.py` keeps vocabulary, status, and resolver
  documentation aligned.
- CSS contract tests assert the intended parent-scoped selectors and reject
  broad descendant selectors.
- Browser tests assert document-level no-overflow, local resolver no-overflow,
  and immediate-child containment where the parent owns placement.
- Manifest tests continue to prove no `layout_resolver`, `layout_parts`, or
  generic `layout_affinity` projection leaks into the current manifest schema.

If the resolver changes user-facing recipes, update the relevant docs and site
bridge in the same change.

## Promotion Boundary

Promotion to descriptor fields or `chirpui-manifest@6` is a separate public API
change. It requires steward review, schema migration notes, generated manifest
updates, generated docs, examples, and tests that prove no component
under-reports resolver parts.

Until then, layout affinity remains an HTML/CSS prototype contract.
