"""Render tests for all chirp-ui components.

Each test verifies:
- Correct HTML structure (BEM classes present)
- Parameter variants (defaults, optional args)
- Slot content injection where applicable
"""

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path

import pytest
from kida import Environment

from chirp_ui.validation import ChirpUIValidationWarning
from tests.helpers import assert_element


@dataclass(frozen=True, slots=True)
class ShellMenuItemStub:
    label: str = ""
    href: str | None = None
    action: str | None = None
    variant: str = "default"
    icon: str | None = None
    divider: bool = False

    def get(self, key: str, default: object = None) -> object:
        value = getattr(self, key, default)
        return default if value is None else value


@dataclass(frozen=True, slots=True)
class ShellActionStub:
    id: str
    label: str
    kind: str = "link"
    href: str | None = None
    action: str | None = None
    variant: str = "default"
    icon: str | None = None
    size: str = "sm"
    disabled: bool = False
    menu_items: tuple[ShellMenuItemStub, ...] = ()
    form_action: str | None = None
    form_method: str = "post"
    hidden_fields: tuple[tuple[str, str], ...] = ()
    include_csrf: bool = True
    hx_post: str | None = None
    hx_target: str | None = None
    hx_swap: str | None = None
    hx_disinherit: str | None = None
    submit_surface: str = "btn"
    attrs: str = ""

    def as_menu_item(self) -> ShellMenuItemStub:
        return ShellMenuItemStub(
            label=self.label,
            href=self.href,
            action=self.action,
            variant=self.variant,
            icon=self.icon,
        )


@dataclass(frozen=True, slots=True)
class ShellActionZoneStub:
    items: tuple[ShellActionStub, ...] = ()

    @property
    def overflow_items(self) -> tuple[ShellMenuItemStub, ...]:
        return tuple(item.as_menu_item() for item in self.items)


@dataclass(frozen=True, slots=True)
class ShellActionsStub:
    primary: ShellActionZoneStub = field(default_factory=ShellActionZoneStub)
    controls: ShellActionZoneStub = field(default_factory=ShellActionZoneStub)
    overflow: ShellActionZoneStub = field(default_factory=ShellActionZoneStub)
    target: str = "chirp-shell-actions"

    @property
    def has_items(self) -> bool:
        return bool(self.primary.items or self.controls.items or self.overflow.items)


def _stub_route_link_attrs(
    target: str,
    *,
    hrefs: frozenset[str] | None = None,
) -> Callable[..., dict[str, str]]:
    allowed = hrefs

    def _route_link_attrs(
        href: str | None,
        *,
        boost: bool = True,
        external: bool = False,
        disabled: bool = False,
        fallback: dict[str, str] | None = None,
        attrs: object = None,
        attrs_map: dict[str, str] | None = None,
    ) -> dict[str, str]:
        if href is None or disabled or external or not boost:
            return {}
        if isinstance(href, str) and (
            "://" in href or href.startswith(("#", "//", "mailto:", "tel:", "javascript:", "data:"))
        ):
            return {}
        if isinstance(attrs_map, dict) and any(str(key).startswith("hx-") for key in attrs_map):
            return {}
        if isinstance(attrs, str) and "hx-" in attrs:
            return {}
        if allowed is not None and href not in allowed:
            return {}
        return {
            "hx-boost": "true",
            "hx-target": f"#{target}",
            "hx-swap": "innerHTML",
        }

    return _route_link_attrs


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

    def test_grid_preset_bento_211(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="bento-211", gap="md") %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-bento-211" in html
        assert "chirpui-grid--gap-md" in html
        assert "chirpui-grid--cols-" not in html

    def test_grid_preset_thirds(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="thirds", gap="lg") %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-thirds" in html
        assert "chirpui-grid--gap-lg" in html

    def test_grid_items_start(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="thirds", items="start") %}A{% end %}'
        ).render()
        assert "chirpui-grid--items-start" in html

    def test_grid_preset_detail_two(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="detail-two", gap="md") %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-detail-two" in html
        assert "chirpui-grid--detail-two-single" not in html

    def test_grid_preset_detail_two_single(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="detail-two", detail_single=true) %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-detail-two" in html
        assert "chirpui-grid--detail-two-single" in html

    def test_grid_preset_detail_two_single_string(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="detail-two-single") %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-detail-two" in html
        assert "chirpui-grid--detail-two-single" in html

    def test_grid_preset_aliases_bento_thirds_detail(self, env: Environment) -> None:
        for preset, want in (
            ("split-2-1-1", "chirpui-grid--preset-bento-211"),
            ("split-thirds", "chirpui-grid--preset-thirds"),
            ("three-equal", "chirpui-grid--preset-thirds"),
            ("split-1-1.35", "chirpui-grid--preset-detail-two"),
        ):
            html = env.from_string(
                '{% from "chirpui/layout.html" import grid %}'
                f'{{% call grid(preset="{preset}") %}}A{{% end %}}'
            ).render()
            assert want in html, preset

    def test_grid_preset_alias_split_1_1_35_single(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(preset="split-1-1.35-single") %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-detail-two" in html
        assert "chirpui-grid--detail-two-single" in html

    def test_label_overline(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/label_overline.html" import label_overline %}'
            '{{ label_overline("Hello", section=true, tag="h3") }}'
        ).render()
        assert "chirpui-label-overline" in html
        assert "chirpui-label-overline--section" in html
        assert "<h3 " in html
        assert "Hello" in html

    def test_grid_preset_overrides_cols(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import grid %}'
            '{% call grid(cols=2, preset="thirds") %}A{% end %}'
        ).render()
        assert "chirpui-grid--preset-thirds" in html
        assert "chirpui-grid--cols-2" not in html

    def test_frame_balanced(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import frame %}{% call frame() %}A{% end %}'
        ).render()
        assert "chirpui-frame" in html
        assert "chirpui-frame--balanced" in html

    def test_frame_hero(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import frame %}'
            '{% call frame(variant="hero") %}A{% end %}'
        ).render()
        assert "chirpui-frame--hero" in html

    def test_frame_sidebar_end(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import frame %}'
            '{% call frame(variant="sidebar-end") %}A{% end %}'
        ).render()
        assert "chirpui-frame--sidebar-end" in html

    def test_frame_sidebar_start(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import frame %}'
            '{% call frame(variant="sidebar-start") %}A{% end %}'
        ).render()
        assert "chirpui-frame--sidebar-start" in html

    def test_frame_gap_lg(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import frame %}{% call frame(gap="lg") %}A{% end %}'
        ).render()
        assert "chirpui-frame--gap-lg" in html

    def test_layout_affinity_frame_resolver_css_is_narrow_and_stack_cluster_unpromoted(
        self,
    ) -> None:
        css = _chirpui_css()
        assert '.chirpui-frame > [data-chirpui-role~="rail"]' in css
        assert '.chirpui-frame > [data-chirpui-role~="content"]' in css
        assert '.chirpui-frame > [data-chirpui-pressure~="compress"]' in css
        assert ".chirpui-cluster > [data-chirpui-pressure" not in css
        assert ".chirpui-cluster > [data-chirpui-affinity" not in css
        assert ".chirpui-stack > [data-chirpui-pressure" not in css
        assert ".chirpui-stack > [data-chirpui-affinity" not in css

    def test_stack(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import stack %}{% call stack() %}A{% end %}'
        ).render()
        assert "chirpui-stack" in html

    def test_stack_gap_variants(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import stack %}'
            '{% call stack(gap="xs") %}A{% end %}'
            '{% call stack(gap="md") %}B{% end %}'
            '{% call stack(gap="xl") %}C{% end %}'
        ).render()
        assert "chirpui-stack--xs" in html
        assert "chirpui-stack--md" in html
        assert "chirpui-stack--xl" in html

    def test_stack_css_owns_direct_child_rhythm_without_overriding_prose(self) -> None:
        css = _chirpui_css()
        stack_rule = css.split(":where(.chirpui-stack:not(.chirpui-prose))", 1)[1].split("}", 1)[0]
        assert "margin-block: 0;" in stack_rule
        assert ".chirpui-prose.chirpui-stack" in css

    def test_cluster(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import cluster %}'
            '{% call cluster(gap="sm") %}<span>A</span><span>B</span>{% end %}'
        ).render()
        assert "chirpui-cluster" in html
        assert "chirpui-cluster--sm" in html

    def test_cluster_css_owns_direct_child_rhythm(self) -> None:
        css = _chirpui_css()
        cluster_rule = css.split(
            ":where(.chirpui-cluster) > :where(:not(script, style, template))", 1
        )[1].split("}", 1)[0]
        assert "margin: 0;" in cluster_rule

    def test_layer_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import layer %}{% call layer() %}A{% end %}'
        ).render()
        assert "chirpui-layer" in html
        assert "chirpui-layer--left" in html
        assert "chirpui-layer--overlap-md" in html
        assert "chirpui-layer--angle-subtle" in html
        assert "chirpui-layer--hover" in html

    def test_layer_center_no_hover(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import layer %}'
            '{% call layer(direction="center", hover=false) %}A{% end %}'
        ).render()
        assert "chirpui-layer--center" in html
        assert "chirpui-layer--hover" not in html

    def test_layer_right_lg_moderate(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import layer %}'
            '{% call layer(direction="right", overlap="lg", angle="moderate") %}A{% end %}'
        ).render()
        assert "chirpui-layer--right" in html
        assert "chirpui-layer--overlap-lg" in html
        assert "chirpui-layer--angle-moderate" in html

    def test_layer_angle_none(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import layer %}{% call layer(angle="none") %}A{% end %}'
        ).render()
        assert "chirpui-layer--angle-none" in html

    def test_layer_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import layer %}{% call layer(cls="my-deck") %}A{% end %}'
        ).render()
        assert "chirpui-layer" in html
        assert "my-deck" in html

    def test_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import block %}{% call block(span=2) %}A{% end %}'
        ).render()
        assert "chirpui-block--span-2" in html

    def test_block_span_full(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import block %}{% call block(span="full") %}A{% end %}'
        ).render()
        assert "chirpui-block--span-full" in html

    def test_chat_layout_fill_emits_modifier(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/chat_layout.html" import chat_layout %}'
            "{% call chat_layout(fill=true, show_activity=false) %}"
            "{% slot messages %}M{% end %}"
            "{% slot input %}I{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-chat-layout--fill" in html
        assert "chirpui-chat-layout__messages" in html

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

    def test_page_header_variant_compact(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import page_header %}'
            '{{ page_header("Ollama Chat", variant="compact") }}'
        ).render()
        assert "chirpui-page-header" in html
        assert "chirpui-page-header--compact" in html
        assert "<h1>Ollama Chat</h1>" in html

    def test_section_header(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section_header %}'
            '{{ section_header("Section", subtitle="Sub") }}'
        ).render()
        assert "chirpui-section-header" in html
        assert "<h2>Section</h2>" in html
        assert "Sub" in html

    def test_section_header_variant_inline(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section_header %}'
            '{% call section_header("Advanced", variant="inline") %}'
            "{% slot actions %}<button>Toggle</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-section-header" in html
        assert "chirpui-section-header--inline" in html
        assert "Advanced" in html
        assert "<h2" in html
        assert "Toggle" in html

    def test_section_header_inline_alias(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section_header_inline %}'
            '{% call section_header_inline("Config") %}'
            "{% slot %}<span>Edit</span>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-section-header--inline" in html
        assert "Config" in html
        assert "<h2" in html
        assert "Edit" in html

    def test_header_relationship_css_owns_child_rhythm_and_pressure(self) -> None:
        css = _chirpui_css()

        page_title_rule = css.split(".chirpui-page-header__top > div:first-child", 1)[1].split(
            "}", 1
        )[0]
        assert "display: flex" in page_title_rule
        assert "flex-direction: column" in page_title_rule
        assert "overflow-wrap: anywhere" in page_title_rule
        assert ".chirpui-page-header__top > div:first-child > *" in css

        section_title_rule = css.split(".chirpui-section-header__title-block > div", 1)[1].split(
            "}", 1
        )[0]
        assert "display: flex" in section_title_rule
        assert "gap: var(--chirpui-spacing-xs)" in section_title_rule
        assert "overflow-wrap: anywhere" in section_title_rule
        assert ".chirpui-section-header__title-block > div > *" in css

        entity_title_rule = css.split(".chirpui-entity-header__content > div", 1)[1].split("}", 1)[
            0
        ]
        assert "display: flex" in entity_title_rule
        assert "gap: var(--chirpui-spacing-xs)" in entity_title_rule
        assert "overflow-wrap: anywhere" in entity_title_rule
        assert ".chirpui-entity-header__content > div > *" in css

        assert "@media (max-width: 42rem)" in css
        assert ".chirpui-page-header__actions,\n    .chirpui-section-header__actions" in css
        assert ".chirpui-entity-header__actions" in css

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
        assert "Content" in html

    def test_section_gradient_surface_variants(self, env: Environment) -> None:
        for variant in (
            "gradient-subtle",
            "gradient-accent",
            "gradient-border",
            "gradient-mesh",
        ):
            html = env.from_string(
                '{% from "chirpui/layout.html" import section %}'
                f'{{% call section("Title", surface_variant="{variant}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-surface--{variant}" in html

    def test_section_full_width_renders_blade(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section %}'
            '{% call section("Wide", full_width=true) %}Content{% end %}'
        ).render()
        assert "chirpui-blade" in html
        assert "chirpui-surface--full" in html
        assert "Content" in html

    def test_section_parallax_renders_blade_modifier(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section %}'
            '{% call section("Motion", full_width=true, parallax=true) %}Content{% end %}'
        ).render()
        assert "chirpui-blade--parallax" in html

    def test_section_collapsible_gradient_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/layout.html" import section_collapsible %}'
            '{% call section_collapsible("Advanced", surface_variant="gradient-subtle") %}'
            "Content"
            "{% end %}"
        ).render()
        assert "chirpui-section-collapsible" in html
        assert "chirpui-surface--gradient-subtle" in html
        assert "Content" in html


class TestWorkbench:
    def test_panel_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/panel.html" import panel %}'
            "{% call panel(title='Activity') %}Body{% end %}"
        ).render()
        assert "chirpui-panel" in html
        assert "chirpui-surface--muted" in html
        assert "chirpui-panel__title" in html
        assert "Activity" in html
        assert "Body" in html

    def test_panel_scroll_with_actions_and_footer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/panel.html" import panel %}'
            '{% call panel(title="Files", subtitle="Tree", scroll_body=true) %}'
            "{% slot actions %}<button>Refresh</button>{% end %}"
            "Body"
            "{% slot footer %}<span>Status</span>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-panel--scroll" in html
        assert "chirpui-panel__body--scroll" in html
        assert "chirpui-panel__actions" in html
        assert "Refresh" in html
        assert "Status" in html

    def test_panel_body_owns_slot_flow_rhythm(self) -> None:
        css = _chirpui_css()
        panel_rule = css.split(".chirpui-panel {", 1)[1].split("}", 1)[0]
        assert "min-width: 0" in panel_rule
        assert "overflow-wrap: anywhere" in panel_rule
        assert ".chirpui-panel__heading" in css
        assert "gap: var(--chirpui-spacing-xs)" in css
        assert ".chirpui-panel__body > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-panel__body > :where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css
        assert ".chirpui-panel__footer > :where(:not(script, style, template))" in css
        assert "margin-block-start: var(--chirpui-spacing-sm);" in css

    def test_split_layout_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_layout.html" import split_layout %}'
            "{% call split_layout() %}"
            "{% slot primary %}Left{% end %}"
            "{% slot secondary %}Right{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-split-layout" in html
        assert "chirpui-split-layout--horizontal" in html
        assert "chirpui-split-layout--sidebar" in html
        assert "chirpui-split-layout--gap-md" in html
        assert "Left" in html
        assert "Right" in html

    def test_split_layout_vertical_wide_secondary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_layout.html" import split_layout %}'
            '{% call split_layout(direction="vertical", ratio="wide-secondary", gap="lg") %}'
            "{% slot primary %}Top{% end %}"
            "{% slot secondary %}Bottom{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-split-layout--vertical" in html
        assert "chirpui-split-layout--wide-secondary" in html
        assert "chirpui-split-layout--gap-lg" in html

    def test_workspace_shell_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/workspace_shell.html" import workspace_shell %}'
            '{% call workspace_shell("Authoring", sidebar_title="Files") %}'
            "{% slot toolbar %}<button>Save</button>{% end %}"
            "{% slot sidebar %}<nav>Tree</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-workspace-shell" in html
        assert "chirpui-workspace-shell__toolbar" in html
        assert "chirpui-workspace-shell__layout" in html
        assert "chirpui-workspace-shell__sidebar" in html
        assert "chirpui-workspace-shell__sidebar-panel" in html
        assert 'data-chirpui-role="rail nav"' in html
        assert 'data-chirpui-role="actions"' in html
        assert 'data-chirpui-pressure="compress"' in html
        assert "Tree" in html
        assert "Main" in html

    def test_workspace_shell_with_inspector(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/workspace_shell.html" import workspace_shell %}'
            '{% call workspace_shell("Authoring", show_inspector=true, sidebar_title="Files", inspector_title="Preview") %}'
            "{% slot sidebar %}<nav>Tree</nav>{% end %}"
            "Editor"
            "{% slot inspector %}<div>Preview body</div>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-workspace-shell__content-layout" in html
        assert "chirpui-workspace-shell__inspector" in html
        assert "chirpui-workspace-shell__inspector-panel" in html
        assert 'data-chirpui-role="rail content"' in html
        assert 'data-chirpui-affinity="end"' in html
        assert "Preview" in html
        assert "Preview body" in html

    def test_workspace_shell_layout_affinity_css_is_component_scoped(self) -> None:
        css = _chirpui_css()
        assert '.chirpui-workspace-shell__heading[data-chirpui-pressure~="flex"]' in css
        assert '.chirpui-workspace-shell__toolbar[data-chirpui-affinity~="end"]' in css
        assert '.chirpui-workspace-shell__sidebar[data-chirpui-pressure~="compress"]' in css
        assert '.chirpui-workspace-shell__inspector[data-chirpui-pressure~="compress"]' in css
        assert ".chirpui-workspace-shell [data-chirpui-pressure" not in css
        assert ".chirpui-workspace-shell [data-chirpui-affinity" not in css

    def test_workspace_dense_primitives_render_layout_affinity(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/workspace_primitives.html" import filter_rail, filter_rail_item, metric_strip, metric_item, result_collection, result_card, inspector_panel %}'
            '{% call filter_rail(label="Areas") %}'
            '{{ filter_rail_item("/ops", "Operations", count=4, icon="OP", active=true) }}'
            "{% end %}"
            '{% call metric_strip(label="Readout") %}'
            '{{ metric_item("12", "workloads") }}'
            "{% end %}"
            '{% call result_collection(label="Results", title="Workloads") %}'
            "{% slot meta %}12 results{% end %}"
            '{% call result_card("Forge Runners", subtitle="Queue workers") %}'
            "{% slot mark %}FR{% end %}"
            "{% slot actions %}<button>Inspect</button>{% end %}"
            "<p>Queue depth above target.</p>"
            "{% slot footer %}<span>Owner Platform</span>{% end %}"
            "{% end %}"
            "{% end %}"
            '{% call inspector_panel(title="Forge Runners", subtitle="Selected workload") %}'
            "{% slot actions %}<button>Refresh</button>{% end %}"
            "<p>Healthy with warnings.</p>"
            "{% slot footer %}<span>Inspector</span>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-filter-rail" in html
        assert "chirpui-filter-rail__item is-active" in html
        assert 'aria-current="page"' in html
        assert "chirpui-metric-strip__item" in html
        assert "chirpui-result-collection__items" in html
        assert 'role="listitem"' in html
        assert "chirpui-result-card__actions" in html
        assert "chirpui-inspector-panel__body" in html
        assert 'data-chirpui-role="rail nav"' in html
        assert 'data-chirpui-pressure="compress"' in html
        assert 'data-chirpui-affinity="fill"' in html
        assert 'data-chirpui-rhythm="stack"' in html
        assert 'data-chirpui-rhythm="group"' in html
        assert 'data-chirpui-rhythm="inset"' in html
        assert 'data-chirpui-rhythm="group separated"' in html

    def test_workspace_primitives_css_uses_scoped_boundaries(self) -> None:
        css = _chirpui_css()
        for selector in (
            "@scope (.chirpui-filter-rail)",
            "@scope (.chirpui-metric-strip)",
            "@scope (.chirpui-result-collection)",
            "@scope (.chirpui-result-card)",
            "@scope (.chirpui-inspector-panel)",
        ):
            assert selector in css
        assert "--chirpui-rhythm-attached" in css
        assert "--chirpui-rhythm-group" in css
        assert "--chirpui-rhythm-stack" in css
        assert "--chirpui-rhythm-inset" in css
        assert "padding: var(--chirpui-rhythm-inset);" in css
        assert "padding-block-start: var(--chirpui-rhythm-separated);" in css
        assert ":scope {\n    display: grid;\n    gap: var(--chirpui-rhythm-stack);" in css
        assert ".chirpui-result-card [data-chirpui-pressure" not in css

    def test_workspace_result_card_css_owns_row_pressure_and_child_rhythm(self) -> None:
        css = _chirpui_css()
        for selector in (
            ".chirpui-result-card__copy > :where(:not(script, style, template))",
            ".chirpui-result-card__actions > :where(:not(script, style, template))",
            ".chirpui-result-card__body > :where(:not(script, style, template))",
            ".chirpui-result-card__footer > :where(:not(script, style, template))",
            ".chirpui-inspector-panel__body > :where(:not(script, style, template))",
            ".chirpui-inspector-panel__footer > :where(:not(script, style, template))",
        ):
            assert selector in css
        assert ".chirpui-result-card__header" in css
        assert "flex-wrap: wrap;" in css
        assert "flex: 999 1 12rem;" in css
        assert "max-inline-size: 100%;" in css

    def test_file_tree_with_header_actions_and_footer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/file_tree.html" import file_tree %}'
            '{% call file_tree(items=[{"title": "docs", "icon": "⊞", "children": ['
            '{"title": "README.md", "href": "/readme", "active": true, "icon": "●"}]}], '
            'title="Files", show_icons=true) %}'
            "{% slot actions %}<button>Refresh</button>{% end %}"
            '{% slot header %}<input type="search" placeholder="Filter">{% end %}'
            "{% slot footer %}<span>1 file</span>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-file-tree" in html
        assert "chirpui-panel__title" in html
        assert "chirpui-nav-tree__icon" in html
        assert "Refresh" in html
        assert 'placeholder="Filter"' in html
        assert "1 file" in html

    def test_file_tree_forwards_branch_mode_to_nav_tree(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/file_tree.html" import file_tree %}'
            '{{ file_tree(items=[{"title": "docs", "href": "/docs", "open": true, '
            '"children": [{"title": "README.md", "href": "/readme"}]}], '
            'title="Files", branch_mode="linked") }}'
        ).render()
        assert "chirpui-nav-tree--linked-branches" in html
        assert "<summary" not in html
        assert 'href="/docs"' in html

    def test_document_header_with_details(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/document_header.html" import document_header %}'
            '{% call document_header("README.md", subtitle="Skill guide", path="docs/README.md", '
            'provenance="Forked from builtin/doc-help", status="Draft", '
            'meta_items=["Modified 2m ago", "Markdown"]) %}'
            "{% slot actions %}<button>Save</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-document-header" in html
        assert "docs/README.md" in html
        assert "Forked from builtin/doc-help" in html
        assert "Draft" in html
        assert "Modified 2m ago" in html
        assert "Save" in html


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
        assert 'class="chirpui-island-root"' in html
        assert "data-island-props=" in html
        assert "chirpui-island-fallback" in html
        assert "Fallback" in html

    def test_island_root_css_owns_fallback_rhythm(self) -> None:
        css = _chirpui_css()

        assert ".chirpui-island-root" in css
        assert ".chirpui-island-fallback" in css
        assert ".chirpui-island-fallback > :where(:not(script, style, template))" in css
        assert "max-inline-size: 100%;" in css

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

    def test_csrf_hidden_macro_without_token_uses_csrf_field(self, env: Environment) -> None:
        """Without an explicit token, prefer Chirp's ``csrf_field()`` over Kida's ``csrf_token()``."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import csrf_hidden %}{{ csrf_hidden() }}'
        ).render()
        assert 'type="hidden"' in html
        assert 'name="_csrf_token"' in html
        assert 'value="test-csrf"' in html

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

    def test_surface_gradient_variants(self, env: Environment) -> None:
        for variant in (
            "gradient-subtle",
            "gradient-accent",
            "gradient-border",
            "gradient-mesh",
        ):
            html = env.from_string(
                '{% from "chirpui/surface.html" import surface %}'
                f'{{% call surface(variant="{variant}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-surface--{variant}" in html

    def test_surface_appearance_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}'
            '{% call surface(appearance="outlined", tone="primary") %}X{% end %}'
        ).render()
        assert "chirpui-surface--outlined" in html
        assert "chirpui-surface--primary" in html

    def test_surface_style_and_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}'
            '{% call surface(style="--x: 1; background: red", '
            'attrs_map={"id": "s1", "data-test": "surf"}) %}In{% end %}'
        ).render()
        assert 'style="--x: 1; background: red"' in html
        assert 'data-test="surf"' in html
        assert 'id="s1"' in html
        assert "In" in html

    def test_surface_owns_inset_and_flow_rhythm(self) -> None:
        css = _chirpui_css()
        assert (
            ":scope:not(.chirpui-surface--no-padding) > :where(:not(script, style, template))"
        ) in css
        assert (
            ":scope:not(.chirpui-surface--no-padding) > "
            ":where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css
        assert "margin-block-start: var(--chirpui-space-card-gap);" in css


# ---------------------------------------------------------------------------
# Aura
# ---------------------------------------------------------------------------


class TestAura:
    def test_aura_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aura.html" import aura %}{% call aura() %}Inner{% end %}'
        ).render()
        assert "chirpui-aura" in html
        assert "chirpui-aura--accent" in html
        assert "chirpui-aura--md" in html
        assert "chirpui-aura__content" in html
        assert "Inner" in html

    def test_aura_tones(self, env: Environment) -> None:
        for tone in ("accent", "warm", "cool", "muted", "primary"):
            html = env.from_string(
                '{% from "chirpui/aura.html" import aura %}'
                f'{{% call aura(tone="{tone}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-aura--{tone}" in html

    def test_aura_spreads(self, env: Environment) -> None:
        for spread in ("sm", "md", "lg"):
            html = env.from_string(
                '{% from "chirpui/aura.html" import aura %}'
                f'{{% call aura(spread="{spread}") %}}X{{% end %}}'
            ).render()
            assert f"chirpui-aura--{spread}" in html

    def test_aura_mirror(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aura.html" import aura %}{% call aura(mirror=true) %}X{% end %}'
        ).render()
        assert "chirpui-aura--mirror" in html

    def test_aura_with_surface(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aura.html" import aura %}'
            '{% from "chirpui/surface.html" import surface %}'
            '{% call aura(tone="cool", spread="sm") %}'
            '{% call surface(variant="glass") %}G{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-aura--cool" in html
        assert "chirpui-aura--sm" in html
        assert "chirpui-surface--glass" in html

    def test_aura_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aura.html" import aura %}'
            '{% call aura(attrs_map={"data-testid": "a1"}) %}X{% end %}'
        ).render()
        assert 'data-testid="a1"' in html


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

    def test_callout_body_owns_slot_flow_rhythm(self) -> None:
        css = _chirpui_css()
        assert ".chirpui-callout__body > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-callout__body > :where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css


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

    def test_hero_mesh_background(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import hero %}'
            '{% call hero(background="mesh") %}Content{% end %}'
        ).render()
        assert "chirpui-hero--mesh" in html

    def test_hero_animated_gradient_background(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import hero %}'
            '{% call hero(background="animated-gradient") %}Content{% end %}'
        ).render()
        assert "chirpui-hero--animated-gradient" in html

    def test_page_hero_mesh_background(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import page_hero %}'
            '{% call page_hero(title="Docs", background="mesh") %}Body{% end %}'
        ).render()
        assert "chirpui-hero--mesh" in html
        assert "chirpui-hero--page" in html

    def test_page_hero_animated_gradient_background(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import page_hero %}'
            '{% call page_hero(title="Docs", background="animated-gradient") %}Body{% end %}'
        ).render()
        assert "chirpui-hero--animated-gradient" in html
        assert "chirpui-hero--page" in html

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

    def test_hero_actions_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import hero %}'
            '{% call hero(title="Welcome") %}'
            '{% slot actions %}<a href="/start">Go</a>{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-hero__action" in html
        assert "Go" in html

    def test_hero_action_slot_backward_compat(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero.html" import hero %}'
            '{% call hero(title="Welcome") %}'
            '{% slot action %}<a href="/start">Go</a>{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-hero__action" in html
        assert "Go" in html


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

    def test_empty_state_resolves_semantic_icon_names(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{{ empty_state(icon="diamond", title="No results") }}'
        ).render()
        assert "chirpui-empty-state__icon" in html
        assert "◇" in html
        assert "diamond" not in html

    def test_empty_state_action_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/new"})),
        )
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{% call empty_state(title="No items", action_label="Create", action_href="/new") %}'
            "<p>Get started.</p>"
            "{% end %}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

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

    def test_empty_panel_state_compact(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty_panel_state.html" import empty_panel_state %}'
            '{% call empty_panel_state(title="No file selected", icon="◎") %}'
            "<p>Select a file to begin.</p>"
            "{% slot action %}<button>Browse</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-empty-panel-state" in html
        assert "chirpui-empty-panel-state--compact" in html
        assert "No file selected" in html
        assert "Browse" in html

    def test_empty_state_actions_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{% call empty_state(title="No items") %}'
            "{% slot actions %}<button>Create</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-empty-state__action" in html
        assert "Create" in html

    def test_empty_state_action_slot_backward_compat(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{% call empty_state(title="No items") %}'
            "{% slot action %}<button>Create</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-empty-state__action" in html
        assert "Create" in html

    def test_empty_panel_state_actions_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty_panel_state.html" import empty_panel_state %}'
            '{% call empty_panel_state(title="Empty", icon="◎") %}'
            "{% slot actions %}<button>Add</button>{% end %}"
            "{% end %}"
        ).render()
        assert "Add" in html


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

    def test_install_snippet_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import install_snippet %}'
            '{{ install_snippet("uv add bengal-chirp") }}'
        ).render()
        assert "chirpui-install-snippet" in html
        assert "chirpui-install-snippet__label" in html
        assert "chirpui-install-snippet__row" in html
        assert "chirpui-install-snippet__command" in html
        assert "$ uv add bengal-chirp" in html
        assert "install" in html  # default label
        assert 'aria-label="Copy install command"' in html

    def test_install_snippet_custom_label_and_prompt(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import install_snippet %}'
            '{{ install_snippet("pip install kida", label="pip", prompt="%") }}'
        ).render()
        assert "pip" in html
        assert "% pip install kida" in html

    def test_install_snippet_no_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import install_snippet %}'
            '{{ install_snippet("npm install foo", label="") }}'
        ).render()
        assert "chirpui-install-snippet__label" not in html
        assert "chirpui-install-snippet__row" in html

    def test_install_snippet_copy_escapes_command(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import install_snippet %}'
            '{{ install_snippet("echo <script>alert(1)</script>") }}'
        ).render()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html or "&#" in html

    def test_install_snippet_custom_id(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import install_snippet %}'
            '{{ install_snippet("uv add chirp-ui", id="my-cmd") }}'
        ).render()
        assert 'id="my-cmd"' in html


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

    def test_nav_tree_links_use_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/", "/docs"})),
        )
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{% call nav_tree(items=[{"title": "Home", "href": "/"}, '
            '{"title": "Docs", "href": "/docs", "active": True}]) %}'
            "{% end %}"
        ).render()
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2

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

    def test_nav_tree_linked_branch_mode_uses_route_links(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=items, branch_mode="linked") }}'
        ).render(
            items=[
                {
                    "title": "Worlds",
                    "href": "/worlds",
                    "open": True,
                    "children": [{"title": "Earth", "href": "/worlds/earth"}],
                },
                {
                    "title": "Closed",
                    "href": "/closed",
                    "children": [{"title": "Hidden", "href": "/closed/hidden"}],
                },
            ]
        )
        assert "chirpui-nav-tree--linked-branches" in html
        assert "<details" not in html
        assert "<summary" not in html
        assert 'href="/worlds"' in html
        assert "Earth" in html
        assert "Hidden" not in html

    def test_nav_tree_linked_branch_mode_keeps_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/worlds"})),
        )
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=[{"title": "Worlds", "href": "/worlds", "children": [{"title": "Earth"}]}], branch_mode="linked") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_nav_tree_badge_and_state_hooks(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=[{"title": "Inbox", "href": "/inbox", "badge": 0, "active": true, "muted": true}, '
            '{"title": "Worlds", "href": "/worlds", "open": true, "children": [{"title": "Earth", "href": "/worlds/earth"}]}], '
            'branch_mode="linked") }}'
        ).render()
        assert "chirpui-nav-tree__badge" in html
        assert ">0<" in html
        assert "chirpui-nav-tree__item--active" in html
        assert "chirpui-nav-tree__item--muted" in html
        assert "chirpui-nav-tree__item--branch" in html
        assert "chirpui-nav-tree__item--open" in html
        assert "chirpui-nav-tree__item--child" in html

    def test_nav_tree_unknown_branch_mode_falls_back_to_disclosure(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=[{"title": "API", "href": "/api", "children": [{"title": "Ref", "href": "/api/ref"}]}], '
            'branch_mode="unknown") }}'
        ).render()
        assert "chirpui-nav-tree--linked-branches" not in html
        assert "<details" in html
        assert "<summary" in html
        assert "Ref" in html

    def test_nav_tree_icons(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{% call nav_tree(items=[{"title": "API", "href": "/api", "icon": "◎"}], show_icons=true) %}'
            "{% end %}"
        ).render()
        assert "chirpui-nav-tree__icon" in html
        assert "◎" in html

    def test_nav_tree_item_hint_wraps_route_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=[{"title": "Inbox", "href": "/inbox", "hint": "Unread & urgent"}]) }}'
        ).render()
        assert "chirpui-nav-tree__hint" in html
        assert "chirpui-tooltip--block" in html
        assert 'data-tooltip="Unread &amp; urgent"' in html
        assert 'href="/inbox"' in html
        assert "chirpui-nav-tree__link" in html

    def test_nav_tree_branch_hint_uses_inline_wrapper_inside_summary(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=[{"title": "Docs", "href": "/docs", "hint": "Docs detail", "children": [{"title": "API"}]}]) }}'
        ).render()
        summary = html[html.index("<summary") : html.index("</summary>")]
        assert '<span class="chirpui-tooltip' in summary
        assert '<div class="chirpui-tooltip' not in summary

    def test_nav_tree_item_hint_keeps_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/inbox"})),
        )
        html = env.from_string(
            '{% from "chirpui/nav_tree.html" import nav_tree %}'
            '{{ nav_tree(items=[{"title": "Inbox", "href": "/inbox", "hint": "Unread detail"}]) }}'
        ).render()
        assert "chirpui-nav-tree__hint" in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html


class TestPrimaryNav:
    def test_primary_nav_badge_accessible_label_and_reserved_state(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/primary_nav.html" import primary_nav %}'
            '{{ primary_nav(items=[{"label": "Issues", "href": "/issues", "badge": 12, "badge_label": "12 open issues"}, '
            '{"label": "Runs", "href": "/runs", "badge_loading": true}, '
            '{"label": "Inbox", "href": "/inbox", "badge_expected": true}], current_path="/issues") }}'
        ).render()
        assert 'aria-label="12 open issues"' in html
        assert "chirpui-primary-nav__badge--loading" in html
        assert "chirpui-primary-nav__badge--reserved" in html
        assert html.count('aria-hidden="true"') == 2


class TestRouteTabs:
    def test_route_tabs_badge_accessible_label_and_reserved_state(self, env: Environment) -> None:
        from chirp_ui.route_tabs import tab_is_active

        env.add_global("tab_is_active", tab_is_active)
        html = env.from_string(
            '{% from "chirpui/route_tabs.html" import route_tabs %}'
            '{{ route_tabs(tabs=[{"label": "Pulls", "href": "/pulls", "badge": 2, "badge_label": "2 pull requests"}, '
            '{"label": "Runs", "href": "/runs", "badge_loading": true}, '
            '{"label": "Audit", "href": "/audit", "badge_expected": true}], current_path="/pulls") }}'
        ).render()
        assert 'aria-label="2 pull requests"' in html
        assert "chirpui-route-tab__badge--loading" in html
        assert "chirpui-route-tab__badge--reserved" in html
        assert html.count('aria-hidden="true"') == 3


# ---------------------------------------------------------------------------
# Drag and sortable rows
# ---------------------------------------------------------------------------


class TestDragAndSortableRows:
    def test_sortable_list_render(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sortable_list.html" import sortable_list, sortable_item %}'
            "{% call sortable_list() %}"
            "{% call sortable_item() %}"
            '<span class="chirpui-sortable__handle">☰</span>'
            '<span class="chirpui-sortable__content">First</span>'
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-sortable" in html
        assert "chirpui-sortable__item" in html
        assert 'role="listbox"' in html
        assert 'role="option"' in html

    def test_dnd_primitives_render(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dnd.html" import dnd_list, dnd_item, dnd_handle, dnd_drop_indicator, dnd_board, dnd_column, dnd_card %}'
            "{% call dnd_list() %}"
            "{% call dnd_item() %}{{ dnd_handle() }}{{ dnd_drop_indicator() }}Row{% end %}"
            "{% end %}"
            "{% call dnd_board() %}"
            '{% call dnd_column(title="Todo") %}'
            "{% call dnd_card() %}Card{% end %}"
            "{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-dnd chirpui-dnd--row" in html
        assert "chirpui-dnd__handle" in html
        assert "chirpui-dnd__drop-indicator" in html
        assert "chirpui-dnd chirpui-dnd--board" in html
        assert "chirpui-dnd__column-header" in html
        assert "chirpui-dnd__card" in html

    def test_drag_and_sortable_css_owns_row_pressure(self) -> None:
        css = _chirpui_css()
        assert "@scope (.chirpui-sortable)" in css
        assert "@scope (.chirpui-dnd)" in css
        for selector in (
            ".chirpui-sortable__item > :where(:not(script, style, template))",
            ".chirpui-sortable__content > :where(:not(script, style, template))",
            ".chirpui-dnd__item > :where(:not(script, style, template))",
            ".chirpui-dnd__column > :where(:not(script, style, template))",
            ".chirpui-dnd__card > :where(:not(script, style, template))",
        ):
            assert selector in css
        assert ":scope.chirpui-dnd--board" in css
        assert "overflow-x: auto;" in css
        assert "overscroll-behavior-x: contain;" in css
        assert "flex-wrap: wrap;" in css


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

    def test_params_table_title_is_not_a_heading(self, env: Environment) -> None:
        # The title is a table label, not a document section: it must not
        # impose a heading level (would cause an h1->h3 heading-order jump on
        # /api/ pages). It keeps its class + text but renders as a <p>.
        html = env.from_string(
            '{% from "chirpui/params_table.html" import params_table %}'
            '{{ params_table(rows=[{"name": "x", "type": "int"}], '
            'title="Parameters", columns=["name", "type"]) }}'
        ).render()
        assert "chirpui-params-table__title" in html
        assert "Parameters" in html
        assert "<h3" not in html
        assert "</h3>" not in html

    def test_params_table_wrap_is_keyboard_scrollable(self, env: Environment) -> None:
        # The horizontally-scrollable wrap must be focusable (tabindex) and
        # carry an accessible name (aria-label) so keyboard users can scroll
        # it — axe scrollable-region-focusable. No role="region" (would add a
        # landmark per table -> landmark-unique).
        html = env.from_string(
            '{% from "chirpui/params_table.html" import params_table %}'
            '{{ params_table(rows=[{"name": "x", "type": "int"}], '
            'title="Arguments", columns=["name", "type"]) }}'
        ).render()
        assert 'class="chirpui-params-table__wrap"' in html
        assert 'tabindex="0"' in html
        assert 'aria-label="Arguments"' in html
        assert 'role="region"' not in html

    def test_params_table_wrap_has_default_accessible_name(self, env: Environment) -> None:
        # When no title is given the wrap still needs an accessible name.
        html = env.from_string(
            '{% from "chirpui/params_table.html" import params_table %}'
            '{{ params_table(rows=[{"name": "x", "type": "int"}], '
            'columns=["name", "type"]) }}'
        ).render()
        assert 'tabindex="0"' in html
        assert 'aria-label="Parameters"' in html

    def test_params_table_css_owns_code_heavy_row_pressure(self) -> None:
        css = _chirpui_css()
        assert "@scope (.chirpui-params-table)" in css
        assert ":scope > :where(:not(script, style, template))" in css
        assert ".chirpui-params-table__wrap" in css
        assert "overflow-x: auto;" in css
        assert "overscroll-behavior-x: contain;" in css
        assert "min-width: max-content;" in css
        assert ".chirpui-params-table__td--description" in css
        assert "overflow-wrap: anywhere;" in css


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

    def test_signature_css_owns_local_overflow(self) -> None:
        css = _chirpui_css()
        assert "@scope (.chirpui-signature)" in css
        assert ".chirpui-signature__code" in css
        assert "max-inline-size: 100%;" in css
        assert "overflow-x: auto;" in css
        assert "min-inline-size: max-content;" in css
        assert "white-space: pre;" in css


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

    def test_index_card_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/api/foo"})),
        )
        html = env.from_string(
            '{% from "chirpui/index_card.html" import index_card %}'
            '{{ index_card(href="/api/foo", title="foo", description="Does something.", badge="function") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_index_card_external_href_stays_plain(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content", hrefs=frozenset({"https://example.com/api/foo"})
            ),
        )
        html = env.from_string(
            '{% from "chirpui/index_card.html" import index_card %}'
            '{{ index_card(href="https://example.com/api/foo", title="foo") }}'
        ).render()
        assert 'href="https://example.com/api/foo"' in html
        assert "hx-target=" not in html


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

    def test_btn_defaults_to_type_button(self, env: Environment) -> None:
        """btn() defaults to type='button' to prevent accidental form submission."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Click") }}'
        ).render()
        assert 'type="button"' in html
        assert 'type="submit"' not in html

    def test_btn_explicit_type_submit(self, env: Environment) -> None:
        """Explicit type='submit' is preserved for form submission buttons."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", type="submit", variant="primary") }}'
        ).render()
        assert 'type="submit"' in html

    def test_btn_primary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Submit", variant="primary") }}'
        ).render()
        assert "chirpui-btn--primary" in html

    def test_btn_appearance_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Delete", appearance="outlined", tone="danger") }}'
        ).render()
        assert "chirpui-btn--outlined" in html
        assert "chirpui-btn--danger" in html

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

    def test_btn_small(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Small", size="sm") }}'
        ).render()
        assert "chirpui-btn--sm" in html

    def test_btn_disabled_link_strips_href_and_htmx_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Disabled", href="/demo", hx_get="/demo", disabled=true) }}'
        ).render()
        assert 'aria-disabled="true"' in html
        assert 'href="/demo"' not in html
        assert 'hx-get="/demo"' not in html

    def test_btn_link_with_htmx_emits_boost_and_select_overrides(self, env: Environment) -> None:
        """Link buttons with htmx verbs emit hx-boost='false' and hx-select='unset'."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/demo", hx_get="/demo", hx_target="#content") }}'
        ).render()
        assert 'hx-boost="false"' in html
        assert 'hx-select="unset"' in html

    def test_btn_link_with_htmx_explicit_hx_select(self, env: Environment) -> None:
        """Explicit hx_select on link button overrides the auto-default."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/demo", hx_get="/demo", hx_select="#my-target") }}'
        ).render()
        assert 'hx-select="#my-target"' in html
        assert 'hx-select="unset"' not in html

    def test_btn_link_without_htmx_no_hx_boost(self, env: Environment) -> None:
        """Plain link buttons should not emit hx-boost or hx-select."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Go", href="/demo") }}'
        ).render()
        assert "hx-boost" not in html
        assert "hx-select" not in html

    def test_btn_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/demo"}))
        )
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Go", href="/demo") }}'
        ).render()
        assert 'hx-boost="true"' in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-swap="innerHTML"' in html

    def test_btn_link_with_explicit_htmx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/demo"}))
        )
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/demo", hx_get="/demo", hx_target="#content") }}'
        ).render()
        assert 'hx-target="#site-content"' not in html
        assert 'hx-target="#content"' in html
        assert 'hx-boost="false"' in html

    def test_btn_link_with_explicit_htmx_config_skips_route_link_attrs(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/demo"}))
        )
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/demo", hx_target="#content") }}'
        ).render()
        assert 'hx-target="#site-content"' not in html
        assert 'hx-target="#content"' in html
        assert 'hx-boost="true"' not in html

    def test_btn_link_with_attrs_map_hx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/demo"}))
        )
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/demo", attrs_map={"hx-target": "#content"}) }}'
        ).render()
        assert 'hx-target="#site-content"' not in html
        assert 'hx-target="#content"' in html

    def test_btn_link_disabled_no_hx_boost(self, env: Environment) -> None:
        """Disabled link buttons should not emit hx-boost or hx-select."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/demo", hx_get="/demo", disabled=true) }}'
        ).render()
        assert "hx-boost" not in html
        assert "hx-select" not in html

    def test_btn_hx_dict_shorthand(self, env: Environment) -> None:
        """hx={} dict produces identical output to individual hx_* params."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", hx={"post": "/save", "target": "#result"}) }}'
        ).render()
        assert 'hx-post="/save"' in html
        assert 'hx-target="#result"' in html
        assert 'hx-select="unset"' in html
        assert 'hx-sync="this:drop"' in html
        assert 'hx-disabled-elt="this"' in html

    def test_btn_hx_button_explicit_select_overrides_unset(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", hx={"post": "/save", "target": "#result", "select": "#fragment"}) }}'
        ).render()
        assert 'hx-select="#fragment"' in html
        assert 'hx-select="unset"' not in html

    def test_btn_hx_button_explicit_sync_overrides_drop_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Save", hx={"post": "/save", "target": "#result"},'
            ' hx_sync="#result:queue last", hx_disabled_elt="closest form") }}'
        ).render()
        assert 'hx-sync="#result:queue last"' in html
        assert 'hx-disabled-elt="closest form"' in html
        assert 'hx-sync="this:drop"' not in html

    def test_btn_hx_dict_on_link(self, env: Environment) -> None:
        """hx={} on a link button emits hx-boost=false and hx-select=unset."""
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}'
            '{{ btn("Go", href="/page", hx={"get": "/page", "target": "#main"}) }}'
        ).render()
        assert 'hx-boost="false"' in html
        assert 'hx-select="unset"' in html
        assert 'hx-get="/page"' in html


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------


