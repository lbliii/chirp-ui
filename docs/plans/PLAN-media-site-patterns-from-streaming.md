# chirp-ui: Media Site Patterns from Streaming Platforms

## Goal

Turn the observed 2026 Netflix, YouTube, and Apple TV media-site grammar into
ChirpUI-native recipes for streaming, video, creator, and catalog pages without
expanding the public component surface prematurely.

The target is not to copy any platform. The target is to identify the repeatable
media-site jobs behind them, express those jobs with existing ChirpUI primitives
first, and only add registry-backed components when recipes prove too verbose or
too easy to misuse.

References observed 2026-05-02:

- Netflix: <https://www.netflix.com/>
- About Netflix: <https://about.netflix.com/en>
- Netflix downloads: <https://help.netflix.com/en/node/54816>
- Netflix kids profiles: <https://help.netflix.com/en/node/114275>
- Netflix mobile games: <https://help.netflix.com/en/node/121442>
- YouTube TV: <https://tv.youtube.com/welcome/>
- YouTube Live: <https://support.google.com/youtube/answer/13361370>
- YouTube on TV AI: <https://blog.youtube/news-and-events/youtube-conversational-ai-tool-available-smart-tvs/>
- Apple TV: <https://www.apple.com/apple-tv/>
- Apple TV app: <https://www.apple.com/apple-tv-app/>
- Apple TV catalog: <https://tv.apple.com/>

---

## Design Read

These sites work because they treat media pages as decision and continuity
systems, not just galleries.

| Platform move | Media-site job | ChirpUI lesson |
|---------------|----------------|----------------|
| Netflix first-viewport subscription pitch | Convert anonymous visitors with one clear offer before browsing | `hero`, `site_header`, `band`, and `btn` can handle acquisition pages today |
| Netflix trending and reason-to-join sections | Pair catalog pull with utility promises: TV, offline, everywhere, kids | Need recipes that combine ranked rails, `logo_cloud`, proof, and device/support copy |
| Netflix recommendations and profiles | Personalize catalog discovery by viewer, maturity, and context | `resource_index`, `filter_chips`, `video_card`, and `channel_card` need media-catalog recipes |
| Netflix downloads, kids, and games | Treat availability, restrictions, and profile eligibility as first-class UI | Recipes need metadata badges, constraint callouts, and profile-scoped states |
| YouTube TV plans and add-ons | Help users compare live bundles, add-ons, devices, DVR, and streams | Existing `card`, `resource_card`, `grid`, `accordion`, and `stat` can cover live-TV comparison |
| YouTube creator formats: Videos, Shorts, Live | Segment by content format and intent, not just category | `tabs_panels` should document media-format tabs and no-JS fallback content |
| YouTube Live chat and community | Make real-time participation visible around the player | Existing comments/chat patterns may need a live companion-panel recipe before new macros |
| YouTube smart-TV conversational AI | Keep interactive help near the watch surface without interrupting playback | `popover`, `drawer`, or `chat_layout` should be tested as watch-side companions |
| Apple TV offer stack | Show subscription, bundle, device, student, and family-sharing options together | `card`, `resource_card`, `bento_grid`, `cta_band`, and `callout` can express offer choice without a new plan component |
| Apple TV catalog cards | Combine artwork, release cadence, genres, summary, trial CTA, and add action | `video_card` is too YouTube-shaped for premium-title cards; start with recipe, then consider `title_card` |
| Apple TV sports and live shelves | Separate live events from evergreen catalog and make timing/state legible | Need live-event rail recipes with `badge`, `stat`, `callout`, and `carousel` |
| Apple TV device availability | Reassure users where they can watch and continue watching | `logo_cloud`, `marquee`, `cluster`, and `grid` can cover device/support proof |

---

## Current ChirpUI Surface

ChirpUI already has useful media and commerce primitives:

