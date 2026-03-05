"""Render tests for all chirp-ui components.

Each test verifies:
- Correct HTML structure (BEM classes present)
- Parameter variants (defaults, optional args)
- Slot content injection where applicable
"""

from kida import Environment

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------


class TestLayout:
    def test_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import container %}'
            "{% call container() %}Content{% end %}"
        ).render()
        assert "chirpui-container" in html
        assert "Content" in html

    def test_grid(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}{% call grid() %}A{% end %}'
        ).render()
        assert "chirpui-grid" in html

    def test_grid_cols_2(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}{% call grid(cols=2) %}A{% end %}'
        ).render()
        assert "chirpui-grid--cols-2" in html

    def test_grid_gap_sm(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}{% call grid(gap="sm") %}A{% end %}'
        ).render()
        assert "chirpui-grid--gap-sm" in html

    def test_grid_gap_md(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}{% call grid(gap="md") %}A{% end %}'
        ).render()
        assert "chirpui-grid--gap-md" in html

    def test_grid_gap_lg(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}{% call grid(gap="lg") %}A{% end %}'
        ).render()
        assert "chirpui-grid--gap-lg" in html

    def test_grid_cols_and_gap(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(cols=3, gap="md") %}A{% end %}'
        ).render()
        assert "chirpui-grid--cols-3" in html
        assert "chirpui-grid--gap-md" in html

    def test_stack(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import stack %}{% call stack() %}A{% end %}'
        ).render()
        assert "chirpui-stack" in html

    def test_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import block %}{% call block(span=2) %}A{% end %}'
        ).render()
        assert "chirpui-block--span-2" in html

    def test_page_header(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import page_header %}'
            '{{ page_header("Title", subtitle="Subtitle text") }}'
        ).render()
        assert "chirpui-page-header" in html
        assert "chirpui-stack" in html
        assert "<h1>Title</h1>" in html
        assert "Subtitle text" in html

    def test_page_header_no_subtitle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import page_header %}{{ page_header("Title") }}'
        ).render()
        assert "<h1>Title</h1>" in html
        assert "chirpui-text-muted" not in html

    def test_section_header(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section_header %}'
            '{{ section_header("Section", subtitle="Sub") }}'
        ).render()
        assert "chirpui-section-header" in html
        assert "<h2>Section</h2>" in html
        assert "Sub" in html

    def test_section_with_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section %}'
            '{% from "chirpui/button.html" import btn %}'
            '{% call section("Setup", subtitle="Configure") %}'
            '{% slot actions %}{{ btn("Refresh") }}{% end %}'
            "<p>Content</p>"
            "{% end %}"
        ).render()
        assert "chirpui-section-header" in html
        assert "<h2>Setup</h2>" in html
        assert "Refresh" in html


class TestIslands:
    def test_island_root_with_props(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/islands.html" import island_root %}'
            '{% call island_root("editor", props={"doc_id": 42}, mount_id="editor-root") %}'
            "<p>Fallback</p>"
            "{% end %}"
        ).render()
        assert 'data-island="editor"' in html
        assert 'id="editor-root"' in html
        assert "data-island-props=" in html
        assert "chirpui-island-fallback" in html
        assert "Fallback" in html

    def test_island_root_with_raw_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/islands.html" import island_root %}'
            '{% call island_root("editor", raw_attrs=\' data-island="editor" id="raw-root"\') %}'
            "Body"
            "{% end %}"
        ).render()
        assert 'id="raw-root"' in html
        assert "Body" in html


class TestStatePrimitives:
    def test_state_sync_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/state_primitives.html" import state_sync %}'
            '{% call state_sync("search", mount_id="search-sync") %}<input data-state-field>{% end %}'
        ).render()
        assert 'data-island="state_sync"' in html
        assert 'data-island-primitive="state_sync"' in html
        assert 'data-island-src="/static/islands/state_sync.js"' in html

    def test_grid_state_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/state_primitives.html" import grid_state %}'
            '{% call grid_state("team_grid", ["name", "role"], mount_id="grid-root") %}<div>{% end %}'
        ).render()
        assert 'data-island="grid_state"' in html
        assert 'data-island-primitive="grid_state"' in html
        assert 'id="grid-root"' in html
        assert "team_grid" in html

    def test_upload_state_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/state_primitives.html" import upload_state %}'
            '{% call upload_state("avatar_upload", "/upload", mount_id="upload-root") %}<div>{% end %}'
        ).render()
        assert 'data-island="upload_state"' in html
        assert 'data-island-src="/static/islands/upload_state.js"' in html
        assert "avatar_upload" in html


class TestAuthPrimitives:
    def test_password_field_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import password_field %}'
            '{{ password_field("password", label="Password", autocomplete="new-password") }}'
        ).render()
        assert 'type="password"' in html
        assert 'autocomplete="new-password"' in html

    def test_csrf_hidden_macro_with_explicit_token(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import csrf_hidden %}{{ csrf_hidden("token-123") }}'
        ).render()
        assert 'type="hidden"' in html
        assert 'name="_csrf_token"' in html
        assert 'value="token-123"' in html

    def test_login_form_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/auth.html" import login_form %}'
            '{{ login_form(action="/login", csrf="abc") }}'
        ).render()
        assert '<form method="post" action="/login"' in html
        assert 'name="_csrf_token"' in html
        assert 'type="password"' in html
        assert 'autocomplete="current-password"' in html


# ---------------------------------------------------------------------------
# Surface
# ---------------------------------------------------------------------------


class TestSurface:
    def test_surface_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}{% call surface() %}Content{% end %}'
        ).render()
        assert "chirpui-surface" in html
        assert "chirpui-surface--default" in html
        assert "Content" in html

    def test_surface_variants(self, env: Environment) -> None:
        for variant in ("muted", "elevated", "accent", "glass", "frosted", "smoke"):
            html = env.from_string(
                '{% from "chirpui/surface.html" import surface %}'
                f'{{% call surface(variant="{variant}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-surface--{variant}" in html

    def test_surface_full_width_no_padding(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}'
            "{% call surface(full_width=true, padding=false) %}X{% end %}"
        ).render()
        assert "chirpui-surface--full" in html
        assert "chirpui-surface--no-padding" in html


# ---------------------------------------------------------------------------
# Callout
# ---------------------------------------------------------------------------


class TestCallout:
    def test_callout_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/callout.html" import callout %}'
            "{% call callout() %}Tip content{% end %}"
        ).render()
        assert "chirpui-callout" in html
        assert "chirpui-callout--info" in html
        assert "chirpui-callout__body" in html
        assert "Tip content" in html

    def test_callout_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/callout.html" import callout %}'
            '{% call callout(title="Note") %}Body{% end %}'
        ).render()
        assert "chirpui-callout__title" in html
        assert "Note" in html
        assert "Body" in html

    def test_callout_variants(self, env: Environment) -> None:
        for variant in ("success", "warning", "error", "neutral"):
            html = env.from_string(
                '{% from "chirpui/callout.html" import callout %}'
                f'{{% call callout(variant="{variant}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-callout--{variant}" in html

    def test_callout_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/callout.html" import callout %}'
            '{% call callout(icon="💡", title="Tip") %}Use this pattern.{% end %}'
        ).render()
        assert "chirpui-callout__icon" in html
        assert "💡" in html


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------


class TestHero:
    def test_hero_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import hero %}{% call hero() %}Content{% end %}'
        ).render()
        assert "chirpui-hero" in html
        assert "chirpui-hero--solid" in html
        assert "chirpui-hero__inner" in html
        assert "Content" in html

    def test_hero_with_title_subtitle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import hero %}'
            '{% call hero(title="Welcome", subtitle="Build something.") %}CTA{% end %}'
        ).render()
        assert "chirpui-hero__title" in html
        assert "Welcome" in html
        assert "chirpui-hero__subtitle" in html
        assert "Build something." in html
        assert "CTA" in html

    def test_hero_backgrounds(self, env: Environment) -> None:
        for bg in ("muted", "gradient"):
            html = env.from_string(
                '{% from "chirpui/hero.html" import hero %}'
                f'{{% call hero(background="{bg}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-hero--{bg}" in html

    def test_page_hero(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import page_hero %}'
            '{% call page_hero(title="API Reference", subtitle="Explore.", variant="editorial") %}'
            "Body"
            "{% end %}"
        ).render()
        assert "chirpui-hero--page" in html
        assert "chirpui-hero--page-editorial" in html
        assert "API Reference" in html
        assert "Explore." in html
        assert "Body" in html


