# Epic: Descriptor Coverage — Make the Design System Self-Aware

**Status**: Complete
**Created**: 2026-04-12
**Target**: v0.4.0
**Estimated Effort**: 18–26h
**Dependencies**: None (purely additive; no code changes to templates or CSS)
**Source**: Codebase audit of `components.py` COMPONENTS dict vs `templates/chirpui/*.html`

---

## Why This Matters

108 of 195 component templates (55%) have no `ComponentDescriptor` entry, leaving the design system unable to validate, introspect, or document the majority of its own surface area.

1. **No validation for most components** — `validate_variant` / `validate_size` only work for the 87 registered components. The other 108 silently accept invalid variant/size values, including high-traffic components like `table`, `pagination`, `avatar`, `forms`, `app_shell`, and `sidebar`.
2. **`design_system_report()` is incomplete** — consuming apps that call this function get metadata for 45% of the library. The 23 unregistered data-display components (table, bar_chart, donut, timeline, etc.) and 14 unregistered layout components (app_shell, sidebar, tray, split_layout) are invisible.
3. **No machine-readable API surface** — tooling (automated docs, IDE autocomplete, theme builders) cannot discover what variants, sizes, slots, or tokens a component accepts without reading raw template source. This blocks downstream adoption tooling.
4. **Inconsistent quality signal** — registered components (98) feel production-grade; unregistered ones (108) feel provisional. The gap undermines confidence in the library for new adopters.

Close the gap by adding `ComponentDescriptor` entries for all 108 unregistered templates, organized in category-based sprints that each ship independently.

### Evidence

| Layer/Source | Key Finding | Proposal Impact |
|-------------|-------------|-----------------|
| `components.py` audit | 98 registered descriptors vs 195 template files = 44.6% coverage | FIXES |
| Descriptor complexity analysis | 66% of existing descriptors have 1 feature type (usually variants only) — most new descriptors will be simple | FIXES (effort is bounded) |
| Data display gap | 23 unregistered data/analytics templates = largest unregistered category | FIXES |
| Layout gap | 14 unregistered layout templates including app_shell, sidebar, tray | FIXES |
| `design_system_report()` | Returns metadata for 87/195 components | FIXES |
| Existing test infrastructure | `test_validation.py` covers VARIANT_REGISTRY/SIZE_REGISTRY | MITIGATES (tests auto-cover new entries) |

### Invariants

These must remain true throughout or we stop and reassess:

1. **No template changes**: Descriptors are metadata-only additions to `components.py`. No `.html` or `.css` files are modified in this epic.
2. **All tests pass after each sprint**: `uv run poe ci` succeeds — the CSS contract test, transition token test, and existing component tests remain green.
3. **Descriptor accuracy**: Every registered variant, size, modifier, element, and slot must correspond to an actual CSS class or template construct. No speculative entries.

---

## Target Architecture

**Before:**
```
COMPONENTS = {
    "alert": ComponentDescriptor(block="chirpui-alert", variants=(...), ...),
    # ... 97 more entries
    # === 108 templates have NO entry ===
}
```

**After:**
```
COMPONENTS = {
    # ... 195+ entries covering every template
    # (some templates export multiple macros → multiple descriptors)
}
```

