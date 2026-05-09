---
title: Forum Patterns
description: Community, topic list, thread, Q&A, moderation, and activity recipes
draft: false
weight: 40
lang: en
type: doc
keywords: [chirp-ui, forums, community, discussion, moderation, q&a]
category: patterns
---

Forum-shaped products combine discovery, participation, identity, governance,
moderation, and durable knowledge retrieval. Chirp UI can compose these pages
from existing primitives before adding a public `forum_*` namespace.

Use the canonical repository guide for the full recipe set:
[`docs/FORUM-SITE-PATTERNS.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/FORUM-SITE-PATTERNS.md?plain=1).

## Use This When

- A community home needs rules, categories, visibility, stats, and posting
  state.
- A topic list needs filters, replies, labels, saved views, or activity state.
- A thread page needs root post, replies, local navigation, composer, and
  secondary management controls.
- Q&A, moderation, and inbox surfaces need dense but separated operating state.

## Blessed Surfaces

- `app_shell`, `site_shell`, `route_tabs`, `nav_tree`, `breadcrumbs`, and
  `split_layout`.
- `detail_header`, `thread_reader_layout`, `post_card`, `rendered_content`,
  `comment_thread`, and `comment`.
- `resource_index`, `resource_card`, `facet_chip`, `badge`, and `counter_badge`.
- `action_bar`, `share_menu`, `reaction_pill`, `message_reactions`, and `btn`.
- `callout`, `alert`, `confirm_dialog`, `form`, `action_strip`, and `toast` for
  governance and moderation.

## Checks

- Rules, visibility, and posting permissions appear before composers.
- Locked, archived, removed, or moderator-only states are visible before reply
  forms.
- Reply and moderation actions are keyboard reachable and labeled.
- Long threads provide anchors, sort controls, or continuation markers.
- Sanitized body HTML remains app-owned; recipes do not add new unsafe escape
  hatches.