# ---------------------------------------------------------------------------
# Empty State
# ---------------------------------------------------------------------------


class TestEmptyState:
    def test_empty_state_with_action(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{% call empty_state(title="No items", action_label="Create", action_href="/new") %}'
            "<p>Get started.</p>"
            "{% end %}"
        ).render()
        assert "chirpui-empty-state__action" in html
        assert 'href="/new"' in html
        assert "Create" in html

    def test_empty_state_with_code_and_suggestions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{% call empty_state(title="No results", code="query", '
            'search_hint="Try different terms", suggestions=["Tip 1", "Tip 2"]) %}'
            "<p>Nothing found.</p>"
            "{% end %}"
        ).render()
        assert "chirpui-empty-state__code" in html
        assert "query" in html
        assert "chirpui-empty-state__search-hint" in html
        assert "Try different terms" in html
        assert "chirpui-empty-state__suggestions" in html
        assert "Tip 1" in html


# ---------------------------------------------------------------------------
# Code
# ---------------------------------------------------------------------------


class TestCode:
    def test_code_inline(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import code %}{{ code("path/to/file") }}'
        ).render()
        assert "chirpui-code" in html
        assert "path/to/file" in html
        assert "<code" in html

    def test_code_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import code_block %}'
            '{{ code_block("def foo():\\n    pass") }}'
        ).render()
        assert "chirpui-code-block" in html
        assert "<pre" in html
        assert "<code>" in html
        assert "def foo():" in html


# ---------------------------------------------------------------------------
# Nav tree
# ---------------------------------------------------------------------------


class TestNavTree:
    def test_nav_tree_flat(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{% call nav_tree(items=[{"title": "Home", "href": "/"}, '
            '{"title": "Docs", "href": "/docs", "active": True}]) %}'
            "{% end %}"
        ).render()
        assert "chirpui-nav-tree" in html
        assert 'href="/"' in html
        assert 'href="/docs"' in html
        assert 'aria-current="page"' in html

    def test_nav_tree_nested(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{% call nav_tree(items=[{"title": "API", "href": "/api", '
            '"children": [{"title": "Ref", "href": "/api/ref", "children": []}]}]) %}'
            "{% end %}"
        ).render()
        assert "chirpui-nav-tree__node" in html
        assert "API" in html
        assert "Ref" in html


# ---------------------------------------------------------------------------
# Params table
# ---------------------------------------------------------------------------


class TestParamsTable:
    def test_params_table(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/params_table.html" import params_table %}'
            '{{ params_table(rows=[{"name": "x", "type": "int", "default": "0", '
            '"description": "A number"}], title="Parameters") }}'
        ).render()
        assert "chirpui-params-table" in html
        assert "Parameters" in html
        assert "x" in html
        assert "int" in html
        assert "0" in html
        assert "A number" in html


# ---------------------------------------------------------------------------
# Signature
# ---------------------------------------------------------------------------


class TestSignature:
    def test_signature(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/signature.html" import signature %}'
            '{{ signature(text="def foo(): pass", language="python") }}'
        ).render()
        assert "chirpui-signature" in html
        assert "def foo(): pass" in html
        assert 'data-language="python"' in html


# ---------------------------------------------------------------------------
# Index card
# ---------------------------------------------------------------------------


class TestIndexCard:
    def test_index_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/index_card.html" import index_card %}'
            '{{ index_card(href="/api/foo", title="foo", description="Does something.", badge="function") }}'
        ).render()
        assert "chirpui-index-card" in html
        assert 'href="/api/foo"' in html
        assert "foo" in html
        assert "Does something." in html
        assert "chirpui-index-card__badge" in html
        assert "function" in html


# ---------------------------------------------------------------------------
# Overlay
# ---------------------------------------------------------------------------


class TestOverlay:
    def test_overlay_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/overlay.html" import overlay %}{{ overlay() }}'
        ).render()
        assert "chirpui-overlay" in html
        assert "chirpui-overlay--dark" in html
        assert 'aria-hidden="true"' in html

    def test_overlay_variants(self, env: Environment) -> None:
        for variant in ("gradient-bottom", "gradient-top"):
            html = env.from_string(
                f'{{% from "chirpui/overlay.html" import overlay %}}{{{{ overlay("{variant}") }}}}'
            ).render()
            assert f"chirpui-overlay--{variant}" in html


# ---------------------------------------------------------------------------
# Carousel
# ---------------------------------------------------------------------------


class TestCarousel:
    def test_carousel_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/carousel.html" import carousel, carousel_slide %}'
            "{% call carousel() %}"
            "{% call carousel_slide(1) %}A{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-carousel" in html
        assert "chirpui-carousel--compact" in html
        assert "chirpui-carousel__track" in html
        assert "chirpui-carousel__slide" in html
        assert 'id="slide-1"' in html
        assert "A" in html

    def test_carousel_page_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/carousel.html" import carousel, carousel_slide %}'
            '{% call carousel(variant="page") %}'
            "{% call carousel_slide(1) %}X{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-carousel--page" in html

    def test_carousel_with_dots(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/carousel.html" import carousel, carousel_slide %}'
            "{% call carousel(slide_count=3, show_dots=true) %}"
            "{% call carousel_slide(1) %}A{% end %}"
            "{% call carousel_slide(2) %}B{% end %}"
            "{% call carousel_slide(3) %}C{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-carousel__dots" in html
        assert "chirpui-carousel__dot" in html
        assert 'href="#slide-1"' in html
        assert 'href="#slide-2"' in html
        assert 'href="#slide-3"' in html


# ---------------------------------------------------------------------------
# Button
# ---------------------------------------------------------------------------


class TestButton:
    def test_btn_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Click me") }}'
        ).render()
        assert "chirpui-btn" in html
        assert "Click me" in html
        assert "chirpui-btn__label" in html
        assert "<button" in html

    def test_btn_primary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Submit", variant="primary") }}'
        ).render()
        assert "chirpui-btn--primary" in html

    def test_btn_loading(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", variant="primary", loading=true) }}'
        ).render()
        assert "chirpui-btn--loading" in html
        assert 'aria-busy="true"' in html
        assert "chirpui-btn__spinner" in html
        assert "chirpui-spinner" in html

    def test_button_group(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn, button_group %}'
            "{% call button_group() %}"
            '{{ btn("Submit", variant="primary") }}'
            '{{ btn("Cancel", href="/") }}'
            "{% end %}"
        ).render()
        assert "chirpui-btn-group" in html
        assert "Submit" in html
        assert "Cancel" in html

    def test_btn_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Demo", variant="primary", href="/demo") }}'
        ).render()
        assert "<a " in html
        assert 'href="/demo"' in html
        assert "chirpui-btn--primary" in html

    def test_btn_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Save", icon="✓") }}'
        ).render()
        assert "chirpui-btn__icon" in html
        assert "✓" in html

    def test_btn_with_attrs_map(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", attrs_map={"hx-post": "/save", "hx-target": "#result"}) }}'
        ).render()
        assert 'hx-post="/save"' in html
        assert 'hx-target="#result"' in html


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------


class TestStreaming:
    def test_streaming_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block() %}Content{% end %}"
        ).render()
        assert "chirpui-streaming-block" in html
        assert "Content" in html
        assert "aria-live" in html

    def test_streaming_block_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block(streaming=true) %}Partial{% end %}"
        ).render()
        assert "chirpui-streaming-block--active" in html
        assert "chirpui-streaming-block__cursor" in html

    def test_streaming_block_sse_swap_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block(streaming=true, sse_swap_target=true) %}{% end %}"
        ).render()
        assert 'sse-swap="fragment"' in html
        assert 'hx-target="this"' in html

    def test_copy_btn(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}'
            '{{ copy_btn(label="Copy", copy_text="hello") }}'
        ).render()
        assert "chirpui-copy-btn" in html
        assert 'data-copy-text="hello"' in html

    def test_model_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card(title="Llama 3", badge="42ms") %}Answer{% end %}'
        ).render()
        assert "chirpui-model-card" in html
        assert "Llama 3" in html
        assert "42ms" in html
        assert "Answer" in html

    def test_model_card_sse_streaming(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card("llama3", badge="A", sse_connect="/stream", sse_streaming=true) %}'
            "{% end %}"
        ).render()
        assert "chirpui-model-card" in html
        assert 'sse-connect="/stream"' in html
        assert 'hx-ext="sse"' in html
        assert 'sse-swap="fragment"' in html


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


