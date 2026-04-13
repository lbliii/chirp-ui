# Epic: Sharp Edges Phase 3 — Structural & Behavioral Hardening

**Status**: Complete
**Created**: 2026-04-13
**Target**: 0.4.x
**Estimated Effort**: 18–26h
**Dependencies**: Sharp Edges Phases 1–2 (complete, sprints 0–8)
**Source**: Fresh full-stack audit (2026-04-13) cross-referenced against Phase 1–2 plan. Identified 9 structural/behavioral sharp edges that survive the warning system, API normalization, CSS token, and documentation work.

---

## Why This Matters

Phases 1–2 fixed the *feedback loop* (warnings instead of silence), *naming consistency* (variant/size defaults), *CSS tokens* (replacing hardcoded values), and *documentation coverage* (195/195 templates). But the audit revealed a second class of sharp edges — structural problems where the *shape* of the API or *semantics* of the HTML cause bugs that no amount of warnings can prevent.

**Consequences of the current state:**

1. **`btn()` defaults to `type="submit"`** — 17 instances across 9 templates. Every button inside a `<form>` that omits `type=` silently submits the form. This is the single most common UI bug pattern in web development; a component library should protect against it, not inherit the browser's footgun.
2. **`inline_edit_field` ID collision** — both `inline_edit_field_display()` and `inline_edit_field_form()` fall back to `id="inline-edit-field"` when no `swap_id` is provided. Two edit fields on one page target the same element. Works in development with one field, breaks when you add a second.
3. **`build_hx_attrs()` accepts any key** — `build_hx_attrs(hx={"typo": "/url"})` silently produces `hx-typo="/url"`. No validation against known htmx attributes. Compare to `bem()` which validates modifiers — htmx attributes deserve the same rigor.
4. **`field_errors()` drops non-list values** — `errors={"email": {"code": "invalid"}}` returns `[]`. Some frameworks (DRF, Pydantic) produce nested error dicts. Silent empty result means the form looks error-free.
5. **Pagination uses `<span aria-disabled>` instead of `<button disabled>`** — 2 disabled navigation elements use `<span>` which is not keyboard-focusable and not semantically a control. Screen readers may not announce the disabled state.
6. **Avatar has no decorative mode** — always renders `role="img"`. No way to mark decorative avatars as `role="presentation"`. Lists of avatars (e.g., participant lists where names are shown separately) create screen reader noise.
7. **Alpine `register()` has no idempotency guard per component** — the script-level `__chirpuiAlpineRuntimeLoaded` guard prevents double-loading the entire script, but external callers of `register(name, factory)` can overwrite existing registrations without warning. Store initialization in the catch block unconditionally overwrites.
8. **`localStorage` failures are invisible** — `safeSetItem()` catches all exceptions and does nothing. Theme preference, sidebar state, and other persisted settings silently fail to save. No console warning, no fallback indicator.
9. **Provide/consume contracts undocumented in templates** — 16 providers and 28 consumers across 18 components. Zero have docstrings explaining what context they expect or emit. External docs exist (PROVIDE-CONSUME-KEYS.md) but developers reading a template can't see the contract.

### Evidence Table

| Finding | Source | Proposal Impact |
|---------|--------|-----------------|
| `btn()` type="submit" default | button.html:12 | **FIXES** — Sprint 9 |
| `inline_edit_field` hardcoded fallback ID | inline_edit_field.html:20,38 | **FIXES** — Sprint 9 |
| `build_hx_attrs()` no key validation | filters.py:533-556 | **FIXES** — Sprint 10 |
| `field_errors()` drops dict values silently | filters.py:468-481 | **FIXES** — Sprint 10 |
| Pagination `<span aria-disabled>` not `<button disabled>` | pagination.html:31-32,76-77 | **FIXES** — Sprint 11 |
| Avatar no `role="presentation"` option | avatar.html:13,16-17 | **FIXES** — Sprint 11 |
| Alpine `register()` no idempotency per component | chirpui-alpine.js:106-126 | **FIXES** — Sprint 12 |
| Alpine store init overwrites in catch block | chirpui-alpine.js:128-147 | **FIXES** — Sprint 12 |
| `safeSetItem()` silent failure | chirpui-alpine.js:17-21 | **FIXES** — Sprint 12 |
| Provide/consume not in template docstrings | 18 template files | **FIXES** — Sprint 13 |
| `color-mix(in srgb)` no @supports fallback (172 instances) | chirpui.css | **UNRELATED** — srgb color-mix has >95% browser support; oklch already guarded |