class TestStreaming:
    def test_streaming_bubble_sse_connect_renders_child_swap_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(sse_connect="/stream") %}Partial{% end %}'
        ).render()
        assert 'sse-connect="/stream"' in html
        assert html.count('sse-swap="fragment"') == 1
        assert 'hx-swap="beforeend"' in html
        assert 'aria-label="assistant response"' in html

    def test_streaming_block(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block() %}Content{% end %}"
        ).render()
        assert "chirpui-streaming-block" in html
        assert "Content" in html
        assert 'role="log"' in html
        assert 'aria-relevant="additions text"' in html

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

    def test_load_sentinel(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import load_sentinel %}'
            '{{ load_sentinel(label="Loading more activity items", busy=true) }}'
        ).render()
        assert "chirpui-load-sentinel" in html
        assert 'role="status"' in html
        assert 'aria-label="Loading more activity items"' in html
        assert 'aria-busy="true"' in html

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

    # --- streaming_bubble role variants & aria-label ---

    def test_streaming_bubble_role_user(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="user") %}Hi{% end %}'
        ).render()
        assert "chirpui-message-bubble--user" in html
        assert 'aria-label="user message"' in html

    def test_streaming_bubble_role_system(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="system") %}Prompt{% end %}'
        ).render()
        assert "chirpui-message-bubble--system" in html
        assert 'aria-label="system message"' in html

    def test_streaming_bubble_role_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="default") %}Msg{% end %}'
        ).render()
        assert "chirpui-message-bubble--default" not in html
        assert 'aria-label="message"' in html

    def test_streaming_bubble_role_assistant_aria_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(role="assistant") %}Reply{% end %}'
        ).render()
        assert 'aria-label="assistant response"' in html

    # --- streaming_bubble non-streaming state ---

    def test_streaming_bubble_not_streaming(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            "{% call streaming_bubble(streaming=false) %}Done{% end %}"
        ).render()
        assert "chirpui-streaming-block--active" not in html
        assert "chirpui-streaming-block__cursor" not in html
        assert "Done" in html

    def test_streaming_bubble_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(cls="my-bubble") %}X{% end %}'
        ).render()
        assert "my-bubble" in html
        assert "chirpui-message-bubble" in html

    def test_streaming_bubble_custom_sse_close(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(sse_connect="/s", sse_close="end") %}{% end %}'
        ).render()
        assert 'sse-close="end"' in html

    # --- streaming state variants ---

    def test_streaming_bubble_state_thinking(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(state="thinking") %}{% end %}'
        ).render()
        assert "chirpui-streaming-bubble--thinking" in html
        assert 'aria-busy="true"' in html
        assert "chirpui-streaming-bubble__thinking" in html
        assert "chirpui-streaming-block__cursor" not in html

    def test_streaming_bubble_state_error(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(state="error") %}<p>Failed</p>{% end %}'
        ).render()
        assert "chirpui-streaming-bubble--error" in html
        assert 'role="alert"' in html

    def test_streaming_bubble_state_content_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(state="content") %}Done{% end %}'
        ).render()
        assert "chirpui-streaming-bubble--" not in html
        assert "Done" in html

    def test_streaming_bubble_state_empty_is_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            "{% call streaming_bubble() %}Body{% end %}"
        ).render()
        assert "chirpui-streaming-bubble--thinking" not in html
        assert "chirpui-streaming-bubble--error" not in html

    def test_streaming_bubble_thinking_no_streaming_cursor(self, env: Environment) -> None:
        """Thinking state shows thinking indicator, not the streaming cursor."""
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(state="thinking", streaming=true) %}{% end %}'
        ).render()
        assert "chirpui-streaming-bubble__thinking" in html
        assert "chirpui-streaming-block__cursor" not in html

    def test_streaming_bubble_state_invalid_falls_back(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            '{% call streaming_bubble(state="bogus") %}OK{% end %}'
        ).render()
        assert "chirpui-streaming-bubble--bogus" not in html

    # --- sse_retry loading state ---

    def test_sse_retry_has_alpine_loading_state(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}{{ sse_retry("/api/stream") }}'
        ).render()
        assert "x-data" in html
        assert "retrying" in html
        assert "x-show" in html

    def test_sse_retry_loading_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}{{ sse_retry("/api/stream") }}'
        ).render()
        assert "chirpui-sse-retry__loading" in html

    # --- streaming_block additional ---

    def test_streaming_block_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            '{% call streaming_block(cls="my-block") %}X{% end %}'
        ).render()
        assert "chirpui-streaming-block my-block" in html

    def test_streaming_block_not_active_no_cursor(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block(streaming=false) %}Done{% end %}"
        ).render()
        assert "chirpui-streaming-block--active" not in html
        assert "chirpui-streaming-block__cursor" not in html

    # --- copy_btn additional ---

    def test_copy_btn_aria_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}{{ copy_btn(label="Copy code") }}'
        ).render()
        assert 'aria-label="Copy code"' in html

    def test_copy_btn_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}{{ copy_btn(cls="my-copy") }}'
        ).render()
        assert "chirpui-copy-btn my-copy" in html

    def test_copy_btn_alpine_state(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}{{ copy_btn(copy_text="hello") }}'
        ).render()
        assert "x-data" in html
        assert "x-show" in html

    def test_copy_btn_escapes_copy_text(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}{{ copy_btn(copy_text="a&b<c") }}'
        ).render()
        assert "a&amp;b&lt;c" in html

    # --- model_card additional ---

    def test_model_card_no_badge(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card(title="GPT-4") %}Answer{% end %}'
        ).render()
        assert "chirpui-model-card__badge" not in html
        assert "GPT-4" in html

    def test_model_card_with_footer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card(title="M", footer="Actions here") %}Body{% end %}'
        ).render()
        assert "chirpui-model-card__footer" in html
        assert "Actions here" in html

    def test_model_card_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import model_card %}'
            '{% call model_card(title="M", cls="wide") %}B{% end %}'
        ).render()
        assert "chirpui-model-card chirpui-card wide" in html

    def test_streaming_bubble_error_boundary(self, env: Environment) -> None:
        """Broken slot content falls back to error state instead of crashing."""
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_bubble %}'
            "{% call streaming_bubble() %}{{ undefined_var.bad }}{% end %}"
        ).render()
        assert "chirpui-message-bubble" in html
        assert "chirpui-streaming--error" in html
        assert "Content unavailable" in html

    def test_streaming_block_error_boundary(self, env: Environment) -> None:
        """Broken slot content falls back to error state instead of crashing."""
        html = env.from_string(
            '{% from "chirpui/streaming.html" import streaming_block %}'
            "{% call streaming_block() %}{{ undefined_var.bad }}{% end %}"
        ).render()
        assert "chirpui-streaming-block" in html
        assert "chirpui-streaming--error" in html


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

    def test_card_css_has_quiet_header_footer_and_body_margin_reset(self) -> None:
        css = _chirpui_css()
        header_rule = css.split(".chirpui-card__header", 1)[1].split("}", 1)[0]
        assert "flex-wrap: wrap" in header_rule
        assert "background: color-mix" in header_rule
        assert "var(--chirpui-border-subtle)" in header_rule
        assert ".chirpui-card__body-content > :first-child" in css
        assert ".chirpui-card__body-content > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-card__body-content > :where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css
        assert ".chirpui-card__footer-wrap:not(:empty)" in css
        assert "background: color-mix(in srgb, var(--chirpui-surface) 90%" in css
        assert '.chirpui-card__header [data-chirpui-role~="content"]' in css
        assert '.chirpui-card__header [data-chirpui-role~="actions"]' in css
        assert '.chirpui-card__footer-wrap[data-chirpui-pressure~="compress"]' in css
        assert '.chirpui-card__header-actions[data-chirpui-affinity~="end"]' in css
        assert ":scope [data-chirpui-pressure" not in css
        assert ":scope [data-chirpui-affinity" not in css

    def test_card_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Hello") %}Content{% end %}'
        ).render()
        assert "chirpui-card__header" in html
        assert 'data-chirpui-role="content"' in html
        assert 'data-chirpui-pressure="flex"' in html
        assert 'data-chirpui-affinity="fill"' in html
        assert 'data-chirpui-role="actions"' in html
        assert 'data-chirpui-pressure="rigid"' in html
        assert 'data-chirpui-affinity="end"' in html
        assert "Hello" in html

    def test_card_appearance_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Review", appearance="outlined", tone="danger") %}Content{% end %}'
        ).render()
        assert "chirpui-card--outlined" in html
        assert "chirpui-card--danger" in html

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

    def test_card_attrs_map_id_for_htmx_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="W", attrs_map={"id": "widget-usage"}) %}Body{% end %}'
        ).render()
        assert 'id="widget-usage"' in html
        assert "chirpui-card__title" in html

    def test_card_collapsible_attrs_map(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="T", collapsible=true, attrs_map={"id": "foldable"}) %}B{% end %}'
        ).render()
        assert "<details" in html
        assert 'id="foldable"' in html

    def test_card_hoverable(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}{% call card(hoverable=true) %}Body{% end %}'
        ).render()
        assert "chirpui-card--hoverable" in html

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

    def test_card_main_link_supports_independent_meta_and_footer_links(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card_main_link %}'
            '{% call card_main_link("/skill/demo", "Demo") %}'
            '{% slot top_meta %}<a href="/collections/demo">demo</a>{% end %}'
            "{% slot header_subtitle %}<code>alias-demo</code>{% end %}"
            "<p>Description</p>"
            '{% slot footer %}<a href="/tags/demo">tag</a>{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-card--linked" in html
        assert "chirpui-card__top-meta" in html
        assert 'href="/skill/demo"' in html
        assert 'href="/collections/demo"' in html
        assert 'href="/tags/demo"' in html
        assert "alias-demo" in html

    def test_card_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/skill/demo"})),
        )
        html = env.from_string(
            '{% from "chirpui/card.html" import card_link %}'
            '{% call card_link("/skill/demo", "Demo") %}'
            "<p>Description</p>"
            "{% end %}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_card_link_external_href_stays_plain(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"https://example.com/demo"})),
        )
        html = env.from_string(
            '{% from "chirpui/card.html" import card_link %}'
            '{% call card_link("https://example.com/demo", "Demo") %}'
            "<p>Description</p>"
            "{% end %}"
        ).render()
        assert 'href="https://example.com/demo"' in html
        assert "hx-target=" not in html

    def test_card_main_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content", hrefs=frozenset({"/skill/demo", "/collections/demo"})
            ),
        )
        html = env.from_string(
            '{% from "chirpui/card.html" import card_main_link %}'
            '{% call card_main_link("/skill/demo", "Demo") %}'
            '{% slot top_meta %}<a href="/collections/demo">demo</a>{% end %}'
            "<p>Description</p>"
            "{% end %}"
        ).render()
        assert 'href="/skill/demo"' in html
        assert 'hx-target="#site-content"' in html
        assert html.count('hx-target="#site-content"') == 1

    def test_resource_card_full_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import resource_card %}'
            '{% call resource_card("/skills/demo", "Demo", description="Summary", top_meta="builtin") %}'
            "{% slot badges %}<span>badge</span>{% end %}"
            "{% slot subtitle %}<code>::demo</code>{% end %}"
            "{% slot footer %}<span>tag</span>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-resource-card" in html
        assert "chirpui-card--link" in html
        assert "Summary" in html
        assert "builtin" in html
        assert "::demo" in html
        assert "tag" in html
        assert 'data-chirpui-role="metadata"' in html
        assert 'data-chirpui-pressure="compress"' in html
        assert 'data-chirpui-affinity="block-start"' in html
        assert 'data-chirpui-affinity="block-end"' in html

    def test_resource_card_full_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/skills/demo"})),
        )
        html = env.from_string(
            '{% from "chirpui/card.html" import resource_card %}'
            '{% call resource_card("/skills/demo", "Demo", description="Summary", top_meta="builtin") %}'
            "{% end %}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_resource_card_links_use_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content",
                hrefs=frozenset({"/skills/demo", "/collections/demo"}),
            ),
        )
        html = env.from_string(
            '{% from "chirpui/card.html" import resource_card %}'
            '{% call resource_card("/skills/demo", "Demo", description="Summary", top_meta="collection", top_meta_href="/collections/demo", link_mode="main") %}'
            "{% end %}"
        ).render()
        assert 'href="/skills/demo"' in html
        assert 'href="/collections/demo"' in html
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2

    def test_resource_card_main_link_keeps_meta_link_separate(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import resource_card %}'
            '{% call resource_card("/skills/demo", "Demo", description="Summary", top_meta="collection", top_meta_href="/collections/demo", link_mode="main") %}'
            '{% slot footer %}<a href="/tags/demo">tag</a>{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-card--linked" in html
        assert 'href="/skills/demo"' in html
        assert 'href="/collections/demo"' in html
        assert 'href="/tags/demo"' in html

    def test_resource_card_css_owns_content_and_metadata_pressure(self) -> None:
        css = _chirpui_css()
        assert "@scope (.chirpui-resource-card)" in css
        for selector in (
            ":scope .chirpui-card__body > :where(:not(script, style, template))",
            ":scope .chirpui-card__footer-wrap > :where(:not(script, style, template))",
            ":scope .chirpui-card__top-meta > :where(:not(script, style, template))",
        ):
            assert selector in css
        assert ".chirpui-resource-card__description" in css
        assert "overflow-wrap: anywhere;" in css

    def test_card_gradient_border(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(border_variant="gradient") %}Content{% end %}'
        ).render()
        assert "chirpui-card--gradient-border" in html

    def test_card_gradient_header(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Title", header_variant="gradient") %}Content{% end %}'
        ).render()
        assert "chirpui-card--gradient-header" in html

    def test_card_gradient_border_and_header_combined(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Title", border_variant="gradient", header_variant="gradient") %}Content{% end %}'
        ).render()
        assert "chirpui-card--gradient-border" in html
        assert "chirpui-card--gradient-header" in html

    def test_card_collapsible_gradient_border(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="Toggle", collapsible=true, border_variant="gradient") %}Body{% end %}'
        ).render()
        assert "<details" in html
        assert "chirpui-card--gradient-border" in html

    def test_card_footer_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="T") %}Body'
            "{% slot footer %}Slot footer{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-card__footer-wrap" in html
        assert "Slot footer" in html

    def test_card_footer_param_backward_compat(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(footer="Legacy footer") %}Body{% end %}'
        ).render()
        assert "chirpui-card__footer-wrap" in html
        assert "Legacy footer" in html

    def test_card_footer_slot_collapsible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="T", collapsible=true) %}Body'
            "{% slot footer %}Slot footer{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-card__footer-wrap" in html
        assert "Slot footer" in html

    def test_card_attrs_unsafe(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="T", attrs_unsafe=\'data-x="1"\') %}Body{% end %}'
        ).render()
        assert 'data-x="1"' in html

    def test_card_attrs_legacy_still_works(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="T", attrs=\'data-old="y"\') %}Body{% end %}'
        ).render()
        assert 'data-old="y"' in html


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
        for size in ("sm", "md", "lg"):
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
        assert 'x-data="chirpuiDialogTarget()"' in html
        assert 'data-dialog-target="dlg"' in html

    def test_modal_no_header_when_no_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}{% call modal("dlg") %}Body{% end %}'
        ).render()
        assert "chirpui-modal__header" not in html

    def test_modal_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal, modal_trigger %}'
            '{{ modal_trigger("dlg", label="Open") }}'
            '{% call modal("dlg", title="Settings", size="lg") %}'
            "Body"
            "{% slot header_actions %}<button>Help</button>{% end %}"
            '{% slot footer %}<form method="dialog"><button>Done</button></form>{% end %}'
            "{% end %}"
        ).render()
        assert '<dialog id="dlg"' in html
        assert 'class="chirpui-modal chirpui-modal--lg"' in html
        assert 'closedby="any"' in html
        assert 'class="chirpui-modal-trigger"' in html
        assert 'type="button"' in html
        assert 'x-data="chirpuiDialogTarget()"' in html
        assert 'data-dialog-target="dlg"' in html
        assert '@click="open()"' in html
        assert "chirpui-modal__header" in html
        assert "chirpui-modal__title" in html
        assert "chirpui-modal__header-actions" in html
        assert 'form method="dialog"' in html
        assert 'class="chirpui-modal__close"' in html
        assert 'aria-label="Close"' in html
        assert "chirpui-modal__body" in html
        assert "chirpui-modal__footer" in html

    def test_modal_css_owns_region_rhythm_and_pressure(self) -> None:
        css = _chirpui_css()

        assert ".chirpui-modal__body" in css
        assert ".chirpui-modal__body > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-modal__body > :where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css
        assert ".chirpui-modal__footer > :where(:not(script, style, template))" in css
        assert ".chirpui-modal__header > form" in css
        assert "overflow-wrap: anywhere" in css


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

    def test_tab_with_htmx_emits_boost_and_select_overrides(self, env: Environment) -> None:
        """Tabs with hx_target emit hx-boost='false' and hx-select='unset'."""
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("t1", "Tab", url="/tab/1", hx_target="#content") }}'
        ).render()
        assert 'hx-boost="false"' in html
        assert 'hx-select="unset"' in html

    def test_tab_without_htmx_no_hx_boost(self, env: Environment) -> None:
        """Tabs without hx_target should not emit hx-boost or hx-select."""
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}{{ tab("t1", "Tab", url="/tab/1") }}'
        ).render()
        assert "hx-boost" not in html
        assert "hx-select" not in html

    def test_tab_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/tab/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}{{ tab("t1", "Tab", url="/tab/1") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_tab_with_htmx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/tab/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tab %}'
            '{{ tab("t1", "Tab", url="/tab/1", hx_target="#content") }}'
        ).render()
        assert 'hx-target="#content"' in html
        assert 'hx-target="#site-content"' not in html

    def test_tabs_htmx_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tabs, tab %}'
            '{% call tabs(cls="extra-tabs") %}'
            '{{ tab("details", "Details", url="/tabs/details", hx_target="#tab-content", active=true) }}'
            "{% end %}"
        ).render()
        assert 'class="chirpui-tabs extra-tabs"' in html
        assert 'role="tablist"' in html
        assert 'class="chirpui-tab chirpui-tab--active"' in html
        assert 'id="tab-details"' in html
        assert 'role="tab"' in html
        assert 'aria-selected="true"' in html
        assert 'href="/tabs/details"' in html
        assert 'hx-boost="false"' in html
        assert 'hx-select="unset"' in html
        assert 'hx-get="/tabs/details"' in html
        assert 'hx-target="#tab-content"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'hx-push-url="false"' in html

    def test_tabs_panels_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs_panels.html" import tabs_container, tab_button, tab_panel %}'
            '{% call tabs_container(active="overview") %}'
            '{{ tab_button("overview", "Overview") }}'
            "{% call tab_panel('overview') %}Panel{% end %}"
            "{% end %}"
        ).render()
        assert 'class="chirpui-tabs"' in html
        assert "x-id=\"['tab', 'tabpanel']\"" in html
        assert 'x-data="chirpuiTabs()"' in html
        assert 'data-active="overview"' in html
        assert 'class="chirpui-tabs__tab"' in html
        assert 'data-tab-id="overview"' in html
        assert 'role="tab"' in html
        assert ':aria-selected="active === $el.dataset.tabId"' in html
        assert ":aria-controls=\"$id('tabpanel', $el.dataset.tabId)\"" in html
        assert ":id=\"$id('tab', $el.dataset.tabId)\"" in html
        assert '@click="selectTab($el)"' in html
        assert 'class="chirpui-tab-panel"' in html
        assert 'role="tabpanel"' in html
        assert ":aria-labelledby=\"$id('tab', $el.dataset.tabId)\"" in html
        assert "x-cloak" in html
        assert "x-transition" in html

    def test_tabs_panels_payload_uses_data_attributes_not_inline_js_literals(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs_panels.html" import tabs_container, tab_button, tab_panel %}'
            '{% call tabs_container(active="bad\' } ); alert(1)//") %}'
            '{{ tab_button("bad\' } ); alert(1)//", "Bad <tab>") }}'
            '{% call tab_panel("bad\' } ); alert(1)//") %}Panel{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui:tab-changed" not in html
        assert '@click="selectTab($el)"' in html
        assert 'data-active="bad&#39; } ); alert(1)//"' in html
        assert 'data-tab-id="bad&#39; } ); alert(1)//"' in html
        assert "&lt;tab&gt;" in html
        assert "<tab>" not in html


class TestAsciiTabs:
    def test_ascii_tab_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/tab/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tab %}'
            '{{ ascii_tab("t1", "Tab", url="/tab/1") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_ascii_tab_with_htmx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/tab/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/ascii_tabs.html" import ascii_tab %}'
            '{{ ascii_tab("t1", "Tab", url="/tab/1", hx_target="#panel") }}'
        ).render()
        assert 'hx-target="#panel"' in html
        assert 'hx-target="#site-content"' not in html


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

    def test_dropdown_menu_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_menu %}'
            "{{ dropdown_menu('Actions', items=["
            '{"label": "Edit", "action": "edit"},'
            '{"divider": true},'
            '{"label": "Docs", "href": "/docs"},'
            '{"label": "Plain"}'
            "]) }}"
        ).render()
        assert 'x-data="chirpuiDropdown()"' in html
        assert "x-id=\"['dropdown-menu']\"" in html
        assert ':data-align-x="alignX"' in html
        assert ':data-align-y="alignY"' in html
        assert 'x-ref="trigger"' in html
        assert 'role="button"' in html
        assert 'tabindex="0"' in html
        assert 'aria-haspopup="menu"' in html
        assert ':aria-expanded="open"' in html
        assert ":aria-controls=\"$id('dropdown-menu')\"" in html
        assert 'x-ref="panel"' in html
        assert 'role="menu"' in html
        assert 'aria-orientation="vertical"' in html
        assert "x-cloak" in html
        assert 'role="separator"' in html
        assert 'role="menuitem"' in html
        assert 'data-label="Edit"' in html
        assert 'data-action="edit"' in html
        assert 'data-label="Docs"' in html
        assert 'data-href="/docs"' in html
        assert '@click="selectItem($el, $refs.trigger)"' in html

    def test_dropdown_select_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_select %}'
            '{{ dropdown_select("View", items=[{"label": "Open", "value": "open"}]) }}'
        ).render()
        assert 'class="chirpui-dropdown chirpui-dropdown--select"' in html
        assert 'x-data="chirpuiDropdownSelect()"' in html
        assert 'x-init="init()"' in html
        assert "x-id=\"['dropdown-select', 'listbox-option']\"" in html
        assert 'data-item-count="1"' in html
        assert 'data-selected="Open"' in html
        assert 'role="combobox"' in html
        assert 'aria-haspopup="listbox"' in html
        assert ':aria-expanded="open"' in html
        assert ":aria-activedescendant=\"open ? $id('listbox-option', focusedIndex) : ''\"" in html
        assert 'role="listbox"' in html
        assert 'role="option"' in html
        assert 'tabindex="-1"' in html
        assert 'data-label="Open"' in html
        assert 'data-value="open"' in html

    def test_dropdown_split_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_split %}'
            '{{ dropdown_split("Export", primary_href="/export", items=[{"label": "CSV", "href": "/csv"}]) }}'
        ).render()
        assert 'class="chirpui-dropdown chirpui-dropdown--split"' in html
        assert 'x-data="chirpuiDropdown()"' in html
        assert "x-id=\"['dropdown-split']\"" in html
        assert (
            'class="chirpui-dropdown__split-primary chirpui-btn chirpui-btn--primary chirpui-btn--sm"'
            in html
        )
        assert 'href="/export"' in html
        assert 'class="chirpui-dropdown__trigger chirpui-dropdown__trigger--split"' in html
        assert 'aria-haspopup="menu"' in html
        assert ":aria-controls=\"$id('dropdown-split')\"" in html
        assert 'role="menu"' in html
        assert 'data-label="CSV"' in html
        assert 'data-href="/csv"' in html
        assert '@click="selectItem($el, $refs.trigger)"' in html


