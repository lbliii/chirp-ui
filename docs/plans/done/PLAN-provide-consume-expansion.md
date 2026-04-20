# Epic: Provide/Consume Expansion — Context Flow for Composite Components

**Status**: Complete (Sprint 5 documentation polish deferred)
**Created**: 2026-04-09
**Target**: 0.3.0
**Estimated Effort**: 12–20h
**Dependencies**: kida ≥ 0.3.4 (already adopted in 0.2.6)
**Source**: Codebase audit of all 188 chirp-ui templates, provide/consume adoption in #39

---

## Why This Matters

Kida 0.3.4 introduced `{% provide %}` / `consume()` for parent-to-child state flow across slot boundaries. Chirp-ui adopted it in 0.2.6 for three use cases (table alignment, hero variant, bar density). But **the majority of composite components still rely on explicit parameter forwarding or no context flow at all**, forcing users to repeat variant/density/surface values at every nesting level.

### Consequences

1. **Boilerplate in templates** — Users must pass `surface_variant=` to every nested component inside a `section()`, `panel()`, or `app_shell()` region, even when the parent already knows.
2. **Silent inconsistency** — A card inside a `surface(variant="accent")` has no way to know it's on an accent surface; child components can't auto-adapt contrast or styling.
3. **Accordion name coordination is fragile** — `accordion_item(name=)` must manually match `accordion(name=)`. A typo breaks the exclusive-open behavior with no warning.
4. **Form field context is disconnected** — `form()` sets up HTMX context and density, but `field_wrapper()` and individual fields have no way to inherit form-level settings (dense mode, error display variant).
5. **Sidebar/navbar active state requires global context** — Children expect `current_path` in page context rather than receiving it from a navigation parent, making standalone testing harder.

### Evidence Table

| Source | Finding | Proposal Impact |
|--------|---------|-----------------|
| template audit | 6 provide / 8 consume across 11 files (of 188 total) | FIXES — expands to ~25 additional consume sites |
| `section()`, `panel()` | Accept `surface_variant` but don't provide to slot children | FIXES — children inherit surface context |
| `accordion` | `name` param must be manually coordinated between parent/child | FIXES — parent provides name |
| `form()` / `field_wrapper()` | No context flow; density/errors passed per-field | FIXES — form provides density + error context key |
| `sidebar()` / `navbar()` | Children read `current_path` from global context, not parent | MITIGATES — parent can provide it, improving testability |
| `card()` | Variant applied to container CSS only; children can't adapt | FIXES — card provides variant for aware children |
| `app_shell()` | `topbar_variant`, `sidebar_variant` applied to CSS classes only | MITIGATES — regions can provide variant to slot children |
| `tabs_panels()` | Active state managed by Alpine.js `x-data`, not template context | UNRELATED — Alpine owns interactive state |
| `dropdown_menu()` | Open/close state managed by Alpine.js | UNRELATED — Alpine owns interactive state |

### The Fix

Expand provide/consume to every composite component where a parent wraps children in a slot and those children benefit from knowing parent state — surface variant, density, name coordination, and navigation context.

---

### Invariants

These must remain true throughout or we stop and reassess:

1. **Explicit params always win** — `consume()` is a fallback only. `{% set _variant = (variant if variant else consume("_parent_variant", "")) %}` is the canonical pattern. No component changes behavior if the user passes an explicit param.
2. **Standalone rendering never breaks** — Every component must render correctly without any provided context. `consume("_key", "sensible_default")` ensures this. Tests must cover both with-parent and without-parent cases.
3. **Full test suite passes at every sprint** — No sprint introduces a regression. `uv run poe ci` is the gate.

---

## Target Architecture

### Context Keys (underscore-prefixed, namespaced)

```
_surface_variant   — provided by: surface(), section(), panel(), app_shell regions
_bar_surface       — provided by: command_bar(), filter_bar() (already exists)
_bar_density       — provided by: command_bar(), filter_bar() (already exists)
_hero_variant      — provided by: hero_effects() (already exists)
_table_align       — provided by: table() (already exists)
_card_variant      — provided by: card()
_accordion_name    — provided by: accordion()
_form_density      — provided by: form()
_nav_current_path  — provided by: sidebar(), navbar(), route_tabs()
```

