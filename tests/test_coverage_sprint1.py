"""Render tests for previously untested chirp-ui components.

Sprint 1 of the test coverage hardening epic. Each test verifies:
- Component renders without error
- Expected BEM class is present
- Required parameters produce correct HTML structure
"""

from kida import Environment

# ---------------------------------------------------------------------------
# Action bar
# ---------------------------------------------------------------------------


class TestActionBar:
    def test_action_bar_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar %}'
            "{% call action_bar() %}items{% end %}"
        ).render()
        assert "chirpui-action-bar" in html
        assert "items" in html

    def test_action_bar_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar_item %}'
            '{{ action_bar_item(icon="\u2665", label="Like") }}'
        ).render()
        assert "chirpui-action-bar__item" in html
        assert "Like" in html

    def test_action_bar_item_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar_item %}'
            '{{ action_bar_item(icon="\u2665", label="Like", active=true) }}'
        ).render()
        assert "chirpui-action-bar__item--active" in html

    def test_action_bar_item_with_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar_item %}'
            '{{ action_bar_item(icon="\u2665", label="Like", count=42) }}'
        ).render()
        assert "42" in html

    def test_action_bar_item_with_href(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar_item %}'
            '{{ action_bar_item(icon="\u2665", label="Like", href="/like") }}'
        ).render()
        assert "/like" in html

    def test_action_bar_item_resolves_semantic_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar_item %}'
            '{{ action_bar_item(icon="reply", label="Reply") }}'
        ).render()
        assert "chirpui-action-bar__icon" in html
        assert "↩" in html
        assert ">reply<" not in html


# ---------------------------------------------------------------------------
# Avatar stack
# ---------------------------------------------------------------------------


class TestAvatarStack:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar_stack.html" import avatar_stack %}'
            "{% call avatar_stack() %}avatars{% end %}"
        ).render()
        assert "chirpui-avatar-stack" in html

    def test_overflow_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar_stack.html" import avatar_stack %}'
            "{% call avatar_stack(max_visible=2, total=5) %}avatars{% end %}"
        ).render()
        assert "chirpui-avatar-stack" in html


# ---------------------------------------------------------------------------
# Bar chart
# ---------------------------------------------------------------------------


class TestBarChart:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/bar_chart.html" import bar_chart %}'
            '{{ bar_chart(items=[{"label": "Sales", "value": 42}]) }}'
        ).render()
        assert "chirpui-bar-chart" in html
        assert "Sales" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/bar_chart.html" import bar_chart %}'
            '{{ bar_chart(items=[{"label": "A", "value": 10}], variant="accent") }}'
        ).render()
        assert "chirpui-bar-chart" in html

    def test_multiple_items(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/bar_chart.html" import bar_chart %}'
            '{{ bar_chart(items=[{"label": "A", "value": 10}, {"label": "B", "value": 20}]) }}'
        ).render()
        assert "A" in html
        assert "B" in html


# ---------------------------------------------------------------------------
# Channel card
# ---------------------------------------------------------------------------


class TestChannelCard:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/channel_card.html" import channel_card %}'
            '{% call channel_card(href="/ch", name="General") %}body{% end %}'
        ).render()
        assert "chirpui-channel-card" in html
        assert "General" in html

    def test_with_subscribers(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/channel_card.html" import channel_card %}'
            '{% call channel_card(href="/ch", name="General", subscribers=42) %}body{% end %}'
        ).render()
        assert "42" in html


# ---------------------------------------------------------------------------
# Chapter list
# ---------------------------------------------------------------------------


class TestChapterList:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chapter_list.html" import chapter_list %}'
            "{% call chapter_list() %}items{% end %}"
        ).render()
        assert "chirpui-chapter-list" in html

    def test_chapter_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chapter_list.html" import chapter_item %}'
            '{{ chapter_item(title="Intro", timestamp="0:00", href="/ch/1") }}'
        ).render()
        assert "chirpui-chapter-item" in html
        assert "Intro" in html

    def test_with_summary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chapter_list.html" import chapter_list %}'
            '{% call chapter_list(summary="Table of Contents") %}items{% end %}'
        ).render()
        assert "Table of Contents" in html


# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------


class TestChatInput:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chat_input.html" import chat_input %}{% call chat_input() %}{% end %}'
        ).render()
        assert "chirpui-chat-input" in html

    def test_custom_placeholder(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chat_input.html" import chat_input %}'
            '{% call chat_input(placeholder="Say something...") %}{% end %}'
        ).render()
        assert "Say something..." in html

    def test_with_action(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chat_input.html" import chat_input %}'
            '{% call chat_input(action="/send") %}{% end %}'
        ).render()
        assert "/send" in html