# ---------------------------------------------------------------------------
# Alpine magics and chirpui:* events
# ---------------------------------------------------------------------------


class TestAlpineMagics:
    """Verify dropdown_menu, tabs_panels, tray, modal_overlay emit chirpui:* events."""

    def test_dropdown_menu_emits_selection_handler(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_menu %}'
            '{{ dropdown_menu("<span>X</span>", items=[{"label": "A", "href": "/a"}]) }}'
        ).render()
        assert 'data-label="A"' in html
        assert 'data-href="/a"' in html
        assert '@click="selectItem($el, $refs.trigger)"' in html
        assert "chirpui:dropdown-selected" not in html
        assert 'x-ref="trigger"' in html
        assert 'x-ref="panel"' in html
        assert ':data-align-x="alignX"' in html
        assert 'x-data="chirpuiDropdown()"' in html

    def test_dropdown_menu_payload_uses_data_attributes_not_inline_js_literals(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_menu %}'
            "{{ dropdown_menu('Payloads', items=["
            '{"label": "Quote \\\' <script>", "action": "archive\\\' } ); alert(1);//"}'
            "]) }}"
        ).render()
        click_handlers = re.findall(r'@click="([^"]*)"', html)
        assert "selectItem($el, $refs.trigger)" in click_handlers
        assert "chirpui:dropdown-selected" not in html
        assert "&lt;script&gt;" in html
        assert "<script>" not in html
        assert 'data-action="archive&#39; } ); alert(1);//"' in html

    def test_dropdown_menu_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/a"}))
        )
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_menu %}'
            '{{ dropdown_menu("<span>X</span>", items=[{"label": "A", "href": "/a"}]) }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_tabs_panels_emits_dispatch(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs_panels.html" import tabs_container, tab_button, tab_panel %}'
            '{% call tabs_container(active="a") %}'
            '{{ tab_button("a", "A") }}{{ tab_button("b", "B") }}'
            '{% call tab_panel("a") %}x{% end %}{% call tab_panel("b") %}y{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui:tab-changed" not in html
        assert 'x-data="chirpuiTabs()"' in html
        assert 'data-active="a"' in html
        assert 'data-tab-id="a"' in html
        assert '@click="selectTab($el)"' in html
        assert "x-id=\"['tab'" in html or "x-id=" in html

    def test_tray_emits_dispatch(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tray.html" import tray %}'
            '{% call tray("filters", "Filters") %}content{% end %}'
        ).render()
        assert "chirpui:tray-closed" in html
        assert "x-trap.inert.noscroll" in html

    def test_tray_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tray.html" import tray, tray_trigger %}'
            '{{ tray_trigger("filters", "Filters", icon="settings") }}'
            '{% call tray("filters", "Filters", position="left") %}content{% end %}'
        ).render()
        assert 'class="chirpui-btn chirpui-btn--default chirpui-btn--sm"' in html
        assert 'data-tray-id="filters"' in html
        assert '@click="$store.trays[trayId] = true"' in html
        assert 'aria-controls="tray-filters"' in html
        assert ':aria-expanded="$store.trays[trayId]"' in html
        assert 'class="chirpui-tray chirpui-tray--left chirpui-tray--closed"' in html
        assert 'id="tray-filters"' in html
        assert 'role="dialog"' in html
        assert 'aria-modal="true"' in html
        assert 'aria-labelledby="tray-filters-title"' in html
        assert 'aria-hidden="true"' in html
        assert ':aria-hidden="!$store.trays[trayId]"' in html
        assert "chirpui-tray__backdrop" in html
        assert "chirpui-tray__panel" in html
        assert 'x-trap.inert.noscroll="$store.trays[trayId]"' in html
        assert 'id="tray-filters-title"' in html
        assert "chirpui-tray__close" in html
        assert "chirpui:tray-closed" in html

    def test_tray_css_owns_body_rhythm_and_pressure(self) -> None:
        css = _chirpui_css()

        assert ".chirpui-tray__panel" in css
        assert ".chirpui-tray__body > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-tray__body > :where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css
        assert ".chirpui-tray__title" in css
        assert "overflow-wrap: anywhere" in css

    def test_tray_id_stays_out_of_alpine_literals(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tray.html" import tray, tray_trigger %}'
            '{{ tray_trigger("bad\\\'];alert(1)//", "Open") }}'
            '{% call tray("bad\\\'];alert(1)//", "Bad") %}content{% end %}'
        ).render()
        assert "$store.trays['bad" not in html
        assert "$store.trays[trayId]" in html
        assert "data-tray-id=" in html

    def test_tray_renders_closed_by_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tray.html" import tray %}'
            '{% call tray("filters", "Filters") %}content{% end %}'
        ).render()
        assert "chirpui-tray--closed" in html

    def test_modal_overlay_emits_dispatch(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal_overlay.html" import modal_overlay %}'
            '{% call modal_overlay("confirm", "Confirm") %}content{% end %}'
        ).render()
        assert "chirpui:modal-closed" in html
        assert "x-trap.inert.noscroll" in html

    def test_modal_overlay_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal_overlay.html" import modal_overlay, modal_overlay_trigger %}'
            '{{ modal_overlay_trigger("confirm", "Open", variant="danger") }}'
            '{% call modal_overlay("confirm", "Confirm") %}content{% end %}'
        ).render()
        assert 'class="chirpui-btn chirpui-btn--danger chirpui-btn--sm"' in html
        assert 'data-modal-id="confirm"' in html
        assert '@click="$store.modals[modalId] = true"' in html
        assert 'aria-controls="modal-confirm"' in html
        assert ':aria-expanded="$store.modals[modalId]"' in html
        assert 'class="chirpui-modal chirpui-modal--closed"' in html
        assert 'id="modal-confirm"' in html
        assert 'role="dialog"' in html
        assert 'aria-modal="true"' in html
        assert 'aria-labelledby="modal-confirm-title"' in html
        assert ':aria-hidden="!$store.modals[modalId]"' in html
        assert "chirpui-modal__backdrop" in html
        assert "chirpui-modal__panel" in html
        assert 'x-trap.inert.noscroll="$store.modals[modalId]"' in html
        assert 'id="modal-confirm-title"' in html

    def test_modal_id_stays_out_of_alpine_literals(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal_overlay.html" import modal_overlay, modal_overlay_trigger %}'
            '{{ modal_overlay_trigger("bad\\\'];alert(1)//", "Open") }}'
            '{% call modal_overlay("bad\\\'];alert(1)//", "Bad") %}content{% end %}'
        ).render()
        assert "$store.modals['bad" not in html
        assert "$store.modals[modalId]" in html
        assert "data-modal-id=" in html


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

    def test_toast_custom_id(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("msg", id="my-toast") }}'
        ).render()
        assert 'id="my-toast"' in html

    def test_toast_role_alert(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("Error!", variant="error") }}'
        ).render()
        assert 'role="alert"' in html

    def test_toast_container_custom_id(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast_container %}'
            '{{ toast_container(id="my-toasts") }}'
        ).render()
        assert 'id="my-toasts"' in html

    def test_toast_container_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast_container %}'
            '{{ toast_container(cls="custom-container") }}'
        ).render()
        assert "chirpui-toast-container custom-container" in html

    def test_toast_message_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toast.html" import toast %}{{ toast("Hello") }}'
        ).render()
        assert "chirpui-toast__message" in html
        assert "Hello" in html


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

    def test_table_data_driven_rows(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(headers=["Name", "Email"],'
            ' rows=[("Alice", "alice@x.com"), ("Bob", "bob@x.com")]) }}'
        ).render()
        assert "Alice" in html
        assert "Bob" in html
        assert "alice@x.com" in html
        assert html.count("chirpui-table__row") == 2

    def test_table_data_driven_rows_with_alignment(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(headers=["Name", "Count"],'
            ' rows=[("Alice", "42")],'
            ' align=["left", "right"]) }}'
        ).render()
        assert "chirpui-table__th--left" in html
        assert "chirpui-table__th--right" in html
        assert "chirpui-table__td--left" in html
        assert "chirpui-table__td--right" in html

    def test_table_data_driven_ignores_slot(self, env: Environment) -> None:
        """When rows= is provided, slot content is not rendered."""
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name"],'
            ' rows=[("Alice",)]) %}'
            '{{ row("SHOULD_NOT_APPEAR") }}'
            "{% end %}"
        ).render()
        assert "Alice" in html
        assert "SHOULD_NOT_APPEAR" not in html

    def test_table_slot_still_works_without_rows(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name"]) %}'
            '{{ row("Alice") }}'
            "{% end %}"
        ).render()
        assert "Alice" in html

    def test_row_inherits_alignment_from_table(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name", "Count"], align=["left", "right"]) %}'
            '{{ row("Alice", "42") }}'
            "{% end %}"
        ).render()
        assert "chirpui-table__td--left" in html
        assert "chirpui-table__td--right" in html

    def test_row_standalone_without_provide(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import row %}{{ row("Alice", "42") }}'
        ).render()
        assert "Alice" in html
        assert "chirpui-table__td--" not in html

    def test_row_alignment_partial(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["A", "B", "C"], align=["center"]) %}'
            '{{ row("1", "2", "3") }}'
            "{% end %}"
        ).render()
        assert "chirpui-table__td--center" in html
        assert html.count("chirpui-table__td--") == 1

    def test_row_alignment_multiple_rows(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name", "Count"], align=["left", "right"]) %}'
            '{{ row("Alice", "42") }}'
            '{{ row("Bob", "7") }}'
            "{% end %}"
        ).render()
        assert html.count("chirpui-table__td--left") == 2
        assert html.count("chirpui-table__td--right") == 2

    def test_aligned_row_still_works(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, aligned_row %}'
            '{% call table(headers=["Name", "Count"]) %}'
            '{{ aligned_row(["Alice", "42"], align=["left", "right"]) }}'
            "{% end %}"
        ).render()
        assert "chirpui-table__td--left" in html
        assert "chirpui-table__td--right" in html

    def test_table_css_owns_cell_and_action_relationships(self) -> None:
        css = _chirpui_css()
        assert ".chirpui-table-wrap" in css
        assert "max-inline-size: 100%;" in css
        assert ".chirpui-table__td > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-table__td:not(.chirpui-table__td--actions):not(:has(.chirpui-row-actions__trigger))"
            in css
        )
        assert ".chirpui-table__td:has(.chirpui-row-actions__trigger)" in css
        assert "overflow-x: auto;" in css
        assert "overscroll-behavior-x: contain;" in css


# ---------------------------------------------------------------------------
# Donut
# ---------------------------------------------------------------------------


class TestDonut:
    def test_donut_default_percentage(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}{{ donut(value=75, max=100) }}'
        ).render()
        assert "75%" in html
        assert "chirpui-donut" in html
        assert "chirpui-donut--gold" in html

    def test_donut_text_overrides_center(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}{{ donut(value=3, max=5, text="3/5") }}'
        ).render()
        assert "3/5" in html
        assert "60%" not in html

    def test_donut_caption(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}'
            '{{ donut(value=40, max=100, caption="Success") }}'
        ).render()
        assert "40%" in html
        assert "Success" in html
        assert "chirpui-donut__caption" in html

    def test_donut_text_and_caption(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}'
            '{{ donut(value=3, max=5, text="3/5", caption="Tasks") }}'
        ).render()
        assert "3/5" in html
        assert "Tasks" in html

    def test_donut_no_caption_no_caption_element(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}{{ donut(value=50, max=100) }}'
        ).render()
        assert "chirpui-donut__caption" not in html

    def test_donut_label_backwards_compat(self, env: Environment) -> None:
        """label= still works as alias for text=."""
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}{{ donut(value=3, max=5, label="3/5") }}'
        ).render()
        assert "3/5" in html

    def test_donut_variants(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}{{ donut(value=50, variant="success") }}'
        ).render()
        assert "chirpui-donut--success" in html

    def test_donut_sizes(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}{{ donut(value=50, size="lg") }}'
        ).render()
        assert "chirpui-donut--lg" in html

    def test_donut_aria_label_with_caption(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/donut.html" import donut %}'
            '{{ donut(value=40, max=100, caption="Uptime") }}'
        ).render()
        assert 'aria-label="40%: Uptime"' in html


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

    def test_pagination_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content",
                hrefs=frozenset(
                    {
                        "/items?page=1",
                        "/items?page=2",
                        "/items?page=3",
                        "/items?page=4",
                        "/items?page=5",
                    }
                ),
            ),
        )
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=2, total=5,"
            ' url_pattern="/items?page={page}") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

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
        assert "<button" in html
        assert "disabled" in html
        assert 'aria-label="Previous page"' in html

    def test_pagination_next_disabled_on_last(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=3, total=3,"
            ' url_pattern="/p?page={page}") }}'
        ).render()
        assert "<button" in html
        assert "disabled" in html
        assert 'aria-label="Next page"' in html

    def test_pagination_with_htmx(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=2, total=5,"
            ' url_pattern="/p?page={page}",'
            ' hx_target="#list") }}'
        ).render()
        assert 'hx-target="#list"' in html
        assert "hx-get" in html

    def test_pagination_hx_select(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            "{{ pagination(current=2, total=5,"
            ' url_pattern="/p?page={page}",'
            ' hx_target="#main", hx_select="#main") }}'
        ).render()
        assert 'hx-select="#main"' in html


class TestFilterBar:
    def test_filter_group_and_chip(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_chips.html" import filter_group, filter_chip %}'
            '{% call filter_group(name="Type") %}'
            '{{ filter_chip("All", href="/", active=true) }}'
            '{{ filter_chip("Grass", color="#78c850", href="/g") }}'
            "{% end %}"
        ).render()
        assert 'role="radiogroup"' in html
        assert "chirpui-filter-group" in html
        assert "chirpui-filter-chip" in html
        assert "chirpui-badge--custom" in html

    def test_filter_chip_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/g"})),
        )
        html = env.from_string(
            '{% from "chirpui/filter_chips.html" import filter_chip %}'
            '{{ filter_chip("Grass", color="#78c850", href="/g") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_filter_chip_with_htmx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/g"})),
        )
        html = env.from_string(
            '{% from "chirpui/filter_chips.html" import filter_chip %}'
            '{{ filter_chip("Grass", color="#78c850", href="/g", hx_target="#panel") }}'
        ).render()
        assert 'hx-target="#panel"' in html
        assert 'hx-target="#site-content"' not in html

    def test_filter_row_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_row %}'
            '{% call filter_row("/search") %}'
            '<input name="q" />'
            "{% end %}"
        ).render()
        assert "chirpui-filter-row" in html
        assert "chirpui-cluster" in html
        assert "chirpui-font-sm" in html
        assert "<form" in html
        assert 'action="/search"' in html
        assert 'method="get"' in html
        assert '<input name="q" />' in html

    def test_filter_row_custom_gap(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_row %}'
            '{% call filter_row(gap="md") %}x{% end %}'
        ).render()
        assert "chirpui-cluster--gap-md" in html

    def test_filter_row_htmx_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_row %}'
            '{% call filter_row("/filter",'
            ' attrs_map={"hx-get": "/filter", "hx-target": "#results", "hx-swap": "innerHTML"}) %}'
            "x{% end %}"
        ).render()
        assert 'hx-get="/filter"' in html
        assert 'hx-target="#results"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'hx-select="unset"' in html
        assert 'hx-disinherit="hx-select"' in html
        assert 'hx-sync="this:replace"' in html

    def test_filter_row_preserves_explicit_htmx_coordination(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_row %}'
            '{% call filter_row("/filter",'
            ' attrs_map={"hx-get": "/filter", "hx-target": "#results",'
            ' "hx-select": "#rows", "hx-sync": "#results:queue last"}) %}'
            "x{% end %}"
        ).render()
        assert 'hx-select="#rows"' in html
        assert 'hx-sync="#results:queue last"' in html
        assert 'hx-select="unset"' not in html
        assert html.count("hx-sync=") == 1

    def test_filter_row_no_action(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_row %}'
            "{% call filter_row() %}x{% end %}"
        ).render()
        assert "action=" not in html

    def test_filter_row_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_row %}'
            '{% call filter_row(cls="my-extra") %}x{% end %}'
        ).render()
        assert "my-extra" in html


class TestStatusIndicator:
    def test_status_custom_color(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/status.html" import status_indicator %}'
            '{{ status_indicator("Live", color="#78c850") }}'
        ).render()
        assert "chirpui-status-indicator--custom" in html
        assert "--chirpui-status-color: #78c850" in html


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

    def test_alert_appearance_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(appearance="outlined", tone="danger") %}msg{% end %}'
        ).render()
        assert "chirpui-alert--outlined" in html
        assert "chirpui-alert--danger" in html

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

    def test_alert_with_semantic_info_icon_no_warning(
        self,
        env: Environment,
        recwarn: pytest.WarningsRecorder,
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(icon="info") %}Info message{% end %}'
        ).render()
        assert "chirpui-alert__icon" in html
        assert "◎" in html
        assert not [w for w in recwarn if issubclass(w.category, ChirpUIValidationWarning)]

    def test_alert_with_title(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(title="Heads up") %}Body text{% end %}'
        ).render()
        assert "chirpui-alert__title" in html
        assert "Heads up" in html
        assert "Body text" in html

    def test_alert_header_actions_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(variant="error") %}msg'
            "{% slot header_actions %}<button>Retry</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-alert__actions" in html
        assert "Retry" in html

    def test_alert_actions_slot_backward_compat(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(variant="error") %}msg'
            "{% slot actions %}<button>Retry</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-alert__actions" in html
        assert "Retry" in html

    def test_collapsible_alert_uses_owned_body_spacing(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            '{% call alert(collapsible=true, title="More") %}Details{% end %}'
        ).render()
        css = _chirpui_css()

        assert "chirpui-mt-sm" not in html
        assert ".chirpui-alert > .chirpui-alert__body + .chirpui-alert__body" in css


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

    def test_form_css_owns_direct_child_rhythm(self) -> None:
        css = _chirpui_css()
        form_rule = css.split(".chirpui-form {", 1)[1].split("}", 1)[0]
        child_rule = css.split(".chirpui-form > :where(:not(script, style, template))", 1)[1].split(
            "}", 1
        )[0]
        actions_rule = css.split(".chirpui-form > .chirpui-form-actions", 1)[1].split("}", 1)[0]
        assert "display: flex;" in form_rule
        assert "gap: var(--chirpui-space-stack-gap);" in form_rule
        assert "margin-block: 0;" in child_rule
        assert "margin-block-start: 0;" in actions_rule

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

    def test_form_macro_reset_on_success_default_for_hx_forms(self, env: Environment) -> None:
        """Forms with hx-post/put/patch/delete get reset-on-success by default."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", hx_post="/x", hx_target="#y") %}Body{% end %}'
        ).render()
        assert 'hx-on::after-request="if(event.detail.successful) this.reset()"' in html
        assert 'hx-sync="this:drop"' in html
        assert 'hx-disabled-elt="find button, find input[type=submit]"' in html

    def test_form_macro_reset_on_success_via_attrs_map(self, env: Environment) -> None:
        """Forms with hx-post in attrs_map get reset-on-success by default."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", attrs_map={"hx-post": "/x", "hx-target": "#y"}) %}Body{% end %}'
        ).render()
        assert 'hx-on::after-request="if(event.detail.successful) this.reset()"' in html
        assert 'hx-sync="this:drop"' in html

    def test_form_macro_explicit_submit_coordination_overrides_defaults(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", hx_post="/x", hx_sync="#result:queue last",'
            ' hx_disabled_elt="closest form") %}Body{% end %}'
        ).render()
        assert 'hx-sync="#result:queue last"' in html
        assert 'hx-disabled-elt="closest form"' in html
        assert 'hx-sync="this:drop"' not in html

    def test_form_macro_reset_on_success_opt_out(self, env: Environment) -> None:
        """hx_reset_on_success=false disables form reset."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", hx_post="/x", hx_reset_on_success=false) %}Body{% end %}'
        ).render()
        assert "hx-on::after-request" not in html

    def test_form_macro_no_reset_without_hx(self, env: Environment) -> None:
        """Forms without hx attributes do not get reset-on-success."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/submit", method="post") %}<input>{% end %}'
        ).render()
        assert "hx-on::after-request" not in html

    def test_form_auto_hx_select_unset(self, env: Environment) -> None:
        """htmx forms auto-add hx-select='unset' to prevent boost inheritance."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", hx_post="/x") %}Body{% end %}'
        ).render()
        assert 'hx-select="unset"' in html
        assert 'hx-disinherit="hx-select"' in html

    def test_form_explicit_hx_select_overrides_auto(self, env: Environment) -> None:
        """Explicit hx_select overrides the auto-default, no disinherit."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/x", hx_post="/x", hx_select="#my-target") %}Body{% end %}'
        ).render()
        assert 'hx-select="#my-target"' in html
        assert "hx-disinherit" not in html

    def test_form_no_hx_select_without_htmx(self, env: Environment) -> None:
        """Plain forms (no htmx) should not get hx-select or hx-disinherit."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/submit", method="post") %}<input>{% end %}'
        ).render()
        assert "hx-select" not in html
        assert "hx-disinherit" not in html

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

    def test_fieldset_css_owns_grouped_content_rhythm(self) -> None:
        css = _chirpui_css()
        fieldset_rule = css.split(".chirpui-fieldset {", 1)[1].split("}", 1)[0]
        child_rule = css.split(
            ".chirpui-fieldset > :where(:not(legend, script, style, template))", 1
        )[1].split("}", 1)[0]
        sibling_rule = css.split("+ :where(:not(legend, script, style, template))", 1)[1].split(
            "}", 1
        )[0]
        assert "min-width: 0;" in fieldset_rule
        assert "margin: 0 0 var(--chirpui-spacing);" in fieldset_rule
        assert "margin-block: 0;" in child_rule
        assert "margin-block-start: var(--chirpui-space-stack-gap);" in sibling_rule

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

    def test_text_field_appearance_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("budget", label="Budget", appearance="outlined", tone="primary") }}'
        ).render()
        assert "chirpui-field--outlined" in html
        assert "chirpui-field--primary" in html

    def test_text_field_error_state_is_not_shared_error_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email", errors={"email": ["Required"]}, tone="danger") }}'
        ).render()
        assert "chirpui-field--danger" in html
        assert "chirpui-field--error" in html
        assert 'tone="error"' not in html

    def test_masked_field_static(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import masked_field %}'
            '{{ masked_field("ssn", mask="999-99-9999", label="SSN") }}'
        ).render()
        assert "chirpui-field" in html
        assert 'name="ssn"' in html
        assert 'x-mask="999-99-9999"' in html

    def test_masked_field_dynamic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import masked_field %}'
            '{{ masked_field("amt", mask_dynamic="$money($input)", label="Amount") }}'
        ).render()
        assert "chirpui-field" in html
        assert 'x-mask:dynamic="$money($input)"' in html

    def test_phone_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import phone_field %}'
            '{{ phone_field("phone", label="Phone") }}'
        ).render()
        assert "chirpui-field" in html
        assert 'type="tel"' in html
        assert 'x-mask="(999) 999-9999"' in html

    def test_phone_field_uk_format(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import phone_field %}'
            '{{ phone_field("phone", format="uk", label="Phone") }}'
        ).render()
        assert 'x-mask="9999 999 9999"' in html

    def test_money_field(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import money_field %}'
            '{{ money_field("amount", label="Amount") }}'
        ).render()
        assert "chirpui-field" in html
        assert 'inputmode="decimal"' in html
        assert "x-mask:dynamic" in html
        assert "$money($input" in html

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

    def test_form_control_internals_own_attachment_and_pressure(self) -> None:
        css = _chirpui_css()

        for selector in [
            ".chirpui-field--checkbox > :where(:not(script, style, template))",
            ".chirpui-field--radio > :where(:not(script, style, template))",
            ".chirpui-field--range > :where(:not(script, style, template))",
            ".chirpui-field--input-group > :where(:not(script, style, template))",
            ".chirpui-search-bar > :where(:not(script, style, template))",
        ]:
            assert selector in css

        radio_group_rule = css.split(".chirpui-field__radio-group", 1)[1].split("}", 1)[0]
        assert "min-width: 0" in radio_group_rule
        assert "max-width: 100%" in radio_group_rule

        input_group_rule = css.split(".chirpui-input-group {", 1)[1].split("}", 1)[0]
        assert "width: 100%" in input_group_rule
        assert "min-width: 0" in input_group_rule

        input_affix_rule = css.split(".chirpui-input-group__prefix,", 1)[1].split("}", 1)[0]
        assert "max-inline-size: min(40%, 16rem)" in input_affix_rule
        assert "overflow-wrap: anywhere" in input_affix_rule

        search_inner_rule = css.split(".chirpui-search-bar__inner", 1)[1].split("}", 1)[0]
        assert "width: 100%" in search_inner_rule
        assert "min-width: 0" in search_inner_rule

    def test_specialized_form_controls_own_pressure(self) -> None:
        css = _chirpui_css()

        file_rule = css.split(".chirpui-field__file {", 1)[1].split("}", 1)[0]
        assert "box-sizing: border-box" in file_rule
        assert "min-inline-size: 0" in file_rule
        assert "max-inline-size: 100%" in file_rule

        for selector in [
            ".chirpui-star-rating {",
            ".chirpui-thumbs {",
            ".chirpui-number-scale {",
        ]:
            rule = css.split(selector, 1)[1].split("}", 1)[0]
            assert "flex-wrap: wrap" in rule
            assert "max-inline-size: 100%" in rule

        star_label_rule = css.split(".chirpui-star-rating__label {", 1)[1].split("}", 1)[0]
        assert "display: inline-flex" in star_label_rule
        assert "min-inline-size: var(--chirpui-control-block-size-sm)" in star_label_rule

        segmented_label_rule = css.split(".chirpui-segmented > .chirpui-segmented__label {", 1)[
            1
        ].split("}", 1)[0]
        assert "overflow-wrap: anywhere" in segmented_label_rule
        assert "max-inline-size: 100%" in segmented_label_rule
        assert ".chirpui-search-bar--with-button .chirpui-search-bar__inner" in css

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
        assert 'hx-select="unset"' in html
        assert 'hx-disinherit="hx-select"' in html
        assert 'hx-sync="this:replace"' in html

    def test_search_field_with_htmx_select(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_field %}'
            '{{ search_field("q", search_url="/search", search_target="#main", search_hx_select="#page-content") }}'
        ).render()
        assert 'hx-select="#page-content"' in html
        assert 'hx-target="#main"' in html
        assert "hx-disinherit" not in html

    def test_search_field_preserves_explicit_search_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_field %}'
            '{{ search_field("q", search_url="/search", search_target="#results",'
            ' search_attrs_map={"hx-select": "#items", "hx-sync": "#results:queue last"}) }}'
        ).render()
        assert 'hx-select="#items"' in html
        assert 'hx-sync="#results:queue last"' in html
        assert 'hx-select="unset"' not in html
        assert html.count("hx-sync=") == 1

    def test_search_bar_with_htmx_uses_fragment_safe_sync(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_bar %}'
            '{{ search_bar("q", search_url="/search", search_target="#results") }}'
        ).render()
        assert 'hx-select="unset"' in html
        assert 'hx-disinherit="hx-select"' in html
        assert 'hx-sync="this:replace"' in html

    def test_search_bar_resolves_button_icon_name_with_button(self, env: Environment) -> None:
        """with-button variant resolves a button_icon NAME via `| icon` (#136).

        In chirp-ui the `icon` filter resolves a registered name to its glyph
        (the SVG-equivalent at theme runtime, where Bengal's `icon` filter
        emits an <svg>). The literal name must not leak into the markup.
        """
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_bar %}'
            '{{ search_bar("q", variant="with-button", button_icon="search") }}'
        ).render()
        assert "chirpui-btn__icon" in html
        assert "⌕" in html
        # the raw icon name must not appear inside the button icon span
        icon_span = html.split("chirpui-btn__icon")[1].split("</span>")[0]
        assert "search" not in icon_span

    def test_search_bar_resolves_button_icon_name_with_icon(self, env: Environment) -> None:
        """with-icon (solo prefix) variant resolves button_icon NAME via `| icon` (#136)."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_bar %}'
            '{{ search_bar("q", variant="with-icon", button_icon="search") }}'
        ).render()
        assert "chirpui-search-bar__icon" in html
        assert "⌕" in html
        # the raw icon name must not appear inside the icon span
        icon_span = html.split("chirpui-search-bar__icon")[1].split("</span>")[0]
        assert "search" not in icon_span

    def test_search_bar_default_icon_renders_glyph(self, env: Environment) -> None:
        """Default search_bar() still renders the ⌕ glyph (registered name 'search')."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import search_bar %}'
            '{{ search_bar("q", variant="with-icon") }}'
        ).render()
        assert "chirpui-search-bar__icon" in html
        assert "⌕" in html

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

    # -- a11y: aria-describedby, role=alert, error container --

    def test_text_field_aria_describedby(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email") }}'
        ).render()
        assert 'aria-describedby="errors-email"' in html

    def test_text_field_error_container_role_alert(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email", errors={"email": ["Required"]}) }}'
        ).render()
        assert 'role="alert"' in html
        assert 'aria-live="polite"' in html
        assert 'id="errors-email"' in html
        assert "Required" in html

    def test_field_wrapper_has_id(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("username", label="Username") }}'
        ).render()
        assert 'id="field-username"' in html

    def test_field_wrapper_oob(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import field_wrapper %}'
            '{% call field_wrapper("name", oob=true) %}'
            '<input name="name">'
            "{% end %}"
        ).render()
        assert 'hx-swap-oob="true"' in html
        assert 'id="field-name"' in html

    def test_field_wrapper_custom_field_id(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import field_wrapper %}'
            '{% call field_wrapper("name", field_id="edit-field-name") %}'
            '<input name="name">'
            "{% end %}"
        ).render()
        assert 'id="edit-field-name"' in html

    def test_checkbox_field_aria_describedby(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import checkbox_field %}'
            '{{ checkbox_field("agree", label="I agree") }}'
        ).render()
        assert 'aria-describedby="errors-agree"' in html
        assert 'id="field-agree"' in html

    def test_radio_field_error_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import radio_field %}'
            '{% set opts = [{"value": "a", "label": "A"}] %}'
            '{{ radio_field("choice", options=opts, errors={"choice": ["Pick one"]}) }}'
        ).render()
        assert 'id="errors-choice"' in html
        assert 'role="alert"' in html
        assert "Pick one" in html

    def test_form_error_summary_with_errors(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form_error_summary %}'
            '{{ form_error_summary({"email": ["Required"], "name": ["Too short"]}) }}'
        ).render()
        assert "chirpui-form-error-summary" in html
        assert 'role="alert"' in html
        assert 'aria-live="assertive"' in html
        assert "2 errors" in html
        assert 'href="#field-email"' in html
        assert 'href="#field-name"' in html

    def test_form_error_summary_no_errors(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form_error_summary %}'
            "{{ form_error_summary(none) }}"
        ).render()
        # Should render nothing when no errors
        assert "chirpui-form-error-summary__heading" not in html

    def test_form_error_summary_oob(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form_error_summary %}'
            '{{ form_error_summary({"x": ["Bad"]}, oob=true) }}'
        ).render()
        assert 'hx-swap-oob="true"' in html

    def test_empty_error_container_always_present(self, env: Environment) -> None:
        """Error container is always in DOM (for aria-describedby), just empty."""
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("title", label="Title") }}'
        ).render()
        assert 'id="errors-title"' in html
        assert 'role="alert"' in html


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

    def test_action_strip_scroll_css_reserves_hover_lift_room(self) -> None:
        css = _chirpui_css()
        scroll_rule = css.split(".chirpui-action-strip--scroll .chirpui-action-strip__inner", 1)[
            1
        ].split("}", 1)[0]
        assert "padding-block: var(--chirpui-spacing-2xs)" in scroll_rule
        assert "overflow-x: auto" in scroll_rule
        assert (
            "align-items: center"
            in css.split(".chirpui-action-strip__inner", 1)[1].split("}", 1)[0]
        )
        field_rule = css.split(".chirpui-action-strip__inner .chirpui-field", 1)[1].split("}", 1)[0]
        assert "margin-block-end: 0" in field_rule

    def test_command_bar_css_supports_direct_search_and_hint_groups(self) -> None:
        css = _chirpui_css()
        assert ".chirpui-surface:has(> .chirpui-command-bar)" in css
        assert (
            '.chirpui-action-strip__inner\n    > :where([data-chirpui-role~="search"], form, [role="search"])'
            in css
        )
        assert ":where(.chirpui-command-bar, .chirpui-filter-bar)" in css
        assert '[data-chirpui-role~="hints"]' in css
        assert '[data-chirpui-pressure~="compress"]' in css
        assert '[data-chirpui-affinity~="end"]' in css
        assert '.chirpui-action-strip__inner\n    > [data-chirpui-pressure~="flex"]' in css
        assert '.chirpui-action-strip__inner\n    > [data-chirpui-affinity~="end"]' in css
        assert ".chirpui-command-bar [data-chirpui-pressure" not in css
        assert ".chirpui-command-bar [data-chirpui-affinity" not in css
        assert ".chirpui-filter-bar [data-chirpui-pressure" not in css
        assert ".chirpui-filter-bar [data-chirpui-affinity" not in css
        assert "> div[aria-label]" in css
        search_rule = css.split(
            '[data-chirpui-role~="search"], form, [role="search"])',
            1,
        )[1].split("}", 1)[0]
        assert "flex: 1 1 28rem" in search_rule
        assert "flex-wrap: wrap" in search_rule
        assert "min-inline-size: min(100%, 18rem)" in search_rule
        assert '.chirpui-action-strip__inner:has(> [data-chirpui-role~="hints"])' in css
        assert "> label:not(.chirpui-visually-hidden)" in css
        assert '[data-chirpui-role~="hints"][data-chirpui-affinity~="end"]' in css
        assert ".chirpui-action-strip__primary > :where(:not(script, style, template))" in css

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

    def test_filter_bar_accepts_layout_affinity_recipe_markup(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/filter_bar.html" import filter_bar %}'
            '{% call filter_bar("/items", attrs_map={"id": "item_filters"}) %}'
            '<div class="chirpui-action-strip__primary" data-chirpui-role="search" '
            'data-chirpui-pressure="flex" data-chirpui-affinity="fill">'
            '<input name="q" type="search"></div>'
            '<div class="chirpui-action-strip__controls" data-chirpui-role="filters" '
            'data-chirpui-pressure="compress"><select name="role"><option>All</option></select></div>'
            '<div class="chirpui-action-strip__actions" data-chirpui-role="actions" '
            'data-chirpui-pressure="rigid" data-chirpui-affinity="end">'
            '<button type="submit">Export</button></div>'
            "{% end %}"
        ).render()
        assert 'id="item_filters"' in html
        assert "chirpui-filter-bar" in html
        assert 'data-chirpui-role="search"' in html
        assert 'data-chirpui-role="filters"' in html
        assert 'data-chirpui-role="actions"' in html
        assert 'data-chirpui-pressure="rigid"' in html
        assert 'data-chirpui-affinity="end"' in html

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

    def test_command_bar_accepts_link_native_search_recipe_markup(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_bar.html" import command_bar %}'
            "{% call command_bar(wrap='wrap') %}"
            '<form action="/catalog" method="get" role="search" '
            'data-chirpui-role="search" data-chirpui-pressure="flex" '
            'data-chirpui-affinity="fill">'
            '<label for="q">Search</label><input id="q" name="q" type="search">'
            '<button type="submit">Search</button></form>'
            '<div aria-label="Suggested searches" data-chirpui-role="hints" '
            'data-chirpui-pressure="compress" data-chirpui-affinity="end">'
            '<a href="/catalog?q=api">API</a></div>'
            "{% end %}"
        ).render()
        assert 'action="/catalog" method="get" role="search"' in html
        assert 'data-chirpui-role="search"' in html
        assert 'data-chirpui-pressure="compress"' in html
        assert 'aria-label="Suggested searches"' in html
        assert "chirpui-action-strip--wrap" in html

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

    def test_search_header_css_owns_composite_rhythm_and_pressure(self) -> None:
        css = _chirpui_css()

        search_rule = css.split(".chirpui-search-header {", 1)[1].split("}", 1)[0]
        assert "width: 100%" in search_rule
        assert "min-width: 0" in search_rule
        assert ".chirpui-search-header > :where(:not(script, style, template))" in css
        assert ".chirpui-search-header > .chirpui-page-header" in css

        primary_rule = css.split(".chirpui-search-header__strip .chirpui-action-strip__primary", 1)[
            1
        ].split("}", 1)[0]
        assert "flex: 999 1 24rem" in primary_rule
        assert "min-inline-size: min(100%, 18rem)" in primary_rule
        assert ".chirpui-search-header__strip .chirpui-action-strip__controls:empty" in css
        assert ".chirpui-search-header__strip .chirpui-search-bar__inner" in css

    def test_resource_index_grid_results(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/resource_index.html" import resource_index %}'
            '{% from "chirpui/card.html" import resource_card %}'
            "{% call resource_index("
            '"Skills", "/skills", query="doc", subtitle="Browse skills", '
            'filter_action="/skills", filter_label="Tag filters", selected_count=2, '
            'results_layout="grid", results_cols=2'
            ") %}"
            "{% slot toolbar_controls %}<button>Filters</button>{% end %}"
            '{% slot filter_actions %}<button type="submit">Clear</button>{% end %}'
            "{% slot selection %}<a>python x</a>{% end %}"
            '{{ resource_card("/skills/a", "Skill A", description="Docs") }}'
            "{% end %}"
        ).render()
        assert "chirpui-resource-index" in html
        assert "chirpui-search-header" in html
        assert "chirpui-filter-bar" in html
        assert "chirpui-selection-bar" in html
        assert "chirpui-grid--cols-2" in html
        assert "Skill A" in html
        selection_segment = html.split("chirpui-selection-bar", 1)[1].split(
            "chirpui-resource-index__results", 1
        )[0]
        assert "Skill A" not in selection_segment

    def test_resource_index_css_owns_results_rhythm_and_feedback(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/resource_index.html" import resource_index %}'
            "{% call resource_index("
            '"Skills", "/skills", results_layout="grid", mutation_result_id="update-result"'
            ") %}"
            "<article>Skill A</article>"
            "{% end %}"
        ).render()
        css = _chirpui_css()

        assert "chirpui-resource-index__results" in html
        assert "chirpui-mb-sm" not in html
        assert ".chirpui-resource-index > :where(:not(script, style, template))" in css
        assert ".chirpui-resource-index__results > :where(:not(script, style, template))" in css
        assert ".chirpui-resource-index__results > .chirpui-fragment-island" in css
        assert ".chirpui-resource-index__results.chirpui-grid > .chirpui-fragment-island" in css

    def test_resource_index_empty_state(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/resource_index.html" import resource_index %}'
            "{% call resource_index("
            '"Skills", "/skills", has_results=false, empty_title="No skills", empty_hint="python", '
            'empty_message="Try a different filter."'
            ") %}"
            "{% end %}"
        ).render()
        assert "No skills" in html
        assert "Try a different filter." in html
        assert "chirpui-empty-state" in html

    def test_resource_index_mutation_result_id_renders_div(self, env: Environment) -> None:
        """mutation_result_id renders co-located result div at start of results block."""
        html = env.from_string(
            '{% from "chirpui/resource_index.html" import resource_index %}'
            "{% call resource_index("
            '"Skills", "/skills", mutation_result_id="update-result"'
            ") %}"
            "<article>Skill A</article>"
            "{% end %}"
        ).render()
        assert 'id="update-result"' in html
        assert 'aria-live="polite"' in html
        assert "Skill A" in html
        # Div must appear before caller content (co-located in results block)
        idx_result = html.find('id="update-result"')
        idx_content = html.find("Skill A")
        assert idx_result < idx_content

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

    def test_navbar_brand_and_link_use_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/", "/docs"})),
        )
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link %}'
            '{% call navbar(brand="App", brand_url="/") %}'
            '{{ navbar_link("/docs", "Docs") }}'
            "{% end %}"
        ).render()
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2

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

    def test_navbar_aria_label_labels_landmark(self, env: Environment) -> None:
        """aria_label gives the <nav> a static accessible name (#164)."""
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar %}'
            '{% call navbar(brand="App", aria_label="Primary") %}X{% end %}'
        ).render()
        assert 'aria-label="Primary"' in html

    def test_navbar_omits_aria_label_by_default(self, env: Environment) -> None:
        """Back-compat: no aria_label means no aria-label attribute on <nav>."""
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar %}{% call navbar(brand="App") %}X{% end %}'
        ).render()
        nav_open = html[html.index("<nav") : html.index(">", html.index("<nav")) + 1]
        assert "aria-label" not in nav_open