- **Site shell:** `site_shell`, `site_header`, `site_footer`
- **Acquisition and proof:** `hero`, `page_hero`, `band`, `cta_band`, `feature_section`, `logo_cloud`, `marquee`, `metric_grid`
- **Media display:** `video_card`, `video_thumbnail`, `channel_card`, `post_card`, `media_object`
- **Catalog composition:** `carousel`, `tabs_panels`, `resource_index`, `filter_chips`, `grid`, `bento_grid`
- **Commerce and choice:** `card`, `resource_card`, `story_card`, `stat`, `badge`, `accordion`, `callout`
- **Interactive companions:** `popover`, `drawer`, `modal`, `chat_layout`, `comment`

The gap is a media-site recipe layer:

- how to build rails, hero shelves, title detail pages, live-event cards, plan
  comparison, profile-safe catalog states, and watch-side companion panels
  without utility classes;
- where `video_card` is appropriate and where a streaming-title card needs
  different semantics;
- how to document TV, mobile, web, game console, offline, account/profile, and
  content-rights constraints as normal media UI, not bespoke page copy.

---

## Non-Goals

- Do not copy Netflix, YouTube, Apple, or any partner brand treatment.
- Do not add utility classes or raw CSS values.
- Do not add new media tokens, variants, or sizes in this plan.
- Do not add playback controls, DRM surfaces, analytics, recommendations, or
  account logic to ChirpUI.
- Do not add scripts for carousels or marketing interactions. Use the existing
  zero-JS carousel and existing Alpine-backed components only.
- Do not make `video_card` carry every streaming use case by adding speculative
  params.
- Do not expose raw HTML escape hatches for media metadata, artwork, or badges.

---

## Proposed Pattern Recipes

### 1. Streaming Acquisition Hero

**Use when:** A media service needs to convert anonymous visitors before full
catalog exploration.

**Compose from:**

- `site_shell`
- `site_header`
- `hero` or `page_hero`
- `cluster` for CTAs and price/trial details
- `band` for plan, device, or catalog proof immediately below
- `logo_cloud` for supported-device, partner, channel, or studio proof
- `cta_band` for closing conversion sections

**Recipe shape:**

```kida
{% call site_shell() %}
  {% slot header %}...site_header...{% end %}
  {% call hero(title=service_name, subtitle=offer_summary) %}
    {% slot actions %}
      {{ btn("Start watching", variant="primary") }}
      {{ btn("See plans", variant="ghost") }}
    {% end %}
  {% end %}
  {% call band(width="bleed", variant="default") %}
    ...trending rail or device proof...
  {% end %}
{% end %}
```

**Acceptance checks:**

- The H1 names the service, product, or literal offer.
- The CTA path is legible without JavaScript.
- Price, trial, or cancellation caveats are adjacent to the action.
- Long catalog grids do not precede the conversion promise.

### 2. Hero Shelf / Featured Title Rail

**Use when:** A catalog page needs to feature one live event, premiere, bundle,
or editorial pick while still exposing browsable choices.

**Compose from:**

- `carousel(variant="page")` for one-feature-per-viewport shelves
- `video_thumbnail` or app-owned artwork inside `frame`
- `badge` for live, new, all episodes, included, rented, or expiring states
- `cluster` for actions such as play, details, add, trailer

**Recipe shape:**

```kida
{% call carousel(variant="page", slide_count=featured|length, show_dots=true) %}
  {% for title in featured %}
    {% call carousel_slide(loop.index) %}
      {% call feature_section(layout="media-dominant") %}
        {% slot media %}...artwork frame...{% end %}
        {% slot title %}{{ title.name }}{% end %}
        ...metadata, summary, and actions...
      {% end %}
    {% end %}
  {% endfor %}
{% end %}
```

**Acceptance checks:**

- Each slide has a stable heading and text alternative for artwork.
- Badges describe media state, not decorative mood.
- Dots are optional; the rail remains useful as normal document content.
- The recipe respects reduced-motion and native scroll behavior.

### 3. Ranked / Editorial Catalog Rail

**Use when:** A page needs Netflix-style trending, Apple-style release shelves,
or curated YouTube collections.

**Compose from:**

- `carousel(variant="compact")`
- `grid` for non-scroll contexts
- `video_card` for creator/video items
- `card`, `frame`, and `badge` for premium title cards until a dedicated card is justified