class TestCard:
    def test_basic_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}{% call card() %}Body{% end %}'
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-card__body" in html
        assert "Body" in html

    def test_card_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Hello") %}Content{% end %}'
        ).render()
        assert "chirpui-card__header" in html
        assert "Hello" in html

    def test_card_with_footer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(footer="Footer text") %}Content{% end %}'
        ).render()
        assert "chirpui-card__footer" in html
        assert "Footer text" in html

    def test_card_collapsible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Toggle", collapsible=true) %}Hidden{% end %}'
        ).render()
        assert "<details" in html
        assert "<summary" in html
        assert "chirpui-card--collapsible" in html

    def test_card_collapsible_open(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Open", collapsible=true, open=true) %}Visible{% end %}'
        ).render()
        assert "open" in html

    def test_card_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}{% call card() %}Just body{% end %}'
        ).render()
        assert "chirpui-card__header" not in html

    def test_card_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}{% call card(cls="custom") %}Body{% end %}'
        ).render()
        assert "chirpui-card custom" in html

    def test_card_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Feature", icon="◆") %}Content{% end %}'
        ).render()
        assert "chirpui-card__icon" in html
        assert "◆" in html

    def test_card_with_subtitle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Card", subtitle="Optional subtitle") %}Body{% end %}'
        ).render()
        assert "Optional subtitle" in html
        assert "chirpui-text-muted" in html

    def test_card_header_with_actions(self, env: Environment) -> None:
        """Test header actions via card_header macro (or {% slot header_actions %} with Kida 0.3+)."""
        html = env.from_string(
            '{% from "chirpui/card.html" import card, card_header %}'
            "{% call card() %}"
            '{% call card_header(title="Settings", icon="⚙") %}'
            '<button class="chirpui-btn chirpui-btn--ghost">⋯</button>'
            "{% end %}"
            "<p>Body</p>"
            "{% end %}"
        ).render()
        assert "chirpui-card__header" in html
        assert "chirpui-card__header-actions" in html
        assert "Settings" in html
        assert "⚙" in html

    def test_card_body_actions_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="List") %}'
            '{% slot body_actions %}<button class="chirpui-btn">Add</button>{% end %}'
            "<p>Items</p>"
            "{% end %}"
        ).render()
        assert "chirpui-card__body-actions" in html
        assert "Add" in html
        assert "Items" in html


# ---------------------------------------------------------------------------
# Modal
# ---------------------------------------------------------------------------


class TestModal:
    def test_basic_modal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}{% call modal("dlg") %}Content{% end %}'
        ).render()
        assert '<dialog id="dlg"' in html
        assert "chirpui-modal" in html
        assert "chirpui-modal__body" in html
        assert "Content" in html

    def test_modal_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}'
            '{% call modal("dlg", title="Settings") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" in html
        assert "Settings" in html
        assert "chirpui-modal__close" in html

    def test_modal_sizes(self, env: Environment) -> None:
        for size in ("small", "medium", "large"):
            html = env.from_string(
                '{% from "chirpui/modal.html" import modal %}'
                f'{{% call modal("dlg", size="{size}") %}}Body{{% end %}}'
            ).render()
            assert f"chirpui-modal--{size}" in html

    def test_modal_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal_trigger %}'
            '{{ modal_trigger("dlg", label="Click me") }}'
        ).render()
        assert "chirpui-modal-trigger" in html
        assert "Click me" in html
        assert "dlg" in html

    def test_modal_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}{% call modal("dlg") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" not in html


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------


class TestTabs:
    def test_tabs_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tabs, tab %}'
            '{% call tabs() %}{{ tab("t1", "Tab One") }}{% end %}'
        ).render()
        assert "chirpui-tabs" in html
        assert 'role="tablist"' in html

    def test_tab_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("overview", "Overview", active=true) }}'
        ).render()
        assert "chirpui-tab--active" in html
        assert 'aria-selected="true"' in html
        assert "Overview" in html

    def test_tab_inactive(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}{{ tab("details", "Details") }}'
        ).render()
        assert "chirpui-tab--active" not in html
        assert 'aria-selected="false"' in html

    def test_tab_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("t1", "Tab", url="/tab/1", hx_target="#content") }}'
        ).render()
        assert 'hx-get="/tab/1"' in html
        assert 'hx-target="#content"' in html


# ---------------------------------------------------------------------------
# Dropdown
# ---------------------------------------------------------------------------


class TestDropdown:
    def test_basic_dropdown(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown.html" import dropdown %}'
            '{% call dropdown(label="Menu") %}<a href="/">Home</a>{% end %}'
        ).render()
        assert "<details" in html
        assert "<summary" in html
        assert "chirpui-dropdown" in html
        assert "chirpui-dropdown__menu" in html
        assert "Menu" in html

    def test_dropdown_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown.html" import dropdown %}'
            '{% call dropdown(label="Menu", cls="extra") %}Items{% end %}'
        ).render()
        assert "chirpui-dropdown extra" in html


# ---------------------------------------------------------------------------
# Toast
# ---------------------------------------------------------------------------


class TestToast:
    def test_toast_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast_container %}{{ toast_container() }}'
        ).render()
        assert 'id="chirpui-toasts"' in html
        assert "chirpui-toast-container" in html
        assert 'aria-live="polite"' in html

    def test_toast_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("Saved!") }}'
        ).render()
        assert "chirpui-toast--info" in html
        assert "Saved!" in html
        assert "hx-swap-oob" in html

    def test_toast_variants(self, env: Environment) -> None:
        for variant in ("info", "success", "warning", "error"):
            html = env.from_string(
                '{% from "chirpui/toast.html" import toast %}'
                f'{{{{ toast("msg", variant="{variant}") }}}}'
            ).render()
            assert f"chirpui-toast--{variant}" in html

    def test_toast_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("msg", dismissible=true) }}'
        ).render()
        assert "chirpui-toast__close" in html

    def test_toast_not_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("msg", dismissible=false) }}'
        ).render()
        assert "chirpui-toast__close" not in html

    def test_toast_no_oob(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("msg", oob=false) }}'
        ).render()
        assert "hx-swap-oob" not in html


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


class TestTable:
    def test_basic_table(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name", "Email"]) %}'
            '{{ row("Alice", "alice@example.com") }}'
            "{% end %}"
        ).render()
        assert "chirpui-table" in html
        assert "chirpui-table__th" in html
        assert "Name" in html
        assert "Email" in html
        assert "Alice" in html
        assert "alice@example.com" in html

    def test_table_striped(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}{% call table(striped=true) %}{% end %}'
        ).render()
        assert "chirpui-table--striped" in html

    def test_table_no_headers(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table() %}{{ row("Data") }}{% end %}'
        ).render()
        assert "chirpui-table__th" not in html
        assert "chirpui-table__body" in html

    def test_table_sticky_header_and_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name", "Email"], sticky_header=true, actions_header=true) %}'
            '{{ row("Alice", "a@x.com") }}'
            "{% end %}"
        ).render()
        assert "chirpui-table-wrap--sticky" in html
        assert "chirpui-table__th--actions" in html

    def test_row_renders_cells(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import row %}{{ row("A", "B", "C") }}'
        ).render()
        assert html.count("chirpui-table__td") == 3


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


class TestPagination:
    def test_basic_pagination(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=2, total=5,"
            ' url_pattern="/items?page={page}") }}'
        ).render()
        assert "chirpui-pagination" in html
        assert 'aria-label="Pagination"' in html
        assert 'aria-current="page"' in html

    def test_pagination_hidden_when_single_page(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=1, total=1,"
            ' url_pattern="/items?page={page}") }}'
        ).render()
        assert "chirpui-pagination" not in html

    def test_pagination_prev_disabled_on_first(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=1, total=3,"
            ' url_pattern="/p?page={page}") }}'
        ).render()
        assert "chirpui-pagination__link--disabled" in html

    def test_pagination_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=2, total=5,"
            ' url_pattern="/p?page={page}",'
            ' hx_target="#list") }}'
        ).render()
        assert 'hx-target="#list"' in html
        assert "hx-get" in html


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------