class TestShellFrame:
    def test_shell_outlet_renders_boost_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shell_frame.html" import shell_outlet %}'
            "{% call shell_outlet() %}Main{% end %}"
        ).render()
        assert 'id="page-content"' in html
        assert 'hx-boost="true"' in html
        assert 'hx-target="#main"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'hx-select="#page-content"' in html
        assert "Main" in html

    def test_shell_outlet_can_skip_boost_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shell_frame.html" import shell_outlet %}'
            '{% call shell_outlet(include_boost_attrs=false, cls="custom-shell-outlet") %}Main{% end %}'
        ).render()
        assert 'id="page-content"' in html
        assert 'class="custom-shell-outlet"' in html
        assert 'hx-target="#main"' not in html
        assert 'hx-select="#page-content"' not in html


class TestAppShell:
    def test_shell_actions_renderer(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shell_actions.html" import shell_actions_bar %}'
            "{{ shell_actions_bar(shell_actions) }}"
        ).render(
            shell_actions=ShellActionsStub(
                primary=ShellActionZoneStub(
                    items=(ShellActionStub(id="new", label="New", href="/new", variant="primary"),)
                ),
                overflow=ShellActionZoneStub(
                    items=(ShellActionStub(id="archive", label="Archive", action="archive"),)
                ),
            )
        )
        assert "chirpui-shell-actions" in html
        assert 'href="/new"' in html
        assert "chirpui-dropdown" in html

    def test_shell_actions_default_id_unchanged(self, env: Environment) -> None:
        """Default id_suffix="" keeps both fixed ids byte-identical (#224)."""
        html = env.from_string(
            '{% from "chirpui/shell_actions.html" import shell_actions_bar %}'
            "{{ shell_actions_bar(shell_actions) }}"
        ).render(
            shell_actions=ShellActionsStub(
                primary=ShellActionZoneStub(
                    items=(
                        ShellActionStub(
                            id="bulk",
                            label="Bulk",
                            kind="menu",
                            menu_items=(ShellMenuItemStub(label="Delete", href="/del"),),
                        ),
                    )
                ),
                overflow=ShellActionZoneStub(
                    items=(ShellActionStub(id="archive", label="Archive", action="archive"),)
                ),
            )
        )
        assert 'id="chirp-shell-actions-overflow"' in html
        assert 'id="chirpui-shell-action-bulk"' in html

    def test_shell_actions_id_suffix_namespaces_both(self, env: Environment) -> None:
        """id_suffix namespaces BOTH the overflow id and per-action menu ids (#224)."""
        html = env.from_string(
            '{% from "chirpui/shell_actions.html" import shell_actions_bar %}'
            '{{ shell_actions_bar(shell_actions, id_suffix="-drawer") }}'
        ).render(
            shell_actions=ShellActionsStub(
                primary=ShellActionZoneStub(
                    items=(
                        ShellActionStub(
                            id="bulk",
                            label="Bulk",
                            kind="menu",
                            menu_items=(ShellMenuItemStub(label="Delete", href="/del"),),
                        ),
                    )
                ),
                overflow=ShellActionZoneStub(
                    items=(ShellActionStub(id="archive", label="Archive", action="archive"),)
                ),
            )
        )
        assert 'id="chirp-shell-actions-overflow-drawer"' in html
        assert 'id="chirpui-shell-action-bulk-drawer"' in html
        # The un-suffixed canonical ids must NOT appear in the suffixed instance.
        assert 'id="chirp-shell-actions-overflow"' not in html
        assert 'id="chirpui-shell-action-bulk"' not in html

    def test_shell_action_id_suffix_threaded(self, env: Environment) -> None:
        """The suffix reaches shell_action directly, independent of the bar (#224)."""
        html = env.from_string(
            '{% from "chirpui/shell_actions.html" import shell_action %}'
            '{{ shell_action(action, id_suffix="-x") }}'
        ).render(
            action=ShellActionStub(
                id="go",
                label="Go",
                kind="menu",
                menu_items=(ShellMenuItemStub(label="Run", href="/run"),),
            )
        )
        assert 'id="chirpui-shell-action-go-x"' in html

    def test_shell_actions_renders_form_kind(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shell_actions.html" import shell_actions_bar %}'
            "{{ shell_actions_bar(shell_actions) }}"
        ).render(
            shell_actions=ShellActionsStub(
                primary=ShellActionZoneStub(
                    items=(
                        ShellActionStub(
                            id="save",
                            label="Save",
                            kind="form",
                            variant="primary",
                            form_action="/items",
                            hidden_fields=(("id", "1"),),
                            hx_post="/items",
                            hx_target="#toast",
                            submit_surface="shimmer",
                        ),
                    ),
                ),
            )
        )
        assert "chirpui-shell-action-form" in html
        assert 'action="/items"' in html
        assert 'hx-post="/items"' in html
        assert 'hx-target="#toast"' in html
        assert 'hx-sync="this:drop"' in html
        assert 'hx-disabled-elt="find button, find input[type=submit]"' in html
        assert 'name="id"' in html
        assert 'value="1"' in html
        assert "chirpui-shimmer-btn" in html
        assert "_csrf_token" in html

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
        assert 'hx-target="#main"' in html
        assert 'hx-select="#page-content"' in html
        assert "Main" in html

    def test_app_shell_brand_boost_can_be_disabled(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            "{% call app_shell(brand='Brand', brand_boost=false) %}"
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__brand" in html
        assert 'hx-target="#main"' not in html
        assert 'hx-select="#page-content"' not in html

    def test_app_shell_brand_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/"}))
        )
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            "{% call app_shell(brand='Brand') %}"
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__brand" in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-target="#main"' not in html

    def test_app_shell_renders_shell_actions_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            "{% call app_shell(brand='Brand', shell_actions=shell_actions) %}"
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render(
            shell_actions=ShellActionsStub(
                primary=ShellActionZoneStub(
                    items=(ShellActionStub(id="compose", label="Compose", href="/compose"),)
                ),
                controls=ShellActionZoneStub(
                    items=(ShellActionStub(id="filter", label="Filter", action="filter"),)
                ),
                overflow=ShellActionZoneStub(
                    items=(
                        ShellActionStub(
                            id="more",
                            label="More",
                            kind="menu",
                            menu_items=(ShellMenuItemStub(label="Archive", action="archive"),),
                        ),
                    )
                ),
            )
        )
        assert 'id="chirp-shell-actions"' in html
        assert "Compose" in html
        assert "Filter" in html

    def test_app_shell_sidebar_collapsible_renders_toggle_handle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            "{% call app_shell(brand='Brand', sidebar_collapsible=true) %}"
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "data-chirpui-sidebar-toggle" in html
        assert "chirpui-app-shell__sidebar-resize" in html
        assert 'x-data="chirpuiSidebar({ collapsible: true, resizable: true })"' in html

    def test_app_shell_without_toggle_handle_when_not_collapsible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            "{% call app_shell(brand='Brand', sidebar_collapsible=false) %}"
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "data-chirpui-sidebar-toggle" not in html
        assert "chirpui-app-shell__sidebar-resize" not in html

    def test_app_shell_topbar_glass(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", topbar_variant="glass") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__topbar--glass" in html

    def test_app_shell_topbar_gradient(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", topbar_variant="gradient") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__topbar--gradient" in html

    def test_app_shell_sidebar_glass(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", sidebar_variant="glass") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__sidebar--glass" in html

    def test_app_shell_sidebar_muted(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", sidebar_variant="muted") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__sidebar--muted" in html

    def test_app_shell_default_variants_no_modifier_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__topbar--" not in html
        assert "chirpui-app-shell__sidebar--" not in html

    def test_app_shell_context_rail_renders_region(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", context_rail=true, context_rail_label="Inspector") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% slot context_rail %}<p>Details</p>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell--has-context-rail" in html
        assert 'id="chirpui-context-rail"' in html
        assert 'aria-label="Inspector"' in html
        assert "chirpui-app-shell__context-rail" in html
        assert "<p>Details</p>" in html

    def test_app_shell_no_context_rail_by_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell--has-context-rail" not in html
        assert 'id="chirpui-context-rail"' not in html

    def test_app_shell_context_rail_muted_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", context_rail=true, context_rail_variant="muted") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% slot context_rail %}<p>Details</p>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell__context-rail--muted" in html

    def test_context_rail_oob_targets_outlet(self, env: Environment) -> None:
        """The OOB swap protocol: a route response updates #chirpui-context-rail."""
        html = env.from_string(
            '{% from "chirpui/oob.html" import context_rail_oob %}'
            "{% call context_rail_oob() %}<h2>Run details</h2>{% end %}"
        ).render()
        assert 'id="chirpui-context-rail"' in html
        assert 'hx-swap-oob="innerHTML"' in html
        assert "<aside" in html
        assert "<h2>Run details</h2>" in html

    def test_shell_runtime_script_resets_both_shell_regions(self, env: Environment) -> None:
        """The route-scoped stale-clear lives in the shared runtime (emitted by both
        shell entry points) and covers shell-actions AND the context rail."""
        html = env.from_string(
            '{% from "chirpui/shell_frame.html" import shell_runtime_script %}'
            "{{ shell_runtime_script() }}"
        ).render()
        assert "htmx:beforeSwap" in html
        assert "chirp-shell-actions" in html
        assert "chirpui-context-rail" in html

    def test_app_shell_nav_drawer_renders_affordances(self, env: Environment) -> None:
        """nav_drawer=true wires the hamburger, the off-canvas sidebar region,
        the drawer head/close, and the shared scrim (#196)."""
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", nav_drawer=true) %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert "chirpui-app-shell--nav-drawer" in html
        # Hamburger toggle, wired to the sidebar region.
        assert 'data-chirpui-shell-drawer-toggle="sidebar"' in html
        assert 'aria-controls="chirpui-app-shell-sidebar"' in html
        assert 'aria-expanded="false"' in html
        assert "chirpui-app-shell__nav-toggle-bars" in html
        # The hamburger now lives inside the always-present leading zone (#220),
        # which itself sits before the brand anchor.
        start_idx = html.index('class="chirpui-app-shell__topbar-start"')
        toggle_idx = html.index('class="chirpui-app-shell__nav-toggle"')
        brand_idx = html.index('class="chirpui-app-shell__brand"')
        assert start_idx < toggle_idx < brand_idx
        # The sidebar aside is the off-canvas region with a stable id, named via
        # aria-labelledby so it has an accessible name once promoted to dialog.
        assert 'id="chirpui-app-shell-sidebar"' in html
        assert 'data-chirpui-shell-drawer="sidebar"' in html
        assert 'aria-labelledby="chirpui-app-shell-drawer-title"' in html
        assert 'id="chirpui-app-shell-drawer-title"' in html
        # Drawer chrome + scrim.
        assert "chirpui-app-shell__drawer-head" in html
        assert "data-chirpui-shell-drawer-close" in html
        assert "data-chirpui-shell-scrim" in html
        assert 'aria-label="Open Navigation"' in html
        assert 'aria-label="Close Navigation"' in html

    def test_app_shell_no_nav_drawer_by_default(self, env: Environment) -> None:
        """Opt-in and additive: a shell that does not request nav_drawer renders
        none of the drawer *markup* (no behavior change). Asserts on markup-only
        strings — the vanilla controller in shell_runtime_script() always ships
        and legitimately references the drawer data-attributes / modifier class,
        so those substrings are present regardless. Note: the
        .chirpui-app-shell__topbar-start leading zone is now ALWAYS rendered
        (#220) — non-meaningful chrome, not part of the drawer markup — so the
        absent-class assertions below (nav-toggle, scrim, drawer-head) still
        hold."""
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        # Root carries no nav-drawer modifier.
        assert '<div class="chirpui-app-shell">' in html
        # None of the drawer markup is rendered (these classes are never
        # referenced by the controller JS, so absence is meaningful).
        assert 'class="chirpui-app-shell__nav-toggle"' not in html
        assert "chirpui-app-shell__nav-toggle-bars" not in html
        assert 'class="chirpui-app-shell__rail-toggle"' not in html
        assert "chirpui-app-shell__drawer-head" not in html
        assert 'class="chirpui-app-shell__scrim"' not in html

    def test_app_shell_nav_drawer_rail_toggle_and_no_rail_head(self, env: Environment) -> None:
        """With context_rail the rail gets a topbar trigger + drawer data hook,
        but NO injected head — the rail is innerHTML-swapped by OOB fragments so
        any static head would be stranded on the first boosted nav."""
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", nav_drawer=true, context_rail=true, context_rail_label="Inspector") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% slot context_rail %}<p>Details</p>{% end %}"
            "{% end %}"
        ).render()
        assert 'data-chirpui-shell-drawer-toggle="rail"' in html
        assert 'aria-controls="chirpui-context-rail"' in html
        assert 'aria-label="Open Inspector"' in html
        # The rail aside is a drawer region...
        assert 'data-chirpui-shell-drawer="rail"' in html
        # ...but the only injected drawer head is the sidebar's.
        assert html.count("chirpui-app-shell__drawer-head") == 1

    def test_app_shell_nav_drawer_label_customizes_aria(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand", nav_drawer=true, nav_drawer_label="Menu") %}'
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert 'aria-label="Open Menu"' in html
        assert 'aria-label="Close Menu"' in html
        assert ">Menu</span>" in html

    def test_shell_runtime_script_wires_mobile_drawers(self, env: Environment) -> None:
        """The vanilla drawer controller ships in the shared runtime (no Alpine)."""
        html = env.from_string(
            '{% from "chirpui/shell_frame.html" import shell_runtime_script %}'
            "{{ shell_runtime_script() }}"
        ).render()
        assert "setupShellDrawers" in html
        assert "data-chirpui-shell-drawer-toggle" in html
        assert "matchMedia" in html
        assert "aria-modal" in html
        assert 'e.key === "Escape"' in html

    def test_app_shell_layout_has_no_duplicate_region_clear(self) -> None:
        """Regression: the region stale-clear is not duplicated in the layout's
        inline script (it moved into shell_runtime_script). Guards the divergence
        between the macro and layout entry points from returning."""
        layout = Path("src/chirp_ui/templates/chirpui/app_shell_layout.html").read_text()
        assert "responseUpdatesShellActionsOob" not in layout

    def test_app_shell_layout_inline_syncnav_deleted(self) -> None:
        """#197: the divergent blind-prefix syncNav is GONE from the layout's
        inline script (it moved into the canonical shell_runtime_script). The
        layout-specific CSRF handler stays. Scope the read to the layout file so
        we don't falsely match the canonical copy now in shell_frame.html."""
        layout = Path("src/chirp_ui/templates/chirpui/app_shell_layout.html").read_text()
        assert "function syncNav" not in layout
        # The layout-only CSRF handler (depends on the layout's csrf-token meta)
        # must remain.
        assert "htmx:configRequest" in layout

    def test_shell_runtime_script_ships_canonical_syncnav(self, env: Environment) -> None:
        """#197: the canonical active-link sync ships in shell_runtime_script(),
        the script both entry points emit. It mirrors the server's per-item match
        via the data-chirpui-shell-match selector and toggles the right active
        class per link family."""
        html = env.from_string(
            '{% from "chirpui/shell_frame.html" import shell_runtime_script %}'
            "{{ shell_runtime_script() }}"
        ).render()
        assert "data-chirpui-shell-match" in html
        assert "chirpui-sidebar__link--active" in html
        assert "chirpui-navbar__link--active" in html
        assert "htmx:afterSettle" in html

    def test_app_shell_macro_region_announcer_wrappers(self, env: Environment) -> None:
        """#197: the macro wraps topbar-center in #chirpui-topbar-breadcrumbs and
        the sidebar slot in #chirpui-sidebar-nav, both aria-live announcers. This
        is the canonical region contract the layout must mirror (the layout side
        is not env-renderable — it extends chirp/layouts/shell.html — so layout
        parity is proven only by the browser gauntlet)."""
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand") %}'
            "{% slot topbar %}<nav>Crumbs</nav>{% end %}"
            "{% slot sidebar %}<nav>Side</nav>{% end %}"
            "Main"
            "{% end %}"
        ).render()
        assert 'id="chirpui-topbar-breadcrumbs"' in html
        assert 'id="chirpui-sidebar-nav"' in html
        # Both carry the aria-live announcer attributes (drive the
        # chirpui-transitions.css VT/outline-flash suppression rule).
        bc = html.index('id="chirpui-topbar-breadcrumbs"')
        sn = html.index('id="chirpui-sidebar-nav"')
        assert 'aria-live="polite"' in html[bc : bc + 120]
        assert 'aria-atomic="true"' in html[bc : bc + 120]
        assert 'aria-live="polite"' in html[sn : sn + 120]

    def test_sidebar_link_emits_match_data_attr(self, env: Environment) -> None:
        """#197: sidebar_link emits data-chirpui-shell-match ONLY when match= is
        set; explicit active= links stay server-authoritative (no data-attr)."""
        # With match: data-attr present.
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar_link %}'
            '{{ sidebar_link("/dashboard", "Dashboard", match="prefix") }}'
        ).render(current_path="/dashboard")
        assert 'data-chirpui-shell-match="prefix"' in html
        # No match: no data-attr.
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar_link %}{{ sidebar_link("/x", "X") }}'
        ).render()
        assert "data-chirpui-shell-match" not in html
        # Explicit active, no match: active class + aria-current but NO data-attr
        # (server is authoritative; JS leaves it alone).
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar_link %}'
            '{{ sidebar_link("/x", "X", active=true) }}'
        ).render()
        assert "chirpui-sidebar__link--active" in html
        assert 'aria-current="page"' in html
        assert "data-chirpui-shell-match" not in html

    def test_navbar_link_emits_match_data_attr(self, env: Environment) -> None:
        """#197: navbar_link mirrors the sidebar_link match data-attr contract;
        navbar_dropdown's <summary> (hrefless) must NOT carry the attr."""
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar_link %}'
            '{{ navbar_link("/dashboard", "Dashboard", match="prefix") }}'
        ).render(current_path="/dashboard")
        assert 'data-chirpui-shell-match="prefix"' in html
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar_link %}{{ navbar_link("/x", "X") }}'
        ).render()
        assert "data-chirpui-shell-match" not in html
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar_link %}'
            '{{ navbar_link("/x", "X", active=true) }}'
        ).render()
        assert "chirpui-navbar__link--active" in html
        assert 'aria-current="page"' in html
        assert "data-chirpui-shell-match" not in html
        # navbar_dropdown summary has no href — it must never carry the attr
        # (the JS skips hrefless elements; a dropdown trigger is not a link).
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar_dropdown %}'
            '{% call navbar_dropdown("Menu", match="prefix") %}items{% end %}'
        ).render(current_path="/menu")
        assert "data-chirpui-shell-match" not in html

    def test_app_shell_topbar_leading_slot_renders_before_brand(self, env: Environment) -> None:
        """#220: topbar_leading content renders in the leading zone, BEFORE the
        brand <a>, and is NOT nested inside the brand anchor — the core
        anti-footgun assertion (a <button> inside an <a> is invalid HTML and the
        anchor would hijack the click)."""
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand") %}'
            '{% slot topbar_leading %}<button id="lead">x</button>{% end %}'
            "Main"
            "{% end %}"
        ).render()
        assert '<button id="lead">x</button>' in html
        lead_open = html.index('<button id="lead">')
        lead_close = html.index("</button>", lead_open)
        brand_open = html.index('class="chirpui-app-shell__brand"')
        # Leading button comes before the brand, and CLOSES before the brand
        # anchor opens (so it is a sibling, not a descendant of the <a>).
        assert lead_open < brand_open
        assert lead_close < brand_open

    def test_app_shell_topbar_start_wrapper_always_rendered(self, env: Environment) -> None:
        """#220: the leading zone wrapper is always present (stable layout
        contract) even with no nav_drawer and no topbar_leading content."""
        html = env.from_string(
            '{% from "chirpui/app_shell.html" import app_shell %}'
            '{% call app_shell(brand="Brand") %}Main{% end %}'
        ).render()
        assert 'class="chirpui-app-shell__topbar-start"' in html

    def test_topbar_leading_doc_snippet_icon_resolves_to_glyph(
        self, env: Environment, recwarn: pytest.WarningsRecorder
    ) -> None:
        """#220: the copyable topbar_leading affordance snippet (docstrings +
        docs/patterns/navigation.md) uses a REAL icon-registry name so the
        rendered control is a hamburger glyph, not literal pass-through text.
        Guards against regressing to a non-registry name (e.g. "menu"), which
        renders the raw string and emits a ChirpUIValidationWarning."""
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("list", aria_label="Open menu") }}'
        ).render()
        # "list" resolves to the hamburger glyph; the raw name never leaks.
        assert "≡" in html
        assert ">list<" not in html
        assert 'aria-label="Open menu"' in html
        assert not [w for w in recwarn if issubclass(w.category, ChirpUIValidationWarning)]


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

    def test_logo_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/"}))
        )
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(text="Home", image_src="/static/logo.svg", href="/", variant="both") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_logo_external_link_stays_plain(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"https://example.com"})),
        )
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(text="Home", image_src="/static/logo.svg", href="https://example.com", variant="both") }}'
        ).render()
        assert 'href="https://example.com"' in html
        assert "hx-target=" not in html

    def test_logo_image_variant_uses_hidden_text_when_alt_missing(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo.html" import logo %}'
            '{{ logo(text="Accessible brand", image_src="/static/logo.svg", variant="image") }}'
        ).render()
        assert "chirpui-logo--image" in html
        assert 'alt=""' in html
        assert "chirpui-visually-hidden" in html
        assert "Accessible brand" in html

    def test_logo_cloud_items(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo_cloud.html" import logo_cloud %}{{ logo_cloud(items=items) }}'
        ).render(
            items=[
                {"name": "Acme", "src": "/static/acme.svg", "href": "/customers/acme"},
                {"name": "Globex"},
            ]
        )

        assert "chirpui-logo-cloud" in html
        assert "chirpui-logo-cloud--monochrome" in html
        assert "chirpui-logo-cloud__track" in html
        assert "chirpui-logo-cloud__link" in html
        assert 'src="/static/acme.svg"' in html
        assert 'alt="Acme"' in html
        assert "Globex" in html

    def test_logo_cloud_slot_mode(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/logo_cloud.html" import logo_cloud %}'
            '{% call logo_cloud(label="Partners", monochrome=false) %}'
            '<span class="custom-logo">Partner</span>'
            "{% end %}"
        ).render()

        assert 'aria-label="Partners"' in html
        assert "chirpui-logo-cloud--monochrome" not in html
        assert '<span class="custom-logo">Partner</span>' in html


class TestStoryCard:
    def test_story_card_link_with_metric(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/story_card.html" import story_card %}'
            '{{ story_card(customer="Acme", outcome="Reduced review time", '
            'summary="Teams debugged production runs.", href="/stories/acme", metric="80%") }}'
        ).render()

        assert '<a href="/stories/acme"' in html
        assert "chirpui-story-card" in html
        assert "chirpui-story-card--link" in html
        assert "chirpui-story-card__metric" in html
        assert "80%" in html
        assert "Reduced review time" in html
        assert "Read story" in html

    def test_story_card_slots_and_logo(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/story_card.html" import story_card %}'
            '{% call story_card(customer="Globex", outcome="Improved quality", '
            'logo_src="/static/globex.svg", logo_alt="Globex mark") %}'
            "Custom summary"
            "{% slot footer %}<span>Case study</span>{% end %}"
            "{% end %}"
        ).render()

        assert "<article" in html
        assert "chirpui-story-card--link" not in html
        assert 'src="/static/globex.svg"' in html
        assert 'alt="Globex mark"' in html
        assert "Custom summary" in html
        assert "Case study" in html

    def test_story_card_collapses_empty_logo_and_footer(self, env: Environment) -> None:
        # A logo-less, link-less card must emit truly-empty header/footer
        # wrappers so the `:empty { display: none }` rule can collapse them.
        # Otherwise the empty logo holds the header's space-between open and
        # shoves a lone metric to the far edge (the reported "random" float).
        html = env.from_string(
            '{% from "chirpui/story_card.html" import story_card %}'
            '{{ story_card(customer="Python teams", '
            'outcome="Pages and screens share one library.", '
            'summary="Use Chirp UI for cards and forms.", metric="one library") }}'
        ).render()

        assert '<div class="chirpui-story-card__logo"></div>' in html
        assert '<footer class="chirpui-story-card__footer"></footer>' in html
        assert "chirpui-story-card__metric" in html
        assert "Read story" not in html


