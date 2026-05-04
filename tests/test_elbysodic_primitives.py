from kida import Environment


def test_sidebar_link_renders_badge(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/sidebar.html" import sidebar_link %}'
        '{{ sidebar_link("/inbox", "Inbox", badge=3) }}'
    ).render()

    assert "chirpui-sidebar__badge" in html
    assert ">3<" in html


def test_sidebar_link_renders_stable_badge_states(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/sidebar.html" import sidebar_link %}'
        '{{ sidebar_link("/runs", "Runs", badge_loading=true) }}'
        '{{ sidebar_link("/inbox", "Inbox", badge=3, badge_label="3 unread inbox items") }}'
    ).render()

    assert "chirpui-sidebar__badge--reserved" in html
    assert "chirpui-sidebar__badge--loading" in html
    assert 'aria-hidden="true"' in html
    assert 'aria-label="3 unread inbox items"' in html


def test_scope_switcher_renders_dropdown_scope_control(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/scope_switcher.html" import scope_switcher %}'
        '{{ scope_switcher("Prod", items=[{"label": "Prod", "href": "/prod"}], aria_label="Switch scope") }}'
    ).render()

    assert "chirpui-scope-switcher" in html
    assert "chirpui-dropdown" in html
    assert 'aria-label="Switch scope"' in html


def test_saved_view_strip_renders_selected_views(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/saved_view_strip.html" import saved_view_strip %}'
        '{{ saved_view_strip(label="Saved views", current_href="/mine", views=['
        '{"label": "Mine", "href": "/mine"},'
        '{"label": "Blocked", "href": "/blocked"}'
        "]) }}"
    ).render()

    assert "chirpui-saved-view-strip" in html
    assert 'aria-label="Saved views"' in html
    assert 'aria-current="page"' in html
    assert "Mine" in html


def test_primary_nav_renders_badges_dividers_and_active_links(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/primary_nav.html" import primary_nav %}'
        "{{ primary_nav(items=["
        '{"label": "World", "href": "/world", "match": "prefix"},'
        '{"divider": true},'
        '{"label": "Inbox", "href": "/inbox", "badge": 2}'
        '], current_path="/world/places") }}'
    ).render()

    assert 'aria-label="Primary"' in html
    assert "chirpui-primary-nav__link--active" in html
    assert "chirpui-primary-nav__divider" in html
    assert "chirpui-primary-nav__badge" in html


def test_primary_nav_explicit_inactive_overrides_path_match(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/primary_nav.html" import primary_nav %}'
        "{{ primary_nav(items=["
        '{"label": "World", "href": "/world", "match": "prefix", "active": false}'
        '], current_path="/world/places") }}'
    ).render()

    assert "chirpui-primary-nav__link--active" not in html


def test_inline_counter_renders_mark_value_and_label(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/inline_counter.html" import inline_counter %}'
        '{{ inline_counter("#", 12, "posts") }}'
    ).render()

    assert "chirpui-inline-counter__mark" in html
    assert "chirpui-inline-counter__value" in html
    assert "chirpui-inline-counter__label" in html


def test_latest_line_renders_actor_meta_and_tooltip(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/latest_line.html" import latest_line %}'
        '{{ latest_line("Latest", "/threads/1", "Council fire", actor="Lena", meta="today") }}'
    ).render()

    assert "chirpui-latest-line" in html
    assert "Council fire" in html
    assert "Lena" in html
    assert "today" in html
    assert "chirpui-latest-line__tooltip" in html


def test_linked_avatar_stack_renders_links_and_more_count(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/avatar_stack.html" import linked_avatar_stack %}'
        "{{ linked_avatar_stack(items=["
        '{"label": "Ada", "href": "/cast/ada", "initials": "A"},'
        '{"label": "Bea", "href": "/cast/bea", "initials": "B"},'
        '{"label": "Cy", "href": "/cast/cy", "initials": "C"}'
        "], max_visible=2) }}"
    ).render()

    assert "chirpui-avatar-stack__link" in html
    assert 'href="/cast/ada"' in html
    assert "+1" in html


def test_chip_group_and_custom_chip(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/chip_group.html" import chip_group, chip %}'
        '{% call chip_group(label="Facets") %}'
        '{{ chip("Urban", href="/facets/urban", selected=true, color="#78c850") }}'
        '{{ chip("Quiet", muted=true) }}'
        "{% end %}"
    ).render()

    assert 'aria-label="Facets"' in html
    assert "chirpui-chip--selected" in html
    assert "chirpui-chip--custom" in html
    assert "--chirpui-chip-color: #78c850" in html
    assert "chirpui-chip--muted" in html


def test_rendered_content_wraps_slot_content(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/rendered_content.html" import rendered_content %}'
        "{% call rendered_content(compact=true) %}<p>Hello</p>{% end %}"
    ).render()

    assert "chirpui-rendered-content--compact" in html
    assert "<p>Hello</p>" in html


def test_composer_shell_renders_named_regions(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/composer_shell.html" import composer_shell %}'
        "{% call composer_shell() %}"
        "{% slot header %}Header{% end %}"
        "{% slot identity %}Identity{% end %}"
        "{% slot fields %}Fields{% end %}"
        "{% slot body %}Body{% end %}"
        "{% slot actions %}<button>Post</button>{% end %}"
        "{% end %}"
    ).render()

    assert "chirpui-composer-shell__header" in html
    assert "chirpui-composer-shell__identity" in html
    assert "chirpui-composer-shell__fields" in html
    assert "chirpui-composer-shell__body" in html
    assert "chirpui-composer-shell__actions" in html


def test_token_input_renders_tokens_and_results(env: Environment) -> None:
    html = env.from_string(
        '{% from "chirpui/token_input.html" import token_input, token, token_result %}'
        '{% call token_input(label="Cast", input_id="cast", placeholder="Add cast") %}'
        '{% slot tokens %}{{ token("Ada", name="cast", value="ada", removable=true) }}{% end %}'
        '{% slot results %}{{ token_result("Bea", meta="Mage", active=true, href="/cast/bea") }}{% end %}'
        "{% end %}"
    ).render()

    assert 'for="cast"' in html
    assert "chirpui-token-input__token" in html
    assert 'type="hidden"' in html
    assert "chirpui-token-input__remove" in html
    assert "chirpui-token-input__result--active" in html
    assert 'href="/cast/bea"' in html
