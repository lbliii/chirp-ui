# Media Site Patterns

Status: recipe guidance

Use these recipes for streaming, video, catalog, and live-event pages before
proposing `media_*` macros. Chirp UI owns safe responsive structure; app code
owns playback, authorization, recommendations, profile rules, regional
availability, downloads, and DRM.

## Starting Surface

| Area | Components |
|---|---|
| Shell and acquisition | `site_shell`, `site_header`, `site_footer`, `hero`, `page_hero`, `band`, `cta_band`, `btn` |
| Composition | `container`, `stack`, `cluster`, `grid`, `frame`, `block`, `layer` |
| Media display | `video_card`, `video_thumbnail`, `channel_card`, `post_card`, `media_object` |
| Catalog browsing | `carousel`, `tabs_panels`, `resource_index`, `filter_chips`, `bento_grid` |
| Choice and proof | `card`, `resource_card`, `story_card`, `logo_cloud`, `marquee`, `metric_grid`, `stat`, `badge`, `callout`, `accordion` |
| Companion UI | `popover`, `drawer`, `modal`, `chat_layout`, `comment` |

## Recipe Matrix

| Pattern | Use When | Compose With | Checks |
|---|---|---|---|
| Streaming acquisition hero | Anonymous users need the offer, action, proof, and a small catalog signal. | `site_shell`, `site_header`, `hero`, `cluster`, `band`, `logo_cloud`, `cta_band`. | H1 names the service or offer; price/trial caveats sit near the action; catalog can load later. |
| Featured title shelf | The page highlights premieres, live events, editorial picks, or bundles. | `carousel(variant="page")`, `carousel_slide`, `feature_section`, `frame`, `video_thumbnail`, `badge`. | Each slide has a heading and accessible art; state badges use text; title is not image-only. |
| Ranked catalog rail | The page needs trending, new, recommended, top, free, or genre rails. | `band`, `section_header`, `carousel(variant="compact")`, `grid`, `video_card`, `card`, `badge`. | Rank is real text; every item exposes a title; metadata is short and comparable. |
| Format tabs | Channel, creator, show, or collection pages switch between videos, shorts, live, episodes, or replays. | `tabs_panels`, `video_card`, `post_card`, `callout`. | Tabs describe content jobs; default panel works before Alpine; live states are text. |
| Title detail page | A movie, series, episode, live event, game, or channel needs one canonical page. | `page_hero`, `feature_section`, `frame`, `badge`, `description_list`, `stat`, `tabs_panels`, `accordion`. | Watch is primary; availability/maturity sits near the action; details are structured. |
| Live event card | Sports, premieres, concerts, streams, or broadcasts need live/upcoming/replay states. | `media_object`, `card`, `badge`, `stat`, `callout`, `cluster`. | Time, state, and restrictions are text; upcoming vs live does not rely on animation. |
| Watch-side companion | A watch page needs chat, comments, transcript, chapters, recommendations, AI help, or commerce actions. | `grid(preset="detail-two")`, `frame`, `tabs_panels`, `chat_layout`, `comment`, `drawer`, `popover`. | Player owns aspect ratio; companion stacks below on narrow screens; user content remains escaped. |
| Plan, bundle, add-on comparison | Plans, premium channels, devices, family sharing, DVR, streams, 4K, or offline add-ons must be compared. | `card`, `resource_card`, `grid`, `bento_grid`, `badge`, `description_list`, `stat`, `accordion`. | Renewal, trial, restrictions, and add-on status are visible before CTA. |
| Story and fandom proof | Awards, watch-party adoption, creator reach, partner quotes, or franchise proof matter. | `story_card`, `grid`, `metric_grid`, `stat`, `logo_cloud`. | Outcomes are specific; metrics are text; logos have alt text or adjacent names. |
| Profile-safe catalog states | Catalog visibility depends on profile, maturity, household, device, download, kids mode, or controls. | App-owned profile state, `badge`, `callout`, `resource_index`. | Restrictions say what changed and what to do next; policy stays app-owned. |

## Minimal Skeleton

```kida
{% call site_shell() %}
  {% slot header %}...site_header...{% end %}

  {% call hero(title=service_name, subtitle=offer_summary) %}
    {% slot actions %}
      {% call cluster(gap="sm") %}
        {{ btn("Start watching", href=start_href, variant="primary") }}
        {{ btn("See plans", href=plans_href, variant="ghost") }}
      {% end %}
    {% end %}
  {% end %}

  {% call band(width="bleed") %}
    ...trending rail, plan proof, or supported-device proof...
  {% end %}
{% end %}
```

## Promotion Gates

| Candidate | Default | Promote only when |
|---|---|---|
| `media_hero_shelf` | Built | Page-carousel plus title-card structure needs a default accessible shelf. |
| `catalog_rail` | Built | Heading plus carousel title-card rail repeats enough to ship as a default. |
| `title_card` | Built | Streaming/premium metadata differs from creator-video metadata. |
| `title_detail` | Recipe | Artwork, metadata, CTA, and episode sections repeat across real pages. |
| `live_event_card` | Built | Live/upcoming/replay/restricted states need readable default structure. |
| `watch_companion_layout` | Built | Player plus side-panel responsive behavior is easy to get wrong locally. |
| `profile_catalog_notice` | Recipe | Profile/maturity/download restrictions repeat across apps. |

A promoted macro needs a descriptor, emitted-class coverage, CSS partials,
template docs, manifest projection, and browser coverage.