### Consume Pattern (standardized)

```jinja2
{# Child macro — variant-aware #}
{% set _variant = (variant if variant else consume("_surface_variant", "")) | validate_variant("child-block", ...) %}
```

Every consuming component:
- Checks explicit param first
- Falls back to `consume()` with a safe default
- Validates the result through existing `validate_variant` / `validate_size`

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: key naming, consume patterns, test strategy | 2h | Low | Yes (RFC only) |
| 1 | Surface variant propagation (section, panel, surface) | 4h | Low | Yes |
| 2 | Card variant + accordion name coordination | 3h | Low | Yes |
| 3 | Form density context | 3h | Medium | Yes |
| 4 | Navigation current_path context | 3h | Medium | Yes |
| 5 | Documentation + showcase updates | 3h | Low | Yes |

---

## Sprint 0: Design & Validate

**Goal**: Lock down naming conventions, the consume pattern, and test expectations before writing any template changes.

### Task 0.1 — Finalize context key registry

Document all keys in a `docs/PROVIDE-CONSUME-KEYS.md` reference:
- Key name, provider(s), consumer(s), type, default
- Naming rule: `_<scope>_<property>` (e.g., `_surface_variant`, `_card_variant`)
- Rule: keys are underscore-prefixed to signal "internal chirp-ui context, not user data"

**Acceptance**: `docs/PROVIDE-CONSUME-KEYS.md` exists with all keys from Target Architecture section.

### Task 0.2 — Define test pattern

Establish the two-test pattern for every provide/consume pair:
1. `test_<child>_standalone_no_context` — renders with sensible defaults, no `{% provide %}` wrapper
2. `test_<child>_consumes_<key>_from_parent` — renders with `{% provide _key = value %}` wrapper, asserts class/attribute appears
3. `test_<child>_explicit_overrides_provide` — explicit param beats consumed value

**Acceptance**: Pattern documented; existing hero/table tests already follow it (verify and codify).

### Task 0.3 — Audit kida scoping edge cases

The CLAUDE.md notes: "kida has a scoping issue" with `{% set variant = ... %}` when `variant` is also a macro parameter. Verify:
- Does `consume()` inside a `{% call %}` block read the correct provider?
- Does nested provide (parent provides `_surface_variant`, grandchild consumes) work?
- Does provide inside a `{% for %}` loop scope correctly?

**Files**: Create `tests/test_provide_consume_edge_cases.py`
**Acceptance**: Edge-case tests pass; any kida bugs documented with workarounds.

---

## Sprint 1: Surface Variant Propagation

**Goal**: Components inside `surface()`, `section()`, and `panel()` can auto-detect their surface context.

### Task 1.1 — `surface()` provides `_surface_variant`

Add `{% provide _surface_variant = variant %}` inside `surface.html`.

**Files**: `src/chirp_ui/templates/chirpui/surface.html`
**Acceptance**: `{% provide _surface_variant = "accent" %}` appears in rendered template context.

### Task 1.2 — `section()` and `section_collapsible()` provide `_surface_variant`

These already call `surface(variant=surface_variant)`. After Task 1.1, the surface itself provides. Verify the chain works (section → surface → slot children).

**Files**: `src/chirp_ui/templates/chirpui/layout.html`
**Acceptance**: A component inside `{% call section(surface_variant="accent") %}...{% end %}` can `consume("_surface_variant")` and get `"accent"`.

### Task 1.3 — `panel()` provides `_surface_variant`

Panel wraps surface. Same chain verification as 1.2.

**Files**: `src/chirp_ui/templates/chirpui/panel.html`
**Acceptance**: Same as 1.2 but for panel.

### Task 1.4 — Opt-in consumers: `badge`, `label_overline`, `alert`

These components appear frequently inside surfaces/sections. Add consume-with-fallback for `_surface_variant` so they can auto-adapt (e.g., badge on accent surface uses `muted` variant for contrast).

