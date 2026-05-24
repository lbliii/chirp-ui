# Forum Site Patterns

Status: recipe guidance

Use these recipes for forum, Q&A, discussion, community-support, and threaded
comment pages before adding `forum_*` macros. Chirp UI owns safe, responsive
structure; app code owns ranking, votes, reputation, permissions, moderation
policy, markdown sanitization, notifications, and anti-abuse behavior.

## Starting Surface

| Area | Components |
|---|---|
| Shell and navigation | `app_shell`, `site_shell`, `site_header`, `route_tabs`, `nav_tree`, `breadcrumbs`, `split_layout` |
| Discovery and lists | `resource_index`, `resource_card`, `filter_chips`, `tabs_panels`, `table`, `empty_state`, `infinite_scroll` |
| Posts and threads | `post_card`, `comment`, `comment_thread`, `rendered_content`, `card`, `media_object`, `thread_reader_layout` |
| Conversation tools | `action_bar`, `icon_btn`, `btn`, `share_menu`, `reaction_pill`, `message_reactions`, `chat_layout`, `message_thread` |
| State and identity | `avatar`, `badge`, `counter_badge`, `notification_dot`, `stat`, `description_list`, `timeline`, `facet_chip` |
| Governance and safety | `callout`, `alert`, `confirm_dialog`, `form`, `action_strip`, `toast`, `accordion` |
| Detail surfaces | `detail_header` for community, category, title, or thread orientation |

## Recipe Matrix

| Pattern | Use When | Compose With | Checks |
|---|---|---|---|
| Community home | A community landing page needs identity, rules, visibility, categories, and routes into lists. | `app_shell`, `site_shell`, `detail_header`, `page_hero`, `route_tabs`, `resource_index`, `resource_card`, `facet_chip`, `callout`, `stat`. | Rules and permissions appear before composer; counts are labelled; empty communities offer next actions. |
| Topic list and category view | Category, tag, search, unanswered, active/latest, or saved-view lists. | `resource_index`, `filter_chips`, `facet_chip`, `resource_card`, `table`, `badge`, `counter_badge`. | Rows expose title, author/community, activity, counts, and labels; state is not color-only. |
| Thread page | One canonical discussion, post, or topic page. | `thread_reader_layout`, `detail_header`, `post_card`, `rendered_content`, `action_bar`, `share_menu`, `comment_thread`, `comment`, `message_reactions`, `callout`. | Bodies are sanitized upstream; locked/archived/moderator-only states appear before reply forms; long threads expose anchors or sort controls. |
| Q&A answer set | Stack Overflow-like questions or accepted-answer discussions. | `post_card`, `comment`, `card`, `badge`, `action_bar`, `callout`. | Accepted answers use labels; closed/duplicate status explains next steps; comments stay secondary. |
| Votes, reactions, and karma | Posts or replies need community ranking, feedback, or reputation display. | `action_bar`, `icon_btn`, `badge`, `counter_badge`, `stat`, `reaction_pill`, `message_reactions`, `toast`. | Score math and hidden/permission states are app-owned; positive/negative feedback is not color-only. |
| Pinned, highlighted, announcements | Sticky posts, highlights, incidents, releases, events, or moderator notices. | `carousel`, `resource_card`, `post_card`, `badge`, `callout`. | Highlights do not hide the normal list; labels are text; closed/archived state is explained. |
| Composer and edit flow | Asking, replying, editing, reporting, and moderator action forms. | `form`, field macros, `rendered_content`, `tabs_panels`, `callout`, `inline_edit_field`. | Rules and required fields appear before submit; preview HTML is sanitized; destructive actions confirm. |
| Moderation queue | Reports, pending posts, spam review, approvals, removals, locks, moves, merges, or user-management queues. | `table`, `resource_index`, `badge`, `action_strip`, `confirm_dialog`, `callout`, `timeline`, `toast`. | Reason, source, target, history, and actions are distinct; destructive bulk actions confirm. |
| Member identity and trust | Author chips, profile summaries, moderator labels, badges, reputation, trust levels, flair, and roles. | `avatar`, `badge`, `description_list`, `stat`, `timeline`, `resource_card`. | Staff/moderator labels are explicit; reputation is contextual and app-owned; privacy controls apply. |
| Notifications, inbox, activity | Replies, mentions, followed topics, moderation events, accepted answers, badges, messages, or digests. | `conversation_item`, `timeline`, `notification_dot`, `counter_badge`, `message_thread`, `message_bubble`, `empty_state`. | Unread state is not only a dot; system, moderation, mention, and reply events are distinguishable. |

## Thread Skeleton

```kida
{% call thread_reader_layout(label=thread.title) %}
  {% slot header %}
    {% call detail_header(thread.title, summary=thread.summary, eyebrow=thread.category) %}
      {% slot badges %}
        {% for tag in thread.tags %}
          {{ facet_chip(tag.label, href=tag.href, selected=tag.selected) }}
        {% endfor %}
      {% end %}
    {% end %}
  {% end %}

  {% slot posts %}
    {% call post_card(name=post.author, handle=post.handle, time=post.time) %}
      {% call rendered_content() %}
        {{ post.body_html }}
      {% end %}
    {% end %}

    {% call comment_thread() %}...replies...{% end %}
  {% end %}
{% end %}
```

## Promotion Gates

| Candidate | Default | Promote only when |
|---|---|---|
| `topic_card` | Built | Topic metadata, counters, state, and latest activity need a reusable default. |
| `vote_control` | Not yet | Vote buttons, score states, hidden scores, and permission notices repeat after scoring semantics are known. |
| `thread_reader_layout` | Built | Root post plus replies plus composer needs stable reader regions without owning ranking or composer behavior. |
| `answer_card` | Built | Accepted/closed answer state needs a readable default without owning Q&A logic. |
| `moderation_queue_item` | Built | Report reason, target, state, and review actions need a reusable default. |
| `detail_header` | Built | Community, thread, title, and product orientation need a reusable detail surface. |
| `facet_chip` | Built | Badge plus selected/search/filter behavior needs a compact default without owning filter state. |

Elbysodic is the first real consumer pass. Start with one surface, not a new
Chirp UI macro: thread-list cards, thread page header, transcript skim
navigation, activity rows, or posts/replies. Keep play-by-post semantics,
character portraits, staff controls, composer behavior, and delivery/privacy in
the app until the same slot shape repeats across real pages.

A promoted macro needs a descriptor, emitted-class coverage, CSS partials,
template docs, manifest projection, and browser coverage.
