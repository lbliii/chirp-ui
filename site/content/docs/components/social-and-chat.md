---
title: Social and chat
description: message_bubble, conversation_list, chat_input, typing_indicator
draft: false
weight: 24
lang: en
type: doc
keywords: [chirp-ui, chat, message]
icon: chats-circle
---

# Social and chat

Components for real-time messaging, threaded comments, and social interactions. Templates live under `chirpui/`.

## Quick reference

| Template | Macro(s) | Role |
|----------|----------|------|
| `chat_layout.html` | `chat_layout` | Full chat page structure |
| `chat_input.html` | `chat_input` | Message composer form |
| `message_bubble.html` | `message_bubble` | Single chat message |
| `message_thread.html` | `message_thread` | Vertical stack of messages |
| `conversation_list.html` | `conversation_list` | Sidebar conversation list |
| `conversation_item.html` | `conversation_item` | Conversation row |
| `comment.html` | `comment`, `comment_thread` | Nested comments |
| `mention.html` | `mention` | @username inline link |
| `reaction_pill.html` | `reaction_pill`, `message_reactions` | Emoji reaction buttons |
| `typing_indicator.html` | `typing_indicator` | Animated typing dots |
| `share_menu.html` | `share_menu` | Social share dropdown |

---

## Chat layout

`chat_layout` provides the top-level page structure for a chat view. Use `fill=true` for full-viewport-height layouts.

```text
chat_layout(show_activity=false, cls="", fill=false)
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `show_activity` | `bool` | `false` | Show the activity/presence sidebar |
| `cls` | `str` | `""` | Extra CSS classes |
| `fill` | `bool` | `false` | Stretch to fill available height |

```text
{% call chat_layout(fill=true, show_activity=true) %}
  {# conversation list, message thread, etc. #}
{% endcall %}
```

---

## Chat input

Composer form for sending messages. Renders a `<form>` with a textarea and submit button.

```text
chat_input(action="", name="message", placeholder="Type a message...", rows=2, maxlength=none, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `action` | `str` | `""` | Form action URL |
| `name` | `str` | `"message"` | Textarea field name |
| `placeholder` | `str` | `"Type a message..."` | Placeholder text |
| `rows` | `int` | `2` | Visible textarea rows |
| `maxlength` | `int\|none` | `none` | Character limit |
| `cls` | `str` | `""` | Extra CSS classes |

```text
{{ chat_input(action="/api/messages", name="body", rows=3, maxlength=2000) }}
```

---

## Message bubble

A single chat message. Use `align` to position left (incoming) or right (outgoing), and `role` for visual variants.

```text
message_bubble(align="left", role="default", status=none, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `align` | `str` | `"left"` | `"left"` or `"right"` |
| `role` | `str` | `"default"` | `"default"`, `"user"`, `"assistant"`, `"system"` |
| `status` | `str\|none` | `none` | Delivery status (e.g. `"sent"`, `"delivered"`, `"read"`) |
| `cls` | `str` | `""` | Extra CSS classes |

```text
{% call message_bubble(align="right", role="user", status="delivered") %}
  Hello, world!
{% endcall %}

{% call message_bubble(align="left", role="assistant") %}
  Hi there! How can I help?
{% endcall %}
```

---

## Message thread

Vertical container for a sequence of `message_bubble` calls. Handles scroll and spacing.

```text
message_thread(cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cls` | `str` | `""` | Extra CSS classes |

```text
{% call message_thread() %}
  {% call message_bubble(align="left") %}First message{% endcall %}
  {% call message_bubble(align="right", role="user") %}Reply{% endcall %}
{% endcall %}
```

---

## Conversation list and item

Sidebar list of conversations. Each row is a `conversation_item`.

```text
conversation_list(cls="")
conversation_item(href, name, preview, time=none, unread=none, muted=false, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | `str` | required | Link to the conversation |
| `name` | `str` | required | Display name |
| `preview` | `str` | required | Last message preview text |
| `time` | `str\|none` | `none` | Timestamp label |
| `unread` | `int\|none` | `none` | Unread badge count |
| `muted` | `bool` | `false` | Dim the row for muted conversations |
| `cls` | `str` | `""` | Extra CSS classes |

```text
{% call conversation_list() %}
  {{ conversation_item(
      href="/chat/42",
      name="Alice",
      preview="See you tomorrow!",
      time="2m",
      unread=3
  ) }}
  {{ conversation_item(
      href="/chat/99",
      name="Team Updates",
      preview="Deploy finished.",
      muted=true
  ) }}
{% endcall %}
```

---

## Comments

Nested comment threads. `comment` renders a single comment with optional avatar and reply affordance. `comment_thread` wraps a list of comments.

```text
comment(author, time=none, href=none, avatar_src=none, avatar_initials=none, replies_url=none, replies_count=none, cls="")
comment_thread(cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `author` | `str` | required | Author display name |
| `time` | `str\|none` | `none` | Timestamp label |
| `href` | `str\|none` | `none` | Permalink for the comment |
| `avatar_src` | `str\|none` | `none` | Avatar image URL |
| `avatar_initials` | `str\|none` | `none` | Fallback initials when no image |
| `replies_url` | `str\|none` | `none` | HTMX URL to load replies |
| `replies_count` | `int\|none` | `none` | Number of replies to show |
| `cls` | `str` | `""` | Extra CSS classes |

```text
{% call comment_thread() %}
  {% call comment(author="Dana", time="5m ago", avatar_initials="DA", replies_count=2, replies_url="/comments/7/replies") %}
    Great write-up, thanks for sharing.
  {% endcall %}
  {% call comment(author="Eli", time="1m ago", avatar_src="/avatars/eli.jpg") %}
    Agreed!
  {% endcall %}
{% endcall %}
```

---

## Mention

Inline @username link. Renders a styled anchor (or `<span>` when no `href`).

```text
mention(username, href=none, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `username` | `str` | required | Username to display (without `@`) |
| `href` | `str\|none` | `none` | Profile link |
| `cls` | `str` | `""` | Extra CSS classes |

```text
Hey {{ mention("alice", href="/u/alice") }}, take a look at this.
```

---

## Reaction pill

Emoji reaction button with count. Wrap multiple pills in `message_reactions`.

```text
reaction_pill(emoji, count=1, active=false, cls="")
message_reactions(cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `emoji` | `str` | required | Emoji character |
| `count` | `int` | `1` | Reaction count |
| `active` | `bool` | `false` | Highlight as the current user's reaction |
| `cls` | `str` | `""` | Extra CSS classes |

```text
{% call message_reactions() %}
  {{ reaction_pill(emoji="👍", count=4, active=true) }}
  {{ reaction_pill(emoji="🎉", count=2) }}
{% endcall %}
```

---

## Typing indicator

Animated dots that signal another user is typing. Typically injected via HTMX or SSE.

```text
typing_indicator(cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cls` | `str` | `""` | Extra CSS classes |

```text
{{ typing_indicator() }}
```

---

## Share menu

Dropdown with common share targets (copy link, email, social). Pass `share_url` to override the current page URL.

```text
share_menu(label="Share", share_url=none, cls="")
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `label` | `str` | `"Share"` | Button label text |
| `share_url` | `str\|none` | `none` | URL to share (defaults to current page) |
| `cls` | `str` | `""` | Extra CSS classes |

```text
{{ share_menu(share_url="https://example.com/post/42") }}
```

---

## Related

- [Streaming](./streaming.md) — SSE message streaming
- [Avatars and media](./avatars-and-media.md) — avatar components used in comments and conversations
- [Layout](./layout.md) — `chat_layout` uses `fill` layout patterns