class TestAlert:
    def test_basic_alert(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}{% call alert() %}Hello{% end %}'
        ).render()
        assert "chirpui-alert--info" in html
        assert 'role="alert"' in html
        assert "Hello" in html

    def test_alert_variants(self, env: Environment) -> None:
        for variant in ("info", "success", "warning", "error"):
            html = env.from_string(
                '{% from "chirpui/alert.html" import alert %}'
                f'{{% call alert(variant="{variant}") %}}msg{{% end %}}'
            ).render()
            assert f"chirpui-alert--{variant}" in html

    def test_alert_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            "{% call alert(dismissible=true) %}msg{% end %}"
        ).render()
        assert "chirpui-alert__close" in html

    def test_alert_not_dismissible_by_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}{% call alert() %}msg{% end %}'
        ).render()
        assert "chirpui-alert__close" not in html

    def test_alert_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(icon="⚠") %}Warning message{% end %}'
        ).render()
        assert "chirpui-alert__icon" in html
        assert "⚠" in html

    def test_alert_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(title="Heads up") %}Body text{% end %}'
        ).render()
        assert "chirpui-alert__title" in html
        assert "Heads up" in html
        assert "Body text" in html


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------


class TestForms:
    """Test form macros.

    Note: ``field_errors`` filter is provided by Chirp, not chirp-ui.
    These tests exercise the macros without error display (errors=none).
    """

    def test_form_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/submit", method="post") %}<input>{% end %}'
        ).render()
        assert "chirpui-form" in html
        assert 'action="/submit"' in html
        assert 'method="post"' in html
        assert "<input>" in html

    def test_form_macro_with_htmx_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", attrs=\'hx-post="/x" hx-target="#y" hx-swap="innerHTML"\') %}'
            "Body"
            "{% end %}"
        ).render()
        assert "chirpui-form" in html
        assert "hx-post" in html
        assert "hx-target" in html
        assert "hx-swap" in html
        assert "Body" in html

    def test_form_macro_with_attrs_map(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", attrs_map={"hx-post": "/x", "hx-target": "#y", "hx-swap": "innerHTML"}) %}'
            "Body"
            "{% end %}"
        ).render()
        assert 'hx-post="/x"' in html
        assert 'hx-target="#y"' in html
        assert 'hx-swap="innerHTML"' in html

    def test_form_macro_explicit_hx_params_override_attrs_map(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", attrs_map={"hx-target": "#old"}, hx_target="#new") %}'
            "Body"
            "{% end %}"
        ).render()
        assert 'hx-target="#new"' in html

    def test_fieldset_macro(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import fieldset %}'
            '{% call fieldset(legend="Options") %}Content{% end %}'
        ).render()
        assert "chirpui-fieldset" in html
        assert "chirpui-fieldset__legend" in html
        assert "Options" in html
        assert "Content" in html

    def test_fieldset_macro_no_legend(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import fieldset %}{% call fieldset() %}Content{% end %}'
        ).render()
        assert "chirpui-fieldset" in html
        assert "chirpui-fieldset__legend" not in html
        assert "Content" in html

    def test_text_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("title", value="Hello", label="Title") }}'
        ).render()
        assert "chirpui-field" in html
        assert "chirpui-field__label" in html
        assert "chirpui-field__input" in html
        assert 'name="title"' in html
        assert 'value="Hello"' in html
        assert "Title" in html

    def test_text_field_required(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email", required=true) }}'
        ).render()
        assert "required" in html
        assert "chirpui-field__required" in html

    def test_text_field_with_hint(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("name", hint="Enter your full name") }}'
        ).render()
        assert "chirpui-field__hint" in html
        assert "Enter your full name" in html

    def test_textarea_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import textarea_field %}'
            '{{ textarea_field("desc", value="Content",'
            ' label="Description", rows=6) }}'
        ).render()
        assert "<textarea" in html
        assert 'rows="6"' in html
        assert "Content" in html

    def test_select_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import select_field %}'
            '{% set opts = [{"value": "a", "label": "Alpha"},'
            ' {"value": "b", "label": "Beta"}] %}'
            '{{ select_field("choice", options=opts,'
            ' selected="b", label="Pick") }}'
        ).render()
        assert "<select" in html
        assert "Alpha" in html
        assert "Beta" in html
        assert "selected" in html

    def test_checkbox_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import checkbox_field %}'
            '{{ checkbox_field("agree", label="I agree", checked=true) }}'
        ).render()
        assert 'type="checkbox"' in html
        assert "checked" in html
        assert "I agree" in html

    def test_hidden_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import hidden_field %}'
            '{{ hidden_field("id", value="42") }}'
        ).render()
        assert 'type="hidden"' in html
        assert 'name="id"' in html
        assert 'value="42"' in html

    def test_toggle_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import toggle_field %}'
            '{{ toggle_field("notify", label="Notifications", checked=true) }}'
        ).render()
        assert "chirpui-field--toggle" in html
        assert "chirpui-toggle" in html
        assert "chirpui-toggle__track" in html
        assert "Notifications" in html
        assert "checked" in html

    def test_radio_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import radio_field %}'
            '{% set opts = [{"value": "a", "label": "Alpha"},'
            ' {"value": "b", "label": "Beta"}] %}'
            '{{ radio_field("plan", options=opts, selected="b", label="Plan") }}'
        ).render()
        assert "<fieldset" in html
        assert "chirpui-field--radio" in html
        assert "chirpui-field__radio-group" in html
        assert "Alpha" in html
        assert "Beta" in html
        assert 'value="b"' in html
        assert "checked" in html
        assert "Plan" in html

    def test_radio_field_horizontal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import radio_field %}'
            '{% set opts = [{"value": "x", "label": "X"}] %}'
            '{{ radio_field("opt", options=opts, layout="horizontal") }}'
        ).render()
        assert "chirpui-field--radio-horizontal" in html

    def test_radio_field_with_errors(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import radio_field %}'
            '{% set opts = [{"value": "a", "label": "A"}] %}'
            '{{ radio_field("x", options=opts, errors={"x": ["Required"]}) }}'
        ).render()
        assert "chirpui-field--error" in html
        assert "Required" in html

    def test_file_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import file_field %}'
            '{{ file_field("avatar", label="Avatar", accept="image/*") }}'
        ).render()
        assert "chirpui-field--file" in html
        assert 'type="file"' in html
        assert 'name="avatar"' in html
        assert 'accept="image/*"' in html
        assert "Avatar" in html

    def test_file_field_multiple(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import file_field %}'
            '{{ file_field("files", multiple=true) }}'
        ).render()
        assert "multiple" in html

    def test_date_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import date_field %}'
            '{{ date_field("birthday", value="1990-01-15", label="Birthday") }}'
        ).render()
        assert 'type="date"' in html
        assert 'name="birthday"' in html
        assert 'value="1990-01-15"' in html
        assert "Birthday" in html

    def test_date_field_min_max(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import date_field %}'
            '{{ date_field("d", min="2020-01-01", max="2030-12-31") }}'
        ).render()
        assert 'min="2020-01-01"' in html
        assert 'max="2030-12-31"' in html

    def test_range_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import range_field %}'
            '{{ range_field("volume", value=75, min=0, max=100, label="Volume") }}'
        ).render()
        assert 'type="range"' in html
        assert 'name="volume"' in html
        assert 'value="75"' in html
        assert 'min="0"' in html
        assert 'max="100"' in html
        assert "Volume" in html

    def test_range_field_show_value(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import range_field %}'
            '{{ range_field("vol", value=50, show_value=true) }}'
        ).render()
        assert "chirpui-field__range-value" in html
        assert "50" in html

    def test_input_group(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import input_group %}'
            '{{ input_group("price", prefix="$", suffix=".00", value="10", label="Price") }}'
        ).render()
        assert "chirpui-input-group" in html
        assert "chirpui-input-group__prefix" in html
        assert "chirpui-input-group__suffix" in html
        assert "$" in html
        assert ".00" in html
        assert 'value="10"' in html

    def test_multi_select_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import multi_select_field %}'
            '{% set opts = [{"value": "a", "label": "A"}, {"value": "b", "label": "B"}] %}'
            '{{ multi_select_field("x", options=opts, selected=["a"]) }}'
        ).render()
        assert "multiple" in html
        assert "chirpui-field__input--multi" in html
        assert "A" in html
        assert "B" in html
        assert "selected" in html

    def test_search_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_field %}'
            '{{ search_field("q", value="", placeholder="Search...") }}'
        ).render()
        assert 'type="search"' in html
        assert "Search..." in html

    def test_search_field_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_field %}'
            '{{ search_field("q", search_url="/search", search_target="#results") }}'
        ).render()
        assert "hx-get" in html
        assert "hx-target" in html
        assert "#results" in html
        assert "hx-trigger" in html

    def test_form_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form_actions %}'
            '{% from "chirpui/button.html" import btn %}'
            "{% call form_actions() %}"
            '{{ btn("Submit", variant="primary") }}'
            '{{ btn("Cancel", href="/") }}'
            "{% end %}"
        ).render()
        assert "chirpui-form-actions" in html
        assert "Submit" in html
        assert "Cancel" in html

    def test_form_actions_align_end(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form_actions %}'
            '{% call form_actions(align="end") %}'
            '<button type="submit">Save</button>'
            "{% end %}"
        ).render()
        assert "chirpui-form-actions--end" in html


