"""Alpine runtime detection for chirp-ui.

chirp-ui has a small, enumerable set of macros that require
``chirpui-alpine.js`` to work at runtime (theme toggle, dialogs,
dropdowns, collapsible sidebar, etc). When an app ships a layout that
imports those macros but forgets the script tag, every interactive
component breaks silently.

This module exposes the manifest of Alpine-requiring factories and a
pure :func:`check_alpine_runtime` helper. Chirp's ``use_chirp_ui(app)``
calls the helper against the first rendered response at freeze time so
the mistake surfaces as a warning (or a raised error, in dev) at startup
rather than as broken UI in production.

Example::

    from chirp_ui.alpine import check_alpine_runtime

    result = check_alpine_runtime(rendered_html)
    if not result.ok:
        missing = ", ".join(sorted(result.missing))
        raise RuntimeError(
            f"layout uses Alpine factories {{{missing}}} but "
            "chirpui-alpine.js is not in the rendered HTML"
        )
"""

import re
from dataclasses import dataclass

__all__ = [
    "ALPINE_REQUIRED_COMPONENTS",
    "AlpineRequirement",
    "AlpineRuntimeCheck",
    "check_alpine_runtime",
]


@dataclass(frozen=True)
class AlpineRequirement:
    """A single Alpine factory and the macros that emit it.

    *factory* is the identifier used in ``x-data="chirpuiXxx(...)"`` — the
    grep target inside rendered HTML.

    *macros* are the chirp-ui template macros that emit this factory.
    Included for documentation; detection is purely by factory name.

    *conditional* describes the macro argument combination that triggers
    the requirement when it is not unconditional. Informational only.
    """

    factory: str
    macros: tuple[str, ...]
    conditional: str | None = None