**Recipe shape:**

```kida
{% call band(width="container") %}
  {{ section_header("Trending now") }}
  {% call carousel(variant="compact") %}
    {% for item in ranked_titles %}
      {% call carousel_slide(loop.index) %}
        ...rank marker, artwork, title, metadata...
      {% end %}
    {% endfor %}
  {% end %}
{% end %}
```

**Acceptance checks:**

- Rank is real content, not background decoration.
- The title is available as text even when artwork carries branding.
- Metadata is concise: format, genre, duration, release cadence, or availability.
- Rails can become grids at wider or print-like contexts without losing content.

### 4. Format Tabs: Videos / Shorts / Live / Episodes

**Use when:** A channel, creator, or media detail page has multiple content
formats that users understand as different browsing modes.

**Compose from:**

- `tabs_panels`
- `video_card` for long-form videos
- `post_card` or app-owned cards for Shorts-like items
- `callout` for empty, restricted, or scheduled live states

**Recipe shape:**

```kida
{% call tabs_container(active="videos") %}
  {{ tab_button("videos", "Videos", active=true) }}
  {{ tab_button("shorts", "Shorts") }}
  {{ tab_button("live", "Live") }}

  {% call tab_panel("videos", active=true) %}
    ...video card grid...
  {% end %}
{% end %}
```

**Acceptance checks:**

- Tabs describe content jobs, not visual layouts.
- The default tab renders a useful list without Alpine.
- Live tabs can show scheduled, active, and archived states.
- Format-specific metadata does not require a new card variant until repeated.

### 5. Title Detail Page

**Use when:** A movie, series, event, or game needs one canonical detail view.

**Compose from:**

- `page_hero` or `feature_section`
- `badge` for maturity, format, live, included, rental, or download state
- `description_list` or `stat` for structured metadata
- `accordion` for episodes, seasons, availability, or accessibility details
- `tabs_panels` when episodes, extras, cast, and related content are peer sections

**Recipe shape:**

```kida
{% call feature_section(layout="balanced") %}
  {% slot media %}...poster or key art...{% end %}
  {% slot title %}{{ title.name }}{% end %}
  ...genre, runtime, release cadence, actions...
{% end %}
```

**Acceptance checks:**

- Play/watch actions are primary; add/share/details actions are secondary.
- Maturity and availability information is near the action, not buried.
- Episodes and extras are structured content, not a raw paragraph.
- App-owned authorization state stays outside ChirpUI.

### 6. Live Event / Sports Card

**Use when:** A page needs to show live, upcoming, replay, blackout, market, or
league-specific event states.

**Compose from:**

- `card` or `media_object`
- `badge` for live, upcoming, replay, local, restricted
- `stat` for start time, teams, channel, or availability
- `callout` for market, device, or subscription restrictions

**Recipe shape:**

```kida
{% call media_object(use_slots=true) %}
  {% slot media %}...league art or matchup mark...{% end %}
  <h3>{{ event.name }}</h3>
  {{ badge(event.state) }}
  ...time, teams, subscription, actions...
{% end %}
```

**Acceptance checks:**

- Time is rendered as text, not only color or icon.
- Live and upcoming states are distinguishable without motion.
- Restrictions are explicit and screen-reader reachable.
- The card does not assume sports only; concerts and premieres use the same shape.

### 7. Watch-Side Companion Panel

**Use when:** Playback needs adjacent chat, comments, Q&A, recommendations, AI
assistance, transcript, chapters, or purchase options.

**Compose from:**

- `frame` for the media viewport
- `chat_layout`, `comment`, `drawer`, or `popover`
- `tabs_panels` for transcript / chat / details / related

**Recipe shape:**

```kida
{% call grid(preset="detail-two") %}
  {% call frame() %}...player embed...{% end %}
  {% call tabs_container(active="chat") %}
    ...chat, transcript, related...
  {% end %}
{% end %}
```

**Acceptance checks:**