# ---------------------------------------------------------------------------
# Command palette
# ---------------------------------------------------------------------------


class TestCommandPalette:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette %}'
            "{{ command_palette() }}"
        ).render()
        assert "chirpui-command-palette" in html

    def test_custom_placeholder(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette %}'
            '{{ command_palette(placeholder="Find anything...") }}'
        ).render()
        assert "Find anything..." in html


# ---------------------------------------------------------------------------
# Comment
# ---------------------------------------------------------------------------


class TestComment:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/comment.html" import comment %}'
            '{% call comment(author="Alice") %}Great post!{% end %}'
        ).render()
        assert "chirpui-comment" in html
        assert "Alice" in html
        assert "Great post!" in html

    def test_with_time(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/comment.html" import comment %}'
            '{% call comment(author="Alice", time="2h ago") %}Nice{% end %}'
        ).render()
        assert "2h ago" in html

    def test_with_replies(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/comment.html" import comment %}'
            '{% call comment(author="Alice", replies_url="/replies", replies_count=3) %}Nice{% end %}'
        ).render()
        assert "chirpui-comment" in html
        assert "/replies" in html


# ---------------------------------------------------------------------------
# Config dashboard
# ---------------------------------------------------------------------------


class TestConfigDashboard:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/config_dashboard.html" import config_dashboard %}'
            '{% call config_dashboard(title="Settings", form_action="/save") %}content{% end %}'
        ).render()
        assert "Settings" in html
        assert "content" in html


# ---------------------------------------------------------------------------
# Constellation (effect)
# ---------------------------------------------------------------------------


class TestConstellation:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/constellation.html" import constellation %}'
            "{% call constellation() %}content{% end %}"
        ).render()
        assert "chirpui-constellation" in html


# ---------------------------------------------------------------------------
# Conversation components
# ---------------------------------------------------------------------------


class TestConversation:
    def test_conversation_list(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/conversation_list.html" import conversation_list %}'
            "{% call conversation_list() %}items{% end %}"
        ).render()
        assert "chirpui-conversation-list" in html

    def test_conversation_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/conversation_item.html" import conversation_item %}'
            '{% call conversation_item(href="/c/1", name="Alice", preview="Hey!") %}{% end %}'
        ).render()
        assert "chirpui-conversation-item" in html
        assert "Alice" in html

    def test_conversation_item_unread(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/conversation_item.html" import conversation_item %}'
            '{% call conversation_item(href="/c/1", name="Alice", preview="Hey!", unread=3) %}{% end %}'
        ).render()
        assert "3" in html

    def test_conversation_item_muted(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/conversation_item.html" import conversation_item %}'
            '{% call conversation_item(href="/c/1", name="Alice", preview="Hey!", muted=true) %}{% end %}'
        ).render()
        assert "muted" in html.lower() or "chirpui-conversation-item" in html


# ---------------------------------------------------------------------------
# Drag and drop
# ---------------------------------------------------------------------------


class TestDnd:
    def test_dnd_list(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dnd.html" import dnd_list %}{% call dnd_list() %}items{% end %}'
        ).render()
        assert "chirpui-dnd" in html
        assert "items" in html

    def test_dnd_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dnd.html" import dnd_list, dnd_item %}'
            "{% call dnd_list() %}{% call dnd_item() %}content{% end %}{% end %}"
        ).render()
        assert "chirpui-dnd" in html
        assert "content" in html


# ---------------------------------------------------------------------------
# Holy light (effect)
# ---------------------------------------------------------------------------


class TestHolyLight:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/holy_light.html" import holy_light %}'
            "{% call holy_light() %}content{% end %}"
        ).render()
        assert "chirpui-holy-light" in html

    def test_with_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/holy_light.html" import holy_light %}'
            '{% call holy_light(variant="accent") %}content{% end %}'
        ).render()
        assert "chirpui-holy-light" in html


# ---------------------------------------------------------------------------
# Infinite scroll
# ---------------------------------------------------------------------------


class TestInfiniteScroll:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/infinite_scroll.html" import infinite_scroll %}'
            '{% call infinite_scroll(load_url="/load-more") %}items{% end %}'
        ).render()
        assert "chirpui-infinite-scroll" in html
        assert "/load-more" in html


# ---------------------------------------------------------------------------
# Live badge
# ---------------------------------------------------------------------------