# ---------------------------------------------------------------------------
# Action Containers
# ---------------------------------------------------------------------------


class TestActionContainers:
    def test_action_strip_default_slot_backwards_compatible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_strip.html" import action_strip %}'
            "{% call action_strip() %}"
            '<button class="chirpui-btn">Go</button>'
            "{% end %}"
        ).render()
        assert "chirpui-action-strip" in html
        assert "chirpui-action-strip__inner" in html
        assert "Go" in html

    def test_action_strip_composed_zones(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/action_strip.html" import action_strip %}'
            '{% call action_strip(density="sm", wrap="scroll") %}'
            '<div class="chirpui-action-strip__primary"><input type="search"></div>'
            '<div class="chirpui-action-strip__controls"><button>Filters</button></div>'
            '<div class="chirpui-action-strip__actions"><button>Create</button></div>'
            "{% end %}"
        ).render()
        assert "chirpui-action-strip--sm" in html
        assert "chirpui-action-strip--scroll" in html
        assert "chirpui-action-strip__primary" in html
        assert "Filters" in html
        assert "Create" in html

    def test_filter_bar(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_bar %}'
            '{% call filter_bar("/items") %}'
            '<div class="chirpui-action-strip__primary"><input name="q" type="search"></div>'
            '<div class="chirpui-action-strip__controls"><select name="role"><option>All</option></select></div>'
            '<div class="chirpui-action-strip__actions"><button type="submit">Apply</button></div>'
            "{% end %}"
        ).render()
        assert "chirpui-filter-bar" in html
        assert 'action="/items"' in html
        assert 'name="q"' in html
        assert "Apply" in html

    def test_command_bar(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_bar.html" import command_bar %}'
            "{% call command_bar() %}"
            '<div class="chirpui-action-strip__controls"><button>Bulk edit</button></div>'
            '<div class="chirpui-action-strip__actions"><button>Create</button></div>'
            "{% end %}"
        ).render()
        assert "chirpui-command-bar" in html
        assert 'role="toolbar"' in html
        assert "Bulk edit" in html
        assert "Create" in html

    def test_search_header(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/search_header.html" import search_header %}'
            '{{ search_header("People", "/people", query="alice", subtitle="Directory") }}'
        ).render()
        assert "chirpui-search-header" in html
        assert "chirpui-search-header__strip" in html
        assert 'action="/people"' in html
        assert 'value="alice"' in html
        assert "Directory" in html

    def test_selection_bar_renders_when_count_positive(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/selection_bar.html" import selection_bar %}'
            "{% call selection_bar(count=2) %}<button>Clear</button>{% end %}"
        ).render()
        assert "chirpui-selection-bar" in html
        assert "2 selected" in html
        assert "Clear" in html

    def test_selection_bar_hidden_when_no_selection(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/selection_bar.html" import selection_bar %}'
            "{% call selection_bar(count=0) %}<button>Clear</button>{% end %}"
        ).render()
        assert "chirpui-selection-bar" not in html


# ---------------------------------------------------------------------------
# Navbar, Sidebar, Stepper
# ---------------------------------------------------------------------------


class TestNavbar:
    def test_navbar_with_brand(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link %}'
            '{% call navbar(brand="App", brand_url="/") %}'
            '{{ navbar_link("/docs", "Docs") }}'
            "{% end %}"
        ).render()
        assert "chirpui-navbar" in html
        assert "chirpui-navbar__brand" in html
        assert "App" in html
        assert 'href="/"' in html
        assert "Docs" in html

    def test_navbar_link_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar_link %}'
            '{{ navbar_link("/x", "X", active=true) }}'
        ).render()
        assert "chirpui-navbar__link--active" in html

    def test_navbar_end(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link, navbar_end %}'
            '{% call navbar(brand="App", brand_url="/") %}'
            '{{ navbar_link("/x", "X") }}'
            '{% call navbar_end() %}<a href="/login">Login</a>{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-navbar__links--end" in html
        assert "Login" in html

    def test_navbar_dropdown(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar_dropdown %}'
            '{% call navbar_dropdown("Products") %}'
            '<a href="/a">A</a>'
            "{% end %}"
        ).render()
        assert "chirpui-navbar-dropdown" in html
        assert "Products" in html
        assert 'href="/a"' in html

    def test_navbar_brand_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link %}'
            '{% from "chirpui/logo.html" import logo %}'
            '{% call navbar(brand_url="/", use_slots=true, brand_slot=true) %}'
            '{% slot brand %}{{ logo(text="ChirpUI", image_src="/static/logo.svg", variant="both") }}{% end %}'
            '{{ navbar_link("/docs", "Docs") }}'
            "{% end %}"
        ).render()
        assert "chirpui-navbar__brand" in html
        assert "chirpui-logo" in html
        assert 'src="/static/logo.svg"' in html


class TestAppShell:
    def test_app_shell_brand_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% from "chirpui/logo.html" import logo %}'
            '{% call app_shell(brand_url="/", brand_slot=true) %}'
            '{% slot brand %}{{ logo(text="Brand", image_src="/static/logo.svg", variant="both") }}{% end %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell" in html
        assert "chirpui-app-shell__brand" in html
        assert "chirpui-logo" in html
        assert 'src="/static/logo.svg"' in html
        assert "Main" in html


class TestLogo:
    def test_logo_text_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}{{ logo(text="ChirpUI", variant="text") }}'
        ).render()
        assert "chirpui-logo" in html
        assert "chirpui-logo--text" in html
        assert "chirpui-logo__text" in html
        assert "ChirpUI" in html
        assert "<img" not in html

    def test_logo_image_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(image_src="/static/logo.svg", image_alt="ChirpUI", variant="image") }}'
        ).render()
        assert "chirpui-logo--image" in html
        assert 'src="/static/logo.svg"' in html
        assert 'alt="ChirpUI"' in html
        assert "chirpui-logo__img" in html
        assert "<a " not in html

    def test_logo_both_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(text="ChirpUI", image_src="/static/logo.svg", variant="both", size="lg", align="start") }}'
        ).render()
        assert "chirpui-logo--both" in html
        assert "chirpui-logo--lg" in html
        assert "chirpui-logo--start" in html
        assert "chirpui-logo__img" in html
        assert "chirpui-logo__text" in html

    def test_logo_renders_link_root_when_href_is_set(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(text="Home", image_src="/static/logo.svg", href="/", variant="both") }}'
        ).render()
        assert '<a class="chirpui-logo' in html
        assert 'href="/"' in html
        assert "</a>" in html

    def test_logo_image_variant_uses_hidden_text_when_alt_missing(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(text="Accessible brand", image_src="/static/logo.svg", variant="image") }}'
        ).render()
        assert "chirpui-logo--image" in html
        assert 'alt=""' in html
        assert "chirpui-visually-hidden" in html
        assert "Accessible brand" in html


