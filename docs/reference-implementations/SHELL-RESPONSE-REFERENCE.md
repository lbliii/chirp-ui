# Shell Response Reference Brief

Status: reference implementation brief
Date: 2026-05-23
Candidate: shell response/OOB helper

## Scenario

Build a third hand-written route family outside `mount_pages()` that includes
persistent shell navigation, route-tab page roots, local fragment islands, and
route-scoped shell actions. The reference must prove response-shape ownership
for full-page, shell-targeted, page-root, and local fragment requests.

## Existing Primitives And Recipes To Try

- documented `HX-Target` branching from `SHELL-TABS-CONTRACT.md`
- `shell_outlet_attrs`
- `route_tabs`
- `fragment_island`
- `safe_region`
- shell actions OOB replacement
- filesystem `mount_pages()` as the preferred higher-level comparison path

## Required Proof

- No `HX-Request` returns the full page response.
- `HX-Request` without `HX-Target` does not infer a page-root fragment.
- `HX-Target: main` returns shell-owned content and shell-actions OOB when
  actions change.
- `HX-Target: page-root` returns only page-root chrome/content.
- Local fragment targets return local content without inheriting shell
  selectors.
- Browser proof confirms singleton `#main`, `#page-content`, and `#page-root`.

## Gap To Record

Record a gap only if hand-written route families repeat boilerplate around:

- request target classification,
- OOB shell action inclusion,
- full-page versus page-root response selection,
- local fragment selector clearing,
- parity with filesystem-mounted page contracts.

## Promotion Boundary

This brief does not authorize a public `chirp_ui` helper, Chirp routing API,
visual shell macro, component descriptor, emitted classes, CSS, manifest
updates, generated component options, or a new HTMX protocol.

## Decision Rule

- If the route family remains clear with local helpers, keep the pattern
  documented.
- If three independent hand-written route families repeat the same boilerplate,
  stop and ask whether the owner is Chirp routing, Chirp UI, or app-local recipe
  code.