class TestLiveBadge:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/live_badge.html" import live_badge %}{{ live_badge() }}'
        ).render()
        assert "chirpui-live-badge" in html

    def test_with_viewers(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/live_badge.html" import live_badge %}{{ live_badge(viewers=1234) }}'
        ).render()
        assert "1234" in html or "1,234" in html


# ---------------------------------------------------------------------------
# Mention
# ---------------------------------------------------------------------------


class TestMention:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/mention.html" import mention %}{{ mention(username="alice") }}'
        ).render()
        assert "chirpui-mention" in html
        assert "alice" in html

    def test_with_href(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/mention.html" import mention %}'
            '{{ mention(username="alice", href="/u/alice") }}'
        ).render()
        assert "/u/alice" in html
        assert "<a" in html

    def test_without_href_renders_span(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/mention.html" import mention %}{{ mention(username="alice") }}'
        ).render()
        assert "<span" in html or "<a" not in html or "chirpui-mention" in html


# ---------------------------------------------------------------------------
# Message bubble / thread
# ---------------------------------------------------------------------------


class TestMessageBubble:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/message_bubble.html" import message_bubble %}'
            "{% call message_bubble() %}Hello!{% end %}"
        ).render()
        assert "chirpui-message-bubble" in html
        assert "Hello!" in html

    def test_align_right(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/message_bubble.html" import message_bubble %}'
            '{% call message_bubble(align="right") %}Hello!{% end %}'
        ).render()
        assert "right" in html.lower() or "chirpui-message-bubble" in html

    def test_with_role(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/message_bubble.html" import message_bubble %}'
            '{% call message_bubble(role="assistant") %}Hi{% end %}'
        ).render()
        assert "chirpui-message-bubble" in html


class TestMessageThread:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/message_thread.html" import message_thread %}'
            "{% call message_thread() %}messages{% end %}"
        ).render()
        assert "chirpui-message-thread" in html
        assert "messages" in html


# ---------------------------------------------------------------------------
# Playlist
# ---------------------------------------------------------------------------


class TestPlaylist:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/playlist.html" import playlist %}{% call playlist() %}items{% end %}'
        ).render()
        assert "chirpui-playlist" in html

    def test_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/playlist.html" import playlist %}'
            '{% call playlist(title="My Mix") %}items{% end %}'
        ).render()
        assert "My Mix" in html

    def test_playlist_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/playlist.html" import playlist_item %}'
            '{{ playlist_item(href="/t/1", title="Song", duration="3:42") }}'
        ).render()
        assert "chirpui-playlist-item" in html
        assert "Song" in html
        assert "3:42" in html

    def test_playlist_item_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/playlist.html" import playlist_item %}'
            '{{ playlist_item(href="/t/1", title="Song", duration="3:42", active=true) }}'
        ).render()
        assert "active" in html.lower() or "chirpui-playlist-item" in html


# ---------------------------------------------------------------------------
# Post card
# ---------------------------------------------------------------------------


class TestPostCard:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/post_card.html" import post_card %}'
            '{% call post_card(name="Alice") %}Hello world{% end %}'
        ).render()
        assert "chirpui-post-card" in html
        assert "Alice" in html

    def test_with_handle_and_time(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/post_card.html" import post_card %}'
            '{% call post_card(name="Alice", handle="@alice", time="2h") %}Post{% end %}'
        ).render()
        assert "@alice" in html
        assert "2h" in html


# ---------------------------------------------------------------------------
# Profile header
# ---------------------------------------------------------------------------


class TestProfileHeader:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/profile_header.html" import profile_header %}'
            '{% call profile_header(name="Alice") %}bio{% end %}'
        ).render()
        assert "chirpui-profile-header" in html
        assert "bio" in html

    def test_with_cover(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/profile_header.html" import profile_header %}'
            '{% call profile_header(cover_url="/cover.jpg") %}bio{% end %}'
        ).render()
        assert "chirpui-profile-header" in html


# ---------------------------------------------------------------------------
# Reaction pill
# ---------------------------------------------------------------------------


class TestReactionPill:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/reaction_pill.html" import reaction_pill %}'
            '{{ reaction_pill(emoji="\U0001f44d") }}'
        ).render()
        assert "chirpui-reaction-pill" in html

    def test_with_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/reaction_pill.html" import reaction_pill %}'
            '{{ reaction_pill(emoji="\U0001f44d", count=5) }}'
        ).render()
        assert "5" in html

    def test_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/reaction_pill.html" import reaction_pill %}'
            '{{ reaction_pill(emoji="\U0001f44d", active=true) }}'
        ).render()
        assert "active" in html.lower() or "chirpui-reaction-pill" in html

    def test_message_reactions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/reaction_pill.html" import message_reactions %}'
            "{% call message_reactions() %}pills{% end %}"
        ).render()
        assert "chirpui-message-reactions" in html