class TestCtaBand:
    def test_cta_band_with_standard_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/cta_band.html" import cta_band %}'
            '{{ cta_band(title="Start building", body="Ship production agents.", '
            'primary_label="Start", primary_href="/start", '
            'secondary_label="Demo", secondary_href="/demo") }}'
        ).render()

        assert "chirpui-band" in html
        assert "chirpui-cta-band" in html
        assert "chirpui-cta-band__inner" in html
        assert "Start building" in html
        assert "Ship production agents." in html
        assert 'href="/start"' in html
        assert 'href="/demo"' in html

    def test_cta_band_slots_and_forwarded_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/cta_band.html" import cta_band %}'
            '{% call cta_band(title="Launch", variant="elevated", width="contained") %}'
            "<p>Custom body</p>"
            '{% slot actions %}<a href="/custom">Custom action</a>{% end %}'
            "{% end %}"
        ).render()

        assert "chirpui-band--elevated" in html
        assert "chirpui-band--contained" in html
        assert "<p>Custom body</p>" in html
        assert "Custom action" in html


class TestOfficialPatternAssets:
    def test_lifecycle_showcase_renders_tabs_and_feature_panel(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/marketing_patterns.html" import lifecycle_showcase %}'
            "{{ lifecycle_showcase(items) }}"
        ).render(
            items=[
                {
                    "id": "build",
                    "label": "Build",
                    "title": "Build with control",
                    "body": "Plan the workflow.",
                    "media": "Workflow artifact",
                },
                {
                    "id": "ship",
                    "label": "Ship",
                    "title": "Ship with checks",
                    "body": "Watch the rollout.",
                    "media": "Release artifact",
                },
            ]
        )

        assert "chirpui-lifecycle-showcase" in html
        assert "Build with control" in html
        assert "Workflow artifact" in html
        assert "chirpui-tabs" in html

    def test_media_pattern_assets_render(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/media_patterns.html" import catalog_rail, live_event_card, watch_companion_layout %}'
            '{{ catalog_rail("Trending", items, artwork="/thumb.svg") }}'
            '{{ live_event_card("Final", "Live", "Tonight 8 PM", href="/live", state_variant="error") }}'
            "{% call watch_companion_layout() %}"
            "{% slot player %}<div>Player</div>{% end %}"
            "{% slot companion %}<div>Transcript</div>{% end %}"
            "{% end %}"
        ).render(
            items=[
                {
                    "href": "/watch/1",
                    "title": "North Pier",
                    "duration": "42:00",
                    "meta": "Series",
                    "state": "New",
                }
            ]
        )

        assert "chirpui-catalog-rail" in html
        assert "chirpui-title-card" in html
        assert "North Pier" in html
        assert "chirpui-live-event-card" in html
        assert "Tonight 8 PM" in html
        assert "chirpui-watch-companion-layout__player" in html
        assert "Transcript" in html

    def test_forum_pattern_assets_render(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forum_patterns.html" import answer_card, moderation_queue_item, topic_card %}'
            '{{ topic_card("/topics/1", "Long topic", description="Summary", category="Q&A", '
            'state="open", replies=3, views=12, latest_label="Latest reply") }}'
            '{% call answer_card(title="Accepted answer", accepted=true) %}Use consent tags.{% end %}'
            '{{ moderation_queue_item("/mod/1", "Reported post", "Needs review", target="Rule: safety") }}'
        ).render()

        assert "chirpui-topic-card" in html
        assert "Long topic" in html
        assert "Latest reply" in html
        assert "chirpui-answer-card" in html
        assert "accepted" in html
        assert "chirpui-moderation-queue-item" in html
        assert "Reported post" in html

    def test_detail_header_renders_named_slots(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/detail_header.html" import detail_header %}'
            '{% from "chirpui/badge.html" import badge %}'
            '{% call detail_header("Community name", summary="A focused space.", eyebrow="Forum") %}'
            '{% slot media %}<img src="/avatar.svg" alt="">{% end %}'
            '{% slot badges %}{{ badge("public", variant="success") }}{% end %}'
            "{% slot meta %}<span>12k members</span>{% end %}"
            '{% slot actions %}<a href="/join">Join</a>{% end %}'
            "{% slot aside %}<p>Guidelines</p>{% end %}"
            "{% end %}"
        ).render()

        assert "chirpui-detail-header" in html
        assert "chirpui-detail-header__media" in html
        assert "Community name" in html
        assert "A focused space." in html
        assert "12k members" in html
        assert "Guidelines" in html

    def test_facet_chip_renders_selected_count_and_remove(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/facet_chip.html" import facet_chip %}'
            '{{ facet_chip("Accessibility", href="/tags/a11y", count=24, selected=true, '
            'remove_href="/tags", remove_label="Clear accessibility") }}'
        ).render()

        assert "chirpui-facet-chip" in html
        assert "chirpui-facet-chip--selected" in html
        assert "chirpui-facet-chip--removable" in html
        assert 'aria-current="page"' in html
        assert "chirpui-facet-chip__count" in html
        assert "24" in html
        assert "chirpui-facet-chip__remove" in html
        assert 'aria-label="Clear accessibility"' in html

    def test_thread_reader_layout_renders_reader_regions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/thread_reader_layout.html" import thread_reader_layout %}'
            '{% from "chirpui/detail_header.html" import detail_header %}'
            '{% call thread_reader_layout(label="Design thread") %}'
            '{% slot header %}{{ detail_header("Design systems", summary="Thread summary") }}{% end %}'
            '{% slot local_nav %}<a class="chirpui-thread-reader-layout__nav-link" href="#answer">Answer</a>{% end %}'
            "{% slot posts %}<article>First post</article>{% end %}"
            "{% slot attention_nav %}<aside>Needs review</aside>{% end %}"
            "{% slot composer %}<form>Reply</form>{% end %}"
            "{% end %}"
        ).render()

        assert "chirpui-thread-reader-layout" in html
        assert 'aria-label="Design thread"' in html
        assert "chirpui-thread-reader-layout__header" in html
        assert "chirpui-detail-header" in html
        assert "chirpui-thread-reader-layout__nav-link" in html
        assert "First post" in html
        assert "Needs review" in html
        assert "Reply" in html


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
        assert 'hx-select="#page-content"' in html

    def test_sidebar_aria_label_labels_landmark(self, env: Environment) -> None:
        """aria_label gives the <nav> a static accessible name so it does not
        rely on docs-nav.js runtime injection (#164)."""
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar %}'
            '{% call sidebar(aria_label="Documentation sections") %}X{% end %}'
        ).render()
        assert 'aria-label="Documentation sections"' in html

    def test_sidebar_omits_aria_label_by_default(self, env: Environment) -> None:
        """Back-compat: no aria_label means no aria-label attribute on <nav>."""
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar %}{% call sidebar() %}X{% end %}'
        ).render()
        nav_open = html[html.index("<nav") : html.index(">", html.index("<nav")) + 1]
        assert "aria-label" not in nav_open

    def test_sidebar_current_path_marks_matching_link_active(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_link %}'
            '{% call sidebar(current_path="/carousel") %}'
            '{{ sidebar_link("/carousel", "Carousel", match="exact") }}'
            "{{ sidebar_link('/cards', 'Cards', match='exact') }}"
            "{% end %}"
        ).render()
        assert 'href="/carousel"' in html
        assert html.count("chirpui-sidebar__link--active") == 1
        assert 'aria-current="page"' in html

    def test_shell_brand_link_matches_sidebar_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import shell_brand_link %}'
            "{% call shell_brand_link() %}Brand{% end %}"
        ).render()
        assert "chirpui-app-shell__brand" in html
        assert 'hx-target="#main"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'hx-select="#page-content"' in html
        assert "Brand" in html

    def test_shell_brand_link_prefers_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/"}))
        )
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import shell_brand_link %}'
            "{% call shell_brand_link() %}Brand{% end %}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-target="#main"' not in html

    def test_shell_boosted_link_matches_sidebar_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import shell_boosted_link %}'
            '{% call shell_boosted_link(href="/x", cls="chirpui-btn chirpui-btn--sm") %}Go{% end %}'
        ).render()
        assert 'class="chirpui-btn chirpui-btn--sm"' in html
        assert 'hx-target="#main"' in html
        assert 'hx-select="#page-content"' in html

    def test_sidebar_section(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_section %}'
            "{% call sidebar() %}"
            '{{ sidebar_section("Main") }}'
            "{% end %}"
        ).render()
        assert "chirpui-sidebar__section" in html
        assert "Main" in html

    def test_sidebar_section_can_start_collapsed(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar_section %}'
            '{% call sidebar_section("Group", collapsible=true, open=false) %}'
            '<a href="/docs">Docs</a>'
            "{% end %}"
        ).render()

        assert "<details" in html
        assert "open" not in html.split(">", 1)[0]


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

    def test_stepper_completed_indicator_uses_opaque_fill(self) -> None:
        css = _chirpui_css()
        completed_rule = css.split(
            ".chirpui-stepper__item--completed .chirpui-stepper__indicator", 1
        )[1].split("}", 1)[0]
        assert "var(--chirpui-bg-subtle)" in completed_rule
        assert "15%, transparent" not in completed_rule


class TestWizardForm:
    def test_wizard_form_safe_region_caller_scoping(self, env: Environment) -> None:
        """Minimal test: def→call safe_region→caller() must resolve to def's caller."""
        html = env.from_string(
            '{% from "chirpui/fragment_island.html" import safe_region %}'
            "{% def wrapper() %}"
            '{% call safe_region("x") %}'
            "{{ caller() }}"
            "{% end %}"
            "{% end %}"
            "{% call wrapper() %}Content{% end %}"
        ).render()
        assert "Content" in html

    def test_fragment_island_with_result_renders_mutation_div(self, env: Environment) -> None:
        """fragment_island_with_result renders co-located mutation result div at top of island."""
        html = env.from_string(
            '{% from "chirpui/fragment_island.html" import fragment_island_with_result %}'
            '{% call fragment_island_with_result("collections-results", "update-result") %}'
            "<p>Form content</p>"
            "{% end %}"
        ).render()
        assert 'id="collections-results"' in html
        assert 'id="update-result"' in html
        assert 'aria-live="polite"' in html
        assert "Form content" in html
        assert "chirpui-mb-sm" not in html
        # Result div must appear before caller content
        idx_result = html.find('id="update-result"')
        idx_content = html.find("Form content")
        assert idx_result < idx_content

    def test_fragment_island_css_owns_mutation_region_rhythm(self) -> None:
        css = _chirpui_css()

        assert ".chirpui-fragment-island > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-fragment-island > :where(:not(script, style, template)) + :where(:not(script, style, template))"
            in css
        )
        assert ".chirpui-fragment-island > .chirpui-fragment-island:empty" in css

    def test_poll_trigger_renders_hidden_htmx_button(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/fragment_island.html" import poll_trigger %}'
            '{{ poll_trigger("/status", "#collections-results", delay="2s") }}'
        ).render()
        assert 'type="button"' in html
        assert 'hx-get="/status"' in html
        assert 'hx-trigger="load delay:2s"' in html
        assert 'hx-target="#collections-results"' in html
        assert 'class="chirpui-sr-only"' in html
        assert 'aria-hidden="true"' in html

    def test_wizard_form_safe_region_with_stepper(self, env: Environment) -> None:
        """Same as wizard_form: safe_region + stepper + caller()."""
        html = env.from_string(
            '{% from "chirpui/stepper.html" import stepper %}'
            '{% from "chirpui/fragment_island.html" import safe_region %}'
            "{% def wrapper(id, steps, current) %}"
            '{% call safe_region(id, cls="wizard") %}'
            "{{ stepper(steps=steps, current=current) }}"
            '<div class="body">{{ caller() }}</div>'
            "{% end %}"
            "{% end %}"
            '{% set steps = [{"id": "1", "label": "Step 1"}] %}'
            '{% call wrapper("wiz", steps=steps, current=1) %}Form{% end %}'
        ).render()
        assert "Form" in html
        assert "Step 1" in html

    def test_wizard_form_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wizard_form.html" import wizard_form %}'
            '{% set steps = [{"id": "1", "label": "Details"}, {"id": "2", "label": "Review"}] %}'
            '{% call wizard_form("checkout", steps=steps, current=1) %}'
            "<p>Form content</p>"
            "{% end %}"
        ).render()
        assert 'id="checkout"' in html
        assert "chirpui-wizard-form" in html
        assert "chirpui-stepper" in html
        assert "chirpui-wizard-form__body" in html
        assert "hx-disinherit" in html
        assert "Form content" in html

    def test_wizard_form_includes_stepper(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wizard_form.html" import wizard_form %}'
            '{% set steps = [{"id": "1", "label": "Step 1"}] %}'
            '{% call wizard_form("wiz", steps=steps, current=1) %}x{% end %}'
        ).render()
        assert "chirpui-stepper__item--active" in html
        assert "Step 1" in html

    def test_safe_region_error_boundary(self, env: Environment) -> None:
        """Broken caller content in safe_region produces empty region, not crash."""
        html = env.from_string(
            '{% from "chirpui/fragment_island.html" import safe_region %}'
            '{% call safe_region("broken-region") %}{{ undefined_var.bad }}{% end %}'
        ).render()
        assert 'id="broken-region"' in html
        assert "chirpui-fragment-island" in html


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

    def test_description_item_auto_type_bool(self, env: Environment) -> None:
        """Pass Python bool to description_item; badge with Yes/No appears."""
        html = env.from_string(
            '{% from "chirpui/description_list.html" import description_item %}'
            '{{ description_item("Initialized", True) }}'
        ).render()
        assert "chirpui-dl__detail--bool" in html
        assert "Yes" in html

    def test_description_item_auto_type_path(self, env: Environment) -> None:
        """Pass Path to description_item; --path class applied."""
        from pathlib import Path

        html = env.from_string(
            '{% from "chirpui/description_list.html" import description_item %}'
            '{{ description_item("Workspace", workspace_root) }}'
        ).render(workspace_root=Path("/home/project"))
        assert "chirpui-dl__detail--path" in html
        assert "/home/project" in html

    def test_description_list_items_auto_type_bool(self, env: Environment) -> None:
        """Items with bool detail get auto-detected type and badge."""
        html = env.from_string(
            '{% from "chirpui/description_list.html" import description_list %}'
            '{% set items = [{"term": "Ready", "detail": True}] %}'
            "{{ description_list(items=items) }}"
        ).render()
        assert "chirpui-dl__detail--bool" in html
        assert "Yes" in html


class TestSettingsRow:
    def test_settings_row_list_and_row(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/settings_row.html" import settings_row_list, settings_row %}'
            "{% call settings_row_list() %}"
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
            "{% call settings_row_list() %}"
            '{{ settings_row("X", status="ok", detail="dori setup x") }}'
            "{% end %}"
        ).render()
        assert "chirpui-font-mono" in html
        assert "dori setup x" in html

    def test_settings_row_status_variant_override(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/settings_row.html" import settings_row %}'
            '{{ settings_row("Test", status="Custom", status_variant="error") }}'
        ).render()
        assert "chirpui-badge--error" in html
        assert "Custom" in html


class TestConfigRow:
    def test_config_row_list_renders_grid_with_slot_content(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/config_row.html" import config_row_list, config_row_toggle %}'
            "{% call config_row_list() %}"
            '{{ config_row_toggle("acp.enabled", "ACP enabled", checked=true) }}'
            "{% end %}"
        ).render()
        assert "chirpui-config-row-list" in html
        assert "chirpui-config-row" in html
        assert "ACP enabled" in html
        assert "chirpui-toggle" in html

    def test_config_row_toggle_renders_label_and_toggle_with_form_when_attrs_map(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/config_row.html" import config_row_toggle %}'
            '{{ config_row_toggle("x", "Label", checked=false, form_action="/set", '
            'attrs_map={"hx-post": "/set", "hx-target": "#r", "hx-swap": "innerHTML"}) }}'
        ).render()
        assert "chirpui-config-row__label" in html
        assert "Label" in html
        assert "chirpui-config-row__form" in html
        assert 'hx-post="/set"' in html
        assert 'name="key" value="x"' in html

    def test_config_row_select_renders_label_and_select(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/config_row.html" import config_row_select %}'
            '{{ config_row_select("level", "Log level", options=[{"value": "info", "label": "Info"}, '
            '{"value": "debug", "label": "Debug"}], selected="info") }}'
        ).render()
        assert "chirpui-config-row__label" in html
        assert "Log level" in html
        assert "chirpui-config-row__select" in html
        assert "Info" in html
        assert "Debug" in html
        assert 'value="info"' in html

    def test_config_row_editable_renders_display_mode_with_edit_trigger(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/config_row.html" import config_row_editable %}'
            '{{ config_row_editable("endpoint", "https://api.example.com", edit_url="/edit") }}'
        ).render()
        assert "chirpui-config-row__label" in html
        assert "endpoint" in html
        assert "https://api.example.com" in html
        assert "Edit" in html
        assert 'hx-get="/edit"' in html


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

    def test_timeline_items_link_use_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/detail"})),
        )
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            '{% set items = [{"title": "Step 1", "date": "Jan 1", "content": "Done", "href": "/detail"}] %}'
            "{{ timeline(items=items) }}"
        ).render()
        assert "chirpui-timeline__link-overlay" in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_timeline_items_title_link_mode(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            '{% set items = [{"title": "Step 1", "date": "Jan 1", "href": "/detail"}] %}'
            '{{ timeline(items=items, link_mode="title") }}'
        ).render()
        assert "chirpui-timeline__title-link" in html
        assert "chirpui-timeline__link-overlay" not in html
        assert 'href="/detail"' in html

    def test_timeline_density_and_card_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            '{% set items = [{"title": "Step 1", "date": "Jan 1"}] %}'
            '{{ timeline(items=items, density="compact", variant="cards") }}'
        ).render()
        assert "chirpui-timeline--compact" in html
        assert "chirpui-timeline--cards" in html

    def test_timeline_items_title_link_mode_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/detail"})),
        )
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            '{% set items = [{"title": "Step 1", "date": "Jan 1", "href": "/detail"}] %}'
            '{{ timeline(items=items, link_mode="title") }}'
        ).render()
        assert "chirpui-timeline__title-link" in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_timeline_items_hint_wraps_title_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            '{% set items = [{"title": "Step 1", "date": "Jan 1", "href": "/detail", "hint": "Audit detail"}] %}'
            '{{ timeline(items=items, link_mode="title") }}'
        ).render()
        assert "chirpui-timeline__hint" in html
        assert 'data-tooltip="Audit detail"' in html
        assert "chirpui-timeline__title-link" in html
        assert "chirpui-timeline__link-overlay" not in html

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

    def test_inline_edit_display_warns_without_swap_id(self, env: Environment) -> None:
        """Missing swap_id emits a validation warning about ID collision risk."""
        with pytest.warns(ChirpUIValidationWarning, match="no explicit id provided"):
            env.from_string(
                '{% from "chirpui/inline_edit_field.html" import inline_edit_field_display %}'
                '{{ inline_edit_field_display(value="X", edit_url="/e") }}'
            ).render()

    def test_inline_edit_form_warns_without_swap_id(self, env: Environment) -> None:
        """Missing swap_id on form macro also warns."""
        with pytest.warns(ChirpUIValidationWarning, match="no explicit id provided"):
            env.from_string(
                '{% from "chirpui/inline_edit_field.html" import inline_edit_field_form %}'
                '{{ inline_edit_field_form(name="n", value="v", save_url="/s", cancel_url="/c") }}'
            ).render()

    def test_inline_edit_no_warning_with_swap_id(self, env: Environment) -> None:
        """Explicit swap_id suppresses the warning."""
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error", ChirpUIValidationWarning)
            html = env.from_string(
                '{% from "chirpui/inline_edit_field.html" import inline_edit_field_display %}'
                '{{ inline_edit_field_display(value="X", edit_url="/e", swap_id="my-field") }}'
            ).render()
        assert 'id="my-field"' in html

    def test_row_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/row_actions.html" import row_actions %}'
            '{{ row_actions(items=[{"label": "Edit", "href": "/edit"}, {"label": "Delete", "href": "/del", "variant": "danger"}]) }}'
        ).render()
        assert "chirpui-dropdown" in html
        assert "chirpui-dropdown__trigger" in html
        assert "Edit" in html
        assert "Delete" in html

    def test_row_actions_css_uses_compact_trigger_shape(self) -> None:
        css = _chirpui_css()
        assert ".chirpui-row-actions__trigger" in css
        assert "display: inline-flex;" in css
        assert "min-inline-size: var(--chirpui-control-block-size-sm);" in css
        assert "min-block-size: var(--chirpui-control-block-size-sm);" in css

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
        assert 'x-data="chirpuiDialogTarget()"' in html

    def test_confirm_dialog_htmx_params(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_dialog %}'
            '{{ confirm_dialog("d", title="X", message="Y", confirm_url="/del", confirm_method="DELETE",'
            ' hx_target="#main", hx_swap="innerHTML", hx_select="#content", hx_push_url="/list") }}'
        ).render()
        assert 'hx-delete="/del"' in html
        assert 'hx-disinherit="hx-select hx-target hx-swap"' in html
        assert 'hx-target="#main"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'hx-select="#content"' in html
        assert 'hx-push-url="/list"' in html
        assert 'hx-sync="this:drop"' in html
        assert 'hx-disabled-elt="find button, find input[type=submit]"' in html

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

    def test_confirm_dialog_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confirm.html" import confirm_dialog, confirm_trigger %}'
            '{{ confirm_trigger("d", label="Delete") }}'
            '{{ confirm_dialog("d", title="Delete?", message="Sure?", variant="danger",'
            ' confirm_url="/del", confirm_method="DELETE", hx_target="#main", hx_select="#content") }}'
        ).render()
        assert 'class="chirpui-modal-trigger chirpui-confirm-trigger"' in html
        assert 'x-data="chirpuiDialogTarget()"' in html
        assert 'data-dialog-target="d"' in html
        assert '@click="open()"' in html
        assert '<dialog id="d"' in html
        assert "chirpui-confirm chirpui-modal chirpui-modal--small chirpui-confirm--danger" in html
        assert 'closedby="any"' in html
        assert "chirpui-confirm__icon" in html
        assert "chirpui-modal__header" in html
        assert "chirpui-modal__title" in html
        assert "chirpui-modal__close" in html
        assert 'aria-label="Close"' in html
        assert "chirpui-modal__body" in html
        assert "chirpui-confirm__message" in html
        assert "chirpui-confirm__footer" in html
        assert html.count('form method="dialog"') == 2
        assert 'method="DELETE"' in html
        assert 'action="/del"' in html
        assert 'hx-delete="/del"' in html
        assert 'hx-disinherit="hx-select hx-target hx-swap"' in html
        assert 'hx-target="#main"' in html
        assert 'hx-select="#content"' in html
        assert 'class="chirpui-btn chirpui-btn--danger"' in html


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
        assert 'x-data="chirpuiDialogTarget()"' in html

    def test_drawer_anatomy_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/drawer.html" import drawer, drawer_trigger %}'
            '{{ drawer_trigger("filters", label="Open filters", cls="extra-trigger") }}'
            '{% call drawer("filters", title="Filters", side="left", cls="extra-drawer") %}'
            "{% slot header_actions %}<button>Reset</button>{% end %}"
            "Drawer body"
            "{% end %}"
        ).render()
        assert '<dialog id="filters"' in html
        assert 'class="chirpui-drawer chirpui-drawer--left extra-drawer"' in html
        assert 'closedby="any"' in html
        assert 'class="chirpui-drawer-trigger extra-trigger"' in html
        assert 'type="button"' in html
        assert 'x-data="chirpuiDialogTarget()"' in html
        assert 'data-dialog-target="filters"' in html
        assert '@click="open()"' in html
        assert "chirpui-drawer__panel" in html
        assert "chirpui-drawer__header" in html
        assert "chirpui-drawer__title" in html
        assert "chirpui-drawer__header-actions" in html
        assert 'form method="dialog"' in html
        assert "chirpui-drawer__close" in html
        assert 'aria-label="Close"' in html
        assert "chirpui-drawer__body" in html

    def test_drawer_css_owns_body_rhythm_and_pressure(self) -> None:
        css = _chirpui_css()

        assert ".chirpui-drawer__body > :where(:not(script, style, template))" in css
        assert (
            ".chirpui-drawer__body > :where(:not(script, style, template)) + "
            ":where(:not(script, style, template))"
        ) in css
        assert ".chirpui-drawer__header > form" in css
        assert ".chirpui-drawer__title" in css
        assert "overflow-wrap: anywhere" in css


class TestCommandPalette:
    def test_command_palette_trigger(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette_trigger %}'
            '{{ command_palette_trigger("palette", label="Search") }}'
        ).render()
        assert "chirpui-command-palette__trigger" in html
        assert "chirpui-command-palette-trigger" in html
        assert 'x-data="chirpuiDialogTarget()"' in html
        assert 'data-dialog-target="palette"' in html
        assert 'aria-label="Search"' in html

    def test_command_palette_trigger_dense_chrome_options(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette_trigger %}'
            '{{ command_palette_trigger("palette", label="Search project", placeholder="Search or jump", shortcut="/", icon="search", density="sm") }}'
        ).render()
        assert "chirpui-command-palette-trigger--sm" in html
        assert "chirpui-command-palette__trigger-icon" in html
        assert "chirpui-command-palette__trigger-label" in html
        assert "Search or jump" in html
        assert "<kbd" in html
        assert ">/" in html
        assert 'aria-label="Search project"' in html

    def test_command_palette_combobox_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette %}'
            '{% call command_palette(id="cp", search_url="/s") %}{% end %}'
        ).render()
        # The dialog wraps the arrow-nav factory; the input is a combobox over the
        # results listbox, defended against boost-inherited hx-select.
        assert 'x-data="chirpuiCommandPalette()"' in html
        assert 'role="combobox"' in html
        assert 'aria-controls="cp-results"' in html
        assert ':aria-activedescendant="activeId"' in html
        assert 'hx-select="unset"' in html
        assert 'role="listbox"' in html

    def test_command_palette_item_is_roving_option(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette_item %}'
            '{{ command_palette_item("opt-1", "New file", href="/new", hint="N") }}'
        ).render()
        assert 'id="opt-1"' in html
        assert 'role="option"' in html
        assert 'aria-selected="false"' in html
        assert 'href="/new"' in html
        assert "chirpui-command-palette__item-label" in html
        assert "chirpui-command-palette__item-hint" in html

    def test_command_palette_item_button_with_action(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/command_palette.html" import command_palette_item %}'
            '{{ command_palette_item("opt-2", "Run", action="run") }}'
        ).render()
        assert "<button" in html
        assert 'role="option"' in html
        assert 'data-action="run"' in html


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

    def test_split_button_primary_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/save"}))
        )
        html = env.from_string(
            '{% from "chirpui/split_button.html" import split_button %}'
            '{% call split_button("Save", primary_href="/save") %}'
            '<a href="/export">Export</a>'
            "{% end %}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_split_button_submit(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_button.html" import split_button %}'
            '{% call split_button("Submit", primary_submit=true) %}'
            "{% end %}"
        ).render()
        assert 'type="submit"' in html

    def test_split_button_uses_positioned_alpine_menu(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_button.html" import split_button %}'
            '{% call split_button("Save", primary_href="/save") %}'
            '<a href="/export">Export</a>'
            "{% end %}"
        ).render()
        assert 'x-data="chirpuiDropdown()"' in html
        assert 'x-ref="trigger"' in html
        assert 'aria-haspopup="menu"' in html
        assert 'role="menu"' in html
        assert "x-cloak" in html


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

    def test_calendar_nav_links_use_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content",
                hrefs=frozenset({"/calendar/2024/12", "/calendar/2025/2"}),
            ),
        )
        html = env.from_string(
            '{% from "chirpui/calendar.html" import calendar %}'
            "{% set weeks = [[0,0,1,2,3,4,5],[6,7,8,9,10,11,12]] %}"
            '{{ calendar(weeks=weeks, month_label="January 2025", prev_url="/calendar/2024/12", next_url="/calendar/2025/2") }}'
        ).render()
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2


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

    def test_badge_css_uses_compact_pill_shape_and_subtle_borders(self) -> None:
        css = _chirpui_css()
        badge_root = css.split("@scope (.chirpui-badge)", 1)[1].split(":scope:is(a)", 1)[0]
        assert "border-radius: 999px" in badge_root
        assert "min-block-size: 1.5rem" in badge_root
        primary_rule = css.split(":scope.chirpui-badge--primary", 1)[1].split("}", 1)[0]
        assert "color-mix(in srgb, var(--chirpui-primary) 40%" in primary_rule

    def test_badge_with_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Error", variant="error") }}'
        ).render()
        assert "chirpui-badge--error" in html

    def test_badge_appearance_tone(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}'
            '{{ badge("Danger", appearance="outlined", tone="danger") }}'
        ).render()
        assert "chirpui-badge--outlined" in html
        assert "chirpui-badge--danger" in html

    def test_badge_with_icon(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}'
            '{{ badge("Pending", variant="warning", icon="◆") }}'
        ).render()
        assert "chirpui-badge__icon" in html
        assert "◆" in html

    def test_badge_custom_color(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Grass", color="#78c850") }}'
        ).render()
        assert "chirpui-badge--custom" in html
        assert "--chirpui-badge-color: #78c850" in html

    def test_badge_href(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Tag", href="/tags/x") }}'
        ).render()
        assert "<a " in html
        assert 'href="/tags/x"' in html

    def test_badge_href_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/tags/x"}))
        )
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Tag", href="/tags/x") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_badge_external_href_stays_plain(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"https://example.com/tags/x"})),
        )
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}'
            '{{ badge("Tag", href="https://example.com/tags/x") }}'
        ).render()
        assert 'href="https://example.com/tags/x"' in html
        assert "hx-target=" not in html


class TestRevealOnScroll:
    def test_reveal_on_scroll_renders_intersect_directives(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/reveal_on_scroll.html" import reveal_on_scroll %}'
            "{% call reveal_on_scroll() %}<p>Content</p>{% end %}"
        ).render()
        assert "chirpui-reveal-on-scroll" in html
        assert "x-intersect.once" in html
        assert "x-data" in html
        assert "x-show" in html
        assert "x-transition" in html
        assert "Content" in html

    def test_reveal_on_scroll_with_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/reveal_on_scroll.html" import reveal_on_scroll %}'
            '{% call reveal_on_scroll(cls="my-class") %}x{% end %}'
        ).render()
        assert "chirpui-reveal-on-scroll my-class" in html


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


class TestSuspense:
    def test_suspense_slot_default_skeleton(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("user-profile") }}'
        ).render()
        assert 'id="user-profile"' in html
        assert "chirpui-suspense-slot" in html
        assert "chirpui-skeleton" in html

    def test_suspense_slot_card_skeleton(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("stats", skeleton_variant="card", lines=2) }}'
        ).render()
        assert 'id="stats"' in html
        assert "chirpui-skeleton--card" in html

    def test_suspense_slot_text_skeleton(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("nav", skeleton_variant="text", lines=4) }}'
        ).render()
        assert "chirpui-skeleton--text" in html
        assert html.count("chirpui-skeleton__line") == 4

    def test_suspense_slot_custom_placeholder(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{% call suspense_slot("data") %}<p>Loading data...</p>{% end %}'
        ).render()
        assert 'id="data"' in html
        assert "Loading data..." in html
        assert "chirpui-skeleton" not in html

    def test_suspense_slot_oob_targetable(self, env: Environment) -> None:
        """The slot id is the OOB target — server sends replacement via hx-swap-oob."""
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("deferred-block") }}'
        ).render()
        assert 'id="deferred-block"' in html

    def test_suspense_group_aria_busy(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot, suspense_group %}'
            "{% call suspense_group() %}"
            '{{ suspense_slot("a") }}{{ suspense_slot("b") }}'
            "{% end %}"
        ).render()
        assert "chirpui-suspense-group" in html
        assert 'aria-busy="true"' in html
        assert 'id="a"' in html
        assert 'id="b"' in html

    def test_suspense_slot_with_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("x", cls="my-class") }}'
        ).render()
        assert "chirpui-suspense-slot my-class" in html

    def test_suspense_slot_avatar_skeleton(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("avatar", skeleton_variant="avatar") }}'
        ).render()
        assert "chirpui-skeleton--avatar" in html

    def test_suspense_slot_custom_dimensions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("chart", width="300px", height="200px") }}'
        ).render()
        assert 'id="chart"' in html
        assert "chirpui-skeleton" in html

    def test_suspense_group_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_group %}'
            '{% call suspense_group(cls="my-group") %}content{% end %}'
        ).render()
        assert "chirpui-suspense-group my-group" in html
        assert 'aria-busy="true"' in html

    def test_suspense_slot_multiple_lines(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{{ suspense_slot("feed", skeleton_variant="text", lines=6) }}'
        ).render()
        assert html.count("chirpui-skeleton__line") == 6

    def test_suspense_slot_error_boundary_fallback(self, env: Environment) -> None:
        """If caller content raises, the slot falls back to a default skeleton."""
        html = env.from_string(
            '{% from "chirpui/suspense.html" import suspense_slot %}'
            '{% call suspense_slot("broken") %}{{ undefined_var.bad_attr }}{% end %}'
        ).render()
        assert 'id="broken"' in html
        assert "chirpui-skeleton" in html


class TestNavProgress:
    def test_nav_progress_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_progress.html" import nav_progress %}{{ nav_progress() }}'
        ).render()
        assert "chirpui-nav-progress" in html
        assert 'aria-hidden="true"' in html

    def test_nav_progress_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_progress.html" import nav_progress %}'
            '{{ nav_progress(cls="my-bar") }}'
        ).render()
        assert "chirpui-nav-progress my-bar" in html

    def test_nav_progress_no_extra_class_when_empty(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_progress.html" import nav_progress %}{{ nav_progress() }}'
        ).render()
        assert 'class="chirpui-nav-progress"' in html