**Files**: `badge.html`, `label_overline.html`, `alert.html`
**Acceptance**: `rg 'consume.*_surface_variant' src/chirp_ui/templates/` returns hits for each file. Tests cover standalone + parent-provided cases.

### Task 1.5 — Tests for Sprint 1

Add test classes: `TestSurfaceProvide`, `TestSectionSurfaceProvide`, `TestPanelSurfaceProvide`.

**Acceptance**: `uv run pytest tests/test_components.py -k "SurfaceProvide or SectionSurfaceProvide or PanelSurfaceProvide" -q` passes.

---

## Sprint 2: Card Variant + Accordion Name

**Goal**: Cards provide variant to aware children; accordion coordinates name automatically.

### Task 2.1 — `card()` provides `_card_variant`

Add `{% provide _card_variant = variant %}` in `card.html`.

**Files**: `src/chirp_ui/templates/chirpui/card.html`
**Acceptance**: Children inside card slots can consume `_card_variant`.

### Task 2.2 — `label_overline()` consumes `_card_variant`

Label overline inside cards is the primary consumer — it can auto-style based on card variant.

**Files**: `src/chirp_ui/templates/chirpui/label_overline.html`
**Acceptance**: `label_overline()` inside `{% call card(variant="feature") %}` renders with feature-aware styling.

### Task 2.3 — `accordion()` provides `_accordion_name`

Parent provides name; child consumes with fallback to its own `name` param.

**Files**: `src/chirp_ui/templates/chirpui/accordion.html`
**Acceptance**: `accordion_item()` inside `{% call accordion(name="faq") %}` inherits `name="faq"` without explicit param. Standalone `accordion_item(name="faq")` still works.

### Task 2.4 — Tests for Sprint 2

**Acceptance**: `uv run pytest -k "CardProvide or AccordionProvide" -q` passes.

---

## Sprint 3: Form Density Context

**Goal**: `form()` provides density so field wrappers and controls can auto-compact.

### Task 3.1 — `form()` provides `_form_density`

Add `{% provide _form_density = density %}` in `forms.html` (the form macro).

**Files**: `src/chirp_ui/templates/chirpui/forms.html`
**Acceptance**: `{% provide _form_density %}` appears in form macro.

### Task 3.2 — `field_wrapper()` consumes `_form_density`

Field wrapper uses density to adjust spacing/padding classes.

**Files**: `src/chirp_ui/templates/chirpui/forms.html`
**Acceptance**: `field_wrapper()` inside a `form(density="sm")` renders with compact classes. Standalone `field_wrapper()` renders with default density.

### Task 3.3 — Add `density` parameter to `form()` if missing

Check if `form()` already accepts `density`. If not, add it with default `""` (no density = standard).

**Files**: `src/chirp_ui/templates/chirpui/forms.html`
**Acceptance**: `form(density="sm")` renders without error.

### Task 3.4 — CSS for dense form fields

Add `chirpui-field--dense` modifier class with reduced padding/gap.

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `.chirpui-field--dense` exists in CSS. `test_template_css_contract.py` passes.

### Task 3.5 — Tests for Sprint 3

**Acceptance**: `uv run pytest -k "FormDensity" -q` passes. `uv run poe ci` passes.

---

## Sprint 4: Navigation Current Path

**Goal**: Navigation parents provide `current_path` so children don't depend on global template context.

### Task 4.1 — `sidebar()` provides `_nav_current_path`

Add optional `current_path` param to `sidebar()` and provide it.

**Files**: `src/chirp_ui/templates/chirpui/sidebar.html`
**Acceptance**: `sidebar_link()` inside `sidebar(current_path="/settings")` auto-highlights without global `current_path`.

### Task 4.2 — `navbar()` provides `_nav_current_path`

Same pattern as sidebar.

**Files**: `src/chirp_ui/templates/chirpui/navbar.html`
**Acceptance**: `navbar_link()` inside `navbar(current_path="/home")` auto-highlights.

### Task 4.3 — Update `sidebar_link()` and `navbar_link()` to consume