class TestSidebar:
    def test_sidebar_with_links(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_link %}'
            "{% call sidebar() %}"
            '{{ sidebar_link("/dash", "Dashboard", active=true) }}'
            "{% end %}"
        ).render()
        assert "chirpui-sidebar" in html
        assert "chirpui-sidebar__nav" in html
        assert "chirpui-sidebar__link--active" in html
        assert "Dashboard" in html

    def test_sidebar_section(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_section %}'
            "{% call sidebar() %}"
            '{{ sidebar_section("Main") }}'
            "{% end %}"
        ).render()
        assert "chirpui-sidebar__section" in html
        assert "Main" in html


class TestStepper:
    def test_stepper_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/stepper.html" import stepper %}'
            '{% set steps = [{"id": "1", "label": "One"}, {"id": "2", "label": "Two"}] %}'
            "{{ stepper(steps=steps, current=1) }}"
        ).render()
        assert "chirpui-stepper" in html
        assert "chirpui-stepper__list" in html
        assert "One" in html
        assert "Two" in html
        assert 'aria-current="step"' in html

    def test_stepper_completed(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/stepper.html" import stepper %}'
            '{% set steps = [{"id": "1", "label": "A"}, {"id": "2", "label": "B"}] %}'
            "{{ stepper(steps=steps, current=2) }}"
        ).render()
        assert "chirpui-stepper__item--completed" in html
        assert "chirpui-stepper__item--active" in html


class TestDescriptionList:
    def test_description_list_items(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/description_list.html" import description_list %}'
            '{% set items = [{"term": "A", "detail": "1"}, {"term": "B", "detail": "2"}] %}'
            "{{ description_list(items=items) }}"
        ).render()
        assert "chirpui-dl" in html
        assert "A" in html
        assert "1" in html

    def test_description_list_horizontal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/description_list.html" import description_list %}'
            '{% set items = [{"term": "X", "detail": "Y"}] %}'
            '{{ description_list(items=items, variant="horizontal") }}'
        ).render()
        assert "chirpui-dl--horizontal" in html


class TestSettingsRow:
    def test_settings_row_list_and_row(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/settings_row.html" import settings_row_list, settings_row %}'
            '{% call settings_row_list() %}'
            '{{ settings_row("Cursor IDE", status="Configured", detail="dori setup cursor") }}'
            '{{ settings_row("Skills dir", status="ok", detail="/path/to/skills") }}'
            "{% end %}"
        ).render()
        assert "chirpui-settings-row-list" in html
        assert "chirpui-settings-row" in html
        assert "Cursor IDE" in html
        assert "Configured" in html
        assert "dori setup cursor" in html
        assert "Skills dir" in html
        assert "ok" in html
        assert "/path/to/skills" in html

    def test_settings_row_detail_as_code(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/settings_row.html" import settings_row_list, settings_row %}'
            '{% call settings_row_list() %}'
            '{{ settings_row("X", status="ok", detail="dori setup x") }}'
            "{% end %}"
        ).render()
        assert "<code" in html
        assert "dori setup x" in html

    def test_settings_row_status_variant_override(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/settings_row.html" import settings_row %}'
            '{{ settings_row("Test", status="Custom", status_variant="error") }}'
        ).render()
        assert "chirpui-badge--error" in html
        assert "Custom" in html


class TestTimeline:
    def test_timeline_items(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            '{% set items = [{"title": "Step 1", "date": "Jan 1", "content": "Done"}] %}'
            "{{ timeline(items=items) }}"
        ).render()
        assert "chirpui-timeline" in html
        assert "Step 1" in html
        assert "Jan 1" in html
        assert "Done" in html

    def test_timeline_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline, timeline_item %}'
            "{% call timeline() %}"
            '{{ timeline_item("T", "D", "C") }}'
            "{% end %}"
        ).render()
        assert "chirpui-timeline__item" in html
        assert "T" in html


class TestDashboardPrimitives:
    def test_inline_edit_field_display(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/inline_edit_field.html" import inline_edit_field_display %}'
            '{{ inline_edit_field_display(value="Alice", edit_url="/edit") }}'
        ).render()
        assert "chirpui-inline-edit" in html
        assert "chirpui-inline-edit--display" in html
        assert "Alice" in html
        assert 'hx-get="/edit"' in html

    def test_inline_edit_field_form(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/inline_edit_field.html" import inline_edit_field_form %}'
            '{{ inline_edit_field_form(name="name", value="Bob", save_url="/save", cancel_url="/cancel") }}'
        ).render()
        assert "chirpui-inline-edit--edit" in html
        assert 'name="name"' in html
        assert 'value="Bob"' in html
        assert 'action="/save"' in html

    def test_row_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/row_actions.html" import row_actions %}'
            '{{ row_actions(items=[{"label": "Edit", "href": "/edit"}, {"label": "Delete", "href": "/del", "variant": "danger"}]) }}'
        ).render()
        assert "chirpui-dropdown" in html
        assert "chirpui-dropdown__trigger" in html
        assert "Edit" in html
        assert "Delete" in html

    def test_status_with_hint(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/status_with_hint.html" import status_with_hint %}'
            '{{ status_with_hint("Active", variant="success", hint="Last active 2h ago") }}'
        ).render()
        assert "chirpui-tooltip" in html
        assert "chirpui-badge" in html
        assert "Active" in html
        assert "Last active 2h ago" in html

    def test_status_with_hint_no_hint(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/status_with_hint.html" import status_with_hint %}'
            '{{ status_with_hint("Pending", variant="warning") }}'
        ).render()
        assert "chirpui-badge" in html
        assert "Pending" in html
        assert "chirpui-tooltip" not in html

    def test_entity_header(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/entity_header.html" import entity_header %}'
            '{% call entity_header(title="Chain: My Workflow", meta="3 steps") %}'
            "{% end %}"
        ).render()
        assert "chirpui-entity-header" in html
        assert "chirpui-entity-header__title" in html
        assert "Chain: My Workflow" in html
        assert "3 steps" in html


class TestConfirmDialog:
    def test_confirm_dialog(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_dialog %}'
            '{{ confirm_dialog("d", title="Delete?", message="Sure?") }}'
        ).render()
        assert '<dialog id="d"' in html
        assert "chirpui-confirm" in html
        assert "Delete?" in html
        assert "Sure?" in html

    def test_confirm_dialog_danger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_dialog %}'
            '{{ confirm_dialog("d", title="X", message="Y", variant="danger") }}'
        ).render()
        assert "chirpui-confirm--danger" in html

    def test_confirm_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_trigger %}'
            '{{ confirm_trigger("d", label="Delete") }}'
        ).render()
        assert "chirpui-confirm-trigger" in html
        assert "Delete" in html

    def test_confirm_dialog_htmx_params(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_dialog %}'
            '{{ confirm_dialog("d", title="X", message="Y", confirm_url="/del", confirm_method="DELETE",'
            ' hx_target="#main", hx_swap="innerHTML", hx_select="#content", hx_push_url="/list") }}'
        ).render()
        assert 'hx-delete="/del"' in html
        assert 'hx-target="#main"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'hx-select="#content"' in html
        assert 'hx-push-url="/list"' in html

    def test_confirm_dialog_form_content_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_dialog %}'
            '{% call confirm_dialog("d", title="Uninstall?", message="Sure?", confirm_url="/uninstall", confirm_method="POST") %}'
            '{% slot form_content %}<input type="hidden" name="name" value="my-collection">{% end %}'
            "{% end %}"
        ).render()
        assert 'name="name"' in html
        assert 'value="my-collection"' in html
        assert "Uninstall?" in html


class TestDrawer:
    def test_drawer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/drawer.html" import drawer %}'
            '{% call drawer("d", title="Panel", side="right") %}Content{% end %}'
        ).render()
        assert '<dialog id="d"' in html
        assert "chirpui-drawer" in html
        assert "chirpui-drawer--right" in html
        assert "Panel" in html
        assert "Content" in html

    def test_drawer_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/drawer.html" import drawer_trigger %}'
            '{{ drawer_trigger("d", label="Open") }}'
        ).render()
        assert "chirpui-drawer-trigger" in html
        assert "Open" in html