ALPINE_REQUIRED_COMPONENTS: dict[str, AlpineRequirement] = {
    "chirpuiThemeToggle": AlpineRequirement(
        factory="chirpuiThemeToggle",
        macros=("theme_toggle",),
    ),
    "chirpuiStyleToggle": AlpineRequirement(
        factory="chirpuiStyleToggle",
        macros=("theme_toggle",),
    ),
    "chirpuiStyleSelect": AlpineRequirement(
        factory="chirpuiStyleSelect",
        macros=("theme_toggle",),
    ),
    "chirpuiDialogTarget": AlpineRequirement(
        factory="chirpuiDialogTarget",
        macros=("modal", "drawer", "confirm", "ascii_modal", "command_palette"),
    ),
    "chirpuiSplitPanel": AlpineRequirement(
        factory="chirpuiSplitPanel",
        macros=("split_panel",),
    ),
    "chirpuiDrawer": AlpineRequirement(
        factory="chirpuiDrawer",
        macros=("drawer",),
    ),
    "chirpuiTray": AlpineRequirement(
        factory="chirpuiTray",
        macros=("tray",),
    ),
    "chirpuiDropdown": AlpineRequirement(
        factory="chirpuiDropdown",
        macros=("dropdown_menu",),
    ),
    "chirpuiDropdownSelect": AlpineRequirement(
        factory="chirpuiDropdownSelect",
        macros=("dropdown_menu",),
    ),
    "chirpuiTabs": AlpineRequirement(
        factory="chirpuiTabs",
        macros=("tabs_panels",),
    ),
    "chirpuiCopy": AlpineRequirement(
        factory="chirpuiCopy",
        macros=("code", "copy_button", "streaming", "message_actions"),
    ),
    "chirpuiFader": AlpineRequirement(
        factory="chirpuiFader",
        macros=("ascii_fader",),
    ),
    "chirpuiSseRetry": AlpineRequirement(
        factory="chirpuiSseRetry",
        macros=("sse_status",),
        conditional="sse_retry()",
    ),
    "chirpuiStreamLifecycle": AlpineRequirement(
        factory="chirpuiStreamLifecycle",
        macros=("streaming",),
        conditional="sse_connect or sse_swap_target",
    ),
    "chirpuiSidebar": AlpineRequirement(
        factory="chirpuiSidebar",
        macros=("app_shell", "app_shell_layout"),
        conditional="sidebar_collapsible=true",
    ),
    "chirpuiResponsiveSidebar": AlpineRequirement(
        factory="chirpuiResponsiveSidebar",
        macros=("sidebar",),
        conditional='cls includes "chirpui-sidebar--responsive-dropdowns"',
    ),
    "chirpuiGridSelection": AlpineRequirement(
        factory="chirpuiGridSelection",
        macros=("data_grid",),
        conditional="selectable=true (the data_grid root always carries it)",
    ),
    "chirpuiContextMenu": AlpineRequirement(
        factory="chirpuiContextMenu",
        macros=("context_menu",),
    ),
    "chirpuiPopover": AlpineRequirement(
        factory="chirpuiPopover",
        macros=("popover",),
    ),
    "chirpuiInputOtp": AlpineRequirement(
        factory="chirpuiInputOtp",
        macros=("input_otp",),
    ),
    "chirpuiHoverCard": AlpineRequirement(
        factory="chirpuiHoverCard",
        macros=("hover_card",),
    ),
    "chirpuiMenubar": AlpineRequirement(
        factory="chirpuiMenubar",
        macros=("menubar",),
    ),
    "chirpuiNavigationMenu": AlpineRequirement(
        factory="chirpuiNavigationMenu",
        macros=("navigation_menu",),
    ),
    "chirpuiCombobox": AlpineRequirement(
        factory="chirpuiCombobox",
        macros=("combobox",),
    ),
    "chirpuiCommandPalette": AlpineRequirement(
        factory="chirpuiCommandPalette",
        macros=("command_palette",),
    ),
    "chirpuiDatePicker": AlpineRequirement(
        factory="chirpuiDatePicker",
        macros=("date_picker",),
    ),
    "chirpuiParamOverride": AlpineRequirement(
        factory="chirpuiParamOverride",
        macros=("param_override",),
    ),
    "chirpuiShortcuts": AlpineRequirement(
        factory="chirpuiShortcuts",
        macros=("shortcuts_help",),
    ),
    "chirpuiComposer": AlpineRequirement(
        factory="chirpuiComposer",
        macros=("chat_input",),
    ),
    "chirpuiToast": AlpineRequirement(
        factory="chirpuiToast",
        macros=("toast",),
    ),
    "chirpuiToastStack": AlpineRequirement(
        factory="chirpuiToastStack",
        macros=("toast",),
    ),
}


@dataclass(frozen=True)
class AlpineRuntimeCheck:
    """Result of :func:`check_alpine_runtime`.

    *script_loaded* — ``chirpui-alpine.js`` substring appears in the HTML.

    *factories_used* — named chirp-ui factories detected in ``x-data=``
    attributes. Empty when no interactive chirp-ui components rendered.

    *missing* — factories used in the HTML that are not in the
    :data:`ALPINE_REQUIRED_COMPONENTS` manifest (useful for drift
    detection) OR, when *script_loaded* is False, all
    *factories_used*.

    *ok* — ``True`` when no factories are used, or when the
    ``chirpui-alpine.js`` script tag is present. ``False`` when at least
    one Alpine-requiring component rendered but the script is missing.
    This is the narrow registration-script check; it intentionally does
    **not** consider Alpine core (see below).

    *core_loaded* — an Alpine **core** ``<script>`` is present (detected by
    an ``alpinejs@``/``@alpinejs/csp`` src or Chirp's ``data-chirp="alpine"``
    marker). chirp-ui factories need both ``chirpui-alpine.js`` (to register
    them) and Alpine core (to run them).

    *core_url_valid* — an Alpine core script is present **and** uses the
    browser build (path ends in ``/dist/cdn.min.js``). A bare
    ``alpinejs@<version>`` resolves to the CommonJS main and fails silently
    in browsers — the exact footgun ``problems`` flags.

    *core_loaded* / *core_url_valid* are only meaningful against a fully
    **injected** response or a hand-authored page. At pre-injection layout
    freeze time Alpine core is not in the HTML yet, so rely on *ok* /
    *script_loaded* there.
    """

    script_loaded: bool
    factories_used: frozenset[str]
    missing: frozenset[str]
    ok: bool
    core_loaded: bool = False
    core_url_valid: bool = False

    @property
    def problems(self) -> tuple[str, ...]:
        """Human-readable runtime problems, empty when no factories are used.

        Composes the registration-script, Alpine-core, and CDN-URL findings
        into messages a dev warning can surface. Note the core/URL items are
        only accurate against fully-injected HTML (see class docstring).
        """
        if not self.factories_used:
            return ()
        issues: list[str] = []
        if not self.script_loaded:
            issues.append("chirpui-alpine.js runtime script is not in the HTML")
        if not self.core_loaded:
            issues.append("Alpine core script is not in the HTML")
        elif not self.core_url_valid:
            issues.append(
                "Alpine core script URL is not the browser build "
                "(it must end in /dist/cdn.min.js; a bare alpinejs@<version> "
                "resolves to CommonJS and fails silently in browsers)"
            )
        return tuple(issues)


