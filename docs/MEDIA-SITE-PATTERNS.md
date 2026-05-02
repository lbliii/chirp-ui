# Media Site Patterns

ChirpUI can already compose streaming, video, catalog, and live-event pages from
the public registry. Use these recipes before proposing new `media_*` macros.
The component registry remains the source of truth; this page describes how to
assemble shipped components into media-site flows without utility classes or
brand-specific styling.

These patterns come from a 2026 review of Netflix, YouTube / YouTube TV, and
Apple TV. The lesson is structural: media pages are decision and continuity
systems. They sell an offer, expose a catalog, explain where content can be
watched, and keep users oriented across live, upcoming, watched, restricted, and
profile-specific states.

---

## Existing Surface

Start with these shipped primitives and components:

- **Shell and acquisition:** `site_shell`, `site_header`, `site_footer`, `hero`,
  `page_hero`, `band`, `cta_band`, `btn`
- **Composition:** `container`, `stack`, `cluster`, `grid`, `frame`, `block`,
  `layer`
- **Media display:** `video_card`, `video_thumbnail`, `channel_card`,
  `post_card`, `media_object`
- **Catalog browsing:** `carousel`, `tabs_panels`, `resource_index`,
  `filter_chips`, `bento_grid`
- **Choice and proof:** `card`, `resource_card`, `story_card`, `logo_cloud`,
  `marquee`, `metric_grid`, `stat`, `badge`, `callout`, `accordion`
- **Companion UI:** `popover`, `drawer`, `modal`, `chat_layout`,
  `comment`

App code owns playback, authorization, recommendations, account state, parental
controls, geographic availability, download eligibility, and DRM. ChirpUI owns
the safe, responsive HTML structure around those app decisions.

---

## Streaming Acquisition Hero

Use this for anonymous landing pages where the first job is conversion: name the
service or offer, explain the value, show the primary action, and put proof or a
small catalog signal immediately after the hero.

Compose from:

- `site_shell`
- `site_header`
- `hero` or `page_hero`
- `cluster` for CTA rows and caveats
- `band` for plan, device, catalog, or proof content
- `logo_cloud` for supported devices, partners, channels, or studio proof
- `cta_band` for the closing conversion section

```kida
{% from "chirpui/site_shell.html" import site_shell %}
{% from "chirpui/hero.html" import hero %}
{% from "chirpui/layout.html" import cluster %}
{% from "chirpui/button.html" import btn %}
{% from "chirpui/band.html" import band %}
{% from "chirpui/cta_band.html" import cta_band %}

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

  {{ cta_band(
    title="Start watching",
    body="Pick a plan and continue on any supported device.",
    primary_label="Start",
    primary_href=start_href,
    secondary_label="Compare plans",
    secondary_href=plans_href,
  ) }}
{% end %}
```

Checks:

- The H1 names the service, product, or literal offer.
- Price, trial, renewal, and cancellation caveats are close to the action.
- The page remains useful if the catalog rail below the hero loads later.
- Do not place a long generic catalog before the conversion promise.
- Use `logo_cloud` for proof strips instead of a hand-rolled logo grid.

---

## Featured Title Shelf

Use this for a first catalog section that highlights premieres, live events,
editorial picks, or bundle offers while still letting users browse.

Compose from:

- `carousel(variant="page")`
- `carousel_slide`
- `feature_section`
- `frame` or `video_thumbnail`
- `badge`
- `cluster` for actions

```kida
{% from "chirpui/carousel.html" import carousel, carousel_slide %}
{% from "chirpui/feature_section.html" import feature_section %}
{% from "chirpui/layout.html" import cluster, frame %}

{% call carousel(variant="page", slide_count=featured|length, show_dots=true) %}
  {% for title in featured %}
    {% call carousel_slide(loop.index) %}
      {% call feature_section(layout="media-dominant") %}
        {% slot media %}
          {% call frame() %}
            <img src="{{ title.artwork }}" alt="{{ title.name }}" loading="lazy">
          {% end %}
        {% end %}
        {% slot title %}{{ title.name }}{% end %}
        <p>{{ title.summary }}</p>
        {% call cluster(gap="sm") %}
          ...state badges and actions...
        {% end %}
      {% end %}
    {% end %}
  {% end %}
{% end %}
```

Checks:

- Each slide has a stable heading and accessible artwork text.
- Badges describe content state: live, new, included, rental, expiring, replay.
- The rail remains readable as normal document content without custom scripts.
- Avoid using slide art as the only source of the title.

---

## Ranked Catalog Rail

Use this for trending, new releases, recommended, top videos, free premieres, or
genre rails. A rail is a browsing unit with a heading, optional description, and
repeated media items.

Compose from:

- `band`
- `section_header`
- `carousel(variant="compact")`
- `grid` when scroll is not needed
- `video_card` for YouTube-like creator videos
- `card`, `frame`, and `badge` for premium title cards until `title_card` is
  justified by repeated use

```kida
{% call band(width="container") %}
  {{ section_header("Trending now") }}
  {% call carousel(variant="compact") %}
    {% for item in ranked_titles %}
      {% call carousel_slide(loop.index) %}
        ...rank, artwork, title, metadata, and action...
      {% end %}
    {% endfor %}
  {% end %}
{% end %}
```

Checks:

- Rank is actual text content, not only a background number.
- Every item exposes a title outside the image.
- Metadata is short and comparable: format, runtime, genre, cadence, creator,
  availability, or progress.
- Missing artwork has an app-owned fallback that still preserves layout.

---

## Format Tabs

Use this for channel, creator, show, or collection pages where users switch
between content formats such as videos, shorts, live, episodes, clips, extras,
or replays.

Compose from:

- `tabs_panels`
- `video_card`
- `post_card` or app-owned cards for short-form/social items
- `callout` for empty, scheduled, or restricted states

```kida
{% call tabs_container(active="videos") %}
  {{ tab_button("videos", "Videos", active=true) }}
  {{ tab_button("shorts", "Shorts") }}
  {{ tab_button("live", "Live") }}

  {% call tab_panel("videos", active=true) %}
    ...video card grid...
  {% end %}

  {% call tab_panel("live") %}
    ...active, scheduled, and archived streams...
  {% end %}
{% end %}
```

Checks:

- Tabs describe content jobs, not layout styles.
- The default active panel renders useful content before Alpine initializes.
- Live tabs distinguish active, scheduled, replay, and unavailable states in text.
- Do not add a new card variant just to label a format once.

---

## Title Detail Page

Use this for one canonical page for a movie, series, episode, live event, game,
or premium channel title.

Compose from:

- `page_hero` or `feature_section`
- `frame` for poster or key art
- `badge` for maturity, format, live, included, rental, download, or profile
  states
- `description_list` or `stat` for structured metadata
- `tabs_panels` or `accordion` for episodes, extras, cast, accessibility, and
  availability details

```kida
{% call feature_section(layout="balanced") %}
  {% slot media %}
    {% call frame() %}
      <img src="{{ title.poster }}" alt="{{ title.name }}" loading="lazy">
    {% end %}
  {% end %}
  {% slot title %}{{ title.name }}{% end %}

  <p>{{ title.summary }}</p>
  {% call cluster(gap="sm") %}
    ...maturity, genre, runtime, and availability badges...
  {% end %}
  {% call cluster(gap="sm") %}
    ...watch, trailer, add, or details actions...
  {% end %}
{% end %}
```

Checks:

- Play or watch is the primary action; add/share/details actions are secondary.
- Maturity and availability information appears near the action.
- Episodes, seasons, extras, and accessibility details are structured sections.
- App authorization state is rendered as normal text or badges, not hidden logic.

---

## Live Event Card

Use this for sports, premieres, concerts, streams, or broadcasts with live,
upcoming, replay, local, blackout, subscription, or market states.

Compose from:

- `media_object` or `card`
- `badge`
- `stat`
- `callout`
- `cluster` for actions

```kida
{% call media_object(use_slots=true) %}
  {% slot media %}
    ...league art, matchup mark, or event thumbnail...
  {% end %}
  <h3>{{ event.name }}</h3>
  {% call cluster(gap="xs") %}
    {{ badge(event.state) }}
    {{ badge(event.access) }}
  {% end %}
  ...start time, teams, channel, and actions...
{% end %}
```

Checks:

- Time, state, and restrictions are text, not color-only signals.
- Live and upcoming states are distinguishable without animation.
- The pattern works for non-sports premieres as well as sports.
- Market, household, or subscription restrictions explain what the user can do.

---

## Watch-Side Companion

