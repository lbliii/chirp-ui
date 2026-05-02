# Forum Site Patterns

ChirpUI already has enough shipped surface to compose forum, Q&A, discussion,
community-support, and threaded-comment pages. Use these recipes before adding a
new `forum_*` component namespace. The job is to make conversations legible,
governable, and safe while keeping app-owned policy, ranking, moderation, and
permissions outside ChirpUI.

These patterns come from a 2026 review of Reddit, Discourse, Stack Overflow,
and GitHub Discussions. The lesson is structural: forum-shaped products are not
just feeds. They combine discovery, participation, identity, governance,
moderation, and durable knowledge retrieval.

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

## Existing Surface

Start with these shipped primitives and components:

- **Shell and navigation:** `app_shell`, `site_shell`, `site_header`,
  `route_tabs`, `nav_tree`, `breadcrumbs`, `split_layout`
- **Discovery and lists:** `resource_index`, `resource_card`, `filter_chips`,
  `tabs_panels`, `table`, `empty_state`, `infinite_scroll`
- **Posts and threads:** `post_card`, `comment`, `comment_thread`,
  `rendered_content`, `card`, `media_object`
- **Conversation tools:** `action_bar`, `icon_btn`, `btn`, `share_menu`,
  `reaction_pill`, `message_reactions`, `chat_layout`, `message_thread`
- **State and identity:** `avatar`, `badge`, `counter_badge`,
  `notification_dot`, `stat`, `description_list`, `timeline`
- **Governance and safety:** `callout`, `alert`, `confirm_dialog`, `form`,
  `action_strip`, `toast`, `accordion`

App code owns ranking, voting math, reputation, permissions, policy,
moderation decisions, markdown sanitization, notification delivery, and
anti-abuse logic. ChirpUI owns the safe, responsive HTML structure around those
decisions.

---

## Community Home

Use this for a subreddit-like, Discourse-like, or GitHub Discussions-like
community landing page: explain the community, show rules/state, expose
categories, and route users into topic lists.

Compose from:

- `app_shell` or `site_shell`
- `page_hero` or `entity_header`
- `route_tabs` or `tabs_panels`
- `resource_index`
- `resource_card`
- `callout` for visibility, rules, or posting restrictions
- `stat` for member, topic, answer, or activity counts

```kida
{% call stack(gap="lg") %}
  {{ page_header(community.name, subtitle=community.summary) }}
  {% call callout(variant="info", title=community.visibility_label) %}
    {{ community.visibility_help }}
  {% end %}

  {% call resource_index(
    title="Discussions",
    search_action="/community/search",
    query=q,
    results_title="Latest topics",
  ) %}
    ...topic cards or rows...
  {% end %}
{% end %}
```

Checks:

- Community rules, visibility, and posting permissions are visible before the
  composer.
- Counts are labeled as current activity, members, replies, answers, or views.
- Empty communities include next actions: ask, introduce yourself, or read rules.
- Use route tabs for durable sections such as Discussions, Q&A, Announcements,
  Tags, Members, and Moderation.

---

## Topic List and Category View

Use this for category pages, tag pages, search results, unanswered lists,
active/latest lists, or saved views.

Compose from:

- `resource_index`
- `filter_chips`
- `resource_card` for card lists
- `table` for dense moderation or Q&A listings
- `badge` for labels, solved, locked, pinned, staff, or needs-review states
- `counter_badge` for replies, unread, or new activity

```kida
{% call resource_index(
  title="Questions",
  search_action="/questions",
  query=q,
  results_title="Active questions",
  results_layout="stack",
) %}
  {% for topic in topics %}
    {% call resource_card(topic.href, topic.title, description=topic.excerpt) %}
      {% slot badges %}
        {{ badge(topic.category) }}
        {% if topic.answered %}{{ badge("answered", variant="success") }}{% end %}
      {% end %}
      {% slot footer %}
        {{ topic.reply_count }} replies / {{ topic.last_activity }}
      {% end %}
    {% end %}
  {% endfor %}
{% end %}
```

Checks:

- Filters describe user intent: latest, active, unanswered, solved, pinned,
  category, tag, or mine.
- Do not use color alone for solved, locked, restricted, or moderator states.
- Rows expose title, author/community, activity, reply/answer count, and labels.
- Infinite scroll must preserve a reachable search/filter path.