class TestSplitButton:
    def test_split_button_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_button.html" import split_button %}'
            '{% call split_button("Save", primary_href="/save") %}'
            '<a href="/export">Export</a>'
            "{% end %}"
        ).render()
        assert "chirpui-split-btn" in html
        assert "Save" in html
        assert 'href="/save"' in html
        assert "Export" in html

    def test_split_button_submit(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_button.html" import split_button %}'
            '{% call split_button("Submit", primary_submit=true) %}'
            "{% end %}"
        ).render()
        assert 'type="submit"' in html


class TestPopover:
    def test_popover(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/popover.html" import popover %}'
            '{% call popover(trigger_label="Filters") %}Content{% end %}'
        ).render()
        assert "chirpui-popover" in html
        assert "chirpui-popover__panel" in html
        assert "Filters" in html
        assert "Content" in html


class TestTagInput:
    def test_tag_input(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tag_input.html" import tag_input %}'
            '{{ tag_input("tags", tags=["a", "b"], label="Tags") }}'
        ).render()
        assert "chirpui-tag-input" in html
        assert "a" in html
        assert "b" in html

    def test_tag_input_with_add_remove(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tag_input.html" import tag_input %}'
            '{{ tag_input("t", tags=["x"], add_url="/add", remove_url="/remove") }}'
        ).render()
        assert 'action="/remove"' in html
        assert 'action="/add"' in html


class TestTreeView:
    def test_tree_view(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tree_view.html" import tree_view %}'
            '{% set nodes = [{"id": "1", "label": "Root", "children": []}] %}'
            "{{ tree_view(nodes=nodes) }}"
        ).render()
        assert "chirpui-tree" in html
        assert "Root" in html

    def test_tree_view_with_children(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tree_view.html" import tree_view %}'
            '{% set nodes = [{"id": "1", "label": "Parent", '
            '"children": [{"id": "2", "label": "Child", "children": []}]}] %}'
            "{{ tree_view(nodes=nodes) }}"
        ).render()
        assert "Parent" in html
        assert "Child" in html
        assert "<details" in html


class TestCalendar:
    def test_calendar(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/calendar.html" import calendar %}'
            "{% set weeks = [[0,0,1,2,3,4,5],[6,7,8,9,10,11,12]] %}"
            '{{ calendar(weeks=weeks, month_label="January 2025") }}'
        ).render()
        assert "chirpui-calendar" in html
        assert "January 2025" in html
        assert "1" in html
        assert "12" in html


# ---------------------------------------------------------------------------
# Badge, Skeleton, Progress, Media Object, Stat, App Layout
# ---------------------------------------------------------------------------


class TestBadge:
    def test_badge_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Active") }}'
        ).render()
        assert "chirpui-badge" in html
        assert "chirpui-badge--primary" in html
        assert "Active" in html

    def test_badge_with_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Error", variant="error") }}'
        ).render()
        assert "chirpui-badge--error" in html

    def test_badge_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}'
            '{{ badge("Pending", variant="warning", icon="◆") }}'
        ).render()
        assert "chirpui-badge__icon" in html
        assert "◆" in html


class TestSkeleton:
    def test_skeleton_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/skeleton.html" import skeleton %}{{ skeleton() }}'
        ).render()
        assert "chirpui-skeleton" in html

    def test_skeleton_avatar(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/skeleton.html" import skeleton %}{{ skeleton(variant="avatar") }}'
        ).render()
        assert "chirpui-skeleton--avatar" in html

    def test_skeleton_text_lines(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/skeleton.html" import skeleton %}'
            '{{ skeleton(variant="text", lines=3) }}'
        ).render()
        assert "chirpui-skeleton--text" in html
        assert html.count("chirpui-skeleton__line") == 3

    def test_skeleton_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/skeleton.html" import skeleton %}{{ skeleton(variant="card") }}'
        ).render()
        assert "chirpui-skeleton--card" in html
        assert "chirpui-skeleton--card-img" in html


class TestProgress:
    def test_progress_bar_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/progress.html" import progress_bar %}'
            "{{ progress_bar(value=60, max=100) }}"
        ).render()
        assert "chirpui-progress-bar" in html
        assert 'aria-valuenow="60"' in html
        assert 'aria-valuemax="100"' in html
        assert "chirpui-progress-bar__track" in html
        assert "chirpui-progress-bar__fill" in html

    def test_progress_bar_with_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/progress.html" import progress_bar %}'
            '{{ progress_bar(value=75, max=100, label="75%") }}'
        ).render()
        assert "chirpui-progress-bar__label" in html
        assert "75%" in html

    def test_progress_bar_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/progress.html" import progress_bar %}'
            '{{ progress_bar(value=50, variant="success") }}'
        ).render()
        assert "chirpui-progress-bar--success" in html


class TestMediaObject:
    def test_media_object_default_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/media_object.html" import media_object %}'
            "{% call media_object() %}"
            '<img src="/x.jpg" alt="X"><div><h3>Title</h3><p>Body</p></div>'
            "{% end %}"
        ).render()
        assert "chirpui-media-object" in html
        assert "Title" in html
        assert "Body" in html

    def test_media_object_legacy_macros(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/media_object.html" import media_object, media_object_media, media_object_body %}'
            "{% call media_object() %}"
            '{% call media_object_media() %}<img src="/a">{% end %}'
            "{% call media_object_body() %}Content{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-media-object" in html
        assert "Content" in html


class TestStat:
    def test_stat_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/stat.html" import stat %}{{ stat(value="1.2K", label="Followers") }}'
        ).render()
        assert "chirpui-stat" in html
        assert "chirpui-stat__value" in html
        assert "chirpui-stat__label" in html
        assert "1.2K" in html
        assert "Followers" in html

    def test_stat_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/stat.html" import stat %}'
            '{{ stat(value="42", label="Videos", icon="▶") }}'
        ).render()
        assert "chirpui-stat__icon" in html
        assert "▶" in html


class TestAppLayout:
    def test_app_layout_file_structure(self) -> None:
        """Verify app_layout.html exists and contains expected Chirp-ui wiring."""
        from pathlib import Path

        path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "chirp_ui"
            / "templates"
            / "chirpui"
            / "app_layout.html"
        )
        assert path.exists()
        content = path.read_text()
        assert "chirpui.css" in content
        assert "toast_container" in content


# ---------------------------------------------------------------------------
# Wave 1: Divider, Link, Breadcrumbs, List, Accordion, Collapse, Tooltip
# ---------------------------------------------------------------------------


class TestDivider:
    def test_divider_line_only(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}{{ divider() }}'
        ).render()
        assert "chirpui-divider" in html
        assert 'role="separator"' in html

    def test_divider_with_text(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}{{ divider("OR") }}'
        ).render()
        assert "chirpui-divider__text" in html
        assert "OR" in html

    def test_divider_horizontal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}{{ divider("OR", horizontal=true) }}'
        ).render()
        assert "chirpui-divider--horizontal" in html

    def test_divider_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/divider.html" import divider %}{{ divider("OR", variant="primary") }}'
        ).render()
        assert "chirpui-divider--primary" in html


class TestLink:
    def test_link_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/link.html" import link %}{{ link("Home", href="/") }}'
        ).render()
        assert "chirpui-link" in html
        assert 'href="/"' in html
        assert "Home" in html

    def test_link_external(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/link.html" import link %}'
            '{{ link("Docs", href="https://example.com", external=true) }}'
        ).render()
        assert 'target="_blank"' in html
        assert 'rel="noopener noreferrer"' in html


class TestBreadcrumbs:
    def test_breadcrumbs_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
            '{% set items = [{"label": "Home", "href": "/"}, {"label": "Current"}] %}'
            "{{ breadcrumbs(items) }}"
        ).render()
        assert "chirpui-breadcrumbs" in html
        assert 'aria-label="Breadcrumb"' in html
        assert "Home" in html
        assert "Current" in html
        assert 'href="/"' in html
        assert 'aria-current="page"' in html


class TestList:
    def test_list_with_items(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group %}'
            '{% set items = ["A", "B", "C"] %}'
            "{{ list_group(items) }}"
        ).render()
        assert "chirpui-list" in html
        assert "chirpui-list__item" in html
        assert "A" in html
        assert "B" in html
        assert "C" in html

    def test_list_with_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group, list_item %}'
            "{% call list_group() %}"
            "{% call list_item() %}Row one{% end %}"
            "{% call list_item() %}Row two{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-list" in html
        assert "Row one" in html
        assert "Row two" in html

    def test_list_bordered(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group %}'
            '{% set items = ["A"] %}'
            "{{ list_group(items, bordered=true) }}"
        ).render()
        assert "chirpui-list--bordered" in html