_FACTORY_PATTERN = re.compile(r"""x-data=["'](chirpui\w+)\s*\(""")
_SCRIPT_MARKER = "chirpui-alpine.js"
# Alpine CORE script src: the "alpinejs" npm package or the "@alpinejs/csp"
# build — NOT the @alpinejs/mask|intersect|focus plugins, which themselves
# need core. ``alpinejs@`` matches the bare package; ``alpinejs/csp`` matches
# the CSP build; neither matches ``@alpinejs/mask`` etc. (those read
# ``alpinejs/mask``).
_ALPINE_CORE_SRC = re.compile(
    r"""<script\b[^>]*\bsrc=["']([^"']*alpinejs(?:@|/csp)[^"']*)["']""",
    re.IGNORECASE,
)
# Chirp marks the core injection with data-chirp="alpine" (plugins use
# alpine-mask / alpine-intersect / alpine-focus).
_ALPINE_CORE_MARKER = re.compile(r"""data-chirp=["']alpine["']""")
# The correct browser build always ends the path with /dist/cdn.min.js.
_CDN_BUILD_SUFFIX = "/dist/cdn.min.js"


def check_alpine_runtime(html: str) -> AlpineRuntimeCheck:
    """Scan rendered HTML for chirp-ui Alpine factories and the runtime script.

    Pure function: no I/O, no framework coupling. Pass the full rendered
    HTML of a layout (or any page) and inspect the result.

    The scan matches ``x-data="chirpuiXxx("`` — double or single quoted,
    identifier must begin with ``chirpui``, and must be followed by an
    opening paren (anonymous Alpine state like ``x-data="{ shown: false }"``
    is intentionally ignored; those only need Alpine core, not
    ``chirpui-alpine.js``).

    The script marker match is a plain substring search for
    ``chirpui-alpine.js``. Any path prefix or minification suffix is fine
    as long as the filename appears somewhere in the HTML.

    Alpine **core** detection (``core_loaded`` / ``core_url_valid``) scans for
    an ``alpinejs@``/``@alpinejs/csp`` script src or Chirp's
    ``data-chirp="alpine"`` marker, and verifies the browser build suffix
    ``/dist/cdn.min.js``. These are only meaningful against fully-injected
    HTML — at pre-injection freeze time Alpine core is not in the page yet.
    """
    factories = frozenset(_FACTORY_PATTERN.findall(html))
    script_loaded = _SCRIPT_MARKER in html

    core_srcs = _ALPINE_CORE_SRC.findall(html)
    core_loaded = bool(core_srcs) or bool(_ALPINE_CORE_MARKER.search(html))
    core_url_valid = any(_CDN_BUILD_SUFFIX in src for src in core_srcs)

    if not factories:
        missing: frozenset[str] = frozenset()
        ok = True
    elif script_loaded:
        missing = frozenset()
        ok = True
    else:
        missing = factories
        ok = False

    return AlpineRuntimeCheck(
        script_loaded=script_loaded,
        factories_used=factories,
        missing=missing,
        ok=ok,
        core_loaded=core_loaded,
        core_url_valid=core_url_valid,
    )