---

## Thread Page

Use this for one canonical discussion, post, or topic page.

Compose from:

- `post_card` for the root post
- `rendered_content` for sanitized post bodies
- `action_bar` and `share_menu` for visible actions
- `comment_thread` and `comment` for replies
- `message_reactions` for compact reaction rows
- `callout` for locked, archived, private, or moderation notices

```kida
{% call stack(gap="lg") %}
  {% call post_card(name=post.author, handle=post.handle, time=post.time, href=post.author_href) %}
    {% call rendered_content() %}
      {{ post.body_html }}
    {% end %}
    {% slot actions %}
      ...vote, reply, save, share, report...
    {% end %}
  {% end %}

  {% call comment_thread() %}
    {% for reply in replies %}
      {% call comment(author=reply.author, time=reply.time, avatar_src=reply.avatar) %}
        {% call rendered_content() %}{{ reply.body_html }}{% end %}
        {% slot actions %}...reply, react, report...{% end %}
      {% end %}
    {% endfor %}
  {% end %}
{% end %}
```

Checks:

- Post and reply bodies must be sanitized upstream before rendering as trusted
  HTML. Do not introduce new `| safe` escape hatches in recipes.
- Locked, archived, removed, or moderator-only states appear before reply forms.
- Reply actions are reachable by keyboard and are not icon-only without labels.
- Long threads need anchors, sort controls, or "new since last visit" markers.

---

## Q&A Answer Set

Use this for Stack Overflow-like question pages or GitHub Discussions categories
with answer selection.

Compose from:

- `post_card` for the question
- `comment` or `card` for answers
- `badge` for accepted, answered, recommended, staff, or needs-detail states
- `action_bar` for vote/comment/share/report actions
- `callout` for closed, duplicate, migrated, or needs-edit states

```kida
{% call post_card(name=question.author, time=question.time) %}
  {% call rendered_content() %}{{ question.body_html }}{% end %}
  {% slot actions %}...vote, follow, share...{% end %}
{% end %}

{% for answer in answers %}
  {% call card(title=answer.author) %}
    {% if answer.accepted %}{{ badge("accepted", variant="success") }}{% end %}
    {% call rendered_content() %}{{ answer.body_html }}{% end %}
  {% end %}
{% endfor %}
```

Checks:

- Accepted/recommended answers are labels, not just sort position or color.
- Closed or duplicate status explains what changed and where to go next.
- Comments for clarification are visually secondary to full answers.
- Sort controls make clear whether answers are ordered by votes, activity, or
  accepted state.

---

## Votes, Reactions, and Karma

Use this when posts or replies need community ranking, lightweight feedback, or
reputation-adjacent display.

Compose from:

- `action_bar`
- `icon_btn`
- `badge`, `counter_badge`, or `stat`
- `reaction_pill` and `message_reactions`
- `toast` for post-action feedback

```kida
{% call action_bar() %}
  {{ icon_btn("arrow-up", aria_label="Upvote", hx={"post": post.upvote_url, "target": "#vote-score"}) }}
  {{ counter_badge("vote-score", count=post.score) }}
  {{ icon_btn("arrow-down", aria_label="Downvote", hx={"post": post.downvote_url, "target": "#vote-score"}) }}
{% end %}
```

Checks:

- Vote count, hidden score, contest mode, and score fuzzing are app-owned states.
- The UI explains when voting is unavailable, hidden, or permission-gated.
- Positive and negative feedback are not represented by color alone.
- Reputation and trust-level calculations do not live in ChirpUI.

---

## Pinned, Highlighted, and Announcement Posts

Use this for sticky posts, community highlights, release announcements,
incident threads, and moderator notices.

Compose from:

- `carousel` for small highlight sets
- `resource_card` or `post_card`
- `badge` for pinned, announcement, incident, event, solved, or closed states
- `callout` for policy or visibility messages

```kida
{% call carousel(variant="compact", slide_count=highlights|length) %}
  {% for item in highlights %}
    {% call carousel_slide(loop.index) %}
      {% call resource_card(item.href, item.title, description=item.summary) %}
        {% slot badges %}{{ badge(item.kind) }}{% end %}
      {% end %}
    {% end %}
  {% endfor %}
{% end %}
```

Checks:

- Pinned content must not hide the normal latest/active list.
- Announcement, incident, event, and megathread labels are real text.
- Closed or archived highlights still explain their status.
- Highlight order belongs to app or moderator logic.

---

## Composer and Edit Flow

Use this for asking, replying, editing, reporting, and moderator action forms.

Compose from:

- `form`
- field macros from `forms.html`
- `rendered_content` for preview output after app sanitization
- `tabs_panels` for Write / Preview
- `callout` for rules, duplicate checks, AI/content policy, or rate limits
- `inline_edit_field` for small title/flair edits

```kida
{% call form("/topics", hx_post="/topics", hx_target="#composer-result") %}
  {% call callout(variant="info", title="Before posting") %}
    Read the community rules and add the most specific tags you can.
  {% end %}
  ...title, body, category, flair, and submit fields...
{% end %}
```

Checks:

- Community rules and required fields are visible before submission.
- Preview HTML is sanitized by the app before `rendered_content`.
- Errors tell the user how to repair the post.
- Mod-only actions use confirmations for destructive changes.

---

## Moderation Queue

Use this for reported posts, pending posts, spam review, approvals, removals,
locks, moves, merges, and user-management queues.

Compose from:

- `table` or `resource_index`
- `badge`
- `action_strip`
- `confirm_dialog`
- `callout`
- `timeline` for moderation history
- `toast` for result feedback

```kida
{% call resource_index(
  title="Moderation queue",
  search_action="/moderation",
  results_title="Needs review",
) %}
  ...reported content rows with approve, remove, lock, and escalate actions...
{% end %}
```

Checks:

- Action reasons are visible before irreversible actions.
- Bulk actions require confirmation when destructive.
- Report source, rule, target content, and moderator history are distinct.
- Moderation permissions and policy decisions stay app-owned.

---

## Member Identity and Trust

Use this for author chips, profile summaries, moderator labels, badges,
reputation, trust levels, flair, and member-role indicators.

Compose from:

- `avatar`
- `badge`
- `description_list`
- `stat`
- `timeline`
- `resource_card` for member directory rows

```kida
{% call resource_card(user.href, user.name, description=user.summary) %}
  {% slot badges %}
    {% if user.moderator %}{{ badge("moderator", variant="success") }}{% end %}
    {% if user.flair %}{{ badge(user.flair) }}{% end %}
  {% end %}
  {% slot footer %}
    {{ user.reputation }} reputation / {{ user.joined }}
  {% end %}
{% end %}
```

Checks:

- Moderator/staff labels are explicit text.
- Flair distinguishes people or content without replacing accessible labels.
- Reputation, karma, or trust numbers are app-owned and contextual.
- Privacy controls determine what profile activity is shown.

---

## Notifications, Inbox, and Activity

Use this for replies, mentions, followed topics, moderation events, answer
acceptance, badges earned, private messages, or digest feeds.

Compose from:

- `conversation_item`
- `timeline`
- `notification_dot`
- `counter_badge`
- `message_thread`
- `message_bubble`
- `empty_state`

```kida
{% call timeline(items=activity_items, hoverable=true) %}
{% end %}
```

Checks:

- Unread state is text or aria-visible, not only a dot.
- Mentions, replies, moderator actions, and system events are distinguishable.
- Private messages should not reuse public-thread affordances by accident.
- Notification delivery and read/unread state are app-owned.

---

## Promotion Gates

Keep these as recipes until real pages prove repeated markup is fragile or hard
to keep accessible.

| Candidate | Default | Promote only when |
|-----------|---------|-------------------|
| `topic_card` | Maybe | `resource_card` cannot express topic metadata without repeated local structure |
| `vote_control` | Maybe | Vote buttons, score states, hidden scores, and permission notices repeat across posts and comments |
| `thread_layout` | Recipe | Root post plus replies plus composer needs stable anchors and responsive affordances |
| `answer_card` | Maybe | Accepted/recommended/closed Q&A states repeat across several pages |
| `moderation_queue_item` | Maybe | Report source, rule, target, actions, and history repeat in review tools |
| `community_header` | Recipe | Community identity, rules, counts, and membership actions repeat across apps |
| `flair_badge` | Recipe | Badge plus search/filter behavior becomes common enough to deserve registry coverage |

Any promoted macro needs a descriptor, emitted-class coverage, CSS partials,
template docs, manifest projection, and browser coverage before it ships.
