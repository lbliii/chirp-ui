# chirp-ui: Forum Site Patterns from Community Platforms

## Goal

Turn the observed 2026 Reddit, Discourse, Stack Overflow, and GitHub
Discussions grammar into ChirpUI-native recipes for forum, Q&A, threaded
discussion, community-support, and moderation pages without expanding the
public component surface prematurely.

The target is not to copy any platform. The target is to identify the repeatable
forum-site jobs behind them, express those jobs with existing ChirpUI primitives
first, and only add registry-backed components when recipes prove too verbose or
too easy to misuse.

References observed 2026-05-02:

- Reddit Inc: <https://redditinc.com/>
- Reddit votes: <https://support.reddithelp.com/hc/en-us/articles/7419626610708-What-are-upvotes-and-downvotes>
- Reddit post flair: <https://support.reddithelp.com/hc/en-us/articles/15484545678996-Post-Flair>
- Reddit moderators: <https://support.reddithelp.com/hc/en-us/articles/204533859-What-s-a-moderator>
- Reddit sticky posts: <https://support.reddithelp.com/hc/en-us/articles/15484641176724-Community-Highlights-Sticky-posts>
- Reddit community visibility: <https://support.reddithelp.com/hc/en-us/articles/360060416112-What-are-public-restricted-private-and-premium-only-communities>
- Discourse features: <https://discourse.org/features>
- Stack Overflow tour: <https://stackoverflow.com/tour>
- Stack Overflow voting: <https://stackoverflow.com/help/why-vote>
- GitHub Discussions docs: <https://docs.github.com/discussions>
- GitHub Discussions categories: <https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-categories-for-discussions>

---

## Design Read

These sites work because forum pages balance discoverability, participation,
quality signals, and governance.

| Platform move | Forum-site job | ChirpUI lesson |
|---------------|----------------|----------------|
| Reddit communities and home feeds | Organize participation around interests, posts, comments, and votes | `resource_index`, `post_card`, `comment`, `action_bar`, and `badge` cover the core shape |
| Reddit flair and community rules | Let each community encode local taxonomy and culture | Recipes need `badge`, `filter_chips`, `callout`, and app-owned policy state |
| Reddit sticky/community highlights | Keep important posts above fast-moving lists | `carousel`, `resource_card`, and `badge` can handle highlighted posts without a new macro |
| Reddit visibility and moderation | Public/restricted/private spaces and mod actions change what users can do | Recipes need explicit permission and restriction states near actions |
| Discourse topics and infinite conversation | Make long conversations readable without page-chunk thinking | `infinite_scroll`, anchors, `comment_thread`, and clear sort markers need recipe guidance |
| Discourse trust, badges, moderation, chat | Community health is visible in identity and governance signals | Existing `badge`, `timeline`, `chat_layout`, and `callout` should be composed carefully |
| Stack Overflow Q&A | Separate questions, answers, comments, votes, accepted state, and closure | Need a Q&A recipe before promoting `answer_card` or `vote_control` |
| Stack Overflow reputation and privileges | Explain trust and moderation power as earned community state | `stat`, `description_list`, `badge`, and `timeline` can render app-owned trust state |
| GitHub Discussions categories | Different category formats serve Q&A, announcements, polls, ideas, and show-and-tell | `route_tabs`, `tabs_panels`, `resource_index`, and `badge` cover category browsing |
| GitHub Discussions moderation | Maintainers mark answers, lock, transfer, delete, and categorize discussions | Moderation recipes need confirmations, state labels, and action history |

---

## Current ChirpUI Surface

ChirpUI already has useful forum and discussion primitives:

- **Shell and navigation:** `app_shell`, `site_shell`, `site_header`,
  `route_tabs`, `nav_tree`, `breadcrumbs`, `split_layout`
- **Discovery and lists:** `resource_index`, `resource_card`, `filter_chips`,
  `tabs_panels`, `table`, `empty_state`, `infinite_scroll`
