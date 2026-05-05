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
    "chirpuiDropdown": AlpineRequirement(
        factory="chirpuiDropdown",
        macros=("dropdown_menu",),
    ),
    "chirpuiDropdownSelect": AlpineRequirement(
        factory="chirpuiDropdownSelect",
        macros=("dropdown_menu",),
    ),
    "chirpuiCopy": AlpineRequirement(
        factory="chirpuiCopy",
        macros=("code", "copy_button", "streaming"),
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

    *ok* — ``True`` when no factories are used, or when the script tag
    is present. ``False`` when at least one Alpine-requiring component
    rendered but the script is missing.
    """

    script_loaded: bool
    factories_used: frozenset[str]
    missing: frozenset[str]
    ok: bool


_FACTORY_PATTERN = re.compile(r"""x-data=["'](chirpui\w+)\s*\(""")
_SCRIPT_MARKER = "chirpui-alpine.js"


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
    """
    factories = frozenset(_FACTORY_PATTERN.findall(html))
    script_loaded = _SCRIPT_MARKER in html

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
    )


# TODO(chirp): wire check_alpine_runtime() into use_chirp_ui(app) at
# freeze time. Run against the first rendered layout response; in dev
# (app.debug or strict="auto"), raise on result.missing; otherwise emit
# a warning. See chirp-ui/.context/plan-dev-mode-strict.md § Sprint 3.