class TestAccordion:
    def test_accordion_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion_item %}'
            '{% call accordion_item("Title", name="faq") %}Content{% end %}'
        ).render()
        assert "<details" in html
        assert 'name="faq"' in html
        assert "chirpui-accordion__item" in html
        assert "chirpui-accordion__trigger" in html
        assert "chirpui-accordion__content" in html
        assert "Title" in html
        assert "Content" in html

    def test_accordion_item_open(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion_item %}'
            '{% call accordion_item("Q", open=true) %}A{% end %}'
        ).render()
        assert "open" in html


class TestCollapse:
    def test_collapse_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/collapse.html" import collapse %}'
            '{% call collapse(trigger="Expand") %}Hidden{% end %}'
        ).render()
        assert "<details" in html
        assert "chirpui-collapse" in html
        assert "chirpui-collapse__trigger" in html
        assert "Expand" in html
        assert "Hidden" in html


class TestTooltip:
    def test_tooltip_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tooltip.html" import tooltip %}'
            '{% call tooltip(hint="Help text") %}Hover me{% end %}'
        ).render()
        assert "chirpui-tooltip" in html
        assert 'data-tooltip="Help text"' in html
        assert 'title="Help text"' in html
        assert "Hover me" in html


# ---------------------------------------------------------------------------
# Composition / Nesting
# ---------------------------------------------------------------------------


class TestComposition:
    def test_card_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Outer") %}'
            '{% call card(title="Inner") %}'
            "Nested content"
            "{% end %}"
            "{% end %}"
        ).render()
        assert html.count('<header class="chirpui-card__header">') >= 2
        assert "Outer" in html
        assert "Inner" in html
        assert "Nested content" in html

    def test_table_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% from "chirpui/table.html" import table, row %}'
            '{% call card(title="Users") %}'
            '{% call table(headers=["Name"]) %}'
            '{{ row("Alice") }}'
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-table" in html
        assert "Alice" in html

    def test_alert_inside_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% from "chirpui/alert.html" import alert %}'
            '{% call card(title="Status") %}'
            '{% call alert(variant="success") %}All good{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-card" in html
        assert "chirpui-alert--success" in html
        assert "All good" in html


# ---------------------------------------------------------------------------
# ASCII Icon
# ---------------------------------------------------------------------------


class TestAsciiIcon:
    def test_static_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}{{ ascii_icon("✦") }}'
        ).render()
        assert "chirpui-ascii" in html
        assert "chirpui-ascii--md" in html
        assert "chirpui-ascii__char" in html
        assert "✦" in html
        assert 'aria-hidden="true"' in html

    def test_animation_variants(self, env: Environment) -> None:
        for anim in (
            "blink",
            "pulse",
            "shrink",
            "grow",
            "spin",
            "bounce",
            "throb",
            "wiggle",
            "glow",
        ):
            html = env.from_string(
                '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
                f'{{{{ ascii_icon("◆", animation="{anim}") }}}}'
            ).render()
            assert f"chirpui-ascii--{anim}" in html
            assert "chirpui-ascii__char" in html
            assert "◆" in html

    def test_rotate_produces_four_spans(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("x", animation="rotate") }}'
        ).render()
        assert "chirpui-ascii--rotate" in html
        for i in range(1, 5):
            assert f"chirpui-ascii__char--{i}" in html
        assert "chirpui-ascii__char--2" in html
        assert "chirpui-ascii__char--3" in html
        assert "chirpui-ascii__char--4" in html
        assert "◜" in html
        assert "◝" in html
        assert "◞" in html
        assert "◟" in html

    def test_sizes(self, env: Environment) -> None:
        for size in ("sm", "md", "lg", "xl"):
            html = env.from_string(
                '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
                f'{{{{ ascii_icon("●", size="{size}") }}}}'
            ).render()
            assert f"chirpui-ascii--{size}" in html

    def test_no_animation_class_when_none(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("★", animation="none") }}'
        ).render()
        assert "chirpui-ascii--none" not in html
        assert "chirpui-ascii--blink" not in html

    def test_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ascii_icon.html" import ascii_icon %}'
            '{{ ascii_icon("◇", cls="my-icon") }}'
        ).render()
        assert "my-icon" in html


# ---------------------------------------------------------------------------
# Spinner
# ---------------------------------------------------------------------------


class TestSpinner:
    def test_spinner_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/spinner.html" import spinner %}{{ spinner() }}'
        ).render()
        assert "chirpui-spinner" in html
        assert "chirpui-spinner__mote" in html
        assert "✦" in html
        assert 'role="status"' in html
        assert 'aria-label="Loading"' in html

    def test_spinner_sizes(self, env: Environment) -> None:
        for size in ("sm", "md", "lg"):
            html = env.from_string(
                '{% from "chirpui/spinner.html" import spinner %}'
                f'{{{{ spinner(size="{size}") }}}}'
            ).render()
            assert f"chirpui-spinner--{size}" in html

    def test_spinner_thinking(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/spinner.html" import spinner_thinking %}{{ spinner_thinking() }}'
        ).render()
        assert "chirpui-spinner-thinking" in html
        assert "chirpui-spinner__char" in html
        assert "◜" in html
        assert 'aria-label="Processing"' in html


# ---------------------------------------------------------------------------
# Avatar
# ---------------------------------------------------------------------------


class TestAvatar:
    def test_avatar_initials(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}{{ avatar(initials="AB", alt="Alice") }}'
        ).render()
        assert "chirpui-avatar" in html
        assert "chirpui-avatar__initials" in html
        assert "AB" in html

    def test_avatar_size_variants(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}{{ avatar(initials="X", size="lg") }}'
        ).render()
        assert "chirpui-avatar--lg" in html


# ---------------------------------------------------------------------------
# Video Card
# ---------------------------------------------------------------------------


class TestVideoCard:
    def test_video_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/video_card.html" import video_card %}'
            '{{ video_card(href="/v", thumbnail="/t.jpg", duration="4:32", title="Test") }}'
        ).render()
        assert "chirpui-video-card" in html
        assert "4:32" in html
        assert "Test" in html


# ---------------------------------------------------------------------------
# CSS file
# ---------------------------------------------------------------------------


class TestCSS:
    def test_css_file_loads(self) -> None:
        """Verify the CSS file exists and is loadable from the templates dir."""
        from pathlib import Path

        css_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "chirp_ui"
            / "templates"
            / "chirpui.css"
        )
        assert css_path.exists()
        content = css_path.read_text()
        assert "--chirpui-border" in content
        assert "--chirpui-radius" in content
        assert ".chirpui-card" in content
        assert ".chirpui-modal" in content
        assert ".chirpui-tabs" in content
        assert ".chirpui-dropdown" in content
        assert ".chirpui-toast" in content
        assert ".chirpui-table" in content
        assert ".chirpui-pagination" in content
        assert ".chirpui-alert" in content
        assert ".chirpui-field" in content
        assert ".chirpui-btn" in content
        assert ".chirpui-ascii" in content
        assert ".chirpui-spinner" in content
        assert ".chirpui-divider" in content
        assert ".chirpui-breadcrumbs" in content
        assert ".chirpui-list" in content
        assert ".chirpui-accordion" in content
        assert ".chirpui-collapse" in content
        assert ".chirpui-tooltip" in content
        assert ".chirpui-toggle" in content

    def test_ascii_animation_classes_exist(self) -> None:
        """All ascii animation variants must have matching CSS."""
        from pathlib import Path

        css_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "chirp_ui"
            / "templates"
            / "chirpui.css"
        )
        content = css_path.read_text()
        animations = (
            "blink",
            "pulse",
            "shrink",
            "grow",
            "spin",
            "bounce",
            "throb",
            "wiggle",
            "glow",
            "rotate",
        )
        for anim in animations:
            assert f".chirpui-ascii--{anim}" in content, f"Missing CSS for ascii animation: {anim}"
        assert "@keyframes chirpui-ascii-blink" in content
        assert "@keyframes chirpui-ascii-pulse" in content
        assert "@keyframes chirpui-ascii-rotate-cycle" in content