Use this when a watch page needs adjacent chat, comments, Q&A, recommendations,
AI help, transcript, chapters, or commerce actions.

Compose from:

- `grid(preset="detail-two")` or `frame` for the main player region
- `tabs_panels` for chat / transcript / details / related
- `chat_layout`, `comment`, `drawer`, or `popover`

```kida
{% call grid(preset="detail-two") %}
  {% call frame() %}
    ...player embed or video element...
  {% end %}

  {% call tabs_container(active="chat") %}
    ...chat, transcript, related, or assistant panel...
  {% end %}
{% end %}
```

Checks:

- The player owns its aspect ratio and cannot be squeezed by side content.
- Companion content stacks below the player on narrow screens.
- User/chat content stays escaped through existing form and rendering helpers.
- AI output, transcripts, and comments are content, not `| safe` strings.

---

## Plan, Bundle, and Add-On Comparison

Use this for streaming plans, live-TV bundles, premium channels, device offers,
student offers, family sharing, DVR, streams, and 4K/offline add-ons.

Compose from:

- `card` or `resource_card`
- `grid` or `bento_grid`
- `badge`
- `description_list` or `stat`
- `accordion` for details and caveats

```kida
{% call grid(cols=3, gap="lg") %}
  {% for plan in plans %}
    {% call card(title=plan.name) %}
      <p>{{ plan.price }}</p>
      ...included features, caveats, and action...
    {% end %}
  {% endfor %}
{% end %}
```

Checks:

- Renewal price, trial length, add-on status, and restrictions are visible before
  the CTA.
- Base plans and add-ons are visually and textually distinct.
- The comparison works without color-only emphasis.
- Legal caveats remain normal text and links.

---

## Story and Fandom Proof

Use this when a media page needs to show audience, creator, studio, customer, or
franchise outcomes: awards, watch-party adoption, creator reach, partner quotes,
case studies, or cultural-moment proof.

Compose from:

- `story_card`
- `grid`
- `metric_grid` or `stat`
- `logo_cloud` for partner or studio marks

```kida
{% call grid(cols=3, gap="lg") %}
  {% for story in stories %}
    {{ story_card(
      customer=story.name,
      outcome=story.outcome,
      summary=story.summary,
      metric=story.metric,
      href=story.href,
      logo_src=story.logo,
    ) }}
  {% endfor %}
{% end %}
```

Checks:

- Outcome copy is specific; avoid generic praise cards.
- Metrics are text and remain meaningful without color.
- Logos have alt text or adjacent customer/studio names.
- Use this for proof, not for every catalog title.

---

## Profile-Safe Catalog States

Use this when content visibility depends on profile, maturity, household,
device, download eligibility, games support, kids mode, or parental controls.

Compose from:

- App-owned profile selection
- `badge` for kids, maturity, download, game, profile-only, or restricted states
- `callout` for user-facing explanations and next steps
- `resource_index` for filtered catalogs

```kida
{% call callout(variant="info", title="Kids profile") %}
  This catalog only shows titles and games available for this profile.
{% end %}
```

Checks:

- Restrictions tell users what changed and what they can do next.
- Kids/profile states do not rely on hidden account settings.
- Maturity labels and blocked states are rendered as text.
- ChirpUI never owns policy decisions; it only renders the app-owned state.

---

## Promotion Gates

Keep these as recipes until real pages prove that local markup is repeated,
fragile, or hard to keep accessible.

| Candidate | Default | Promote only when |
|-----------|---------|-------------------|
| `media_hero_shelf` | Recipe | Page-carousel plus feature-section markup repeats with the same accessibility needs |
| `catalog_rail` | Recipe | Heading, rail, fallback-grid, and empty-state structure repeat across pages |
| `title_card` | Maybe | `video_card` cannot represent premium titles without misleading YouTube-specific fields |
| `title_detail` | Recipe | Artwork, metadata, CTA, and episode sections repeat across real pages |
| `live_event_card` | Maybe | Live/upcoming/replay/restricted states repeat across sports and non-sports pages |
| `watch_companion_layout` | Maybe | Player plus side-panel responsive behavior proves too fragile as page markup |
| `profile_catalog_notice` | Recipe | Profile/maturity/download restrictions need consistent structure across apps |

Any promoted macro needs a descriptor, emitted-class coverage, CSS partials,
template docs, manifest projection, and browser coverage before it ships.
