# Page Actions AI Reference Brief

Status: reference implementation brief
Date: 2026-05-23
Candidate: page actions primitive

## Scenario

Build a non-Bengal AI/reference page that needs title-adjacent page commands:
copy canonical URL, open LLM text, copy known prompt text, and open an external
assistant handoff. The page should feel like a product documentation/reference
surface, not a marketing page or social sharing example.

## Existing Primitives To Try

- `page_header` actions
- `page_hero` actions
- `dropdown_menu`
- `share_menu`
- `action_bar`
- `copy_button`

## Required Proof

- Render proof for title, subtitle, metadata, action trigger, share menu,
  dropdown commands, and copy controls.
- Browser proof at 320, 390, 768, and 1024 widths.
- Long command labels stay contained without document-level horizontal
  overflow.
- Copy feedback works for known text.
- External assistant links use safe external-link attributes.
- No Bengal `.chirp-theme-*` selectors are used.

## Gap To Record

Record a gap only if current primitives cannot express the scenario without
repeated app-owned glue around:

- canonical page URL ownership,
- open/copy LLM text,
- external AI handoff,
- grouped non-social page commands,
- copy/fetch status feedback,
- title-adjacent responsive containment.

## Promotion Boundary

This brief does not authorize `page_actions()`, copy/fetch runtime helpers,
descriptor changes, emitted classes, CSS, manifest updates, generated component
options, or docs that teach a public page-actions API.

## Decision Rule

- If existing primitives cover the scenario, keep page actions recipe-only.
- If the same gap repeats in another independent reference implementation,
  stop and ask for a public API/design plan.