---

### Invariants

1. **All existing tests continue to pass** — no behavioral regression. `uv run poe ci` green before and after each sprint.
2. **No new parameters required at existing call sites** — changes to defaults and semantics must be backward-compatible or use opt-in parameters.
3. **Each sprint ships independently** — partial adoption is safe; no sprint depends on a later sprint.

---

## Target Architecture

No structural rewrite. Same files, same macros. The changes are:

```
button.html:           type="button" default (breaking but correct)
inline_edit_field.html: required swap_id parameter (warn on missing)
filters.py:            build_hx_attrs() warns on unknown htmx keys
                       field_errors() warns on non-list values
pagination.html:       <button disabled> instead of <span aria-disabled>
avatar.html:           decorative=false parameter for role="presentation"
chirpui-alpine.js:     register() skips if name already registered
                       safeSetItem() logs warning on failure
                       store init checks existing data before overwrite
templates (18 files):  docstring annotations for provide/consume contracts
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 9 | Template defaults — button type, inline-edit ID | 3–4h | Medium | Yes ✓ |
| 10 | Filter hardening — hx validation, field_errors | 3–4h | Low | Yes ✓ |
| 11 | Accessibility — pagination, avatar, notification | 3–4h | Low | Yes ✓ |
| 12 | Alpine.js resilience — idempotency, storage, stores | 3–5h | Medium | Yes |
| 13 | Provide/consume docstrings — 18 templates | 4–6h | Low | Yes |

---

## Sprint 9: Template Defaults — Stop the Footguns ✓

**Goal:** Fix the two most common "works in dev, breaks in prod" template defaults.
**Status:** Complete (2026-04-13)

### Task 9.1 — Change `btn()` default to `type="button"`

**Rationale:** The HTML spec defaults `<button>` to `type="submit"`. This is widely considered a design mistake. Every major component library (MUI, Chakra, Radix, Shoelace) defaults to `type="button"`. chirp-ui should too.

**Breaking change:** Call sites that rely on implicit `type="submit"` inside forms will need to add `type="submit"` explicitly. This is the correct trade-off — explicit submit is safer than implicit submit.

**Files:** `src/chirp_ui/templates/chirpui/button.html`
- Line 12: Change `type="submit"` → `type="button"`
- Update docstring (lines 2-3) to document the change
- Audit all 8 other template files that use `type="submit"` to ensure they set it explicitly where needed (auth.html, chat_input.html, confirm.html, forms.html, inline_edit_field.html, shell_actions.html, split_button.html, tag_input.html)

**Acceptance:**
- `rg 'type="submit"' src/chirp_ui/templates/chirpui/button.html` returns zero hits on the macro default line
- All 8 dependent templates explicitly pass `type="submit"` where form submission is intended
- `uv run poe ci` passes

### Task 9.2 — Warn on missing `swap_id` in `inline_edit_field`

**Rationale:** Hardcoded fallback ID `"inline-edit-field"` guarantees collision when two edit fields appear on the same page. Rather than generating random IDs (which break htmx targeting), warn developers when they rely on the default.

**Files:** `src/chirp_ui/templates/chirpui/inline_edit_field.html`
- Keep the fallback ID for backward compatibility
- Emit `ChirpUIValidationWarning` when `swap_id` is not provided
- In strict mode, raise `ValueError`

**Acceptance:**
- `inline_edit_field_display(name="x")` without `swap_id` emits a warning
- `inline_edit_field_display(name="x", swap_id="edit-x")` produces no warning
- `uv run poe ci` passes

---

## Sprint 10: Filter Hardening — Validate What Developers Pass ✓

**Goal:** Make `build_hx_attrs()` and `field_errors()` tell developers when their input is wrong, instead of silently producing wrong output.
**Status:** Complete (2026-04-13)

### Task 10.1 — Validate htmx attribute names in `build_hx_attrs()`

**Rationale:** htmx has a finite set of known attributes. Typos currently become invalid HTML attributes with no feedback.

**Files:** `src/chirp_ui/filters.py`
- Add a `_KNOWN_HX_ATTRS` frozenset (hx-get, hx-post, hx-put, hx-patch, hx-delete, hx-trigger, hx-target, hx-swap, hx-select, hx-push-url, hx-confirm, hx-boost, hx-indicator, hx-include, hx-vals, hx-headers, hx-params, hx-encoding, hx-ext, hx-sync, hx-on, hx-disinherit, hx-select-oob, hx-swap-oob, hx-replace-url, hx-disabled-elt, hx-history, hx-history-elt, hx-preserve, hx-prompt)
- After key normalization, warn if the key is not in `_KNOWN_HX_ATTRS` and doesn't start with `hx-on:` (event handlers are dynamic)
- Do NOT reject — just warn. Custom extensions are valid htmx usage.

**Acceptance:**
- `build_hx_attrs(hx={"typo": "/url"})` emits `ChirpUIValidationWarning`
- `build_hx_attrs(hx={"post": "/save", "target": "#r"})` produces no warning
- `build_hx_attrs(hx={"on:click": "alert(1)"})` produces no warning (valid event handler)
- `uv run poe ci` passes

### Task 10.2 — Warn on non-list field error values

**Rationale:** `field_errors({"email": {"code": "invalid"}}, "email")` returns `[]` — the form shows no errors. Frameworks like DRF and Pydantic can produce nested error structures.

**Files:** `src/chirp_ui/filters.py`
- After the `isinstance(val, (list, tuple))` check, add a warning branch for non-None, non-list values
- Return `[str(val)]` as a best-effort fallback (wraps the value as a single error string)
- Emit `ChirpUIValidationWarning` explaining the expected structure

**Acceptance:**
- `field_errors({"f": {"nested": "err"}}, "f")` returns `[str({"nested": "err"})]` and emits warning
- `field_errors({"f": ["err"]}, "f")` returns `["err"]` with no warning (unchanged behavior)
- `field_errors({"f": "single"}, "f")` returns `["single"]` and emits warning
- `uv run poe ci` passes

---

## Sprint 11: Accessibility — Semantic HTML and ARIA ✓

**Goal:** Fix the accessibility gaps that would fail an axe-core audit.
**Status:** Complete (2026-04-13)

### Task 11.1 — Replace pagination `<span>` with `<button disabled>`

**Rationale:** `<span aria-disabled="true">` is not keyboard-focusable and screen readers may not announce it as a disabled control. `<button disabled>` is the semantically correct element.

**Files:** `src/chirp_ui/templates/chirpui/pagination.html`
- Lines 31-32: Replace `<span ... aria-disabled="true">` with `<button disabled class="...">` for previous button
- Lines 76-77: Same for next button
- Ensure CSS `.chirpui-pagination__link--disabled` styles work on both `<span>` and `<button>` (add `button` reset styles if needed)

**Files (CSS):** `src/chirp_ui/templates/chirpui.css`
- Add button reset for `.chirpui-pagination__link--disabled` if needed (remove default button appearance)

**Acceptance:**
- `rg '<span.*aria-disabled' src/chirp_ui/templates/chirpui/pagination.html` returns zero hits
- Pagination renders `<button disabled>` for previous/next when at bounds
- `uv run poe ci` passes

### Task 11.2 — Add `decorative` parameter to `avatar()`

**Rationale:** In participant lists, avatar groups, and other contexts where the name is shown separately, the avatar is decorative. Currently all avatars get `role="img"` which creates screen reader noise.

**Files:** `src/chirp_ui/templates/chirpui/avatar.html`
- Add `decorative=false` parameter
- When `decorative=true`: render `role="presentation" aria-hidden="true"` instead of `role="img" aria-label="..."`
- When `decorative=false` (default): unchanged behavior

**Acceptance:**
- `avatar(src="x.png", decorative=true)` renders `role="presentation" aria-hidden="true"`
- `avatar(src="x.png")` renders `role="img" aria-label="Avatar"` (unchanged)
- `uv run poe ci` passes

### Task 11.3 — Improve `notification_dot` aria-label

**Rationale:** `aria-label="5"` is meaningless without context. Should be `aria-label="5 notifications"`.

**Files:** `src/chirp_ui/templates/chirpui/notification_dot.html`
- Change `aria-label="{{ count }}"` to `aria-label="{{ count }} notification{{ 's' if count != 1 else '' }}"`
- Add optional `aria_label` parameter for custom override

**Acceptance:**
- `notification_dot(count=5)` renders `aria-label="5 notifications"`
- `notification_dot(count=1)` renders `aria-label="1 notification"`
- `notification_dot(count=5, aria_label="5 unread")` renders `aria-label="5 unread"`
- `uv run poe ci` passes

---

## Sprint 12: Alpine.js Resilience — Idempotency, Storage, Stores ✓

**Goal:** Make Alpine component registration and localStorage safe under hot reload, double-load, and storage-restricted environments.

### Task 12.1 — Add idempotency guard to `register()`

**Rationale:** External callers of `register(name, factory)` can overwrite existing registrations. During htmx swaps and hot reload, components may re-register.

**Files:** `src/chirp_ui/templates/chirpui-alpine.js`
- In the `register()` function, track registered names in a `Set`
- If `name` is already in the set, skip registration and optionally log to console in dev mode
- Apply same guard in the deferred `alpine:init` listener path

**Acceptance:**
- Calling `register("chirpuiDropdown", factory)` twice does not overwrite
- First registration wins; second is silently skipped
- `uv run poe ci` passes

### Task 12.2 — Guard store initialization against data loss

**Rationale:** The catch block in `alpine:init` unconditionally creates new stores, wiping any existing data from prior initialization.

**Files:** `src/chirp_ui/templates/chirpui-alpine.js`
- Change store init to check for existing store data before overwriting
- Pattern: `if (!Alpine.store('modals')) { Alpine.store('modals', {}); }`
- Remove the try/catch pattern — use a simple existence check instead

**Acceptance:**
- Pre-existing store data survives Alpine re-initialization
- New stores are created when missing
- `uv run poe ci` passes

### Task 12.3 — Add console warning to `safeSetItem()`

**Rationale:** Silent storage failures mean theme preference, sidebar state, etc. don't persist with no feedback. A console warning is the minimum viable signal.

**Files:** `src/chirp_ui/templates/chirpui-alpine.js`
- In the catch block of `safeSetItem()`, add `console.warn('chirp-ui: localStorage write failed for key "' + key + '":', e.message)`
- Keep the try/catch — don't throw. Just inform.

**Acceptance:**
- When localStorage throws (quota, private browsing), a console warning appears
- Normal localStorage operations produce no warning
- `uv run poe ci` passes

---

## Sprint 13: Provide/Consume Docstrings — Make the Invisible Visible ✓

**Goal:** Add inline documentation to every template that uses provide/consume, so developers reading the template can see the contract without consulting external docs.

### Task 13.1 — Add provider annotations to 8 provider templates

Add a comment block near each `{% provide %}` statement documenting what is provided and who consumes it.

**Pattern:**
```jinja2
{# @provides _card_variant — consumed by: badge, callout, settings_row, divider #}
{% provide _card_variant = variant %}
```

**Files (8 providers):**
- accordion.html (`_accordion_name`)
- card.html (`_card_variant`)
- command_bar.html (`_bar_surface`, `_bar_density`)
- filter_bar.html (`_bar_surface`, `_bar_density`)
- forms.html (`_form_density`)
- hero_effects.html (`_hero_variant`)
- navbar.html (`_nav_current_path`)
- panel.html / surface.html (`_surface_variant`)

**Acceptance:**
- Every `{% provide %}` has an adjacent `{# @provides ... #}` comment
- `rg '@provides' src/chirp_ui/templates/chirpui/ | wc -l` returns ≥ 16

### Task 13.2 — Add consumer annotations to 10+ consumer templates

Add a comment block near each `consume()` call documenting what is consumed and which parent must provide it.

**Pattern:**
```jinja2
{# @consumes _card_variant from: card — falls back to "" if not in card context #}
{% set _inherited = consume("_card_variant", "") %}
```

**Files (10+ consumers):**
- badge.html, alert.html, button.html, callout.html, copy_button.html, divider.html, icon_btn.html, navbar.html (navbar_link, navbar_dropdown), settings_row.html, and visual effect templates (constellation, holy_light, meteor, particle_bg, rune_field)

**Acceptance:**
- Every `consume()` call has an adjacent `{# @consumes ... #}` comment
- `rg '@consumes' src/chirp_ui/templates/chirpui/ | wc -l` returns ≥ 28

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `type="button"` default breaks existing forms | Medium | Medium | Sprint 9 audits all 8 dependent templates; CHANGELOG entry warns upgraders |
| htmx attribute validation is too strict | Low | Low | Sprint 10 uses warn-only, never rejects; `hx-on:*` pattern exempted |
| Pagination `<button>` styling differs from `<span>` | Low | Low | Sprint 11 adds button reset CSS |
| Alpine idempotency guard breaks legitimate re-registration | Low | Medium | Sprint 12 uses name-based Set, not factory comparison; intentional override remains possible via direct Alpine.data() |

---

## Success Metrics

| Metric | Current (Post Phase 2) | After Phase 3 |
|--------|----------------------|---------------|
| Silent wrong-output paths in filters | 2 (field_errors, build_hx_attrs) | 0 |
| Hardcoded fallback IDs | 1 (inline_edit_field) | 0 (warns) |
| `<span aria-disabled>` instead of `<button disabled>` | 2 | 0 |
| Components with `role="img"` and no decorative option | 1 (avatar) | 0 |
| Provide/consume statements with inline documentation | 0/43 | 43/43 |
| Alpine components with idempotency guard | 0 | all |
| Silent localStorage failures | all | 0 (console.warn) |

---

## Relationship to Existing Work

- **Sharp Edges Phase 1–2** — prerequisite, complete. Phase 3 addresses the structural/behavioral layer that Phase 1–2's warning/normalization/token work couldn't fix.
- **PLAN-behavior-layer-hardening** — may overlap on Alpine.js; check for conflicts before Sprint 12.
- **PLAN-test-coverage-hardening** — Sprint 10 filter changes need new tests; coordinate.

---

## Changelog

- 2026-04-13: Draft created from Phase 3 audit findings
- 2026-04-13: Sprint 9 complete — btn() defaults to type="button", inline_edit_field warns on missing swap_id, check_required_id filter added
- 2026-04-13: Sprint 10 complete — build_hx_attrs() validates htmx attr names (33 known attrs, hx-on:* exempt), field_errors() warns and coerces non-list values
- 2026-04-13: Sprint 11 complete — pagination uses <button disabled>, avatar gets decorative= param, notification_dot aria-label contextualizes count