- The player column owns its aspect ratio and cannot be squeezed by side content.
- Companion content remains below the player on narrow screens.
- Chat/comment input must be app-owned and escaped through existing form helpers.
- AI or transcript text is rendered as content, not `| safe`.

### 8. Plan / Bundle / Add-On Comparison

**Use when:** A service needs to compare subscriptions, bundles, add-ons,
channels, DVR, streams, trials, and cancellation rules.

**Compose from:**

- `card` or `resource_card`
- `bento_grid` or `grid`
- `badge` for best fit, limited offer, included, add-on
- `accordion` for legal or plan caveats

**Recipe shape:**

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

**Acceptance checks:**

- The comparison works without color-only emphasis.
- Trial length, renewal price, and restrictions are visible before CTA.
- Add-ons are visually distinct from base plans.
- Legal caveats remain normal text and links.

### 9. Profile / Family / Kids Safe Catalog

**Use when:** Media availability depends on profile, maturity, household, device,
or parental controls.

**Compose from:**

- `avatar` or profile selection patterns owned by the app
- `badge` for kids, maturity, download, game, profile-only states
- `callout` for restrictions or next steps
- `resource_index` for filtered catalogs

**Recipe shape:**

```kida
{% call callout(variant="info", title="Kids profile") %}
  This catalog only shows titles and games available for this profile.
{% end %}
```

**Acceptance checks:**

- Restrictions tell users what changed and what they can do next.
- Kids/profile states do not rely on hidden account settings.
- Maturity labels and blocked states are rendered as text.
- The app owns policy logic; ChirpUI only supplies structure.

---

## Implementation Plan

### Phase 1: Document Recipes (completed 2026-05-02)

Add media-site recipes to docs without changing component APIs.

| File | Action |
|------|--------|
| `docs/MEDIA-SITE-PATTERNS.md` | Added recipe documentation for acquisition heroes, hero shelves, rails, format tabs, title details, live events, companion panels, plan comparison, and profile-safe catalogs |
| `docs/PRIMITIVES.md` | Added a short media-site compositions pointer |
| `docs/INDEX.md` | Indexed the recipe doc under Patterns |
| `docs/plans/PLAN-media-site-patterns-from-streaming.md` | Keep this plan as the active roadmap |

**Done when:**

- Docs show how to build each pattern from existing registry-cited components.
- No new classes, variants, tokens, or macro params are introduced.
- Recipes call out where apps own rights, account, playback, recommendation, and safety logic.

### Phase 2: Build a Showcase Fixture (completed 2026-05-03)

Create one internal showcase page that exercises the recipes against realistic
placeholder media data.

Implemented locations:

- `tests/browser/templates/media_site_patterns.html`
- `tests/browser/test_media_site_patterns.py`
- `/media-site-patterns` route in `tests/browser/app.py`

**Done when:**

- The page renders the recipe set with realistic placeholder catalog data.
- Browser tests verify no mobile horizontal overflow.
- The fixture uses only existing public macros and component classes.
- The watch-side layout proves player aspect ratio and companion panel behavior at phone and desktop widths.

Progress:

- Added the media-site browser fixture with acquisition hero, device proof,
  hero shelf, ranked catalog rail, format tabs, title detail, live-event cards,
  watch-side companion panel, profile-safe catalog, plan comparison, and closing
  CTA recipes.
- Added browser coverage for phone/tablet/desktop horizontal overflow, rendered
  recipe sections, and mobile watch-companion stacking.
- The fixture initially exercised existing primitives without a public
  `media_*` macro, then promoted a small default asset layer so apps have
  battle-tested starting points while playback, entitlement, profile,
  live-state, and chat behavior stay app-owned.

### Phase 3: Promote Repeated Recipes

After the docs recipe and showcase have at least one real consumer, decide
whether any pattern deserves a macro.

Candidate macros, gated by evidence:

| Candidate | Default answer | Promotion trigger |
|-----------|----------------|-------------------|
| `media_hero_shelf` | Built 2026-05-03 | Default carousel + title-card shelf for featured media |
| `catalog_rail` | Built 2026-05-03 | Heading + title-card rail is common enough to ship as a default |
| `title_card` | Built 2026-05-03 | Streaming/premium title metadata differs from creator-video metadata |
| `title_detail` | Recipe only | Detail pages repeat the same artwork, metadata, CTA, and episode structure |
| `live_event_card` | Built 2026-05-03 | Live/upcoming/replay/restricted states need readable default structure |
| `watch_companion_layout` | Built 2026-05-03 | Player + side panel + responsive stacking is easy to get wrong locally |
| `profile_catalog_notice` | Recipe only | Profile/maturity/download restrictions need consistent text structure across apps |

**Done when:**

- Any promoted macro has a `ComponentDescriptor`.
- Emitted classes are in the registry and matching CSS partial.
- Template doc-block, tests, and manifest projection are updated.
- `COMPONENT-OPTIONS.md` documents new params only after the API is real.

### Phase 4: Polish Existing Components

Only after recipe validation, refine existing components where the recipe exposes
friction.

Possible refinements:

- `video_card`: verify channel/video metadata remains creator-video specific.
- `video_thumbnail`: audit progress, duration, and alt text for title-card usage.
- `carousel`: verify compact and page variants are enough for media rails.
- `tabs_panels`: document media-format tabs and useful no-JS default panels.
- `card` / `resource_card`: verify bundle/add-on comparison does not require custom classes.
- `media_object`: verify live-event layout can use it without extra chrome.
- `chat_layout`: verify watch-side companion usage stays safe and responsive.

**Done when:**

- Refinements remain token-based and registry-cited.
- No raw CSS values are added.
- Existing tests for template/CSS/registry parity remain green.

---

## Testing Strategy

For recipe-only phases:

- Run docs checks if docs examples become test-covered.
- Add browser fixture coverage if a showcase template is added.
- Check responsive behavior at phone and desktop widths.
- Include at least one long title, one missing artwork fallback, one live event,
  one restricted title, one kids/profile notice, and one plan comparison.

For any future macro/component promotion:

- `test_template_css_contract.py`
- `test_transition_tokens.py`
- Registry-emits parity test
- Manifest rebuild: `python -m chirp_ui.manifest --json`
- Focused component render tests in `tests/test_components.py`
- Browser smoke coverage for the showcase route

Full done criteria remain `uv run poe ci`.

---

## Steward Notes

- **Registry steward:** New media macros require descriptors before CSS/classes ship.
- **Rendering steward:** Media metadata, titles, descriptions, and user/chat content must remain escaped.
- **Theme steward:** Media polish should use existing tokens before proposing new ones.
- **Docs steward:** Recipes must describe shipped contracts, not aspirational APIs.
- **Planning steward:** Keep this plan active until recipes are documented or promoted into concrete component plans.
- **Site steward:** If exposed on the docs site, examples must render cleanly in the published site shell.
- **Accessibility:** Artwork needs alt text or adjacent title text; live/availability state cannot be color-only.
- **Security:** Playback, account, recommendation, entitlement, and parental-control logic belongs to the app, not ChirpUI.

---

## Not Now

- A full streaming app shell.
- Playback controls, DRM, recommendations, queue state, or entitlement APIs.
- Brand-specific Netflix, YouTube, or Apple visual mimicry.
- JavaScript-powered carousel controls beyond the existing component contract.
- A generic `media_*` namespace before there is usage evidence.
- A title-card macro that is just `video_card` with more optional fields.
- A media-specific utility class vocabulary.

---

## Open Questions

- Should future media-site recipes stay in `docs/MEDIA-SITE-PATTERNS.md`, or should any proven overlap move into a shared product/media pattern doc?
- Is `title_card` distinct enough from `video_card`, `card`, and `index_card` to justify promotion?
- Does `carousel` need an accessible named-label param before media rails are documented heavily?
- Should live-event state be modeled as a generic content-state recipe before any macro exists?
- Should watch-side companions lean on `chat_layout`, `drawer`, `popover`, or a new layout-only macro?
- Do downstream apps need first-class artwork fallback handling, or should app templates own it entirely?