- **Posts and replies:** `post_card`, `comment`, `comment_thread`,
  `rendered_content`, `card`, `media_object`
- **Actions and reactions:** `action_bar`, `icon_btn`, `btn`, `share_menu`,
  `reaction_pill`, `message_reactions`
- **Identity and state:** `avatar`, `badge`, `counter_badge`,
  `notification_dot`, `stat`, `description_list`, `timeline`
- **Governance:** `callout`, `alert`, `confirm_dialog`, `form`,
  `action_strip`, `toast`, `accordion`

The gap is a forum-site recipe layer:

- how to build community homes, topic lists, thread pages, Q&A answer sets,
  vote/reaction controls, highlighted posts, composer forms, moderation queues,
  member identity, and activity feeds without utility classes;
- where `resource_card`, `post_card`, and `comment` are enough, and where a
  dedicated topic or answer macro might be justified later;
- how to keep policy, ranking, permissions, trust, and sanitization app-owned
  while documenting safe ChirpUI structure.

---

## Non-Goals

- Do not copy Reddit, Discourse, Stack Overflow, or GitHub brand treatment.
- Do not add utility classes or raw CSS values.
- Do not add new forum tokens, variants, or sizes in this plan.
- Do not add ranking, voting, reputation, trust-level, permission, or moderation
  logic to ChirpUI.
- Do not add a Markdown parser or sanitizer to ChirpUI.
- Do not introduce new `Markup` or `| safe` paths for user posts/comments.
- Do not promote `topic_card`, `answer_card`, or `vote_control` until recipe
  usage proves repeated friction.

---

## Proposed Pattern Recipes

1. **Community Home** - community identity, rules, categories, stats, and latest
   discussions using `page_header`, `route_tabs`, `resource_index`, `stat`, and
   `callout`.
2. **Topic List and Category View** - searchable, filterable lists using
   `resource_index`, `filter_chips`, `resource_card`, `table`, `badge`, and
   `counter_badge`.
3. **Thread Page** - root post plus replies using `post_card`,
   `rendered_content`, `action_bar`, `share_menu`, `comment_thread`, and
   `comment`.
4. **Q&A Answer Set** - question, answer, accepted/recommended, closed, and
   duplicate states using `post_card`, `card`, `badge`, and `callout`.
5. **Votes, Reactions, and Karma** - vote controls and reaction rows using
   `action_bar`, `icon_btn`, `counter_badge`, `stat`, `reaction_pill`, and
   `message_reactions`.
6. **Pinned and Announcement Posts** - sticky posts, incident threads, and
   highlights using `carousel`, `resource_card`, `post_card`, `badge`, and
   `callout`.
7. **Composer and Edit Flow** - ask/reply/edit/report flows using `form`,
   field macros, `tabs_panels`, `rendered_content`, `callout`, and
   `inline_edit_field`.
8. **Moderation Queue** - reported content, approvals, removals, locks, moves,
   and history using `resource_index`, `table`, `badge`, `action_strip`,
   `confirm_dialog`, `timeline`, and `toast`.
9. **Member Identity and Trust** - author identity, flair, moderator labels,
   reputation, badges, and privacy-aware profile summaries using `avatar`,
   `badge`, `stat`, `description_list`, and `timeline`.
10. **Notifications, Inbox, and Activity** - mentions, replies, follows,
    private messages, moderation events, and digest feeds using
    `conversation_item`, `timeline`, `notification_dot`, `counter_badge`,
    `message_thread`, `message_bubble`, and `empty_state`.

Detailed recipes live in `docs/FORUM-SITE-PATTERNS.md`.

---

## Implementation Plan

### Phase 1: Document Recipes (completed 2026-05-02)

Add forum-site recipes to docs without changing component APIs.

