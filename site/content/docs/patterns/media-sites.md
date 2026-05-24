---
title: Media Site Patterns
description: Streaming, catalog, watch-side, live event, profile, and plan recipes
draft: false
weight: 30
lang: en
type: doc
keywords: [chirp-ui, media sites, streaming, catalog, video, live events]
category: patterns
---

Media pages are decision and continuity systems. They sell an offer, expose a
catalog, explain availability, and keep users oriented across watched, live,
upcoming, restricted, and profile-specific states.

Use the canonical repository guide for the full recipe set:
[`docs/patterns/media-site-patterns.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/patterns/media-site-patterns.md?plain=1).

## Use This When

- A streaming or video service needs acquisition and conversion pages.
- A catalog needs featured shelves, ranked rails, tabs, or detail pages.
- A watch surface needs a companion panel, transcript, chat, or related content.
- Live events, profiles, parental controls, plans, or add-ons need clear state.

## Blessed Surfaces

- `site_shell`, `site_header`, `hero`, `band`, `cta_band`, and `btn`.
- `carousel`, `feature_section`, `frame`, and `video_thumbnail`.
- `video_card`, `channel_card`, `card`, `badge`, and `resource_index`.
- `tabs_panels` for content-format switching.
- `chat_layout`, `comment`, `drawer`, and `modal` for companion UI.
- `logo_cloud`, `story_card`, `metric_grid`, `callout`, and `accordion` for
  proof, comparison, and constraints.

## Checks

- The H1 names the service, product, or literal offer.
- Artwork is not the only source of title text.
- Badges describe content state such as live, new, included, rental, replay, or
  restricted.
- Missing artwork preserves layout.
- Profile and restriction states are visible before the user acts.