class TestSseStatus:
    def test_sse_status_connected(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}{{ sse_status("connected") }}'
        ).render()
        assert "chirpui-sse-status--connected" in html
        assert "Connected" in html
        assert 'role="status"' in html

    def test_sse_status_error(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}{{ sse_status("error") }}'
        ).render()
        assert "chirpui-sse-status--error" in html
        assert "Connection error" in html

    def test_sse_status_disconnected(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}{{ sse_status("disconnected") }}'
        ).render()
        assert "chirpui-sse-status--disconnected" in html
        assert "Disconnected" in html

    def test_sse_status_custom_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}'
            '{{ sse_status("error", label="Connection lost") }}'
        ).render()
        assert "Connection lost" in html
        assert "chirpui-sse-status--error" in html

    def test_sse_status_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}'
            '{{ sse_status("connected", cls="my-indicator") }}'
        ).render()
        assert "my-indicator" in html

    def test_sse_retry_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream/123") }}'
        ).render()
        assert "chirpui-sse-retry" in html
        assert 'hx-get="/api/stream/123"' in html
        assert 'hx-select="unset"' in html
        assert 'hx-disinherit="hx-select"' in html
        assert "Retry" in html

    def test_sse_retry_custom_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream/123", label="Reconnect") }}'
        ).render()
        assert "Reconnect" in html

    def test_sse_retry_post_method(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream/123", method="post") }}'
        ).render()
        assert 'hx-post="/api/stream/123"' in html

    def test_sse_retry_has_btn_classes(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream/123") }}'
        ).render()
        assert "chirpui-btn" in html
        assert "chirpui-btn--sm" in html

    def test_sse_status_invalid_falls_back(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}{{ sse_status("bogus") }}'
        ).render()
        assert "chirpui-sse-status--connected" in html
        assert "Connected" in html

    def test_sse_status_dot_aria_hidden(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}{{ sse_status("connected") }}'
        ).render()
        assert "chirpui-sse-status__dot" in html
        assert 'aria-hidden="true"' in html

    def test_sse_status_aria_live(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_status %}{{ sse_status("error") }}'
        ).render()
        assert 'aria-live="polite"' in html

    def test_sse_retry_custom_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream", target="#chat-container") }}'
        ).render()
        assert 'hx-target="#chat-container"' in html

    def test_sse_retry_custom_swap(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream", swap="innerHTML") }}'
        ).render()
        assert 'hx-swap="innerHTML"' in html

    def test_sse_retry_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sse_status.html" import sse_retry %}'
            '{{ sse_retry("/api/stream", cls="my-retry") }}'
        ).render()
        assert "my-retry" in html


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

    def test_progress_bar_custom_color(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/progress.html" import progress_bar %}'
            '{{ progress_bar(value=40, max=100, color="#78c850") }}'
        ).render()
        assert "chirpui-progress-bar--custom" in html
        assert "--chirpui-progress-color: #78c850" in html


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

    def test_media_object_css_owns_row_pressure_and_child_rhythm(self) -> None:
        css = _chirpui_css()
        assert "@scope (.chirpui-media-object)" in css
        assert ".chirpui-media-object__body > :where(:not(script, style, template))" in css
        assert ".chirpui-media-object__actions > :where(:not(script, style, template))" in css
        assert "flex: 999 1 12rem;" in css
        assert "margin-inline-start: auto;" in css
        assert "overflow-wrap: anywhere;" in css


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

    @pytest.mark.parametrize(
        ("name", "glyph"),
        [("activity", "◎"), ("pause", "Ⅱ"), ("warning", "↑")],
    )
    def test_stat_with_integration_icon_alias_no_warning(
        self,
        env: Environment,
        recwarn: pytest.WarningsRecorder,
        name: str,
        glyph: str,
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/stat.html" import stat %}'
            f'{{{{ stat(value="42", label="Runs", icon="{name}") }}}}'
        ).render()
        assert "chirpui-stat__icon" in html
        assert glyph in html
        assert not [w for w in recwarn if issubclass(w.category, ChirpUIValidationWarning)]


class TestMetricGrid:
    def test_metric_grid(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_grid, metric_card %}'
            "{% call metric_grid() %}"
            '{{ metric_card(value=128, label="Tasks", icon="status") }}'
            "{% end %}"
        ).render()
        assert "chirpui-metric-grid" in html
        assert "chirpui-metric-card" in html
        assert "Tasks" in html

    def test_metric_card_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value="99.9%", label="Uptime", href="/status", hint="This week") }}'
        ).render()
        assert 'href="/status"' in html
        assert "chirpui-card--link" in html
        assert "This week" in html

    def test_metric_card_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/status"}))
        )
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value="99.9%", label="Uptime", href="/status", hint="This week") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_metric_card_attrs_map_on_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value=1, label="N", attrs_map={"id": "kpi-open"}) }}'
        ).render()
        assert 'id="kpi-open"' in html
        assert "chirpui-metric-card" in html

    def test_metric_card_attrs_map_on_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value=1, label="N", href="/x", attrs_map={"id": "kpi-link"}) }}'
        ).render()
        assert 'id="kpi-link"' in html
        assert 'href="/x"' in html

    def test_metric_card_link_attrs_map_hx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/x"}))
        )
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value=1, label="N", href="/x", attrs_map={"hx-target": "#content"}) }}'
        ).render()
        assert 'hx-target="#site-content"' not in html
        assert 'hx-target="#content"' in html


class TestConfigCard:
    def test_config_card_forwards_attrs_map_to_card(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/config_card.html" import config_card %}'
            '{{ config_card(title="T", icon="◇", items=[{"term": "a", "detail": "b"}], '
            'attrs_map={"id": "cfg-logs"}) }}'
        ).render()
        assert 'id="cfg-logs"' in html
        assert "chirpui-card__title" in html


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
        assert '{% extends "chirp/layouts/shell.html" %}' in content
        assert "chirp/layouts/boost.html" not in content
        assert 'id="main"' in content
        assert 'hx-boost="true"' in content
        assert 'hx-select="#page-content"' in content
        assert "{% block head_extra %}{% end %}" in content
        assert "chirpui.css" in content
        assert "app-theme-starter.css" in content
        assert "cdn.jsdelivr.net/npm/alpinejs" not in content
        assert 'src="/static/chirpui-alpine.js"' not in content
        assert "use_chirp_ui(app)" in content
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

    def test_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/"})),
        )
        html = env.from_string(
            '{% from "chirpui/link.html" import link %}{{ link("Home", href="/") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_link_external(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/link.html" import link %}'
            '{{ link("Docs", href="https://example.com", external=true) }}'
        ).render()
        assert 'target="_blank"' in html
        assert 'rel="noopener noreferrer"' in html
        assert "hx-target=" not in html


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

    def test_breadcrumb_links_use_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/", "/docs"})),
        )
        html = env.from_string(
            '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
            '{% set items = [{"label": "Home", "href": "/"}, {"label": "Docs", "href": "/docs"}, {"label": "Current"}] %}'
            "{{ breadcrumbs(items) }}"
        ).render()
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2

    def test_breadcrumbs_overflow_collapse(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
            "{{ breadcrumbs(items, overflow='collapse', max_items=4) }}"
        ).render(
            items=[
                {"label": "Home", "href": "/"},
                {"label": "Workspace", "href": "/workspace"},
                {"label": "Project", "href": "/workspace/project"},
                {"label": "Runs", "href": "/workspace/project/runs"},
                {"label": "Current"},
            ]
        )
        assert "chirpui-breadcrumbs__overflow" in html
        assert "chirpui-breadcrumbs__overflow-list" in html
        assert 'aria-label="Show collapsed breadcrumbs"' in html
        assert "Workspace" in html
        assert "Project" in html
        assert "Runs" in html
        assert html.count('aria-current="page"') == 1

    def test_breadcrumbs_overflow_preserves_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content",
                hrefs=frozenset(
                    {"/", "/workspace", "/workspace/project", "/workspace/project/runs"}
                ),
            ),
        )
        html = env.from_string(
            '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
            "{{ breadcrumbs(items, overflow='collapse', max_items=4) }}"
        ).render(
            items=[
                {"label": "Home", "href": "/"},
                {"label": "Workspace", "href": "/workspace"},
                {"label": "Project", "href": "/workspace/project"},
                {"label": "Runs", "href": "/workspace/project/runs"},
                {"label": "Current"},
            ]
        )
        assert html.count('hx-target="#site-content"') == 4
        assert html.count('hx-boost="true"') == 4


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

    def test_linked_list_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/a"})),
        )
        html = env.from_string(
            '{% from "chirpui/list.html" import list_group %}'
            '{% set items = [{"label": "A", "href": "/a"}] %}'
            "{{ list_group(items, linked=true) }}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_list_css_owns_row_separation_and_child_rhythm(self) -> None:
        css = _chirpui_css()
        assert "@scope (.chirpui-list)" in css
        assert ".chirpui-list__item > :where(:not(script, style, template))" in css
        assert ":scope.chirpui-list--bordered .chirpui-list__item + .chirpui-list__item" in css
        bordered_sibling_rule = css.split(
            ":scope.chirpui-list--bordered .chirpui-list__item + .chirpui-list__item",
            1,
        )[1].split("}", 1)[0]
        assert "margin-top: 0;" in bordered_sibling_rule
        assert "overflow-wrap: anywhere;" in css


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
        assert "Hover me" in html

    def test_tooltip_block_wrapper(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tooltip.html" import tooltip %}'
            '{% call tooltip("More detail", block=true) %}<a href="/x">Route</a>{% end %}'
        ).render()
        assert '<div class="chirpui-tooltip chirpui-tooltip--top chirpui-tooltip--block"' in html
        assert '<a href="/x">Route</a>' in html


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
        assert "chirpui-spinner-thinking__char" in html
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

    def test_avatar_default_has_role_img(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}{{ avatar(src="/a.jpg", alt="Alice") }}'
        ).render()
        assert 'role="img"' in html
        assert 'aria-label="Alice"' in html

    def test_avatar_decorative_suppresses_role_img(self, env: Environment) -> None:
        """decorative=true renders role="presentation" and aria-hidden for screen reader suppression."""
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}'
            '{{ avatar(src="/a.jpg", decorative=true) }}'
        ).render()
        assert 'role="presentation"' in html
        assert 'aria-hidden="true"' in html
        assert 'role="img"' not in html


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

    def test_video_card_links_use_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/v", "/c"})),
        )
        html = env.from_string(
            '{% from "chirpui/video_card.html" import video_card %}'
            '{{ video_card(href="/v", thumbnail="/t.jpg", duration="4:32", title="Test", channel="Ch", channel_href="/c") }}'
        ).render()
        assert 'class="chirpui-video-card__link"' in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html


class TestActionBar:
    def test_action_bar_item_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/share"})),
        )
        html = env.from_string(
            '{% from "chirpui/action_bar.html" import action_bar, action_bar_item %}'
            "{% call action_bar() %}"
            '{{ action_bar_item(icon="↗", label="Share", href="/share") }}'
            "{% end %}"
        ).render()
        assert "chirpui-action-bar__item" in html
        assert 'hx-target="#site-content"' in html


class TestChannelCard:
    def test_channel_card_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/channel/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/channel_card.html" import channel_card %}'
            '{{ channel_card(href="/channel/1", name="Dev Channel", subscribers="12.5K") }}'
        ).render()
        assert "chirpui-channel-card__link" in html
        assert 'hx-target="#site-content"' in html

    def test_channel_card_slot_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/channel/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/channel_card.html" import channel_card %}'
            '{% call channel_card(href="/channel/1", name="Dev Channel", use_slots=true) %}'
            "{% slot body %}<p>Info</p>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-channel-card__link" in html
        assert 'hx-target="#site-content"' in html


class TestProfileHeader:
    def test_profile_header_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/alice"})),
        )
        html = env.from_string(
            '{% from "chirpui/profile_header.html" import profile_header %}'
            '{% call profile_header(name="Alice", href="/alice", use_slots=true) %}'
            "{% slot avatar %}<span>A</span>{% end %}"
            "{% end %}"
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_profile_header_info_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/alice"})),
        )
        html = env.from_string(
            '{% from "chirpui/profile_header.html" import profile_header_info %}'
            '{% call profile_header_info("Alice", href="/alice") %}<p>Bio</p>{% end %}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html


class TestPostCard:
    def test_post_card_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/alice"})),
        )
        html = env.from_string(
            '{% from "chirpui/post_card.html" import post_card %}'
            '{% call post_card(name="Alice", handle="@alice", time="2h", href="/alice") %}'
            "<p>Hello</p>"
            "{% end %}"
        ).render()
        assert "chirpui-post-card__name" in html
        assert 'hx-target="#site-content"' in html

    def test_post_card_header_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/alice"})),
        )
        html = env.from_string(
            '{% from "chirpui/post_card.html" import post_card_header %}'
            '{% call post_card_header("Alice", href="/alice") %}<span>A</span>{% end %}'
        ).render()
        assert "chirpui-post-card__name" in html
        assert 'hx-target="#site-content"' in html


class TestVideoThumbnail:
    def test_video_thumbnail_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/watch/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/video_thumbnail.html" import video_thumbnail %}'
            '{{ video_thumbnail(href="/watch/1", src="/thumb.jpg", alt="Video title", duration="4:32") }}'
        ).render()
        assert "chirpui-video-thumbnail" in html
        assert 'hx-target="#site-content"' in html


class TestMention:
    def test_mention_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/user/alice"})),
        )
        html = env.from_string(
            '{% from "chirpui/mention.html" import mention %}'
            '{{ mention("alice", href="/user/alice") }}'
        ).render()
        assert "chirpui-mention" in html
        assert 'hx-target="#site-content"' in html


class TestTrendingTag:
    def test_trending_tag_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/tag/python"})),
        )
        html = env.from_string(
            '{% from "chirpui/trending_tag.html" import trending_tag %}'
            '{{ trending_tag(tag="python", href="/tag/python", count="12.5K") }}'
        ).render()
        assert "chirpui-trending-tag" in html
        assert 'hx-target="#site-content"' in html


class TestConversationItem:
    def test_conversation_item_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/chat/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/conversation_item.html" import conversation_item %}'
            '{% call conversation_item(href="/chat/1", name="Alice", preview="Hey!", unread=3, time="2m") %}'
            "<span>A</span>"
            "{% end %}"
        ).render()
        assert "chirpui-conversation-item" in html
        assert 'hx-target="#site-content"' in html


class TestPlaylist:
    def test_playlist_item_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/watch/1"})),
        )
        html = env.from_string(
            '{% from "chirpui/playlist.html" import playlist, playlist_item %}'
            "{% call playlist(title='Up next') %}"
            "{{ playlist_item('/watch/1', 'Video 1', duration='4:32', active=true) }}"
            "{% end %}"
        ).render()
        assert "chirpui-playlist-item__link" in html
        assert 'hx-target="#site-content"' in html


class TestComment:
    def test_comment_links_use_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content",
                hrefs=frozenset({"/user/alice", "/comments/1/replies"}),
            ),
        )
        html = env.from_string(
            '{% from "chirpui/comment.html" import comment %}'
            '{% call comment(author="Alice", href="/user/alice", replies_url="/comments/1/replies", replies_count=2) %}'
            "<p>Hello</p>"
            "{% end %}"
        ).render()
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2


class TestBarChart:
    def test_bar_chart_label_link_uses_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/skills/debug-agent"})),
        )
        html = env.from_string(
            '{% from "chirpui/bar_chart.html" import bar_chart %}'
            '{{ bar_chart(items=[{"label": "debug-agent", "value": 18, "href": "/skills/debug-agent"}], max=20) }}'
        ).render()
        assert "chirpui-bar-chart__label-link" in html
        assert 'hx-target="#site-content"' in html


class TestTagBrowse:
    def test_tag_selection_badges_use_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        def tag_toggle_url(tag: str) -> str:
            return f"/tags/{tag.lower()}"

        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs(
                "site-content",
                hrefs=frozenset({"/tags/python", "/tags/clear"}),
            ),
        )
        html = env.from_string(
            '{% from "chirpui/tag_browse.html" import tag_selection_badges %}'
            "{{ tag_selection_badges(selected_tags, tag_toggle_url, clear_url) }}"
        ).render(
            selected_tags=["Python"],
            tag_toggle_url=tag_toggle_url,
            clear_url="/tags/clear",
        )
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2

    def test_tag_browse_tray_renders_tags_with_selection(self, env: Environment) -> None:
        def tag_toggle_url(tag: str) -> str:
            return f"/tags/{tag.lower()}"

        env.add_global("route_link_attrs", _stub_route_link_attrs("site-content"))
        html = env.from_string(
            '{% from "chirpui/tag_browse.html" import tag_browse_tray %}'
            "{{ tag_browse_tray("
            '"my-tray", "Pick tags", tags, selected_tags, tag_toggle_url, clear_url'
            ") }}"
        ).render(
            tags=["Python", "Rust", "Go"],
            selected_tags=["python"],
            tag_toggle_url=tag_toggle_url,
            clear_url="/tags/clear",
        )
        assert "chirpui-badge--primary" in html
        assert "chirpui-badge--muted" in html
        assert "Python" in html
        assert "Rust" in html
        assert "Clear all" in html

    def test_tag_browse_tray_empty_tags(self, env: Environment) -> None:
        env.add_global("route_link_attrs", _stub_route_link_attrs("site-content"))
        html = env.from_string(
            '{% from "chirpui/tag_browse.html" import tag_browse_tray %}'
            '{{ tag_browse_tray("t", "Tags", tags, [], tag_toggle_url, "/clear") }}'
        ).render(tags=[], tag_toggle_url=lambda t: "/")
        assert "No tags available" in html

    def test_tag_filter_actions_shows_clear_when_selected(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/clear"})),
        )
        html = env.from_string(
            '{% from "chirpui/tag_browse.html" import tag_filter_actions %}'
            '{{ tag_filter_actions(selected_tags, "/clear") }}'
        ).render(selected_tags=["Python"])
        assert "Clear all" in html
        assert 'hx-boost="true"' in html

    def test_tag_filter_actions_hidden_when_empty(self, env: Environment) -> None:
        env.add_global("route_link_attrs", _stub_route_link_attrs("site-content"))
        html = env.from_string(
            '{% from "chirpui/tag_browse.html" import tag_filter_actions %}'
            '{{ tag_filter_actions(selected_tags, "/clear") }}'
        ).render(selected_tags=[])
        assert "Clear all" not in html


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

    def test_split_button_css_keeps_segments_fused(self) -> None:
        """Split buttons should render as one compound control, not two adjacent buttons."""
        from pathlib import Path

        css_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "chirp_ui"
            / "templates"
            / "chirpui.css"
        )
        content = css_path.read_text()
        assert "--chirpui-split-btn-divider" in content
        assert ".chirpui-split-btn:has(.chirpui-btn--primary)" in content
        assert ".chirpui-split-btn .chirpui-split-btn__primary" in content
        assert "box-shadow: none;" in content
        assert "border-inline-start: 1px solid var(--chirpui-split-btn-divider)" in content

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


# ---------------------------------------------------------------------------
# New Effects & Primitives
# ---------------------------------------------------------------------------


class TestShimmerButton:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("Get Started") }}'
        ).render()
        assert "chirpui-shimmer-btn" in html
        assert "chirpui-shimmer-btn__shimmer" in html
        assert "Get Started" in html

    def test_primary_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("Go", variant="primary") }}'
        ).render()
        assert "chirpui-shimmer-btn--primary" in html

    def test_as_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("Link", href="/go") }}'
        ).render()
        assert "<a " in html
        assert 'href="/go"' in html

    def test_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/go"}))
        )
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("Link", href="/go") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_link_attrs_map_hx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/go"}))
        )
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("Link", href="/go", attrs_map={"hx-target": "#content"}) }}'
        ).render()
        assert 'hx-target="#site-content"' not in html
        assert 'hx-target="#content"' in html

    def test_disabled_link_strips_href_and_route_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/go"}))
        )
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("Link", href="/go", disabled=true) }}'
        ).render()
        assert 'href="/go"' not in html
        assert "hx-target=" not in html
        assert 'aria-disabled="true"' in html

    def test_type_and_attrs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/shimmer_button.html" import shimmer_button %}'
            '{{ shimmer_button("X", type="submit", attrs=\'data-testid="sb"\') }}'
        ).render()
        assert 'type="submit"' in html
        assert 'data-testid="sb"' in html


class TestRippleButton:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/ripple_button.html" import ripple_button %}'
            '{{ ripple_button("Click Me") }}'
        ).render()
        assert "chirpui-ripple-btn" in html
        assert "x-data" in html
        assert "Click Me" in html


class TestBorderBeam:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/border_beam.html" import border_beam %}'
            "{% call border_beam() %}Content{% end %}"
        ).render()
        assert "chirpui-border-beam" in html
        assert "chirpui-border-beam__beam" in html
        assert "chirpui-border-beam__content" in html
        assert "Content" in html

    def test_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/border_beam.html" import border_beam %}'
            '{% call border_beam(variant="success") %}X{% end %}'
        ).render()
        assert "chirpui-border-beam--success" in html

    def test_attrs_on_root(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/border_beam.html" import border_beam %}'
            "{% call border_beam(attrs='data-testid=\"bb\"') %}Z{% end %}"
        ).render()
        assert 'data-testid="bb"' in html


class TestNotificationDot:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/notification_dot.html" import notification_dot %}'
            "{% call notification_dot() %}<button>Inbox</button>{% end %}"
        ).render()
        assert "chirpui-notification-dot" in html
        assert "chirpui-notification-dot__dot" in html
        assert "chirpui-notification-dot__ping" in html
        assert 'aria-label="notification"' in html

    def test_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/notification_dot.html" import notification_dot %}'
            "{% call notification_dot(count=5) %}<span>Mail</span>{% end %}"
        ).render()
        assert "chirpui-notification-dot--count" in html
        assert "5" in html
        assert 'aria-label="5 notifications"' in html

    def test_count_singular(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/notification_dot.html" import notification_dot %}'
            "{% call notification_dot(count=1) %}<span>Mail</span>{% end %}"
        ).render()
        assert 'aria-label="1 notification"' in html
        assert "notifications" not in html

    def test_custom_aria_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/notification_dot.html" import notification_dot %}'
            '{% call notification_dot(count=5, aria_label="5 unread") %}<span>Mail</span>{% end %}'
        ).render()
        assert 'aria-label="5 unread"' in html


class TestOobHelpers:
    def test_oob_fragment_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_fragment %}'
            '{% call oob_fragment("my-target") %}<p>New</p>{% end %}'
        ).render()
        assert 'id="my-target"' in html
        assert 'hx-swap-oob="true"' in html
        assert "<p>New</p>" in html

    def test_oob_fragment_swap_strategy(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_fragment %}'
            '{% call oob_fragment("stats", swap="innerHTML") %}<span>42</span>{% end %}'
        ).render()
        assert 'hx-swap-oob="innerHTML"' in html

    def test_oob_fragment_custom_tag(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_fragment %}'
            '{% call oob_fragment("nav", tag="nav") %}links{% end %}'
        ).render()
        assert "<nav " in html
        assert "</nav>" in html

    def test_oob_toast(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_toast %}'
            '{{ oob_toast("Saved!", variant="success") }}'
        ).render()
        assert 'hx-swap-oob="beforeend:#chirpui-toasts"' in html
        assert "chirpui-toast--success" in html
        assert "Saved!" in html

    def test_oob_toast_custom_container(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_toast %}'
            '{{ oob_toast("Hi", container_id="my-toasts") }}'
        ).render()
        assert "beforeend:#my-toasts" in html

    def test_counter_badge_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("inbox-count", count=5) }}'
        ).render()
        assert 'id="inbox-count"' in html
        assert "chirpui-counter-badge" in html
        assert ">5<" in html
        assert "hx-swap-oob" not in html

    def test_counter_badge_oob(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("cart", count=3, oob=true) }}'
        ).render()
        assert 'hx-swap-oob="true"' in html
        assert 'id="cart"' in html

    def test_counter_badge_zero_hidden(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("notif", count=0) }}'
        ).render()
        assert "hidden" in html

    def test_counter_badge_overflow(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("msgs", count=150) }}'
        ).render()
        assert "99+" in html

    def test_counter_badge_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("alerts", count=7, variant="danger") }}'
        ).render()
        assert "chirpui-counter-badge--danger" in html

    def test_counter_badge_aria_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}{{ counter_badge("x", count=1) }}'
        ).render()
        assert 'aria-label="1 notification"' in html

    def test_counter_badge_plural_aria(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}{{ counter_badge("x", count=3) }}'
        ).render()
        assert 'aria-label="3 notifications"' in html

    def test_counter_badge_custom_max(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("x", count=50, max_count=25) }}'
        ).render()
        assert "25+" in html

    def test_oob_fragment_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_fragment %}'
            '{% call oob_fragment("target", cls="my-frag") %}content{% end %}'
        ).render()
        assert 'class="my-frag"' in html

    def test_oob_toast_default_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_toast %}{{ oob_toast("Info msg") }}'
        ).render()
        assert "chirpui-toast--info" in html
        assert "hx-swap-oob" in html

    def test_oob_toast_not_dismissible(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_toast %}'
            '{{ oob_toast("Alert!", dismissible=false) }}'
        ).render()
        assert "chirpui-toast__close" not in html

    def test_counter_badge_warning_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}'
            '{{ counter_badge("w", count=2, variant="warning") }}'
        ).render()
        assert "chirpui-counter-badge--warning" in html

    def test_counter_badge_no_variant_no_modifier(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/oob.html" import counter_badge %}{{ counter_badge("x", count=1) }}'
        ).render()
        assert "chirpui-counter-badge--" not in html

    def test_oob_fragment_error_boundary(self, env: Environment) -> None:
        """Broken slot content produces empty OOB fragment, not a crash."""
        html = env.from_string(
            '{% from "chirpui/oob.html" import oob_fragment %}'
            '{% call oob_fragment("broken-target") %}{{ undefined_var.bad }}{% end %}'
        ).render()
        assert 'id="broken-target"' in html
        assert 'hx-swap-oob="true"' in html


class TestNumberTicker:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/number_ticker.html" import number_ticker %}{{ number_ticker(1250) }}'
        ).render()
        assert "chirpui-number-ticker" in html
        assert "--chirpui-num: 1250" in html

    def test_prefix_suffix(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/number_ticker.html" import number_ticker %}'
            '{{ number_ticker(99, prefix="$", suffix="+") }}'
        ).render()
        assert "$" in html
        assert "+" in html


class TestPulsingButton:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pulsing_button.html" import pulsing_button %}'
            '{{ pulsing_button("Try Now") }}'
        ).render()
        assert "chirpui-pulsing-btn" in html
        assert "chirpui-pulsing-btn__ring" in html
        assert "Try Now" in html

    def test_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/live"}))
        )
        html = env.from_string(
            '{% from "chirpui/pulsing_button.html" import pulsing_button %}'
            '{{ pulsing_button("Go Live", icon="◎", href="/live") }}'
        ).render()
        assert 'href="/live"' in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_disabled_link_strips_href_and_route_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/live"}))
        )
        html = env.from_string(
            '{% from "chirpui/pulsing_button.html" import pulsing_button %}'
            '{{ pulsing_button("Go Live", href="/live", disabled=true) }}'
        ).render()
        assert 'href="/live"' not in html
        assert "hx-target=" not in html
        assert 'aria-disabled="true"' in html


class TestMarquee:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/marquee.html" import marquee %}{{ marquee(items=["A", "B", "C"]) }}'
        ).render()
        assert "chirpui-marquee" in html
        assert "chirpui-marquee__track" in html
        assert "chirpui-marquee__item" in html
        # Items duplicated for seamless loop
        assert html.count(">A<") >= 2

    def test_reverse(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/marquee.html" import marquee %}'
            '{{ marquee(items=["X"], reverse=true) }}'
        ).render()
        assert "chirpui-marquee--reverse" in html


class TestMeteor:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/meteor.html" import meteor %}{% call meteor() %}Hero{% end %}'
        ).render()
        assert "chirpui-meteor" in html
        assert "chirpui-meteor__streak" in html
        assert "chirpui-meteor__content" in html
        assert "Hero" in html


class TestTextReveal:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/text_reveal.html" import text_reveal %}'
            '{{ text_reveal("Hello World") }}'
        ).render()
        assert "chirpui-text-reveal" in html
        assert "Hello World" in html

    def test_gradient(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/text_reveal.html" import text_reveal %}'
            '{{ text_reveal("Bold", variant="gradient") }}'
        ).render()
        assert "chirpui-text-reveal--gradient" in html


class TestGradientText:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/gradient_text.html" import gradient_text %}'
            '{{ gradient_text("Premium") }}'
        ).render()
        assert "chirpui-gradient-text" in html
        assert "Premium" in html

    def test_animated(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/gradient_text.html" import gradient_text %}'
            '{{ gradient_text("Shift", animated=true) }}'
        ).render()
        assert "chirpui-gradient-text--animated" in html


class TestGlowCard:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/glow_card.html" import glow_card %}'
            "{% call glow_card() %}Feature{% end %}"
        ).render()
        assert "chirpui-glow-card" in html
        assert "chirpui-glow-card__glow" in html
        assert "chirpui-glow-card__content" in html
        assert "x-data" in html
        assert "Feature" in html

    def test_attrs_on_root(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/glow_card.html" import glow_card %}'
            "{% call glow_card(attrs='data-testid=\"gc\"') %}F{% end %}"
        ).render()
        assert 'data-testid="gc"' in html
        assert "@mousemove=" in html


class TestSpotlightCard:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/spotlight_card.html" import spotlight_card %}'
            "{% call spotlight_card() %}Content{% end %}"
        ).render()
        assert "chirpui-spotlight-card" in html
        assert "chirpui-spotlight-card__spotlight" in html

    def test_attrs_on_root(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/spotlight_card.html" import spotlight_card %}'
            "{% call spotlight_card(attrs='data-testid=\"sc\"') %}C{% end %}"
        ).render()
        assert 'data-testid="sc"' in html


class TestParticleBg:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            "{% call particle_bg() %}Content{% end %}"
        ).render()
        assert "chirpui-particle-bg" in html
        assert "chirpui-particle-bg__dot" in html
        assert "chirpui-particle-bg__content" in html

    def test_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            "{% call particle_bg(count=3) %}X{% end %}"
        ).render()
        assert html.count("chirpui-particle-bg__dot") == 3

    def test_standalone_with_explicit_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% call particle_bg(variant="accent") %}X{% end %}'
        ).render()
        assert "chirpui-particle-bg--accent" in html

    def test_standalone_without_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            "{% call particle_bg() %}X{% end %}"
        ).render()
        assert "chirpui-particle-bg--" not in html

    def test_consumes_variant_from_provide(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% provide _hero_variant = "accent" %}'
            "{% call particle_bg() %}X{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--accent" in html

    def test_explicit_variant_overrides_provide(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            '{% provide _hero_variant = "accent" %}'
            '{% call particle_bg(variant="muted") %}X{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--muted" in html
        assert "chirpui-particle-bg--accent" not in html


class TestHeroEffectsProvide:
    def test_hero_effects_provides_variant_to_child(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero_effects.html" import hero_effects %}'
            '{% call hero_effects(effect="particles", variant="accent") %}'
            "<h1>Hello</h1>"
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--accent" in html

    def test_hero_effects_default_no_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero_effects.html" import hero_effects %}'
            '{% call hero_effects(effect="particles") %}'
            "<h1>Hello</h1>"
            "{% end %}"
        ).render()
        assert "chirpui-particle-bg--" not in html

    def test_hero_effects_meteor_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/hero_effects.html" import hero_effects %}'
            '{% call hero_effects(effect="meteors", variant="accent") %}'
            "<h1>Hello</h1>"
            "{% end %}"
        ).render()
        assert "chirpui-meteor--accent" in html


class TestAnimatedCounter:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/animated_counter.html" import animated_counter %}'
            '{{ animated_counter(500, label="Users") }}'
        ).render()
        assert "chirpui-animated-counter" in html
        assert "--chirpui-num: 500" in html
        assert "Users" in html


class TestBentoGrid:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/bento_grid.html" import bento_grid, bento_item %}'
            "{% call bento_grid() %}"
            "{% call bento_item() %}A{% end %}"
            "{% call bento_item(span=2) %}B{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-bento" in html
        assert "chirpui-bento__item" in html
        assert "chirpui-bento__item--span-2" in html


class TestDock:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dock.html" import dock %}'
            '{{ dock(items=[{"icon": "home", "label": "Home", "href": "/"}]) }}'
        ).render()
        assert "chirpui-dock" in html
        assert "chirpui-dock__item" in html
        assert 'aria-label="Home"' in html
        assert 'href="/"' in html

    def test_dock_links_use_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/"})),
        )
        html = env.from_string(
            '{% from "chirpui/dock.html" import dock %}'
            '{{ dock(items=[{"icon": "home", "label": "Home", "href": "/"}]) }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_glass_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dock.html" import dock %}'
            '{{ dock(items=[{"icon": "home", "label": "Home"}], variant="glass") }}'
        ).render()
        assert "chirpui-dock--glass" in html


class TestAnimatedStatCard:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/animated_stat_card.html" import animated_stat_card %}'
            '{{ animated_stat_card(1250, label="Users", trend="+12%", trend_direction="up") }}'
        ).render()
        assert "chirpui-animated-stat-card" in html
        assert "chirpui-animated-stat-card__trend--up" in html
        assert "+12%" in html


class TestIconBtn:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("✕", aria_label="Close") }}'
        ).render()
        assert "chirpui-icon-btn" in html
        assert 'aria-label="Close"' in html

    def test_variant_and_size(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("⚙", variant="ghost", size="lg", aria_label="Settings") }}'
        ).render()
        assert "chirpui-icon-btn--ghost" in html
        assert "chirpui-icon-btn--lg" in html

    def test_as_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("→", href="/next", aria_label="Next") }}'
        ).render()
        assert "<a " in html
        assert 'href="/next"' in html

    def test_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/next"}))
        )
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("→", href="/next", aria_label="Next") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_link_with_explicit_hx_skips_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/next"}))
        )
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("→", href="/next", aria_label="Next", hx_get="/next", hx_target="#content") }}'
        ).render()
        assert 'hx-target="#site-content"' not in html
        assert 'hx-target="#content"' in html
        assert 'hx-get="/next"' in html
        assert 'hx-boost="false"' in html
        assert 'hx-select="unset"' in html

    def test_button_with_explicit_hx_emits_select_unset(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("→", aria_label="Next", hx_post="/next", hx_target="#content") }}'
        ).render()
        assert "<button " in html
        assert 'hx-post="/next"' in html
        assert 'hx-target="#content"' in html
        assert 'hx-select="unset"' in html
        assert 'hx-sync="this:drop"' in html
        assert 'hx-disabled-elt="this"' in html

    def test_external_link_stays_plain(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"https://example.com/next"})),
        )
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("→", href="https://example.com/next", aria_label="Next") }}'
        ).render()
        assert 'href="https://example.com/next"' in html
        assert "hx-target=" not in html

    def test_disabled_link_strips_href_and_htmx(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/next"}))
        )
        html = env.from_string(
            '{% from "chirpui/icon_btn.html" import icon_btn %}'
            '{{ icon_btn("→", href="/next", aria_label="Next", hx_get="/next", disabled=true) }}'
        ).render()
        assert 'href="/next"' not in html
        assert 'hx-get="/next"' not in html
        assert "hx-target=" not in html
        assert 'aria-disabled="true"' in html