Add `consume("_nav_current_path", "")` as fallback when `current_path` is not in template context.

**Files**: `sidebar.html`, `navbar.html`
**Acceptance**: Navigation links work in three modes: (a) global `current_path`, (b) parent-provided, (c) explicit `active=true`. All existing tests pass.

### Task 4.4 — Tests for Sprint 4

Test all three modes for sidebar and navbar links.

**Acceptance**: `uv run pytest -k "NavProvide" -q` passes. Existing `test_route_tabs.py` unaffected.

---

## Sprint 5: Documentation & Showcase

**Goal**: Document the full provide/consume system and update showcase examples.

### Task 5.1 — Write `docs/PROVIDE-CONSUME-KEYS.md`

Full reference of all context keys with examples.

### Task 5.2 — Update `docs/COMPONENT-OPTIONS.md`

Add "Context-Aware" section to each component that provides or consumes.

### Task 5.3 — Update showcase examples

Add examples showing nested composition with automatic context flow.

### Task 5.4 — Update CLAUDE.md

Add provide/consume expansion to key conventions.

**Acceptance**: `docs/PROVIDE-CONSUME-KEYS.md` exists. COMPONENT-OPTIONS.md references it.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Kida scoping bug with nested provide | Medium | High | Sprint 0 Task 0.3 tests edge cases before any template changes |
| Child consumes wrong key from unrelated parent | Low | Medium | Namespaced keys (`_surface_variant` not `_variant`) reduce collision. Invariant #1 ensures explicit params always win |
| Existing tests break from new provide statements | Low | Low | Provide with no consumer is a no-op in kida; only consumers change behavior |
| `consume()` performance overhead at scale | Low | Low | `consume()` is a dict lookup; negligible vs template rendering |
| Form density CSS conflicts with existing field styles | Medium | Medium | Sprint 3 Task 3.4 adds new modifier class, doesn't change defaults |

---

## Success Metrics

| Metric | Current (0.2.6) | After Sprint 2 | After Sprint 5 |
|--------|-----------------|-----------------|-----------------|
| Templates with `{% provide %}` | 4 | 8 | 12 |
| Templates with `consume()` | 7 | 12 | 18 |
| Context keys in registry | 4 | 7 | 9 |
| Provide/consume test cases | 12 | 28 | 45 |
| Components with documented context-awareness | 0 (ad hoc) | 6 | 18 |

---

## Relationship to Existing Work

- **kida 0.3.4** — prerequisite (already met) — provides the `{% provide %}` / `consume()` primitives
- **PLAN-theme-tokens.md** — parallel — surface variant propagation (Sprint 1) directly supports theme-aware component nesting
- **PLAN-ascii-maturity.md** — complete — ASCII components could later consume surface variant for themed ASCII rendering
- **PLAN-chirpui-alpine-migration.md** — independent — Alpine owns interactive state; provide/consume owns template-time context. No overlap.

---

## Changelog

- **2026-04-12** — Plan audit: Sprints 0-4 verified complete. 16 providers across 12 templates, 23 consumer sites across 17 templates, 45+ tests in test_provide_consume.py. PROVIDE-CONSUME-KEYS.md exists with 12-key registry. `.chirpui-field--dense` CSS shipped. Nav current_path wired in sidebar + navbar. One gap: `label_overline.html` does not consume `_card_variant`/`_surface_variant` despite KEYS.md claiming it does — KEYS.md is aspirational for that component. Sprint 5 (docs polish, showcase updates, COMPONENT-OPTIONS.md context-aware sections) deferred.
- **2026-04-10** — PLAN-behavior-layer-hardening Sprint 2 wired all 7 orphaned provide/consume keys (_card_variant, _bar_surface, _bar_density, _surface_variant, _streaming_role, _suspense_busy, _sse_state) to natural consumers with 30 contract tests. This is a subset of this plan's scope — Sprints 1-4 here (surface propagation, accordion name, form density, nav path) remain future work.
- **2026-04-09** — Draft created from codebase audit (6 provides, 8 consumes across 11 templates)
