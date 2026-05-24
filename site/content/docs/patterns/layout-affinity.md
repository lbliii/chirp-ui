---
title: Layout Affinity
description: Prototype parent-scoped layout intent attributes for Chirp UI recipes
draft: false
weight: 16
lang: en
type: doc
keywords: [chirp-ui, layout, affinity, recipes, responsive, agents]
category: patterns
---

Layout affinity is a prototype recipe contract for describing layout intent with
HTML attributes. It helps dense pages stay readable across screen sizes without
turning Chirp UI into a utility-class vocabulary.

Use the canonical repository guide for the full contract:
[`docs/decisions/layout-affinity.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/decisions/layout-affinity.md?plain=1).
For resolver authoring rules, see
[`docs/patterns/layout-affinity-resolver-authoring.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/patterns/layout-affinity-resolver-authoring.md?plain=1).
For rollout status, see
[`docs/plans/done/PLAN-layout-affinity-rollout.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/plans/done/PLAN-layout-affinity-rollout.md?plain=1).

## Status Block

- Prototype recipe attributes.
- Not yet descriptor API.
- Not yet manifest contract.
- Allowed only where documented parent resolvers consume them.

## Source Of Truth

This page is a published bridge. The repository docs remain the contract for
the prototype vocabulary, parent-scoped resolver model, proof gates, and not-now
promotion questions:

- `docs/decisions/layout-affinity.md` owns the prototype contract.
- `docs/patterns/layout-affinity-resolver-authoring.md` owns maintainer rules for
  adding parent-scoped resolvers.
- `docs/plans/done/PLAN-layout-affinity-rollout.md` owns rollout tasks and deferred
  manifest promotion.
- `docs/patterns/search-shell-recipes.md` shows the search-shell consumer.
- `docs/fundamentals/primitives.md` keeps primitive composition guidance aligned.

Do not add a published-only layout-affinity API here. New descriptor fields,
manifest facts, macro parameters, or emitted classes must ship through the
registry, templates, generated CSS, generated component options, examples, and
tests.

## Current Shape

Layout affinity uses three recipe attributes:

- `data-chirpui-role` describes the element's job, such as `search`,
  `filters`, `hints`, `actions`, `status`, `metadata`, `rail`, or `content`.
- `data-chirpui-pressure` describes how the element behaves as space changes,
  such as `flex`, `compress`, or `rigid`.
- `data-chirpui-affinity` describes natural placement, such as `fill`, `end`,
  `start`, `block-start`, or `block-end`.

These values are tokens, not CSS dimensions. They are only meaningful when a
documented parent resolver consumes them.

## Parent-Scoped Resolvers

The prototype has two future contract shapes:

- `layout_resolver` for parents that consume child intent, such as command
  bars, filter bars, cards, and frames.
- `layout_parts` for component-owned internal parts, such as card header
  content, card actions, badges, metadata, and workspace shell
  sidebar/content/inspector parts.

Those names are design targets, not public schema today. They are intentionally
not part of the current manifest contract.

Resolver CSS must start from the owning parent and stop at the owned boundary:
direct children for command and filter bars, component-owned parts for cards
and `workspace_shell`, and explicit rail/content children for frames. Broad
descendant selectors are not part of the prototype contract.
Broad descendant selectors are rejected because they make unrelated descendants
react to recipe-only layout intent.

## Use This When

- A dense command surface needs search, filters, hints, status, and actions to
  wrap predictably.
- Card headers or metadata need stable internal sizing without app-local CSS.
- A frame recipe needs rails and content to avoid horizontal page overflow.
- A workbench-style shell needs sidebar, main content, and inspector placement
  without page-owned grid CSS.
- An agentic developer needs machine-readable layout intent instead of visual
  guesswork.

## Avoid

- Do not invent values such as `grow`, `left`, `right`, `primary`, or pixel-like
  values.
- Do not use the attributes as a generic styling escape hatch.
- Do not expect `stack` or `cluster` to resolve generic child pressure. Those
  primitive experiments are not promoted.
- Do not add manifest or descriptor fields without a schema-bump plan and
  steward review.

## Checks

- Source values stay inside the documented vocabulary.
- Resolver CSS is parent-scoped and avoids broad descendant selectors.
- Authoring changes follow `docs/patterns/layout-affinity-resolver-authoring.md`.
- Browser proof covers phone, tablet, and desktop widths with no horizontal
  overflow.
- Published docs keep the prototype status visible before any code example.
