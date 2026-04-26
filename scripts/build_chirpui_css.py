"""Concatenate CSS partials into the shipped ``chirpui.css``.

Pure Python, stdlib only, deterministic. See
``docs/DESIGN-css-registry-projection.md § Decision 3`` for the contract.

Usage
-----
From the repo root::

    python scripts/build_chirpui_css.py        # writes chirpui.css
    python scripts/build_chirpui_css.py --check # exits non-zero if stale

The ``--check`` flag is what CI uses: it regenerates into memory, diffs against
the committed output, and fails with a helpful message if they differ.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSS_SRC = REPO_ROOT / "src" / "chirp_ui" / "templates" / "css"
OUTPUT = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui.css"

HEADER = """\
/* ============================================================================
 * chirp-ui — GENERATED FILE; do not hand-edit.
 *
 * Source partials: src/chirp_ui/templates/css/
 * Rebuild:         poe build-css   (or python scripts/build_chirpui_css.py)
 *
 * See docs/PLAN-css-scope-and-layer.md for the authoring model.
 * ============================================================================
 */
"""

# Public cascade order. Consumers win without specificity wars by placing their
# rules in a later-declared layer (typically `@layer app.overrides`). See
# docs/CSS-OVERRIDE-SURFACE.md for the contract.
LAYER_DECLARATION = (
    "@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;\n"
)

# Per-partial layer assignment. Partials not listed default to DEFAULT_LAYER.
# The safe baseline for S3 is: everything in `chirpui.component`, utilities in
# `chirpui.utility`. The `reset`/`token`/`base` slots are declared but left
# empty so future cleanup sprints can move rules into them without a behavioral
# flip today. A partial whose body already starts with `@layer` opts out of
# build-time wrapping — that's how S5's @scope envelopes stay local.
DEFAULT_LAYER = "chirpui.component"
LAYER_BY_PARTIAL: dict[str, str] = {
    "partials/037_utilities.css": "chirpui.utility",
    "partials/086_utility-inline-grouping-and-measures.css": "chirpui.utility",
    "partials/087_utility-auto-fill-grid.css": "chirpui.utility",
}

# Ordered list of partials relative to CSS_SRC. Order matters — this is the
# cascade. As sprints split the monolith, entries get added in the appropriate
# layer position.
MANIFEST: tuple[str, ...] = (
    "partials/001_tokens.css",
    "partials/002_reset.css",
    "partials/003_base.css",
    "partials/004_layout.css",
    "partials/005_workbench.css",
    "partials/006_entity-header.css",
    "partials/007_inline-edit-field.css",
    "partials/008_row-actions.css",
    "partials/009_divider.css",
    "partials/010_avatar.css",
    "partials/011_media-object.css",
    "partials/012_stat.css",
    "partials/013_action-bar.css",
    "partials/014_action-containers.css",
    "partials/015_chat-layout.css",
    "partials/016_message-bubble-and-thread.css",
    "partials/017_typing-indicator.css",
    "partials/018_chat-input.css",
    "partials/019_conversation-list-and-item.css",
    "partials/020_reaction-pill-and-message-reactions.css",
    "partials/021_post-card.css",
    "partials/022_comment-and-comment-thread.css",
    "partials/023_profile-header.css",
    "partials/024_avatar-stack.css",
    "partials/025_trending-tag-and-mention.css",
    "partials/026_breadcrumbs.css",
    "partials/027_navbar.css",
    "partials/028_logo.css",
    "partials/029_sidebar.css",
    "partials/030_stepper.css",
    "partials/031_wizard-form.css",
    "partials/032_description-list.css",
    "partials/033_settings-row.css",
    "partials/034_config-row.css",
    "partials/035_timeline.css",
    "partials/036_list.css",
    "partials/037_utilities.css",
    "partials/038_streaming-and-ai-components.css",
    "partials/039_surface.css",
    "partials/040_aura.css",
    "partials/041_callout.css",
    "partials/042_hero.css",
    "partials/043_overlay.css",
    "partials/044_carousel.css",
    "partials/045_card.css",
    "partials/046_video-card.css",
    "partials/047_channel-card.css",
    "partials/048_video-thumbnail.css",
    "partials/049_live-badge.css",
    "partials/050_playlist.css",
    "partials/051_chapter-list.css",
    "partials/052_modal.css",
    "partials/053_drawer.css",
    "partials/054_tabs.css",
    "partials/055_accordion.css",
    "partials/056_collapse.css",
    "partials/057_dropdown.css",
    "partials/058_toast.css",
    "partials/059_table.css",
    "partials/060_pagination.css",
    "partials/061_alert.css",
    "partials/062_route-tabs.css",
    "partials/063_theme-toggle.css",
    "partials/064_dropdown-menu.css",
    "partials/065_tray.css",
    "partials/066_modal-overlay.css",
    "partials/067_tabs-panels.css",
    "partials/068_data-theme-support.css",
    "partials/069_data-style-support.css",
    "partials/070_form-fields.css",
    "partials/071_button.css",
    "partials/072_badge.css",
    "partials/073_spinner.css",
    "partials/074_ascii-icons.css",
    "partials/075_skeleton.css",
    "partials/076_infinite-scroll.css",
    "partials/077_reveal-on-scroll.css",
    "partials/078_empty-state.css",
    "partials/079_progress-bar.css",
    "partials/080_bar-chart.css",
    "partials/081_donut-chart.css",
    "partials/082_status-indicator.css",
    "partials/083_app-shell.css",
    "partials/084_app-shell-sidebar.css",
    "partials/085_command-palette.css",
    "partials/086_utility-inline-grouping-and-measures.css",
    "partials/087_utility-auto-fill-grid.css",
    "partials/088_inner-shell-sections.css",
    "partials/089_effects-foundation.css",
    "partials/090_shimmer-button.css",
    "partials/091_ripple-button.css",
    "partials/092_border-beam.css",
    "partials/093_notification-dot.css",
    "partials/094_number-ticker.css",
    "partials/095_marquee.css",
    "partials/096_meteor-effect.css",
    "partials/097_text-reveal.css",
    "partials/098_display-text.css",
    "partials/099_gradient-text.css",
    "partials/100_glow-card.css",
    "partials/101_spotlight-card.css",
    "partials/102_particle-background.css",
    "partials/103_animated-counter.css",
    "partials/104_pulsing-button.css",
    "partials/105_bento-grid.css",
    "partials/106_floating-dock.css",
    "partials/107_animated-stat-card.css",
    "partials/108_hero-effects.css",
    "partials/109_marquee-item.css",
    "partials/110_tooltip.css",
    "partials/111_icon-button.css",
    "partials/112_segmented-control.css",
    "partials/113_split-panel.css",
    "partials/114_typewriter.css",
    "partials/115_glitch-text.css",
    "partials/116_neon-text.css",
    "partials/117_aurora-background.css",
    "partials/118_scanline-overlay.css",
    "partials/119_grain-overlay.css",
    "partials/120_svg-pattern-tiles.css",
    "partials/121_css-only-bg-patterns.css",
    "partials/122_band.css",
    "partials/123_page-ambient.css",
    "partials/124_surface-overlays.css",
    "partials/125_orbit.css",
    "partials/126_sparkle.css",
    "partials/127_confetti.css",
    "partials/128_wobble-jello-rubber-band.css",
    "partials/129_symbol-rain.css",
    "partials/130_holy-light.css",
    "partials/131_rune-field.css",
    "partials/132_constellation.css",
    "partials/133_ascii-border.css",
    "partials/134_ascii-divider.css",
    "partials/135_ascii-sparkline.css",
    "partials/136_ascii-progress.css",
    "partials/137_ascii-empty.css",
    "partials/138_ascii-spinner.css",
    "partials/139_ascii-badge.css",
    "partials/140_ascii-glyph-fill.css",
    "partials/141_ascii-error-page.css",
    "partials/142_ascii-skeleton.css",
    "partials/143_ascii-toggle.css",
    "partials/144_ascii-switch.css",
    "partials/145_ascii-breaker-panel.css",
    "partials/146_ascii-indicator-light.css",
    "partials/147_ascii-tile-button.css",
    "partials/148_ascii-knob.css",
    "partials/149_ascii-fader.css",
    "partials/150_ascii-vu-meter.css",
    "partials/151_ascii-7-segment-display.css",
    "partials/152_ascii-checkbox.css",
    "partials/153_ascii-radio.css",
    "partials/154_ascii-stepper.css",
    "partials/155_ascii-split-flap-display.css",
    "partials/156_ascii-ticker.css",
    "partials/157_ascii-table.css",
    "partials/158_row-component-enhancements.css",
    "partials/159_resource-card.css",
    "partials/160_resource-index.css",
    "partials/161_navigation-metadata-authoring.css",
)


def _wrap_in_layer(body: str, layer: str) -> str:
    """Wrap ``body`` in ``@layer NAME { … }``.

    If the body already starts with ``@layer`` (ignoring leading whitespace and
    comments), return it unchanged — the partial owns its own layering (S5's
    envelope form, or any other explicit author).
    """
    # Skip leading whitespace and CSS comments to check the first real token.
    i = 0
    while i < len(body):
        if body[i].isspace():
            i += 1
            continue
        if body.startswith("/*", i):
            end = body.find("*/", i + 2)
            i = len(body) if end == -1 else end + 2
            continue
        break
    if body[i:].lstrip().startswith("@layer "):
        return body
    # Ensure a trailing newline before the closing brace so it sits on its own line.
    if body and not body.endswith("\n"):
        body += "\n"
    return f"@layer {layer} {{\n{body}}}\n"


def build() -> str:
    """Return the full concatenated stylesheet as a string."""
    parts: list[str] = [HEADER, "\n", LAYER_DECLARATION]
    for rel in MANIFEST:
        path = CSS_SRC / rel
        if not path.is_file():
            raise FileNotFoundError(f"Manifest entry not found: {path}")
        layer = LAYER_BY_PARTIAL.get(rel, DEFAULT_LAYER)
        parts.append(f"\n/* === {rel} === */\n")
        parts.append(_wrap_in_layer(path.read_text(encoding="utf-8"), layer))
    # Single trailing newline, no blank-line drift.
    text = "".join(parts)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the committed output is stale.",
    )
    args = parser.parse_args(argv)

    generated = build()

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            sys.stderr.write(
                f"chirpui.css is stale relative to {CSS_SRC.relative_to(REPO_ROOT)}.\n"
                f"Run: poe build-css\n"
            )
            return 1
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    sys.stdout.write(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(generated):,} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