class TestCombobox:
    _OPTS = (
        '[{"label": "Canada", "value": "ca"},'
        ' {"label": "United States", "value": "us"},'
        ' {"label": "Mexico", "value": "mx"}]'
    )

    def _render(self, env: Environment, *, extra: str = "") -> str:
        return env.from_string(
            '{% from "chirpui/combobox.html" import combobox %}'
            '{{ combobox(name="country", label="Country", options=' + self._OPTS + extra + ") }}"
        ).render()

    def test_combobox_contract_and_aria(self, env: Environment) -> None:
        html = self._render(env)
        assert 'class="chirpui-combobox"' in html
        assert 'x-data="chirpuiCombobox()"' in html
        # Input declares the WAI-ARIA combobox contract.
        assert 'role="combobox"' in html
        assert 'aria-autocomplete="list"' in html
        assert 'aria-controls="chirpui-combobox-country-list"' in html
        assert ':aria-activedescendant="activeId"' in html
        # Listbox of options.
        assert 'role="listbox"' in html
        assert html.count('role="option"') == 3
        assert 'data-value="us"' in html
        assert 'data-label="United States"' in html
        # Hidden input submits the selected value under `name`.
        assert 'type="hidden"' in html
        assert 'name="country"' in html
        # Label is associated with the input.
        assert 'for="chirpui-combobox-country-input"' in html

    def test_combobox_initial_value_fills_display_label(self, env: Environment) -> None:
        html = self._render(env, extra=', value="us"')
        # The visible input shows the selected option's label; the hidden input
        # carries the value.
        assert 'value="United States"' in html
        assert 'value="us"' in html

    def test_combobox_option_ids_are_stable_and_unique(self, env: Environment) -> None:
        html = self._render(env)
        for i in range(3):
            assert f'id="chirpui-combobox-country-opt-{i}"' in html

    def test_combobox_multiple_renders_token_scaffold(self, env: Environment) -> None:
        html = self._render(env, extra=", multiple=true")
        assert "chirpui-combobox--multiple" in html
        assert 'data-multiple="true"' in html
        assert "chirpui-combobox__control" in html
        assert "chirpui-combobox__tokens" in html
        assert 'x-for="t in selected"' in html
        assert "chirpui-combobox__token-remove" in html
        # Multi-select submits repeated hidden inputs, not the single-value input.
        assert 'x-ref="value"' not in html


class TestDatePicker:
    def test_single_date_picker_contract(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/date_picker.html" import date_picker %}'
            '{{ date_picker(name="due", label="Due date", value="2025-06-15") }}'
        ).render()
        assert 'x-data="chirpuiDatePicker()"' in html
        assert 'data-range="false"' in html
        assert 'data-value="2025-06-15"' in html
        # Readonly trigger input + a hidden value input submitted under `name`.
        assert 'aria-haspopup="dialog"' in html
        assert 'name="due"' in html
        assert 'value="2025-06-15"' in html
        # Popover dialog + accessible grid.
        assert 'role="dialog"' in html
        assert 'role="grid"' in html
        assert 'role="gridcell"' in html
        assert 'role="columnheader"' in html

    def test_range_date_picker_emits_two_hidden_inputs(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/date_picker.html" import date_picker %}'
            '{{ date_picker(name="span", range=true, min="2025-06-01", max="2025-06-30") }}'
        ).render()
        assert "chirpui-date-picker--range" in html
        assert 'data-range="true"' in html
        assert 'data-min="2025-06-01"' in html
        assert 'data-max="2025-06-30"' in html
        # Start under `name`, end under the default `{name}_end`.
        assert 'name="span"' in html
        assert 'name="span_end"' in html

    def test_range_custom_end_name(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/date_picker.html" import date_picker %}'
            '{{ date_picker(name="start", range=true, end_name="finish") }}'
        ).render()
        assert 'name="finish"' in html


class TestContextMenu:
    def _render(self, env: Environment, *, items: str, label: str = "Row actions") -> str:
        return env.from_string(
            '{% from "chirpui/context_menu.html" import context_menu %}'
            "{% call context_menu(items=" + items + ', label="' + label + '") %}'
            '<div class="chirpui-card">Right-click for actions</div>'
            "{% end %}"
        ).render()

    def test_basic_structure_and_aria(self, env: Environment) -> None:
        html = self._render(
            env,
            items='[{"label": "Open", "action": "open"}, {"label": "Rename", "action": "rename"}]',
        )
        # Region is a focusable trigger wired to the Alpine factory.
        assert 'class="chirpui-context-menu"' in html
        assert 'x-data="chirpuiContextMenu()"' in html
        assert 'role="button"' in html
        assert 'aria-haspopup="menu"' in html
        assert 'aria-label="Row actions"' in html
        assert 'data-item-count="2"' in html
        assert "openAt($event)" in html
        # Panel is a role=menu with roving-tabindex items.
        assert 'class="chirpui-context-menu__panel"' in html
        assert 'role="menu"' in html
        assert html.count('role="menuitem"') == 2
        assert 'x-ref="item-0"' in html
        assert 'x-ref="item-1"' in html
        assert 'tabindex="-1"' in html
        assert 'data-label="Open"' in html
        assert 'data-action="rename"' in html
        # Slotted target content is rendered inside the region.
        assert "Right-click for actions" in html

    def test_variant_href_disabled_and_icon(self, env: Environment) -> None:
        html = self._render(
            env,
            items=(
                '[{"label": "Visit", "href": "/x", "icon": "↗"},'
                ' {"label": "Delete", "action": "delete", "variant": "danger"},'
                ' {"label": "Paste", "action": "paste", "disabled": true}]'
            ),
        )
        # href item renders an <a role="menuitem"> with the link.
        assert 'href="/x"' in html
        assert "chirpui-context-menu__icon" in html
        # danger variant class is emitted.
        assert "chirpui-context-menu__item--danger" in html
        # disabled item is aria-disabled (focusable-but-inert), not natively disabled.
        assert 'aria-disabled="true"' in html
        assert "disabled>" not in html
        assert " disabled " not in html

    def test_item_count_matches_items(self, env: Environment) -> None:
        html = self._render(env, items='[{"label": "Only", "action": "only"}]')
        assert 'data-item-count="1"' in html
        assert html.count('role="menuitem"') == 1


class TestSegmentedControl:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/segmented_control.html" import segmented_control %}'
            "{{ segmented_control(items=["
            '    {"label": "Grid", "value": "grid", "active": true},'
            '    {"label": "List", "value": "list"},'
            "]) }}"
        ).render()
        assert "chirpui-segmented" in html
        assert "chirpui-segmented__option" in html
        assert "chirpui-segmented__option--active" in html
        assert 'role="radiogroup"' in html

    def test_size(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/segmented_control.html" import segmented_control %}'
            '{{ segmented_control(items=[{"label": "A", "value": "a"}], size="sm") }}'
        ).render()
        assert "chirpui-segmented--sm" in html

    def test_css_owns_label_pressure(self) -> None:
        css = _chirpui_css()

        root_rule = css.rsplit(".chirpui-segmented {", 1)[1].split("}", 1)[0]
        assert "flex-wrap: wrap" in root_rule
        assert "max-inline-size: 100%" in root_rule
        assert "min-block-size: var(--_chirpui-segmented-block-size)" in root_rule

        option_rule = css.split(".chirpui-segmented__option {", 1)[1].split("}", 1)[0]
        assert "flex: 1 1 auto" in option_rule
        assert "white-space: normal" in option_rule
        assert "overflow-wrap: anywhere" in option_rule

        label_rule = css.split(".chirpui-segmented__label {", 1)[1].split("}", 1)[0]
        assert "min-inline-size: 0" in label_rule
        assert "overflow-wrap: anywhere" in label_rule


class TestMaturityPrimitives:
    def test_kbd_renders_single_and_chord_keys(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/kbd.html" import kbd %}'
            '{{ kbd(["Ctrl", "K"], size="sm", attrs_map={"aria-label": "Open search"}) }}'
        ).render()
        assert "<kbd" in html
        assert "chirpui-kbd--sm" in html
        assert html.count("chirpui-kbd__key") == 2
        assert 'aria-label="Open search"' in html

    def test_separator_supports_semantic_vertical_orientation(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/separator.html" import separator %}'
            '{{ separator(orientation="vertical", decorative=false, label="Section") }}'
        ).render()
        assert "chirpui-separator--vertical" in html
        assert 'role="separator"' in html
        assert 'aria-orientation="vertical"' in html
        assert "chirpui-separator__label" in html

    def test_aspect_ratio_wraps_default_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aspect_ratio.html" import aspect_ratio %}'
            '{% call aspect_ratio("4 / 3", cls="preview") %}'
            '<img src="/x.png" alt="Preview">'
            "{% end %}"
        ).render()
        assert "chirpui-aspect-ratio preview" in html
        assert "--chirpui-aspect-ratio: 4 / 3;" in html
        assert "chirpui-aspect-ratio__inner" in html
        assert '<img src="/x.png" alt="Preview">' in html

    def test_ui_label_renders_required_and_hint(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/label.html" import ui_label %}'
            '{{ ui_label("Email", for_id="email", required=true, hint="Work address") }}'
        ).render()
        assert 'for="email"' in html
        assert "chirpui-label__text" in html
        assert "chirpui-label__required" in html
        assert "Work address" in html

    def test_toggle_group_single_choice(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toggle_group.html" import toggle_group %}'
            "{{ toggle_group(items=["
            '  {"label": "Left", "value": "left"},'
            '  {"label": "Center", "value": "center"},'
            "], name='align', value='center', size='sm') }}"
        ).render()
        assert "chirpui-toggle-group--single" in html
        assert "chirpui-toggle-group--sm" in html
        assert 'role="radiogroup"' in html
        assert 'type="radio"' in html
        assert 'value="center"' in html
        assert "checked" in html

    def test_toggle_group_multiple_choice_and_disabled_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/toggle_group.html" import toggle_group %}'
            "{{ toggle_group(items=["
            '  {"label": "Bold", "value": "bold", "pressed": true},'
            '  {"label": "Italic", "value": "italic", "disabled": true},'
            "], name='format', type='multiple', orientation='vertical', variant='outline') }}"
        ).render()
        assert "chirpui-toggle-group--multiple" in html
        assert "chirpui-toggle-group--vertical" in html
        assert "chirpui-toggle-group--outline" in html
        assert 'role="group"' in html
        assert 'type="checkbox"' in html
        assert 'name="format[]"' in html
        assert "chirpui-toggle-group__item--disabled" in html

    def test_slider_renders_native_range_with_value_output(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/slider.html" import slider %}'
            '{{ slider("volume", value=25, min=0, max=50, step=5, '
            'label="Volume", show_value=true, size="lg") }}'
        ).render()
        assert "chirpui-slider--lg" in html
        assert 'type="range"' in html
        assert 'name="volume"' in html
        assert 'value="25"' in html
        assert 'min="0"' in html
        assert 'max="50"' in html
        assert "chirpui-slider__label" in html
        assert "chirpui-slider__value" in html

    def test_scroll_area_wraps_default_slot_and_orientation(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/scroll_area.html" import scroll_area %}'
            '{% call scroll_area(max_block_size="12rem", orientation="both", fade=true) %}'
            "<p>Scrollable content</p>"
            "{% end %}"
        ).render()
        assert "chirpui-scroll-area--both" in html
        assert "chirpui-scroll-area--fade" in html
        assert "--chirpui-scroll-area-max-block-size: 12rem;" in html
        assert "chirpui-scroll-area__viewport" in html
        assert "<p>Scrollable content</p>" in html

    def test_item_renders_link_row_with_meta_and_action(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/item.html" import item %}'
            '{% call item(title="Settings", description="Workspace controls", '
            'href="/settings/", meta="Updated", selected=true) %}'
            '{% slot action %}<span aria-hidden="true">Open</span>{% end %}'
            "{% end %}"
        ).render()
        assert "<a" in html
        assert 'href="/settings/"' in html
        assert 'aria-current="page"' in html
        assert "chirpui-item--selected" in html
        assert "chirpui-item__title" in html
        assert "chirpui-item__description" in html
        assert "chirpui-item__meta" in html
        assert "chirpui-item__action" in html

    def test_item_disabled_omits_link_target(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/item.html" import item %}'
            '{{ item(title="Locked", href="/locked/", disabled=true) }}'
        ).render()
        assert "<div" in html
        assert 'href="/locked/"' not in html
        assert 'aria-disabled="true"' in html
        assert "chirpui-item--disabled" in html

    def test_data_table_composes_filters_table_and_pagination(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/data_table.html" import data_table %}'
            '{% call data_table(title="Users", description="Account records", '
            'headers=["Name", "Status"], rows=[["Ada", "Active"]], '
            'filter_action="/users", current=2, total=3, '
            'url_pattern="/users?page={page}", compact=true) %}'
            '<input name="q" value="ada">'
            "{% end %}"
        ).render()
        assert "chirpui-data-table--compact" in html
        assert "chirpui-data-table__header" in html
        assert "chirpui-data-table__filters" in html
        assert 'action="/users"' in html
        assert '<input name="q" value="ada">' in html
        assert "chirpui-table" in html
        assert "<td" in html
        assert "Ada" in html
        assert "chirpui-pagination" in html
        assert "/users?page=1" in html
        assert "/users?page=3" in html

    def test_data_table_empty_state_uses_table_empty_row(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/data_table.html" import data_table %}'
            '{{ data_table(headers=["Name"], rows=[], empty_message="No users") }}'
        ).render()
        assert "chirpui-data-table__body" in html
        assert "chirpui-table__empty" in html
        assert "No users" in html


class TestTableSelectionStickyAdditive:
    """Additive selectable/sticky-first-col params on the legacy table() macro.

    The existing sortable=/sort_url= header|lower branch must stay byte-identical
    (regression lock); the new params are purely additive and default off.
    """

    def test_legacy_sortable_branch_unchanged(self, env: Environment) -> None:
        # Locks the documented-legacy <th>-as-target header|lower sort path.
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(headers=["Name", "Email"], rows=[["Ada", "a@x"]], '
            'sortable=true, sort_url="/users", hx_target="#t") }}'
        ).render()
        assert 'hx-get="/users?sort=name"' in html
        assert 'hx-get="/users?sort=email"' in html
        assert 'hx-target="#t"' in html
        assert 'hx-swap="innerHTML"' in html
        assert 'style="cursor: pointer"' in html
        # The legacy path does NOT emit aria-sort or a sort button.
        assert "aria-sort" not in html
        assert "chirpui-table__sort" not in html

    def test_default_render_has_no_selection_or_sticky_col(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(headers=["Name"], rows=[["Ada"]]) }}'
        ).render()
        assert "chirpui-table--sticky-col" not in html
        assert "chirpui-table__th--select" not in html
        assert "chirpui-table__td--select" not in html

    def test_selectable_prepends_labeled_checkbox_cells(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(headers=["Name"], rows=[["Ada"], ["Bob"]], '
            'selectable=true, select_name="ids") }}'
        ).render()
        assert "chirpui-table__th--select" in html
        assert html.count("chirpui-table__td--select") == 2
        assert_element(html, "input", {"type": "checkbox", "class": "chirpui-table__select-all"})
        assert 'aria-label="Select all rows on this page"' in html
        # Row checkboxes carry the select name + a non-empty per-row aria-label.
        assert 'name="ids"' in html
        assert 'aria-label="Select row 1"' in html

    def test_selectable_value_uses_loop_index_by_default(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(rows=[["Ada"], ["Bob"]], selectable=true) }}'
        ).render()
        assert 'value="0"' in html
        assert 'value="1"' in html

    def test_selectable_row_id_indexes_into_row(self, env: Environment) -> None:
        # row_id=1 -> second column of each row tuple is the stable id.
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(rows=[["Ada", "u-7"], ["Bob", "u-9"]], '
            "selectable=true, row_id=1) }}"
        ).render()
        assert 'value="u-7"' in html
        assert 'value="u-9"' in html

    def test_sticky_first_col_adds_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table %}'
            '{{ table(headers=["Name"], rows=[["Ada"]], sticky_first_col=true) }}'
        ).render()
        assert "chirpui-table--sticky-col" in html


class TestDataGrid:
    """Server-driven interactive data grid (#200)."""

    def _cols(self) -> str:
        return (
            "{% set cols = sort_columns(["
            "{'key':'name','label':'Name','sortable':true},"
            "{'key':'status','label':'Status','sortable':true,'align':'center'},"
            "{'key':'notes','label':'Notes','sortable':false}"
            "], parse_sort('name', default_key='name'), '/users') %}"
        )

    def _render(self, env: Environment, body: str) -> str:
        return env.from_string(
            '{% from "chirpui/data_grid.html" import data_grid %}' + self._cols() + body
        ).render()

    def test_sortable_header_emits_button_with_aria_sort(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(title='Users', columns=cols, rows=[['Ada','Active','n']], "
            "row_ids=['1'], sort_url='/users', selection_id='users') }}",
        )
        # Sortable header has a real <button class="chirpui-table__sort">.
        assert_element(html, "button", {"class": "chirpui-table__sort"})
        assert 'type="button"' in html
        # The active column reflects aria-sort="ascending".
        assert 'aria-sort="ascending"' in html
        # Stable id for focus restoration after the swap.
        assert 'id="users-sort-name"' in html

    def test_exactly_one_active_aria_sort(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g') }}",
        )
        non_none = re.findall(r'aria-sort="(ascending|descending)"', html)
        assert len(non_none) == 1
        # Every other sortable header resets to none.
        assert html.count('aria-sort="none"') >= 1

    def test_static_column_has_no_button_or_aria_sort(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g') }}",
        )
        # The non-sortable "Notes" header renders a plain <th> (no button cell).
        assert re.search(r'<th class="chirpui-table__th" scope="col">Notes</th>', html)

    def test_sort_button_carries_toggle_url_via_build_hx_attrs(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g', hx_target='#g-grid') }}",
        )
        # Active ascending "name" toggles to descending (sort=-name) on next click.
        assert "sort=-name" in html
        assert 'hx-swap="outerHTML"' in html
        assert 'hx-target="#g-grid"' in html
        # Boost-safe: the sort selects its OWN grid region from the response and
        # disinherits the shell's hx-select="#page-content". Without this, inside a
        # boosted app_shell the sort outerHTML-swaps the whole page into the grid,
        # nesting page chrome on every click (#200 regression).
        assert 'hx-select="#g-grid"' in html
        assert 'hx-disinherit="hx-select"' in html

    def test_grid_section_is_a_select_island(self, env: Environment) -> None:
        # The grid owns its own swaps (sort replaces the section; load-more appends
        # bare <tr> rows), so the <section> root disinherits hx-select. This keeps a
        # load-more append into the tbody from inheriting the boosted #main's
        # hx-select="#page-content" (which the <tr> fragment cannot satisfy).
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g') }}",
        )
        section = re.search(r"<section[^>]*\bclass=\"chirpui-data-grid[^>]*>", html)
        assert section is not None
        assert 'hx-disinherit="hx-select"' in section.group(0)

    def test_selectable_emits_select_all_and_indeterminate_binding(self, env: Environment) -> None:
        html = self._render(
            env,
            "{% set sel = selection_state(['1'], page_ids=['1','2'], total=2) %}"
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n'],['Bob','Idle','m']], "
            "row_ids=['1','2'], sort_url='/users', selection_id='g', "
            "selectable=true, selection=sel) }}",
        )
        assert "chirpui-table__select-all" in html
        assert 'aria-label="Select all rows on this page"' in html
        # indeterminate MUST be set via the JS DOM property (x-effect), never as
        # an HTML attribute (which would not reflect to the IDL-only property).
        assert 'x-effect="$el.indeterminate = someSelected"' in html
        assert "indeterminate=" not in html
        assert ":checked=" in html
        # Each row checkbox is labeled and carries its stable id as value.
        assert html.count("chirpui-table__select-row") == 2
        assert 'value="1"' in html
        assert 'value="2"' in html
        # No row_labels supplied -> the label falls back to the STABLE id, never
        # the rendered first cell (which may be markup/empty). See the dedicated
        # row_labels tests below.
        assert 'aria-label="Select 1"' in html
        # Server seeds the selected row checked (JS-off correctness).
        assert "checked" in html

    def test_row_labels_supply_clean_accessible_names(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n'],['Bob','Idle','m']], "
            "row_ids=['1','2'], row_labels=['Ada Lovelace','Bob Jones'], "
            "sort_url='/users', selection_id='g', selectable=true) }}",
        )
        assert 'aria-label="Select Ada Lovelace"' in html
        assert 'aria-label="Select Bob Jones"' in html

    def test_row_checkbox_label_does_not_leak_first_cell_markup(self, env: Environment) -> None:
        # The first column is rich HTML (avatar + bold name). Without row_labels
        # the label must fall back to the stable id, never the escaped markup —
        # a screen reader would otherwise announce "less-than b greater-than".
        html = self._render(
            env,
            "{{ data_grid(columns=cols, "
            "rows=[['<b>Ada</b> Lovelace','Active','n']], "
            "row_ids=['u-1'], sort_url='/users', selection_id='g', "
            "selectable=true) }}",
        )
        assert 'aria-label="Select u-1"' in html
        assert 'aria-label="Select &lt;b&gt;' not in html
        assert 'aria-label="Select <b>' not in html

    def test_row_checkbox_label_falls_back_when_first_cell_empty(self, env: Environment) -> None:
        # An empty/spacer first cell must not degrade the label to a bare
        # "Select " — it falls back to the stable, distinguishing row id.
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['','Active','n'],['','Idle','m']], "
            "row_ids=['u-1','u-2'], sort_url='/users', selection_id='g', "
            "selectable=true) }}",
        )
        assert 'aria-label="Select u-1"' in html
        assert 'aria-label="Select u-2"' in html
        assert 'aria-label="Select "' not in html

    def test_selection_bar_controlled_mode_dropped_count_gate(self, env: Environment) -> None:
        html = self._render(
            env,
            "{% set sel = selection_state([], page_ids=['1'], total=1) %}"
            "{% call data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g', selectable=true, selection=sel) %}"
            "<button id='bulk-export'>Export</button>{% end %}",
        )
        # Controlled bar is in the DOM even with zero selected (x-show gate).
        assert "chirpui-selection-bar" in html
        assert 'x-show="count &gt; 0"' in html or 'x-show="count > 0"' in html
        assert "x-text=" in html
        assert 'aria-live="polite"' in html
        # Bulk-action slot content forwards into the bar.
        assert "bulk-export" in html

    def test_sticky_first_col_and_header(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g', sticky_first_col=true, "
            "sticky_header=true) }}",
        )
        assert "chirpui-table--sticky-col" in html
        assert "chirpui-table-wrap--sticky" in html

    def test_load_more_emits_real_button_sentinel(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='g', load_more_url='/users', "
            "has_more=true) }}",
        )
        assert "chirpui-data-grid__load-more" in html
        # Real <button> (not a span/disabled) carrying the load-more class.
        assert_element(html, "button")
        assert "chirpui-data-grid__load-more-btn" in html
        assert 'hx-get="/users"' in html
        assert 'hx-swap="beforeend"' in html
        assert 'hx-target="#g-grid-body"' in html

    def test_root_carries_alpine_factory_and_config(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[['Ada','Active','n']], row_ids=['1'], "
            "sort_url='/users', selection_id='users', selectable=true, "
            "total=5) }}",
        )
        assert 'x-data="chirpuiGridSelection()"' in html
        assert 'data-selection-id="users"' in html
        assert "data-total-rows=" in html

    def test_empty_rows_renders_empty_message(self, env: Environment) -> None:
        html = self._render(
            env,
            "{{ data_grid(columns=cols, rows=[], sort_url='/users', "
            "selection_id='g', empty_message='No records yet') }}",
        )
        assert "No records yet" in html
        assert "chirpui-table__empty" in html

    def test_data_grid_rows_fragment_renders_tr_only(self, env: Environment) -> None:
        # The load-more/OOB fragment renders bare <tr> rows for hx beforeend.
        html = env.from_string(
            '{% from "chirpui/data_grid.html" import data_grid_rows %}'
            + self._cols()
            + "{{ data_grid_rows(cols, [['Ada','Active','n'],['Bob','Idle','m']], "
            "row_ids=['1','2'], selectable=true, select_name='ids') }}"
        ).render()
        # Two <tr> rows, no wrapping section/thead (pure load-more fragment).
        assert html.count("<tr ") == 2
        assert "<section" not in html
        assert "<thead" not in html
        assert html.count("chirpui-table__select-row") == 2


class TestSplitPanel:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_panel.html" import split_panel %}'
            "{% call split_panel() %}"
            "{% slot left %}Left{% end %}"
            "{% slot right %}Right{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-split-panel" in html
        assert "chirpui-split-panel__handle" in html
        assert "chirpui-split-panel__pane" in html
        assert 'role="separator"' in html

    def test_vertical(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/split_panel.html" import split_panel %}'
            '{% call split_panel(direction="vertical") %}'
            "{% slot left %}Top{% end %}"
            "{% slot right %}Bottom{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-split-panel--vertical" in html


class TestTooltipEnhanced:
    def test_bubble_present(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tooltip.html" import tooltip %}'
            '{% call tooltip("Help text") %}<button>Hover</button>{% end %}'
        ).render()
        assert "chirpui-tooltip__bubble" in html
        assert 'role="tooltip"' in html
        assert "Help text" in html

    def test_position(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tooltip.html" import tooltip %}'
            '{% call tooltip("Below", position="bottom") %}<span>X</span>{% end %}'
        ).render()
        assert "chirpui-tooltip--bottom" in html


class TestTimelineEnhanced:
    def test_icon_timeline(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Deploy", "Now", icon="◎", variant="success") }}'
        ).render()
        assert "chirpui-timeline__icon" in html
        assert "chirpui-timeline__item--success" in html

    def test_avatar_timeline(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Comment", "12:05", avatar="/img/user.jpg") }}'
        ).render()
        assert "chirpui-timeline__avatar" in html
        assert 'src="/img/user.jpg"' in html

    def test_hoverable(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline %}'
            "{% call timeline(hoverable=true) %}items{% end %}"
        ).render()
        assert "chirpui-timeline--hoverable" in html

    def test_link_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Click", "Jan 1", href="/detail") }}'
        ).render()
        assert "chirpui-timeline__link-overlay" in html
        assert 'href="/detail"' in html

    def test_title_link_item(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Click", "Jan 1", href="/detail", link_mode="title") }}'
        ).render()
        assert "chirpui-timeline__title-link" in html
        assert "chirpui-timeline__link-overlay" not in html
        assert 'href="/detail"' in html

    def test_title_link_item_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/detail"})),
        )
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Click", "Jan 1", href="/detail", link_mode="title") }}'
        ).render()
        assert "chirpui-timeline__title-link" in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_hint_item_wraps_title_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Click", "Jan 1", href="/detail", link_mode="title", hint="More context") }}'
        ).render()
        assert "chirpui-timeline__hint" in html
        assert 'data-tooltip="More context"' in html
        assert "chirpui-timeline__title-link" in html
        assert "chirpui-timeline__link-overlay" not in html

    def test_link_item_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/detail"})),
        )
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Click", "Jan 1", href="/detail") }}'
        ).render()
        assert "chirpui-timeline__link-overlay" in html
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_time_column(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/timeline.html" import timeline_item %}'
            '{{ timeline_item("Event", "Jan 1", time="12:05PM") }}'
        ).render()
        assert "chirpui-timeline__time" in html
        assert "12:05PM" in html


class TestToggleEnhanced:
    def test_size_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import toggle_field %}'
            '{{ toggle_field("dark_mode", size="sm") }}'
        ).render()
        assert "chirpui-toggle-wrap--sm" in html

    def test_color_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import toggle_field %}'
            '{{ toggle_field("active", variant="success") }}'
        ).render()
        assert "chirpui-toggle-wrap--success" in html

    def test_label_inside(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import toggle_field %}'
            '{{ toggle_field("power", label_inside=true) }}'
        ).render()
        assert "chirpui-toggle__track-label--on" in html
        assert "chirpui-toggle__track-label--off" in html


class TestMetricCardEnhanced:
    def test_trend_direction(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value="1,250", label="Users", trend="+12%", trend_direction="up") }}'
        ).render()
        assert "chirpui-metric-card__trend--up" in html
        assert "↑" in html

    def test_icon_badge(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value="$48M", label="Revenue", icon="chart", icon_bg="success") }}'
        ).render()
        assert "chirpui-metric-card__icon-badge" in html
        assert "chirpui-metric-card__icon-badge--success" in html

    def test_footer_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value="72", label="Tasks", footer_label="View reports", footer_href="/reports") }}'
        ).render()
        assert "chirpui-metric-card__footer" in html
        assert 'href="/reports"' in html

    def test_footer_link_uses_route_link_attrs_when_available(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/reports"})),
        )
        html = env.from_string(
            '{% from "chirpui/metric_grid.html" import metric_card %}'
            '{{ metric_card(value="72", label="Tasks", footer_label="View reports", footer_href="/reports") }}'
        ).render()
        assert "chirpui-metric-card__footer" in html
        assert 'hx-target="#site-content"' in html


# ==========================================================================
# Playful / decorative effects
# ==========================================================================


def _position_pairs(html: str) -> list[tuple[int, int]]:
    return [(int(x), int(y)) for x, y in re.findall(r"left: (\d+)%; (?:top|bottom): (\d+)%", html)]


def _assert_scattered_effect_positions(html: str) -> None:
    points = sorted(_position_pairs(html))
    assert len(points) >= 6
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    assert max(xs) - min(xs) >= 40
    assert max(ys) - min(ys) >= 40
    assert not all(left <= right for left, right in pairwise(ys))
    assert not all(left >= right for left, right in pairwise(ys))


def _chirpui_css() -> str:
    return (
        Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates" / "chirpui.css"
    ).read_text(encoding="utf-8")


class TestTypewriter:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/typewriter.html" import typewriter %}{{ typewriter("Hello World") }}'
        ).render()
        assert "chirpui-typewriter" in html
        assert "chirpui-typewriter__text" in html
        assert "Hello World" in html
        assert "--chirpui-typewriter-steps: 11" in html

    def test_speed_fast(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/typewriter.html" import typewriter %}'
            '{{ typewriter("Fast", speed="fast") }}'
        ).render()
        assert "chirpui-typewriter--fast" in html

    def test_no_cursor(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/typewriter.html" import typewriter %}'
            '{{ typewriter("No cursor", cursor=false) }}'
        ).render()
        assert "chirpui-typewriter--no-cursor" in html

    def test_delay(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/typewriter.html" import typewriter %}'
            '{{ typewriter("Delayed", delay="2") }}'
        ).render()
        assert "chirpui-typewriter--delay-2" in html

    def test_custom_tag(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/typewriter.html" import typewriter %}'
            '{{ typewriter("Title", tag="h1") }}'
        ).render()
        assert "<h1" in html
        assert "</h1>" in html


class TestGlitchText:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/glitch_text.html" import glitch_text %}{{ glitch_text("ERROR") }}'
        ).render()
        assert "chirpui-glitch" in html
        assert 'data-text="ERROR"' in html
        assert "ERROR" in html

    def test_intense(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/glitch_text.html" import glitch_text %}'
            '{{ glitch_text("GLITCH", variant="intense") }}'
        ).render()
        assert "chirpui-glitch--intense" in html

    def test_subtle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/glitch_text.html" import glitch_text %}'
            '{{ glitch_text("SOFT", variant="subtle") }}'
        ).render()
        assert "chirpui-glitch--subtle" in html

    def test_custom_tag(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/glitch_text.html" import glitch_text %}'
            '{{ glitch_text("BIG", tag="h1") }}'
        ).render()
        assert "<h1" in html


class TestNeonText:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/neon_text.html" import neon_text %}{{ neon_text("OPEN") }}'
        ).render()
        assert "chirpui-neon" in html
        assert "chirpui-neon--cyan" in html
        assert "OPEN" in html

    def test_color_magenta(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/neon_text.html" import neon_text %}'
            '{{ neon_text("LIVE", color="magenta") }}'
        ).render()
        assert "chirpui-neon--magenta" in html

    def test_flicker_animation(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/neon_text.html" import neon_text %}'
            '{{ neon_text("SIGN", animation="flicker") }}'
        ).render()
        assert "chirpui-neon--flicker" in html

    def test_pulse_animation(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/neon_text.html" import neon_text %}'
            '{{ neon_text("GLOW", animation="pulse") }}'
        ).render()
        assert "chirpui-neon--pulse" in html


class TestAurora:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aurora.html" import aurora %}{% call aurora() %}Content{% end %}'
        ).render()
        assert "chirpui-aurora" in html
        assert "chirpui-aurora__blobs" in html
        assert "chirpui-aurora__blob" in html
        assert "chirpui-aurora__content" in html
        assert "Content" in html
        assert html.count("chirpui-aurora__blob") >= 3

    def test_intense(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aurora.html" import aurora %}'
            '{% call aurora(variant="intense") %}X{% end %}'
        ).render()
        assert "chirpui-aurora--intense" in html

    def test_subtle(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/aurora.html" import aurora %}'
            '{% call aurora(variant="subtle") %}X{% end %}'
        ).render()
        assert "chirpui-aurora--subtle" in html


