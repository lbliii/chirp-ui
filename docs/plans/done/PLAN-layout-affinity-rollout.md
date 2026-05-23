# PLAN: Layout Affinity Rollout

Status: shipped
Date: 2026-05-21

## Status Block

- Prototype recipe attributes.
- Not yet descriptor API.
- Not yet manifest contract.
- Allowed only where documented parent resolvers consume them.

Layout affinity gives Chirp UI recipes and primitives a small, inspectable
layout-intent vocabulary: `data-chirpui-role`, `data-chirpui-pressure`, and
`data-chirpui-affinity`. The contract stays recipe-first until resolver
behavior, docs, tests, and steward review justify a manifest schema bump.

## Scope

This plan owns the rollout from HTML/CSS prototype to potential
`chirpui-manifest@6` projection. It does not add public macro parameters,
descriptor fields, or manifest keys until those changes are explicitly
accepted.

## Current Proven Consumers

| Resolver | Surface | Roles | Required Proof |
|---|---|---|---|
| `command_bar` | Catalog shell command surface | `search`, `hints`, `status` | Render tests, CSS resolver test, browser no-overflow proof |
| `filter_bar` | Data filter toolbar | `search`, `filters`, `actions` | Render tests, CSS resolver test, browser no-overflow proof |
| `card` | Card header and metadata chrome | `content`, `actions`, `metadata` | Render tests, scoped CSS test, browser no-overflow proof |
| `frame` | Rail/content/nav shell prototype | `rail`, `content`, `nav` | Render tests, CSS resolver test, browser no-overflow proof |
| `workspace_shell` | Support queue payoff shell | `rail`, `nav`, `content`, `actions` | Render tests, scoped CSS test, browser no-overflow proof |
| `cluster` / `stack` | Micro-resolver prototype, not promotion-ready | `content`, `metadata`, `actions` | Source vocabulary scan and browser no-overflow proof only |

## Next 10 Tasks

1. Keep this dedicated rollout plan discoverable from `docs/INDEX.md` and the
   layout-affinity RFC.
2. Record steward notes for schema promotion before changing
   `ComponentDescriptor` or `chirpui-manifest@5`.
3. Maintain a shared test-only vocabulary helper for allowed emitted source
   values.
4. Maintain a resolver coverage matrix that maps resolver to docs, CSS, and
   browser proof.
5. Prove a rail/content/nav shell prototype with `frame`.
6. Prove a small `cluster` / `stack` micro-resolver without adding utility
   class vocabulary, or keep it out of the manifest promotion set.
7. Keep an agent-facing authoring section with both good examples and
   forbidden anti-examples.
8. Draft the `chirpui-manifest@6` migration before any schema change.
9. Keep test-only descriptor fixtures for `layout_resolver` and `layout_parts`
   until the production descriptor shape is accepted.
10. Run browser responsive proof across catalog shell, data toolbar, cards, and
    layout primitive prototypes.

## Steward Notes

Standing steward guidance applied:

- Core Registry/API: do not add descriptor fields or manifest keys without a
  schema bump, generated `manifest.json`, migration notes, and tests.
- Template/CSS/Behavior: resolver behavior must stay parent-scoped; avoid a
  global rule that changes arbitrary descendants.
- Examples/Showcase: prototypes should be copyable and dummy-data based, not
  vendor-specific.
- Documentation/Published Site: docs must distinguish prototype HTML
  attributes from stable public macro API.
- Tests: every accepted behavior needs render/CSS/browser proof or an explicit
  no-impact note.

Deferred steward items:

- Production `LayoutResolver` / `LayoutPart` descriptor fields.
- `chirpui-manifest@6` schema bump.
- Public macro parameters for affinity values.

## Manifest@6 Migration Plan

Proposed production work, gated:

1. Add frozen descriptor-side types for `layout_resolver` and `layout_parts`.
2. Validate role, pressure, and affinity values against the documented
   vocabulary.
3. Project `layout_resolver` and `layout_parts` from descriptors in
   `manifest.py`.
4. Bump the manifest schema to `chirpui-manifest@6`.
5. Regenerate `src/chirp_ui/manifest.json`.
6. Update `docs/COMPONENT-OPTIONS.md`, docs/site content, changelog, and
   migration notes.
7. Add deterministic manifest tests and backward compatibility guidance for
   `chirpui-manifest@5` consumers.

## Parity Matrix

| Contract | API/CLI | Programmatic | Protocol | Schema/Types | Docs | Examples | Tests |
|---|---|---|---|---|---|---|---|
| Recipe attributes | no public API | rendered HTML only | HTML attrs | none | RFC + recipes | catalog/data/layout/cards | source scan + browser |
| Parent resolvers | none | CSS behavior | parent-scoped CSS | none | RFC matrix | command/filter/frame/cluster/stack | CSS + browser |
| Component parts | none | internal DOM | scoped CSS | none | RFC examples | cards/resource cards | render + browser |
| Manifest projection | not shipped | not shipped | not shipped | planned `@6` | migration plan | no production examples yet | test-only fixture |

## Required Proof

- `tests/docs_contracts/test_layout_affinity_docs.py`
- `tests/test_layout_affinity_descriptor_fixture.py`
- focused render/CSS tests in `tests/test_components.py`
- browser no-overflow proof in `tests/browser/test_catalog_shell_recipe.py`
- generated CSS check after CSS partial changes
- CSS selector-boundary tests that reject broad descendant
  `[data-chirpui-*]` resolver selectors.
- Browser proof for local resolver overflow, containment, and interaction where
  HTMX is part of the surface.
