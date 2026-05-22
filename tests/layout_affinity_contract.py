"""Shared test-only layout-affinity vocabulary and proof matrix."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ALLOWED_SOURCE_VALUES = {
    "data-chirpui-role": {
        "actions",
        "aside",
        "content",
        "filters",
        "hints",
        "metadata",
        "nav",
        "rail",
        "search",
        "status",
    },
    "data-chirpui-pressure": {
        "compress",
        "flex",
        "rigid",
    },
    "data-chirpui-affinity": {
        "block-end",
        "block-start",
        "end",
        "fill",
        "start",
    },
    "data-chirpui-rhythm": {
        "attached",
        "group",
        "inset",
        "separated",
        "stack",
    },
}

RESOLVER_MATRIX = {
    "command_bar": {
        "css": REPO_ROOT / "src/chirp_ui/templates/css/partials/014_action-containers.css",
        "docs": {"command_bar", "Catalog shell"},
        "browser": "test_catalog_shell_responsive_command_surface_has_no_overflow",
    },
    "filter_bar": {
        "css": REPO_ROOT / "src/chirp_ui/templates/css/partials/014_action-containers.css",
        "docs": {"filter_bar", "data/filter toolbar"},
        "browser": "test_data_filter_bar_layout_affinity_has_no_overflow",
    },
    "card": {
        "css": REPO_ROOT / "src/chirp_ui/templates/css/partials/045_card.css",
        "docs": {"card", "component-owned internal layout-affinity contract"},
        "browser": "test_card_layout_affinity_has_no_overflow",
    },
    "frame": {
        "css": REPO_ROOT / "src/chirp_ui/templates/css/partials/004_layout.css",
        "docs": {"frame", "rail/content/nav shell"},
        "browser": "test_layout_affinity_primitives_have_no_overflow",
    },
    "workspace_shell": {
        "css": REPO_ROOT / "src/chirp_ui/templates/css/partials/005_workbench.css",
        "docs": {"workspace_shell", "inspector/workspace resolver"},
        "browser": "test_workspace_shell_layout_affinity_has_no_overflow",
    },
    "workspace_primitives": {
        "css": REPO_ROOT / "src/chirp_ui/templates/css/partials/167_workspace-primitives.css",
        "docs": {"filter_rail", "result_collection", "inspector_panel"},
        "browser": "test_operations_workspace_shell_variant_has_no_overflow",
    },
}