class TestDecorativeScatter:
    def test_particle_background_positions_are_not_formulaic_diagonal(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/particle_bg.html" import particle_bg %}'
            "{% call particle_bg(count=12) %}Particles{% end %}"
        ).render()
        _assert_scattered_effect_positions(html)

    def test_holy_light_positions_are_not_formulaic_diagonal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/holy_light.html" import holy_light %}'
            "{% call holy_light() %}Glow{% end %}"
        ).render()
        _assert_scattered_effect_positions(html)

    def test_rune_field_positions_are_not_formulaic_diagonal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/rune_field.html" import rune_field %}'
            "{% call rune_field() %}Runes{% end %}"
        ).render()
        _assert_scattered_effect_positions(html)

    def test_constellation_positions_are_not_formulaic_diagonal(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/constellation.html" import constellation %}'
            "{% call constellation() %}Stars{% end %}"
        ).render()
        _assert_scattered_effect_positions(html)


class TestScanline:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/scanline.html" import scanline %}'
            "{% call scanline() %}Terminal{% end %}"
        ).render()
        assert "chirpui-scanline" in html
        assert "Terminal" in html

    def test_crt(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/scanline.html" import scanline %}'
            '{% call scanline(variant="crt") %}CRT{% end %}'
        ).render()
        assert "chirpui-scanline--crt" in html

    def test_heavy(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/scanline.html" import scanline %}'
            '{% call scanline(variant="heavy") %}Bold{% end %}'
        ).render()
        assert "chirpui-scanline--heavy" in html

    def test_css_uses_visible_overlay_layers(self) -> None:
        css = _chirpui_css()
        assert ".chirpui-scanline::before" in css
        assert "radial-gradient(circle at 50% 48%" in css
        assert "rgba(255, 255, 255, 0.07)" in css


class TestGrain:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/grain.html" import grain %}{% call grain() %}Photo{% end %}'
        ).render()
        assert "chirpui-grain" in html
        assert "Photo" in html

    def test_heavy(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/grain.html" import grain %}'
            '{% call grain(variant="heavy") %}X{% end %}'
        ).render()
        assert "chirpui-grain--heavy" in html

    def test_animated(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/grain.html" import grain %}{% call grain(animated=true) %}X{% end %}'
        ).render()
        assert "chirpui-grain--animated" in html

    def test_attrs_on_root(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/grain.html" import grain %}'
            "{% call grain(attrs='data-testid=\"gr\"') %}P{% end %}"
        ).render()
        assert 'data-testid="gr"' in html

    def test_css_uses_visible_noise_layers(self) -> None:
        css = _chirpui_css()
        grain_rule = css.split(".chirpui-grain::after", 1)[1].split(".chirpui-grain--", 1)[0]
        assert "feTurbulence" in grain_rule
        assert "radial-gradient" not in grain_rule
        assert "background-size: 97px 89px, 173px 149px" in grain_rule
        assert "opacity: 0.2" in css
        assert "@keyframes chirpui-grain-shift" in css


class TestOrbit:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/orbit.html" import orbit %}'
            '{% call orbit(items=["A", "B", "C"]) %}Center{% end %}'
        ).render()
        assert "chirpui-orbit" in html
        assert "chirpui-orbit__ring" in html
        assert "chirpui-orbit__center" in html
        assert "chirpui-orbit__item" in html
        assert "Center" in html
        assert html.count("chirpui-orbit__item") == 3

    def test_size_lg(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/orbit.html" import orbit %}'
            '{% call orbit(items=["X"], size="lg") %}O{% end %}'
        ).render()
        assert "chirpui-orbit--lg" in html

    def test_speed_fast(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/orbit.html" import orbit %}'
            '{% call orbit(items=["X"], speed="fast") %}O{% end %}'
        ).render()
        assert "chirpui-orbit--fast" in html

    def test_reverse(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/orbit.html" import orbit %}'
            '{% call orbit(items=["X"], reverse=true) %}O{% end %}'
        ).render()
        assert "chirpui-orbit--reverse" in html


class TestSparkle:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sparkle.html" import sparkle %}{% call sparkle() %}Magic{% end %}'
        ).render()
        assert "chirpui-sparkle" in html
        assert "chirpui-sparkle__star" in html
        assert "Magic" in html
        assert html.count("chirpui-sparkle__star") == 6

    def test_gold(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sparkle.html" import sparkle %}'
            '{% call sparkle(variant="gold") %}X{% end %}'
        ).render()
        assert "chirpui-sparkle--gold" in html

    def test_rainbow(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sparkle.html" import sparkle %}'
            '{% call sparkle(variant="rainbow") %}X{% end %}'
        ).render()
        assert "chirpui-sparkle--rainbow" in html

    def test_custom_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sparkle.html" import sparkle %}{% call sparkle(count=3) %}X{% end %}'
        ).render()
        assert html.count("chirpui-sparkle__star") == 3


class TestConfetti:
    def test_basic(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confetti.html" import confetti %}{{ confetti() }}'
        ).render()
        assert "chirpui-confetti" in html
        assert "chirpui-confetti__piece" in html
        assert "x-data" in html
        assert 'data-confetti-event="confetti"' in html
        assert "@confetti.window" not in html

    def test_trigger_button(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confetti.html" import confetti_trigger %}'
            '{{ confetti_trigger("Party!") }}'
        ).render()
        assert "Party!" in html
        assert "$dispatch" in html
        assert 'data-confetti-event="confetti"' in html

    def test_confetti_event_stays_out_of_alpine_literals(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confetti.html" import confetti, confetti_trigger %}'
            '{{ confetti(event="bad\\\'];alert(1)//") }}'
            '{{ confetti_trigger("Party!", event="bad\\\'];alert(1)//") }}'
        ).render()
        assert "$dispatch('bad" not in html
        assert "@bad" not in html
        assert "$el.dataset.confettiEvent" in html

    def test_custom_count(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/confetti.html" import confetti %}{{ confetti(count=10) }}'
        ).render()
        assert html.count("chirpui-confetti__piece") >= 10


class TestWobble:
    def test_wobble_load(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wobble.html" import wobble %}{% call wobble() %}Content{% end %}'
        ).render()
        assert "chirpui-wobble" in html
        assert "Content" in html

    def test_wobble_hover(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wobble.html" import wobble %}'
            '{% call wobble(trigger="hover") %}Content{% end %}'
        ).render()
        assert "chirpui-hover-wobble" in html

    def test_jello(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wobble.html" import jello %}{% call jello() %}Jello{% end %}'
        ).render()
        assert "chirpui-jello" in html

    def test_rubber_band(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wobble.html" import rubber_band %}'
            '{% call rubber_band(trigger="hover") %}Stretch{% end %}'
        ).render()
        assert "chirpui-hover-rubber" in html

    def test_bounce_in(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/wobble.html" import bounce_in %}{% call bounce_in() %}Pop{% end %}'
        ).render()
        assert "chirpui-bounce-in" in html

    def test_css_makes_motion_wrappers_transformable(self) -> None:
        css = _chirpui_css()
        motion_rule = css.split(".chirpui-wobble,", 1)[1].split(".chirpui-wobble {", 1)[0]
        assert "display: inline-block" in motion_rule
        assert "transform-origin: center" in motion_rule
        assert ".chirpui-bounce-in { animation: chirpui-bounce-in 0.6s ease-out both; }" in css


# ---------------------------------------------------------------------------
# Pre-hydration safety — overlays must be inert before Alpine initializes
# ---------------------------------------------------------------------------


class TestPreHydrationSafety:
    """Overlay components must render with a safe static class so they don't
    block clicks or flash content before Alpine.js hydrates."""

    def test_tray_has_static_closed_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tray.html" import tray %}{% call tray("t", "T") %}body{% end %}'
        ).render()
        assert 'class="chirpui-tray chirpui-tray--right chirpui-tray--closed"' in html

    def test_modal_overlay_has_static_closed_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal_overlay.html" import modal_overlay %}'
            '{% call modal_overlay("m", "M") %}body{% end %}'
        ).render()
        assert 'class="chirpui-modal chirpui-modal--closed"' in html

    def test_dropdown_select_menu_has_x_cloak(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_select %}'
            '{{ dropdown_select("Pick", items=[{"label": "A", "value": "a"}, {"label": "B", "value": "b"}]) }}'
        ).render()
        assert "x-cloak" in html
        assert 'x-data="chirpuiDropdownSelect()"' in html
        assert 'aria-label="Pick"' in html
        assert 'data-value="b"' in html

    def test_dropdown_split_menu_has_x_cloak(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_split %}'
            '{{ dropdown_split("Go", primary_href="/go", items=[{"label": "X", "href": "/x"}]) }}'
        ).render()
        assert "x-cloak" in html
        assert 'x-data="chirpuiDropdown()"' in html

    def test_dropdown_split_links_use_route_link_attrs_when_available(
        self, env: Environment
    ) -> None:
        env.add_global(
            "route_link_attrs",
            _stub_route_link_attrs("site-content", hrefs=frozenset({"/go", "/x"})),
        )
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_split %}'
            '{{ dropdown_split("Go", primary_href="/go", items=[{"label": "X", "href": "/x"}]) }}'
        ).render()
        assert html.count('hx-target="#site-content"') == 2
        assert html.count('hx-boost="true"') == 2

    def test_dropdown_split_payload_uses_data_attributes_not_inline_js_literals(
        self, env: Environment
    ) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown_menu.html" import dropdown_split %}'
            "{{ dropdown_split('Go', primary_href='/go', items=["
            '{"label": "Quote \\\' <script>", "action": "archive\\\' } ); alert(1);//"}'
            "]) }}"
        ).render()
        click_handlers = re.findall(r'@click="([^"]*)"', html)
        assert "selectItem($el, $refs.trigger)" in click_handlers
        assert "chirpui:dropdown-selected" not in html
        assert "&lt;script&gt;" in html
        assert "<script>" not in html
        assert 'data-action="archive&#39; } ); alert(1);//"' in html

    def test_copy_button_copied_span_has_x_cloak(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/copy_button.html" import copy_button %}'
            '{{ copy_button("hello", label="Copy") }}'
        ).render()
        assert "x-cloak" in html
        # "Copied!" should not flash before Alpine
        assert 'x-show="copied" x-cloak' in html
        assert 'x-data="chirpuiCopy()"' in html

    def test_code_block_copy_copied_span_has_x_cloak(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/code.html" import code_block %}'
            '{{ code_block("print(1)", copy=true) }}'
        ).render()
        assert 'x-show="copied" x-cloak' in html
        assert 'x-data="chirpuiCopy()"' in html

    def test_streaming_copy_btn_copied_span_has_x_cloak(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/streaming.html" import copy_btn %}'
            '{{ copy_btn(label="Copy", copy_text="hi") }}'
        ).render()
        assert 'x-show="copied" x-cloak' in html


# ---------------------------------------------------------------------------
# HTMX correctness — boost, hx-select, hx-boost="false"
# ---------------------------------------------------------------------------


class TestHtmxCorrectness:
    """Components that emit HTMX attributes must follow the conventions:
    - Boosted links targeting #main must include hx-select="#page-content"
    - Links with their own hx-target must emit hx-boost="false"
    - Fragment swaps should use hx-select="unset"
    """

    def test_nav_link_includes_hx_select(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_link.html" import nav_link %}{{ nav_link("/page", "Next") }}'
        ).render()
        assert 'class="chirpui-nav-link"' in html
        assert 'hx-target="#main"' in html
        assert 'hx-select="#page-content"' in html
        assert 'hx-sync="#main:replace"' in html

    def test_nav_link_with_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_link.html" import nav_link %}'
            '{% call nav_link("/details") %}View{% end %}'
        ).render()
        assert "chirpui-nav-link" in html
        assert 'hx-select="#page-content"' in html
        assert "View" in html

    def test_nav_link_preserves_custom_class(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/nav_link.html" import nav_link %}'
            '{{ nav_link("/page", "Next", cls="extra-link") }}'
        ).render()
        assert 'class="chirpui-nav-link extra-link"' in html

    def test_inline_edit_cancel_has_boost_false(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/inline_edit_field.html" import inline_edit_field_form %}'
            '{{ inline_edit_field_form(name="n", value="v", save_url="/save", cancel_url="/cancel") }}'
        ).render()
        assert 'hx-boost="false"' in html

    def test_inline_edit_cancel_has_select_unset(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/inline_edit_field.html" import inline_edit_field_form %}'
            '{{ inline_edit_field_form(name="n", value="v", save_url="/save", cancel_url="/cancel") }}'
        ).render()
        assert 'hx-select="unset"' in html


# =============================================================================
# Marketing Kit (site mode)
# =============================================================================


class TestSiteShell:
    def test_default_render(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_shell.html" import site_shell %}'
            "{% call site_shell() %}Page content{% end %}"
        ).render()
        assert "chirpui-site-shell" in html
        assert "chirpui-site-shell__main" in html
        assert "Page content" in html

    def test_ambient_mode(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_shell.html" import site_shell %}'
            "{% call site_shell(ambient=true) %}Content{% end %}"
        ).render()
        assert "chirpui-ambient-root" in html
        assert "chirpui-ambient" in html

    def test_header_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_shell.html" import site_shell %}'
            "{% call site_shell() %}"
            "{% slot header %}<header>TOP</header>{% end %}"
            "Body{% end %}"
        ).render()
        assert "<header>TOP</header>" in html
        assert "Body" in html

    def test_footer_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_shell.html" import site_shell %}'
            "{% call site_shell() %}"
            "Body"
            "{% slot footer %}<footer>BOTTOM</footer>{% end %}"
            "{% end %}"
        ).render()
        assert "<footer>BOTTOM</footer>" in html

    def test_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_shell.html" import site_shell %}'
            '{% call site_shell(cls="my-site") %}Content{% end %}'
        ).render()
        assert "my-site" in html


class TestSiteHeader:
    def test_default_glass_sticky(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            "{% call site_header() %}"
            "{% slot brand %}Logo{% end %}"
            "{% slot nav %}Links{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header" in html
        assert "chirpui-site-header--sticky" in html
        assert "chirpui-site-header--glass" in html
        assert "chirpui-site-header__inner" in html
        assert "chirpui-site-header__brand" in html
        assert "Logo" in html
        assert "Links" in html

    def test_solid_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            '{% call site_header(variant="solid") %}'
            "{% slot brand %}Logo{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header--glass" not in html
        assert "chirpui-site-header--solid" not in html

    def test_transparent_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            '{% call site_header(variant="transparent") %}'
            "{% slot brand %}Logo{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header--transparent" in html

    def test_center_brand_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            '{% call site_header(layout="center-brand") %}'
            "{% slot nav %}Left{% end %}"
            "{% slot brand %}LOGO{% end %}"
            "{% slot nav_end %}Right{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header__inner--center-brand" in html
        assert "chirpui-site-header__nav-end" in html
        assert "LOGO" in html

    def test_center_nav_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            '{% call site_header(layout="center-nav") %}'
            "{% slot brand %}Logo{% end %}"
            "{% slot nav %}Centered links{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header__inner--center-nav" in html

    def test_not_sticky(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            "{% call site_header(sticky=false) %}"
            "{% slot brand %}Logo{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header--sticky" not in html

    def test_tools_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            "{% call site_header() %}"
            "{% slot brand %}Logo{% end %}"
            "{% slot tools %}<button>Theme</button>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-header__tools" in html
        assert "<button>Theme</button>" in html


class TestSiteNavLink:
    def test_site_header_brand_uses_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/"}))
        )
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_header %}'
            '{% call site_header(brand_url="/") %}'
            "{% slot brand %}Logo{% end %}"
            "{% end %}"
        ).render()
        assert 'class="chirpui-site-header__brand"' in html
        assert 'hx-target="#site-content"' in html

    def test_basic_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_nav_link %}'
            '{{ site_nav_link("/docs", "Docs") }}'
        ).render()
        assert "chirpui-site-nav__link" in html
        assert 'href="/docs"' in html
        assert "Docs" in html

    def test_basic_link_uses_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/docs"}))
        )
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_nav_link %}'
            '{{ site_nav_link("/docs", "Docs") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_glyph_prefix(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_nav_link %}'
            '{{ site_nav_link("/home", "Home", glyph="~") }}'
        ).render()
        assert "chirpui-site-nav__glyph" in html
        assert "~" in html

    def test_external_link(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_nav_link %}'
            '{{ site_nav_link("https://github.com", "GitHub", external=true) }}'
        ).render()
        assert "chirpui-site-nav__link--external" in html
        assert "noopener" in html

    def test_active_explicit(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_header.html" import site_nav_link %}'
            '{{ site_nav_link("/about", "About", active=true) }}'
        ).render()
        assert "chirpui-site-nav__link--active" in html
        assert 'aria-current="page"' in html


class TestSiteFooter:
    def test_default_columns_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import site_footer, footer_column, footer_link %}'
            "{% call site_footer() %}"
            '{% slot brand %}<a href="/">Logo</a>{% end %}'
            '{% call footer_column(title="Product") %}'
            '{{ footer_link("/docs", "Docs") }}'
            "{% end %}"
            "{% slot colophon %}© 2026{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-footer" in html
        assert "chirpui-site-footer__grid" in html
        assert "chirpui-site-footer__brand" in html
        assert "chirpui-site-footer__column" in html
        assert "chirpui-site-footer__column-title" in html
        assert "Product" in html
        assert "chirpui-site-footer__link" in html
        assert "Docs" in html
        assert "chirpui-site-footer__colophon" in html
        assert "© 2026" in html

    def test_centered_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import site_footer %}'
            '{% call site_footer(layout="centered") %}'
            "{% slot brand %}Brand{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-footer--centered" in html

    def test_simple_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import site_footer %}'
            '{% call site_footer(layout="simple") %}'
            "{% slot brand %}Brand{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-footer--simple" in html

    def test_footer_link_external(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import footer_link %}'
            '{{ footer_link("https://github.com", "GitHub", external=true) }}'
        ).render()
        assert "chirpui-site-footer__link--external" in html
        assert "noopener" in html

    def test_footer_link_uses_route_link_attrs(self, env: Environment) -> None:
        env.add_global(
            "route_link_attrs", _stub_route_link_attrs("site-content", hrefs=frozenset({"/docs"}))
        )
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import footer_link %}'
            '{{ footer_link("/docs", "Docs") }}'
        ).render()
        assert 'hx-target="#site-content"' in html
        assert 'hx-boost="true"' in html

    def test_footer_link_glyph(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import footer_link %}'
            '{{ footer_link("/docs", "Docs", glyph="#") }}'
        ).render()
        assert "chirpui-site-footer__link-glyph" in html
        assert "#" in html

    def test_rule_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/site_footer.html" import site_footer %}'
            "{% call site_footer() %}"
            "{% slot brand %}Brand{% end %}"
            "{% slot rule %}<span>•</span>{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-site-footer__rule" in html
        assert "•" in html


class TestBand:
    def test_default_inset(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}{% call band() %}Band content{% end %}'
        ).render()
        assert "chirpui-band" in html
        assert "chirpui-band--inset" in html
        assert "Band content" in html

    def test_bleed_width(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            '{% call band(width="bleed") %}Content{% end %}'
        ).render()
        assert "chirpui-band--bleed" in html

    def test_contained_width(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            '{% call band(width="contained") %}Content{% end %}'
        ).render()
        assert "chirpui-band--contained" in html

    def test_elevated_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            '{% call band(variant="elevated") %}Content{% end %}'
        ).render()
        assert "chirpui-band--elevated" in html

    def test_accent_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            '{% call band(variant="accent") %}Content{% end %}'
        ).render()
        assert "chirpui-band--accent" in html

    def test_glass_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            '{% call band(variant="glass") %}Content{% end %}'
        ).render()
        assert "chirpui-band--glass" in html

    def test_pattern_integration(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            '{% call band(pattern="grid") %}Content{% end %}'
        ).render()
        assert "chirpui-band--pattern-grid" in html

    def test_header_slot(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/band.html" import band %}'
            "{% call band() %}"
            "{% slot header %}<h2>Featured</h2>{% end %}"
            "Content"
            "{% end %}"
        ).render()
        assert "<h2>Featured</h2>" in html
        assert "Content" in html


class TestFeatureSection:
    def test_default_split(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            "{% call feature_section() %}"
            "{% slot title %}Fast builds{% end %}"
            "<p>Description.</p>"
            '{% slot media %}<img src="/shot.png">{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-feature-section" in html
        assert "chirpui-feature-section--split" in html
        assert "chirpui-feature-section__copy" in html
        assert "chirpui-feature-section__title" in html
        assert "Fast builds" in html
        assert "chirpui-feature-section__media" in html

    def test_reverse_modifier(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            "{% call feature_section(reverse=true) %}"
            "{% slot title %}Title{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-feature-section--reverse" in html

    def test_balanced_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            '{% call feature_section(layout="balanced") %}'
            "{% slot title %}Title{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-feature-section--balanced" in html

    def test_stacked_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            '{% call feature_section(layout="stacked") %}'
            "{% slot title %}Title{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-feature-section--stacked" in html

    def test_media_dominant_layout(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            '{% call feature_section(layout="media-dominant") %}'
            "{% slot title %}Title{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-feature-section--media-dominant" in html

    def test_halo_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            '{% call feature_section(variant="halo") %}'
            "{% slot title %}Title{% end %}"
            '{% slot media %}<img src="/x.png">{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-feature-section__halo" in html

    def test_muted_variant(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            '{% call feature_section(variant="muted") %}'
            "{% slot title %}Title{% end %}"
            "{% end %}"
        ).render()
        assert "chirpui-feature-section--muted" in html

    def test_eyebrow_and_actions(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_section %}'
            "{% call feature_section() %}"
            "{% slot eyebrow %}New{% end %}"
            "{% slot title %}Title{% end %}"
            '{% slot actions %}<a href="/">CTA</a>{% end %}'
            "{% end %}"
        ).render()
        assert "chirpui-feature-section__eyebrow" in html
        assert "New" in html
        assert "chirpui-feature-section__actions" in html
        assert "CTA" in html


class TestFeatureStack:
    def test_default_render(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_stack %}'
            "{% call feature_stack() %}Inner content{% end %}"
        ).render()
        assert "chirpui-feature-stack" in html
        assert "Inner content" in html

    def test_custom_cls(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/feature_section.html" import feature_stack %}'
            '{% call feature_stack(cls="extra") %}Content{% end %}'
        ).render()
        assert "extra" in html


# ---------------------------------------------------------------------------
# Structural assertions (Sprint 18) — verify HTML structure, not just classes
# ---------------------------------------------------------------------------


class TestStructuralBtn:
    """Button must render correct element type with key attributes."""

    def test_btn_renders_button_element_with_type(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Save") }}'
        ).render()
        assert_element(html, "button", {"type": "button"}, contains="Save")

    def test_btn_link_renders_anchor(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Go", href="/x") }}'
        ).render()
        assert_element(html, "a", {"href": "/x"}, contains="Go")
        assert "<button" not in html

    def test_btn_loading_has_aria_busy(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/button.html" import btn %}{{ btn("Wait", loading=true) }}'
        ).render()
        assert_element(html, "button", {"aria-busy": "true"})


class TestStructuralCard:
    """Card must use correct wrapper elements and structural children."""

    def test_card_has_body_div(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}{% call card() %}Body{% end %}'
        ).render()
        assert_element(html, "div", {"class": "chirpui-card__body"}, contains="Body")

    def test_collapsible_card_uses_details_summary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/card.html" import card %}'
            '{% call card(title="T", collapsible=true) %}C{% end %}'
        ).render()
        assert_element(html, "details")
        assert_element(html, "summary")


class TestStructuralModal:
    """Modal must render as <dialog> with correct id."""

    def test_modal_renders_dialog_element(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/modal.html" import modal %}'
            '{% call modal("my-dlg", title="Edit") %}Body{% end %}'
        ).render()
        assert_element(html, "dialog", {"id": "my-dlg"})
        assert "chirpui-modal__header" in html
        assert "chirpui-modal__close" in html


class TestStructuralAlert:
    """Alert must have role=alert and correct variant class."""

    def test_alert_has_role_alert(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}{% call alert() %}Warning{% end %}'
        ).render()
        assert_element(html, "div", {"role": "alert"}, contains="Warning")

    def test_alert_dismissible_has_close_button(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/alert.html" import alert %}'
            "{% call alert(dismissible=true) %}msg{% end %}"
        ).render()
        assert "chirpui-alert__close" in html
        assert_element(html, "button", {"aria-label": "Dismiss"})


class TestStructuralBadge:
    """Badge renders <span> by default, <a> with href."""

    def test_badge_renders_span(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("New") }}'
        ).render()
        assert_element(html, "span", contains="New")
        assert "<a" not in html

    def test_badge_with_href_renders_anchor(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("Link", href="/x") }}'
        ).render()
        assert_element(html, "a", {"href": "/x"}, contains="Link")


class TestStructuralForm:
    """Form must render <form> with action and method."""

    def test_form_renders_form_element(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import form %}'
            '{% call form("/submit", method="post") %}fields{% end %}'
        ).render()
        assert_element(html, "form", {"action": "/submit", "method": "post"})

    def test_text_field_has_aria_describedby(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/forms.html" import text_field %}'
            '{{ text_field("email", label="Email") }}'
        ).render()
        assert_element(html, "input", {"id": "email", "aria-describedby": "errors-email"})
        assert_element(html, "div", {"id": "errors-email", "role": "alert"})


class TestStructuralTable:
    """Table must use <table> with proper thead/tbody structure."""

    def test_table_renders_table_element(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/table.html" import table, row %}'
            '{% call table(headers=["Name"]) %}{{ row("Alice") }}{% end %}'
        ).render()
        assert_element(html, "table")
        assert_element(html, "th", contains="Name")
        assert_element(html, "td", contains="Alice")


class TestStructuralTabs:
    """Tabs must use role=tablist container."""

    def test_tabs_container_has_role_tablist(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tabs.html" import tabs, tab %}'
            "{% call tabs() %}"
            '{{ tab("overview", "Overview", url="/o", active=true) }}'
            "{% end %}"
        ).render()
        assert_element(html, "nav", {"role": "tablist"})
        assert 'aria-selected="true"' in html
        assert "Overview" in html


class TestStructuralDropdown:
    """Dropdown must use <details>/<summary> pattern."""

    def test_dropdown_uses_details_summary(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/dropdown.html" import dropdown %}'
            '{% call dropdown(label="Menu") %}<a>Item</a>{% end %}'
        ).render()
        assert_element(html, "details")
        assert_element(html, "summary", contains="Menu")
        assert "chirpui-dropdown__menu" in html


class TestStructuralAccordion:
    """Accordion items must use <details> with name for exclusive groups."""

    def test_accordion_uses_details_with_name(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/accordion.html" import accordion_item %}'
            '{% call accordion_item("Q1", name="faq") %}A1{% end %}'
        ).render()
        assert_element(html, "details", {"name": "faq"})
        assert_element(html, "summary", contains="Q1")
        assert "A1" in html


class TestStructuralSidebar:
    """Sidebar must render as <nav> with proper link structure."""

    def test_sidebar_renders_nav(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_link %}'
            "{% call sidebar() %}"
            '{{ sidebar_link("/dash", "Dashboard", active=true) }}'
            "{% end %}"
        ).render()
        assert_element(html, "nav")
        assert 'aria-current="page"' in html
        assert "chirpui-sidebar__link--active" in html


class TestStructuralPagination:
    """Pagination must render as <nav> with aria-label."""

    def test_pagination_renders_nav_with_aria(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            '{{ pagination(current=2, total=5, url_pattern="/items?page={page}") }}'
        ).render()
        assert_element(html, "nav", {"aria-label": "Pagination"})

    def test_pagination_current_page_is_aria_current(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/pagination.html" import pagination %}'
            '{{ pagination(current=2, total=5, url_pattern="/items?page={page}") }}'
        ).render()
        assert 'aria-current="page"' in html


class TestStructuralAvatar:
    """Avatar must have role=img by default, suppressed when decorative."""

    def test_avatar_has_role_img(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}{{ avatar(initials="JD") }}'
        ).render()
        assert_element(html, "span", {"role": "img"})

    def test_avatar_decorative_has_presentation_role(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/avatar.html" import avatar %}'
            '{{ avatar(initials="JD", decorative=true) }}'
        ).render()
        assert_element(html, "span", {"role": "presentation"})


class TestStructuralBreadcrumbs:
    """Breadcrumbs must render as <nav> with aria-label and <ol>."""

    def test_breadcrumbs_renders_nav_ol(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
            '{{ breadcrumbs([{"label": "Home", "href": "/"}, {"label": "Page"}]) }}'
        ).render()
        assert_element(html, "nav", {"aria-label": "Breadcrumb"})
        assert_element(html, "ol")
        assert 'aria-current="page"' in html


class TestStructuralDrawer:
    """Drawer must render as <dialog> with correct id and panel."""

    def test_drawer_renders_dialog(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/drawer.html" import drawer %}'
            '{% call drawer("d1", title="Settings") %}Content{% end %}'
        ).render()
        assert_element(html, "dialog", {"id": "d1"})
        assert "chirpui-drawer__panel" in html
        assert "chirpui-drawer__body" in html
        assert "Settings" in html


class TestStructuralSurface:
    """Surface renders as <div> (or <section>) with class."""

    def test_surface_renders_div(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/surface.html" import surface %}{% call surface() %}Inside{% end %}'
        ).render()
        assert_element(html, "div", contains="Inside")
        assert "chirpui-surface" in html


class TestStructuralCallout:
    """Callout must render as <aside> with structural children."""

    def test_callout_renders_aside(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/callout.html" import callout %}'
            '{% call callout(variant="warning", title="Heads up") %}Caution{% end %}'
        ).render()
        assert_element(html, "aside")
        assert "chirpui-callout--warning" in html
        assert "chirpui-callout__header" in html
        assert "chirpui-callout__body" in html
        assert "Heads up" in html


class TestStructuralTooltip:
    """Tooltip must have data-tooltip and role=tooltip bubble."""

    def test_tooltip_has_data_attr_and_role(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/tooltip.html" import tooltip %}'
            '{% call tooltip(hint="Help") %}Hover{% end %}'
        ).render()
        assert_element(html, "span", {"data-tooltip": "Help"})
        assert_element(html, "span", {"role": "tooltip"})


class TestStructuralNotificationDot:
    """Notification dot must have aria-label and ping element."""

    def test_dot_has_aria_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/notification_dot.html" import notification_dot %}'
            "{% call notification_dot(count=3) %}<button>Inbox</button>{% end %}"
        ).render()
        assert_element(html, "span", {"aria-label": "3 notifications"})
        assert 'aria-hidden="true"' in html

    def test_dot_without_count_default_label(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/notification_dot.html" import notification_dot %}'
            "{% call notification_dot() %}<button>Inbox</button>{% end %}"
        ).render()
        assert_element(html, "span", {"aria-label": "notification"})


class TestStructuralEmpty:
    """Empty state must render correct structure with actions slot."""

    def test_empty_state_structure(self, env: Environment) -> None:
        html = env.from_string(
            '{% from "chirpui/empty.html" import empty_state %}'
            '{% call empty_state(title="No results", action_label="Retry", action_href="/r") %}'
            "<p>Get started.</p>"
            "{% end %}"
        ).render()
        assert "chirpui-empty-state" in html
        assert "chirpui-empty-state__title" in html
        assert "chirpui-empty-state__action" in html
        assert "Retry" in html
        assert "No results" in html


class TestNavLandmarkNames:
    """Every <nav> rendered for the docs / showcase / app-shell page families
    must have a UNIQUE, non-empty accessible name so that screen-reader
    landmark menus do not list 'navigation, navigation, navigation' and
    axe-core's landmark-unique rule passes (#164/#129).
    """

    @staticmethod
    def _nav_labels(html: str) -> list[str]:
        """Collect the aria-label of every <nav> opening tag in ``html``."""
        labels: list[str] = []
        for nav_open in re.findall(r"<nav\b[^>]*>", html):
            match = re.search(r'aria-label="([^"]*)"', nav_open)
            # Record every <nav>, using None for an absent/empty name so the
            # uniqueness + non-empty assertions catch the unlabelled case.
            labels.append(match.group(1) if match else "")
        return labels

    def test_docs_page_family_navs_have_unique_names(self, env: Environment) -> None:
        """The docs page renders two navigation landmarks side by side: the
        filter_rail catalog and the sidebar sections tree. Mirror that
        composition and assert each <nav> has a distinct non-empty name.
        """
        html = env.from_string(
            '{% from "chirpui/workspace_primitives.html" import filter_rail %}'
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_link %}'
            "{% call filter_rail(label='Documentation catalog') %}"
            '<a href="/">Home</a>'
            "{% end %}"
            "{% call sidebar(aria_label='Documentation sections') %}"
            '{{ sidebar_link("/start", "Getting started") }}'
            "{% end %}"
        ).render()
        labels = self._nav_labels(html)
        assert len(labels) == 2
        assert all(labels), f"a docs <nav> has no accessible name: {labels!r}"
        assert len(set(labels)) == len(labels), f"duplicate nav names: {labels!r}"
        assert "Documentation catalog" in labels
        assert "Documentation sections" in labels

    def test_app_shell_family_navs_have_unique_names(self, env: Environment) -> None:
        """The primary navbar and a labelled sidebar must not collide."""
        html = env.from_string(
            '{% from "chirpui/navbar.html" import navbar, navbar_link %}'
            '{% from "chirpui/sidebar.html" import sidebar, sidebar_link %}'
            "{% call navbar(brand='App', aria_label='Primary') %}"
            '{{ navbar_link("/docs", "Docs") }}'
            "{% end %}"
            "{% call sidebar(aria_label='Showcase sections') %}"
            '{{ sidebar_link("/x", "X") }}'
            "{% end %}"
        ).render()
        labels = self._nav_labels(html)
        assert len(labels) == 2
        assert all(labels), f"an app-shell <nav> has no accessible name: {labels!r}"
        assert len(set(labels)) == len(labels), f"duplicate nav names: {labels!r}"
        assert "Primary" in labels
        assert "Showcase sections" in labels