**Verification:**
```bash
# Zero templates without a descriptor (Sprint 5 acceptance)
python -c "
from pathlib import Path
from chirp_ui.components import COMPONENTS
templates = {p.stem for p in Path('src/chirp_ui/templates/chirpui').glob('*.html')}
registered = {c.template.replace('.html','') for c in COMPONENTS.values() if c.template}
print(f'Unregistered: {sorted(templates - registered)}')
" | grep 'Unregistered: \[\]'
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: descriptor conventions for multi-macro files | 2h | Low | Yes (RFC only) |
| 1 | Data display components (23 templates) | 5–7h | Low | Yes |
| 2 | Layout & shell components (14 templates) | 4–6h | Medium | Yes |
| 3 | Forms, navigation & interactive (16 templates) | 3–5h | Low | Yes |
| 4 | Effects, ASCII remainders & utility (55 templates) | 4–6h | Low | Yes |
| 5 | Validation & docs: 100% coverage gate | 2h | Low | Yes |

---

## Sprint 0: Design & Validate Conventions

**Goal**: Establish descriptor conventions for edge cases before writing 108 entries.

### Task 0.1 — Multi-macro file convention

Several templates export multiple macros (e.g., `forms.html` exports `form`, `text_field`, `select_field`, etc.; `oob.html` exports `oob_fragment`, `oob_toast`, `counter_badge`). Decide:
- One descriptor per exported macro? Or one per file with compound elements?
- Naming convention for sub-macros (e.g., `"form"`, `"text-field"`, `"select-field"` as separate keys, or `"forms"` with elements)?

**Acceptance**: Decision documented in this plan's changelog. Consistent with existing patterns (e.g., `"dropdown"` and `"dropdown__item"` are already separate keys).

### Task 0.2 — Descriptor-only vs structural templates

Some templates are pure layout wiring (e.g., `app_shell_layout.html` is an `{% extends %}` base, `fragment_island.html` is infrastructure). Decide:
- Which templates get descriptors vs which are explicitly excluded?
- Document the exclusion list and rationale.

**Acceptance**: Exclusion list with rationale. Expected: 5–10 templates excluded (layout bases, infrastructure-only files).

### Task 0.3 — Audit existing descriptors for accuracy

Spot-check 10 existing descriptors against their templates to verify the convention is reliable. Fix any stale entries.

**Acceptance**: `rg 'variants=' src/chirp_ui/components.py | wc -l` matches count before and after (or net change documented).

---

## Sprint 1: Data Display (23 templates)

**Goal**: Register the largest unregistered category — tables, charts, lists, cards, and data visualization components.

### Task 1.1 — Tables & pagination

Register: `table`, `pagination`, `resource_index`, `row_actions`, `params_table`

**Files**: `src/chirp_ui/components.py`
**Acceptance**: `python -c "from chirp_ui.components import COMPONENTS; assert all(k in COMPONENTS for k in ['table','pagination','resource-index','row-actions','params-table'])"`

### Task 1.2 — Charts & metrics

Register: `bar_chart`, `donut`, `metric_grid`, `stat`, `animated_stat_card`

**Acceptance**: All 5 keys present in COMPONENTS.

### Task 1.3 — Lists & timelines

Register: `list`, `sortable_list`, `timeline`, `tree_view`, `chapter_list`, `playlist`, `conversation_list`, `conversation_item`

**Acceptance**: All 8 keys present in COMPONENTS.

### Task 1.4 — Cards & content

Register: `post_card`, `channel_card`, `video_card`, `video_thumbnail`, `index_card`, `trending_tag`

**Acceptance**: All 6 keys present. `uv run pytest tests/test_validation.py -q` passes.

---

## Sprint 2: Layout & Shell (14 templates)

**Goal**: Register the structural components that define app architecture — shells, sidebars, trays, and layout primitives.

### Task 2.1 — App shell family

Register: `app_shell`, `app_shell_layout`, `app_layout`, `shell_frame`, `shell_actions`, `workspace_shell`

**Files**: `src/chirp_ui/components.py`
**Acceptance**: All 6 keys present. These are the highest-complexity descriptors (variants for topbar/sidebar, modifiers for collapsed state, tokens for widths/colors).

### Task 2.2 — Navigation chrome

Register: `sidebar`, `tray`, `drawer`

**Acceptance**: All 3 keys present. Sidebar descriptor includes tokens (`--chirpui-sidebar-expanded-width`, etc.).

### Task 2.3 — Layout compositions

Register: `split_layout`, `split_panel`, `tabbed_page_layout`, `chat_layout`, `accordion`

**Acceptance**: All 5 keys present. `uv run poe ci` passes.

---

## Sprint 3: Forms, Navigation & Interactive (16 templates)

**Goal**: Register form controls, navigation components, and interactive patterns.

### Task 3.1 — Form macros

Register descriptors for macros exported by `forms.html` (per Sprint 0 convention), plus: `auth`, `chat_input`, `inline_edit_field`, `tag_input`, `wizard_form`, `search_header`

**Acceptance**: All form-related keys present.

### Task 3.2 — Navigation

Register: `nav_link`, `nav_tree`, `navbar`, `nav_progress`, `route_tabs`, `tabs_panels`

**Acceptance**: All 6 keys present.

### Task 3.3 — Interactive patterns

Register: `command_palette`, `command_bar`, `selection_bar`, `collapse`

**Acceptance**: All 4 keys present. `uv run poe ci` passes.

---

## Sprint 4: Effects, ASCII & Utility (55 templates)

**Goal**: Register remaining components — effects, ASCII panel remainders, and utility/composition primitives.

### Task 4.1 — Effects & animation

Register: `gradient_text`, `hero_effects`, `infinite_scroll`, `reveal_on_scroll`, `stepper`, `dnd`

**Acceptance**: All 6 keys present.

### Task 4.2 — ASCII remainders

Register: `ascii_breaker_panel`, `ascii_error`, `ascii_icon`

**Acceptance**: All 3 keys present.

### Task 4.3 — Utility components

Register: `avatar`, `avatar_stack`, `calendar`, `carousel`, `copy_button`, `divider`, `empty`, `empty_panel_state`, `filter_chips`, `label_overline`, `link`, `live_badge`, `logo`, `media_object`, `mention`, `popover`, `profile_header`, `reaction_pill`, `share_menu`, `signature`, `spinner`, `split_button`, `theme_toggle`, `typing_indicator`

**Acceptance**: All 24 keys present.

### Task 4.4 — Composition & infrastructure

Register (or document as excluded per Sprint 0): `config_card`, `config_dashboard`, `config_row`, `action_bar`, `action_strip`, `bento_grid`, `callout`, `entity_header`, `fragment_island`, `islands`, `modal_overlay`, `oob`, `sse_status`, `state_primitives`, `suspense`, `status_with_hint`

**Acceptance**: All keys either registered or on the documented exclusion list. `uv run poe ci` passes.

---

## Sprint 5: Validation & Documentation

**Goal**: Enforce 100% coverage and update docs.

### Task 5.1 — Coverage gate test

Add a test to `tests/test_validation.py` that asserts every `.html` template in `templates/chirpui/` has a COMPONENTS entry (minus the exclusion list from Sprint 0).

**Files**: `tests/test_validation.py`
**Acceptance**: `uv run pytest tests/test_validation.py::test_descriptor_coverage -q` passes.

### Task 5.2 — Update design_system_report()

Verify `design_system_report()` now returns metadata for all components. Update `COMPONENT-OPTIONS.md` if the report format changed.

**Acceptance**: `python -c "from chirp_ui.components import design_system_report; r = design_system_report(); print(f'{len(r)} components'); assert len(r) >= 190"`

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Descriptor inaccuracy — registered variants don't match CSS | Medium | Medium | Sprint 0 Task 0.3 spot-checks convention; Sprint 5 coverage gate catches drift |
| Multi-macro files bloat COMPONENTS dict | Low | Low | Sprint 0 Task 0.1 establishes convention; follow existing `dropdown`/`dropdown__item` pattern |
| Stale descriptors after future template changes | Medium | Medium | Sprint 5 Task 5.1 adds CI gate — any new template without descriptor fails the build |
| Sprint 4 utility batch is large (55 templates) | Medium | Low | Most utility descriptors are simple (1 feature type); can split into 4a/4b if needed |
| app_shell descriptor complexity (Sprint 2) | Low | Medium | app_shell has the most parameters; read template carefully, focus on CSS-visible API only |

---

## Success Metrics

| Metric | Current | After Sprint 2 | After Sprint 5 |
|--------|---------|----------------|----------------|
| Registered descriptors | 98 | ~135 | 195+ |
| Coverage % (descriptors / templates) | 44.6% | ~69% | 100% |
| `design_system_report()` component count | 98 | ~135 | 195+ |
| CI gate for descriptor coverage | None | None | Enforced (test fails on gap) |

---

## Relationship to Existing Work

- **PLAN-layout-widget-brainstorm** — parallel — some brainstorm items (config_card, action_bar) get descriptors here but no new templates are created
- **PLAN-theme-tokens** — parallel — token fields in descriptors document which components have theme-overridable custom properties
- **Typography scale completion** — independent — font token usage is orthogonal to descriptor metadata

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-12 | Initial draft | Codebase audit revealed 55% descriptor gap |
| 2026-04-12 | Sprint 0 complete | Conventions established, exclusions identified, spot-check passed |

### Sprint 0 Decisions

**Task 0.1 — Multi-macro convention:** One descriptor per distinct BEM block, not per macro.
Multiple macros sharing the same `chirpui-*` block get one descriptor. This follows existing
precedent: `dropdown`/`dropdown__item`, `settings-row-list`/`settings-row`, `tabs`/`tab`,
`feature-section`/`feature-stack`, `install-snippet` (from `code.html`), `filter-row`
(from `filter_bar.html`).

For `forms.html` (23 macros): register `form`, `field`, `toggle`, `form-actions`,
`form-error-summary` as separate descriptors — each is a distinct BEM block.

**Task 0.2 — Exclusion list (2 templates):**
- `app_shell_layout.html` — `{% extends %}` base layout, no macros, no BEM output
- `app_layout.html` — `{% extends %}` base layout, no macros, no BEM output

All other templates (including `islands.html`, `fragment_island.html`, `state_primitives.html`,
`hero_effects.html`, `oob.html`) produce `chirpui-*` classes and WILL get descriptors.

**Task 0.3 — Spot-check:** 10 existing descriptors verified against templates. Convention is
reliable: variants/sizes map to `--{value}` CSS modifier classes, elements map to `__{element}`
sub-classes, tokens map to `--chirpui-{block}-*` custom properties.