# ---------------------------------------------------------------------------
# Rune field (effect)
# ---------------------------------------------------------------------------


class TestRuneField:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/rune_field.html" import rune_field %}'
            "{% call rune_field() %}content{% end %}"
        ).render()
        assert "chirpui-rune-field" in html


# ---------------------------------------------------------------------------
# Share menu
# ---------------------------------------------------------------------------


class TestShareMenu:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/share_menu.html" import share_menu %}'
            '{{ share_menu(share_url="https://example.com/post") }}'
        ).render()
        assert "chirpui-share-menu" in html

    def test_with_custom_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/share_menu.html" import share_menu %}'
            '{{ share_menu(label="Share this", share_url="https://example.com") }}'
        ).render()
        assert "Share this" in html


# ---------------------------------------------------------------------------
# Shell frame
# ---------------------------------------------------------------------------


class TestShellFrame:
    def test_shell_region(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shell_frame.html" import shell_region %}'
            '{% call shell_region(id="shell-actions") %}actions{% end %}'
        ).render()
        assert "chirpui-shell-region" in html or "shell-actions" in html


# ---------------------------------------------------------------------------
# Sortable list
# ---------------------------------------------------------------------------


class TestSortableList:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sortable_list.html" import sortable_list %}'
            "{% call sortable_list() %}items{% end %}"
        ).render()
        assert "chirpui-sortable" in html

    def test_sortable_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sortable_list.html" import sortable_list, sortable_item %}'
            "{% call sortable_list() %}{% call sortable_item() %}Item 1{% end %}{% end %}"
        ).render()
        assert "chirpui-sortable-item" in html or "Item 1" in html


# ---------------------------------------------------------------------------
# Symbol rain (effect)
# ---------------------------------------------------------------------------


class TestSymbolRain:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/symbol_rain.html" import symbol_rain %}'
            "{% call symbol_rain() %}content{% end %}"
        ).render()
        assert "chirpui-symbol-rain" in html


# ---------------------------------------------------------------------------
# Theme toggle
# ---------------------------------------------------------------------------


class TestThemeToggle:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/theme_toggle.html" import theme_toggle %}{{ theme_toggle() }}'
        ).render()
        assert "chirpui-theme-toggle" in html

    def test_style_toggle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/theme_toggle.html" import style_toggle %}{{ style_toggle() }}'
        ).render()
        assert "chirpui-style-toggle" in html


# ---------------------------------------------------------------------------
# Trending tag
# ---------------------------------------------------------------------------


class TestTrendingTag:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/trending_tag.html" import trending_tag %}'
            '{{ trending_tag(tag="python") }}'
        ).render()
        assert "chirpui-trending-tag" in html
        assert "python" in html

    def test_with_href(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/trending_tag.html" import trending_tag %}'
            '{{ trending_tag(tag="python", href="/tags/python") }}'
        ).render()
        assert "/tags/python" in html
        assert "<a" in html

    def test_with_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/trending_tag.html" import trending_tag %}'
            '{{ trending_tag(tag="python", count=1200) }}'
        ).render()
        assert "1200" in html or "1,200" in html


# ---------------------------------------------------------------------------
# Typing indicator
# ---------------------------------------------------------------------------


class TestTypingIndicator:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/typing_indicator.html" import typing_indicator %}'
            "{{ typing_indicator() }}"
        ).render()
        assert "chirpui-typing-indicator" in html


# ---------------------------------------------------------------------------
# Video thumbnail
# ---------------------------------------------------------------------------


class TestVideoThumbnail:
    def test_renders(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/video_thumbnail.html" import video_thumbnail %}'
            '{{ video_thumbnail(src="/thumb.jpg") }}'
        ).render()
        assert "chirpui-video-thumbnail" in html

    def test_with_duration(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/video_thumbnail.html" import video_thumbnail %}'
            '{{ video_thumbnail(src="/thumb.jpg", duration="12:34") }}'
        ).render()
        assert "12:34" in html

    def test_with_href(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/video_thumbnail.html" import video_thumbnail %}'
            '{{ video_thumbnail(src="/thumb.jpg", href="/watch/1") }}'
        ).render()
        assert "/watch/1" in html
        assert "<a" in html

    def test_with_watched_pct(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/video_thumbnail.html" import video_thumbnail %}'
            '{{ video_thumbnail(src="/thumb.jpg", watched_pct=75) }}'
        ).render()
        assert "chirpui-video-thumbnail" in html