| File | Action |
|------|--------|
| `docs/FORUM-SITE-PATTERNS.md` | Added recipe documentation for community homes, topic lists, threads, Q&A, votes/reactions, pinned posts, composers, moderation, member identity, and activity |
| `docs/PRIMITIVES.md` | Added a short forum-site compositions pointer |
| `docs/INDEX.md` | Indexed the recipe doc under Patterns |
| `docs/plans/PLAN-forum-site-patterns-from-communities.md` | Keep this plan as the active roadmap |

**Done when:**

- Docs show how to build each pattern from existing registry-cited components.
- No new classes, variants, tokens, or macro params are introduced.
- Recipes call out where apps own ranking, moderation, permissions, trust, and
  sanitization logic.

### Phase 2: Build a Showcase Fixture (completed 2026-05-03)

Create one internal showcase page that exercises the recipes against realistic
placeholder forum data.

Implemented locations:

- `tests/browser/templates/forum_site_patterns.html`
- `tests/browser/test_forum_site_patterns.py`
- `/forum-site-patterns` route in `tests/browser/app.py`

**Done when:**

- The page renders community home, topic list, thread, Q&A, moderation, and
  activity recipes with realistic placeholder data.
- Browser tests verify no mobile horizontal overflow.
- The fixture uses only existing public macros and component classes.
- The thread layout proves long titles, nested replies, and action rows at phone
  and desktop widths.
- The fixture includes Elbysodic-shaped PBP pressure points: local route tabs,
  dense scene cards, scene/read/management action separation, Q&A accepted
  state, moderation queue, and compact writer-desk activity.

### Phase 3: Promote Repeated Recipes (decision checkpoint 2026-05-03)

After the docs recipe and showcase have at least one real consumer, decide
whether any pattern deserves a macro.

#### Elbysodic consumer pass

Elbysodic is the first real PBP-shaped consumer to pressure-test these recipes.
Its current thread pages separate orientation, reading, acting, management, and
continuation controls well, but the functionality is spread across app-local
thread-card, scene-header, post-frame, activity, and toolbar markup.

Try these migrations before proposing new chirp-ui APIs:

| Elbysodic surface | First ChirpUI mapping | Keep app-owned for now |
|-------------------|-----------------------|------------------------|
| Thread list cards | `resource_card` title/content/media/actions slots, `badge`, `inline_counter`, `linked_avatar_stack`, `latest_line` | Scene Slate poster treatment, board-specific premise copy, per-game state rules |
| Thread page header | `card`/`surface`, `section_header`, `cluster`, `badge`, `action_bar`, plus a recipe-level management disclosure | Place-path semantics, story timeline copy, GM-only controls |
| Transcript skim nav | Existing route/local navigation recipe plus anchors | Exact sticky behavior and scene-specific headings |
| Activity and inbox rows | `resource_card`, `latest_line`, `inline_counter`, `badge` | Read/unread delivery semantics and privacy rules |
| Posts and replies | `post_card`, `comment_thread`, `rendered_content`, `action_bar` | Character portrait treatment, actor/GM identity rules, composer shell |

The first pass should migrate one Elbysodic surface without adding public
chirp-ui macros, then record where markup becomes genuinely repetitive or
awkward. `scene_header`, `topic_card`, `post_frame`, and `inline_filter_rail`
remain app-local or recipe-only until that migration produces a concrete slot
sketch, repeated emitted classes, and browser evidence across phone and desktop
widths.

The first browser fixture did **not** justify a new public forum component yet.
It showed that `resource_card`, `badge`, `inline_counter`, `latest_line`,
`linked_avatar_stack`, `post_card`, `comment_thread`, `rendered_content`, and
`action_bar` can express dense community and play-by-post surfaces without
page-local utility classes. The only immediate friction was action icon
ergonomics: forum/social action rows had to pass raw glyphs or plain words into
`action_bar_item`. That was handled by resolving `action_bar_item(icon=...)`
through the existing icon registry and adding semantic action names.

Candidate macros, gated by evidence:

| Candidate | Default answer | Promotion trigger |
|-----------|----------------|-------------------|
| `topic_card` | Not yet | `resource_card` cannot express title, author, category, labels, replies, views, and latest activity without repeated local structure across at least two real pages |
| `vote_control` | Not yet | Vote buttons, score states, hidden scores, and permission notices repeat across posts and comments after app-owned scoring semantics are known |
| `thread_layout` | Recipe only | Root post plus replies plus composer needs stable anchors and responsive affordances |
| `answer_card` | Not yet | Accepted/recommended/closed Q&A states repeat across several pages and need structure beyond `card` + `badge` |
| `moderation_queue_item` | Not yet | Report source, rule, target content, actions, and history repeat in review tools beyond `resource_card` |
| `community_header` | Recipe only | Community identity, rules, counts, and membership actions repeat across apps |
| `flair_badge` | Recipe only | Badge plus search/filter behavior becomes common enough to deserve registry coverage |

Current conclusion: continue polishing existing components and recipes. Do not
promote `topic_card`, `vote_control`, `answer_card`, or
`moderation_queue_item` on the fixture alone.

**Done when:**

- Any promoted macro has a `ComponentDescriptor`.
- Emitted classes are in the registry and matching CSS partial.
- Template doc-block, tests, and manifest projection are updated.
- `COMPONENT-OPTIONS.md` documents new params only after the API is real.

### Phase 4: Polish Existing Components

Only after recipe validation, refine existing components where the recipe exposes
friction.

Possible refinements:

- `resource_card`: verified by fixture for topic and moderation cards; revisit
  after real app pages repeat the same slot choreography.
- `post_card`: verify root-post action and media slots cover forum posts.
- `comment` / `comment_thread`: verify reply nesting and action rows remain
  accessible.
- `action_bar` / `icon_btn`: action rows can now use semantic registry icons
  such as `reply`, `up`, `down`, `watch`, `follow`, `report`, and `share`
  without custom classes.
- `resource_index`: verify category/search/filter composition fits forum lists.
- `rendered_content`: verify docs clearly state upstream sanitization duties.
- `timeline`: verify moderation and activity history are readable at small
  widths.

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
- Include at least one long topic title, one locked thread, one accepted answer,
  one hidden-score state, one pinned post, one moderation queue item, and one
  member with flair.

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

- **Registry steward:** New forum macros require descriptors before CSS/classes ship.
- **Rendering steward:** Forum posts, comments, previews, and moderation notes
  must remain escaped unless sanitized upstream.
- **Theme steward:** Forum density and state labels should use existing tokens
  before proposing new ones.
- **Docs steward:** Recipes must describe shipped contracts, not aspirational APIs.
- **Planning steward:** Keep this plan active until recipes are documented or
  promoted into concrete component plans.
- **Site steward:** If exposed on the docs site, examples must render cleanly in
  the published site shell.
- **Accessibility:** Votes, accepted answers, pinned states, moderator labels,
  and hidden scores cannot be color-only.
- **Security:** Ranking, voting, permissions, moderation, trust, and
  sanitization logic belongs to the app, not ChirpUI.

---

## Not Now

- A full forum engine.
- Ranking, voting, reputation, trust-level, moderation, notification, or search
  backend logic.
- Brand-specific Reddit, Discourse, Stack Overflow, or GitHub visual mimicry.
- A Markdown parser, sanitizer, or rich text editor.
- A public `forum_*` namespace before usage evidence.
- A vote-control macro that assumes one platform's scoring semantics.
- A forum-specific utility class vocabulary.

---

## Open Questions

- Should future forum recipes stay in `docs/FORUM-SITE-PATTERNS.md`, or should
  proven overlap move into a shared community/social pattern doc?
- Is `topic_card` distinct enough from `resource_card` to justify promotion?
- Should `vote_control` be generic community feedback, or forum-specific?
- Can `comment_thread` cover nested discussions after browser fixture testing?
- Should moderation history lean on `timeline`, or does it need a review-specific
  item macro after real usage?
