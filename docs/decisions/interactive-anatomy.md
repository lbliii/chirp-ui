# DESIGN: Interactive Anatomy Contracts

**Status:** accepted Sprint 5 contract, metadata projection deferred
**Created:** 2026-05-11
**Purpose:** document interactive components only after their rendered contracts are executable.

## Decision

Interactive anatomy is a contract over rendered HTML, runtime assets, and
behavior. It must not be prose-only. Anatomy docs and LLM endpoints may publish
only what unit and browser tests verify.

Sprint 5 shipped anatomy as durable docs plus tests, not descriptor or manifest
metadata. Registry-projected anatomy remains deferred until a later schema
design proves stable field names, migration behavior, and downstream consumers.

## Initial Families

- Modal/dialog and confirm dialog.
- Dropdown/menu/split button.
- Tabs and route tabs.
- Drawer/tray.
- Bengal theme controls: theme popover, search modal, mobile nav, tab/TOC enhancements.

## Anatomy Fields

Each documented family should identify:

- macro names
- required slots or child macros
- owned classes
- required ids and relationships
- ARIA roles and attributes
- state attributes
- HTMX behavior, including boost/select/disinherit rules
- Alpine factory or native browser API
- keyboard behavior
- focus entry and focus return
- reduced-motion or responsive constraints where relevant

If these fields become agent-facing, they should be projected from descriptor or
adjacent registry metadata rather than copied into endpoint prose.

## Resolved Pre-Doc Blocker

Dropdown menu item payloads previously interpolated values into Alpine event
expressions. Sprint 5 resolved this by moving payload assembly to
`chirpuiDropdown().selectItem()` and reading escaped DOM `data-*` attributes.
Future menu-family work must keep one of these approaches:

- `data-*` payloads read by named Alpine code, or
- a proven JS-string-safe escaping filter with tests.

HTML attribute escaping alone is not a JavaScript string escaping contract.

## Tabs Distinction

Route tabs and navigation tabs are not always WAI-ARIA tablists. Anatomy docs
must distinguish:

- route/navigation semantics
- true tablist/panel semantics
- Alpine-controlled panel visibility
- HTMX-swapped route content

## Bengal Theme Distinction

The packaged Bengal theme has static-first behavior hooks and storage keys that
are not the same as Chirp app component macros. Anatomy docs must identify
which Bengal selectors, data attributes, local storage keys, and assets are:

- stable package contracts
- transitional aliases
- docs-site-only implementation details

## Required Proof

- Unit render tests for structure, roles, ids, and attributes.
- Browser tests for opening, closing, keyboard navigation, focus return, and Alpine lifecycle.
- HTMX fragment tests where applicable.
- Bengal theme smoke coverage outside docs-site-only context.
- Manifest/runtime requirement tests if anatomy metadata is projected.

## Evidence Ledger

Use this ledger for complex interactive, shell-adjacent, or promotion-sensitive
surfaces. It is a docs/tests contract, not descriptor or manifest metadata.

| Field | Required answer |
| --- | --- |
| Surface | Component, recipe, theme hook, or shell region being evaluated. |
| Label | `stable`, `experimental`, `recipe-only`, `compatibility`, or `research`, matching [PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md). |
| Anatomy | Owned parts, slots, ids, classes, state attributes, and parent/child relationships. |
| Native semantics | Native element, role, name, state, and ARIA contract; prefer native HTML before ARIA. |
| Keyboard | Keyboard entry, activation, navigation, Escape/close behavior, and disabled-state behavior when relevant. |
| Focus | Initial focus, visible focus, focus containment, focus return, and HTMX/Alpine remount behavior when relevant. |
| Runtime | Required browser API, HTMX contract, Alpine factory, CSS feature, or no-JS fallback. |
| Motion | Reduced-motion handling and transition-token use when animation exists. |
| Responsive and overflow | Stress widths, local overflow owner, wrapping/truncation behavior, and no document-level horizontal overflow when relevant. |
| Security and escaping | Attribute/data trust boundary, `Markup`/`safe` use, raw HTML allowance, and escaping tests when inputs render into HTML or JS-adjacent data. |
| Performance | Expensive selectors, layout/scroll listeners, observers, asset loading, and page-global behavior risks. |
| Proof | Render tests, browser tests, JS tests, static showcase, visual audit, Bengal package tests, or explicit no-impact reason. |
| Residual risk | Known manual-testing gaps, browser gaps, assistive-technology caveats, or deferred evidence. |

For small static display components, the ledger can be a short note in the
promotion row. For interactive components, shell regions, page actions, Bengal
theme hooks, and dense reference surfaces, use the full ledger before changing
public maturity, preferred authoring status, macro signatures, descriptor
fields, runtime requirements, or generated docs.

Do not claim screen-reader or assistive-technology proof unless it was manually
verified and the environment is named. Automated render/browser proof can cover
semantics, focus movement, and keyboard events, but it is not a substitute for
manual AT verification.

## Projection Decision

Descriptor and manifest anatomy metadata is intentionally not part of the
current shipped contract. The docs now cite executable proof for each family,
and the manifest stays focused on registry-owned component facts.

A future projection can reopen this only with:

- a concrete consumer for machine-readable anatomy
- explicit manifest schema migration notes
- parity tests between descriptors, docs, templates, browser behavior, and any
  generated endpoint that publishes the metadata
- a policy for Bengal theme hooks, which are packaged theme contracts rather
  than Chirp UI component registry contracts

## Stop-And-Ask Items

- Adding anatomy metadata to descriptors or manifest.
- Changing Alpine lifecycle, storage keys, or runtime requirements.
- Publishing anatomy for an untested interactive family.
- Adding behavior dependencies.

## Non-Goals

- A framework-component state model.
- Prose-only accessibility promises.
- Inline scripts in macros.
