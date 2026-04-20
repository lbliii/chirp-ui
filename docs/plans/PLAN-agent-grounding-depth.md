# Epic: Agent Grounding Depth — make the manifest the whole registry

**Status**: Draft
**Created**: 2026-04-20
**Target**: pre-1.0
**Estimated Effort**: 30–48h (Sprint 0–6)
**Dependencies**: None (builds on shipped `chirpui-manifest@1`)
**Source**: Vibe-coding readiness evaluation — see conversation 2026-04-20 and `docs/VISION.md § Agent-groundable manifest`

---

## Why This Matters

The manifest is the one bet (`docs/VISION.md`). Today it grounds the **CSS class surface** but not the **macro Python API**, so coding agents that "ground in the manifest" still have to grep templates to call a macro — re-introducing the hallucination risk the registry was built to eliminate.

1. **Manifest descriptors lack call signatures.** `metric_card` has 11 parameters in the macro definition (`value, label, icon, trend, trend_direction, hint, href, icon_bg, footer_label, footer_href, attrs_*`); the manifest entry exposes `slots: []`, `variants: []`, no `params` field. An agent reading the manifest cannot construct a valid call.
2. **64/309 components are signature-opaque from the manifest** — they have a `template` but neither slots nor variants nor params. 110/309 are `category=auto` (descriptor coverage gap).
3. **Slot lists drift from `{% slot %}` reality.** Hand-authored `slots` field in `ComponentDescriptor` is what the manifest reports; `metric_card` uses `card`'s slots transitively but reports `[]`.
4. **`COMPONENT-OPTIONS.md` is 3,594 lines of hand-authored API reference.** A 3.5k-line markdown doc is the same drift problem as Tailwind's class strings — exactly the failure mode the registry-as-source-of-truth thesis exists to prevent. It must become a *projection* of the manifest, not a parallel source.
5. **Manifest is not shipped with the wheel.** `site/public/chirpui.manifest.json` only exists after `poe docs-build-all`. An agent doing zero-shot grounding (no build step) cannot read it. There's no `from chirp_ui import MANIFEST_PATH`.
6. **31 `PLAN-*.md` files in `docs/` mix completed and in-flight.** `PLAN-sharp-edges.md` (complete) and `PLAN-css-scope-and-layer.md` (in progress) sit in the same folder. Agents cite stale plans as current truth.
7. **`{#- chirp-ui: ... #}` doc-block convention is excellent but optional.** Only 32/195 templates carry it. Where present (e.g. `card.html`, `button.html`), it's the highest-signal piece of agent-readable intent in the codebase.

The fix is to deepen descriptors so the manifest is a complete projection of every component's public Python surface — params, slots, doc-block, all auto-extracted from the macro source — and to make that manifest reachable from package data.

### Evidence

| Layer/Source | Key Finding | Proposal Impact |
|--------------|-------------|-----------------|
| `chirp_ui.manifest.build_manifest()` | 309 entries; descriptor schema has no `params` field | FIXES (Sprint 1) |
| `metric_grid.html` macro | 11 params; manifest reports zero | FIXES (Sprint 1) |
| `chirp_ui.components.ComponentDescriptor` fields | `slots` is hand-authored; drifts from `{% slot %}` reality | FIXES (Sprint 2) |
| `site/public/chirpui.manifest.json` | Doesn't exist in `src/chirp_ui/` package data | FIXES (Sprint 3) |
| `grep -l "{#- chirp-ui:" templates/chirpui/*.html` | 32/195 templates carry doc-block | FIXES (Sprint 4) |
| `wc -l docs/COMPONENT-OPTIONS.md` | 3,594 lines hand-authored | FIXES (Sprint 5) |
| `ls docs/PLAN-*.md` | 31 plans, completed and in-flight intermixed | FIXES (Sprint 6) |
| `grep -l "@provides\|@consumes" templates/chirpui/*.html` | 24/195 templates annotated; `PROVIDE-CONSUME-KEYS.md` is the doc | MITIGATES (Sprint 4 doc-block can include provides/consumes; full coverage is out-of-scope) |

### Invariants

These must remain true throughout or we stop and reassess:

1. **Schema stability**: `chirpui-manifest@1` consumers don't break. Bump to `@2` is additive only — `params` and `description` fields appear; existing fields keep their meaning. Old keys are not removed in this epic.
2. **Determinism**: `python -m chirp_ui.manifest --json` continues to produce byte-identical output across runs. Sort order, field set, escaping all stable.
3. **Registry stays the single source of truth**: every new manifest field is *derived* from the descriptor or template source. No field is hand-authored in the manifest itself; if it can't be derived, it goes in the descriptor.
4. **Free-threading-compatible tooling only**: parsers, builders, CI scripts must be pure-Python (per `AGENTS.md`). No regex-based template parsing escalates into pulling in a JIT/parser dependency that fails on 3.14t.

---

## Target Architecture

End state: `chirpui-manifest@2`, shipped as package data, with each component entry carrying its full Python surface.

```jsonc
{
  "schema": "chirpui-manifest@2",
  "version": "0.X.Y",
  "components": {
    "metric-card": {
      "block": "metric-card",
      "category": "data-display",
      "template": "metric_grid.html",
      "macro": "metric_card",                    // NEW — macro name in template
      "description": "Overview/KPI wrapper ...", // NEW — from {#- chirp-ui: ... -#} doc-block
      "params": [                                // NEW — auto-extracted from {% def %}
        {"name": "value",          "default": null,         "kind": "positional"},
        {"name": "label",          "default": null,         "kind": "positional"},
        {"name": "icon",           "default": "none",       "kind": "keyword"},
        {"name": "trend",          "default": "none",       "kind": "keyword"},
        {"name": "trend_direction","default": "\"\"",       "kind": "keyword"},
        {"name": "hint",           "default": "none",       "kind": "keyword"},
        {"name": "href",           "default": "none",       "kind": "keyword"},
        {"name": "icon_bg",        "default": "\"\"",       "kind": "keyword"},
        {"name": "footer_label",   "default": "none",       "kind": "keyword"},
        {"name": "footer_href",    "default": "none",       "kind": "keyword"},
        {"name": "attrs_map",      "default": "none",       "kind": "keyword"}
      ],
      "slots": ["", "header_actions", "media", "body_actions", "footer"],  // auto + hand-merged
      "variants": [],
      "sizes": [],
      "modifiers": [],
      "elements": [...],
      "emits": [...],
      "provides": ["_card_variant"],   // NEW — from @provides annotation
      "consumes": []                   // NEW — from @consumes annotation
    }
  },
  "tokens": {...},
  "stats": {...}
}
```

Surface contract:

```python
# Importable, offline, zero-build
from chirp_ui import MANIFEST_PATH, load_manifest
manifest = load_manifest()                # cached dict
metric_card = manifest["components"]["metric-card"]
print(metric_card["params"])              # full call signature
```

CLI:

```bash
python -m chirp_ui.manifest --json        # existing — unchanged contract, schema bumped
python -m chirp_ui find dashboard         # NEW — search by name/category/description
python -m chirp_ui find --category=data-display
```

Docs:

```
docs/COMPONENT-OPTIONS.md                  # hand-authored guides + generated API tables
docs/plans/                                # in-flight plans (PLAN-*.md)
docs/plans/done/                           # completed plans
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: parser strategy, schema bump, packaging path | 4h | Low | Yes (RFC only) |
| 1 | Auto-extract macro signatures → `params` field | 8h | Medium | Yes |
| 2 | Auto-extract slots + provides/consumes from templates | 6h | Medium | Yes |
| 3 | Ship manifest as package data + `MANIFEST_PATH` API | 4h | Low | Yes |
| 4 | Doc-block extraction → `description` field; backfill policy | 8h | Low | Yes |
| 5 | Generate `COMPONENT-OPTIONS.md` API tables from manifest | 8h | Medium | Yes |
| 6 | Plan triage (`docs/plans/done/`) + `chirp_ui find` CLI | 4h | Low | Yes |

Each sprint produces a self-contained PR. Sprint 0 is paper-only; Sprints 1–6 each leave the manifest more grounding-capable than before, with no half-converted state.

---

## Sprint 0: Design & Validate

**Goal**: Solve the three fork-in-the-road decisions on paper before writing a parser.

### Task 0.1 — Pick the macro-source parser strategy

Choose between:
- **(a)** Regex on `{% def name(params...) %}` (pure-Python, ~30 LOC, fragile to grammar drift)
- **(b)** Kida AST API if exposed (precise, dependency on kida internals)
- **(c)** Hybrid: try (b), fall back to (a)

Decision criteria: free-threading-safe (rules out anything GIL-gated), zero new runtime deps, must handle multi-line `{% def %}` bodies and default values containing `,` (e.g. `attrs_map=none`).

**Acceptance**: One-page RFC committed at `docs/DESIGN-manifest-signature-extraction.md` naming the chosen strategy, with a worked example for `btn` and `metric_card` showing the extracted shape.

### Task 0.2 — Lock in the schema bump (`@1` → `@2`)

Specify additively: new fields (`macro`, `description`, `params`, `provides`, `consumes`); existing fields unchanged. Document the migration story for downstream consumers (none break; the new fields just appear).

**Acceptance**: Schema diff in the RFC + a frozen JSON-Schema-style description of `@2`. Existing `@1` consumers still validate against the relevant subset.

### Task 0.3 — Decide manifest packaging mechanism

Pick: build-time generation into `src/chirp_ui/manifest.json` (committed) vs. runtime build inside `load_manifest()` cached on first call.

Constraint: `from chirp_ui import MANIFEST_PATH` must work after `pip install chirp-ui` with no build step on the consumer's machine. Free-threading-safe caching.

**Acceptance**: RFC names the chosen approach + lists the CI gate that prevents `manifest.json` from going stale (similar to `poe build-css-check`).

---

## Sprint 1: Auto-extract macro signatures

**Goal**: Every descriptor surfaces a `params` list in the manifest, derived from the macro source.

### Task 1.1 — Build the parser

Implement the strategy chosen in Task 0.1. Module: `src/chirp_ui/_macro_introspect.py` (underscore-prefixed, internal).

**Files**: `src/chirp_ui/_macro_introspect.py` (new), `src/chirp_ui/components.py` (reads parser output).
**Acceptance**:
- `uv run python -c "from chirp_ui._macro_introspect import macro_signature; print(macro_signature('chirpui/metric_grid.html', 'metric_card'))"` returns the 11-param list.
- Round-trips correctly for `btn`, `card`, `form`, `metric_card`, `field_wrapper` (largest signatures).

### Task 1.2 — Wire `params` into the descriptor + manifest

Add `params` field to `ComponentDescriptor` and to the manifest emit in `chirp_ui/manifest.py`. Bump `SCHEMA = "chirpui-manifest@2"`.

**Files**: `src/chirp_ui/components.py`, `src/chirp_ui/manifest.py`.
**Acceptance**:
- `python -m chirp_ui.manifest --json` shows `"params"` for every component with a discoverable macro.
- `m["components"]["metric-card"]["params"]` has 11 entries.
- Manifest output remains deterministic: two consecutive runs are byte-identical (`diff <(python -m chirp_ui.manifest --json) <(python -m chirp_ui.manifest --json)` returns nothing).

### Task 1.3 — Tests

Add `tests/test_manifest_signatures.py` covering:
- 5 representative macros (positional, defaults, `none`-defaulted, multi-kwarg).
- Components with no template (`category=auto`) emit `params: []`, not an error.
- Schema field is `chirpui-manifest@2`.

**Acceptance**: `uv run poe ci` green; new tests pass.

---

## Sprint 2: Auto-extract slots + provides/consumes

**Goal**: Eliminate hand-authored `slots` drift; surface `provides`/`consumes` in the manifest.

### Task 2.1 — Slot parser

Parse `{% slot name %}` (and unnamed default slot) from the macro body. Merge with hand-authored `descriptor.slots` (descriptor wins where they disagree, but emit a warning so drift is visible).

**Files**: `src/chirp_ui/_macro_introspect.py`, `src/chirp_ui/components.py`.
**Acceptance**:
- `m["components"]["card"]["slots"]` includes `["", "header_actions", "media", "body_actions", "footer"]`.
- New test `test_slot_parity` warns when descriptor and parsed slots disagree.

### Task 2.2 — Provides/consumes from `@provides` / `@consumes` annotations

Parse the existing `{# @provides _key — consumed by: ... #}` and `{# @consumes _key from: ... #}` comment annotations. Emit as `provides: [...]`, `consumes: [...]` in the manifest entry.

**Files**: `src/chirp_ui/_macro_introspect.py`, `src/chirp_ui/manifest.py`.
**Acceptance**:
- `m["components"]["card"]["provides"]` includes `_card_variant`.
- `m["components"]["btn"]["consumes"]` includes `_bar_density`, `_suspense_busy`.
- 24/195 currently-annotated templates surface their keys without manual descriptor edits.

### Task 2.3 — Update `docs/PROVIDE-CONSUME-KEYS.md` to be a projection

Add a CI gate: keys in the manifest must match keys in `docs/PROVIDE-CONSUME-KEYS.md`. Drift fails CI, just like `test_template_css_contract.py`.

**Files**: `tests/test_provide_consume_doc_parity.py` (new).
**Acceptance**: Test fails when a documented key disappears from the manifest, or when a manifest key is undocumented.

---

## Sprint 3: Ship manifest as package data

**Goal**: `from chirp_ui import MANIFEST_PATH` works after a clean `pip install`.

### Task 3.1 — Build-time emission of `manifest.json`

Add `scripts/build_manifest.py` (pure-Python, stdlib-only). Wire into `poe ci` as `poe build-manifest` + `poe build-manifest-check` (matching the existing `poe build-css` / `poe build-css-check` pattern).

**Files**: `scripts/build_manifest.py` (new), `pyproject.toml` (poe tasks), `src/chirp_ui/manifest.json` (generated, committed).
**Acceptance**:
- `uv run poe build-manifest` regenerates the file deterministically.
- `uv run poe build-manifest-check` fails if the committed file is stale.
- `pyproject.toml` lists `manifest.json` under package data.

### Task 3.2 — Public API: `MANIFEST_PATH`, `load_manifest()`

Expose from `chirp_ui.__init__`:

```python
from importlib.resources import files
MANIFEST_PATH = files("chirp_ui").joinpath("manifest.json")

@functools.cache
def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
```

Cache must be free-threading-safe; `functools.cache` on a no-arg function is OK under 3.14t.

**Files**: `src/chirp_ui/__init__.py`, `tests/test_public_api.py`.
**Acceptance**:
- `uv run python -c "from chirp_ui import MANIFEST_PATH, load_manifest; print(load_manifest()['stats']['total_components'])"` prints 309+.
- `MANIFEST_PATH` exists post-install in a fresh venv.

---

## Sprint 4: Doc-block extraction + backfill policy

**Goal**: Every component carries an agent-readable description in the manifest.

### Task 4.1 — Parse `{#- chirp-ui: ... -#}` block

Extract the leading doc-comment from each template; emit as `description` per descriptor.

**Files**: `src/chirp_ui/_macro_introspect.py`, `src/chirp_ui/manifest.py`.
**Acceptance**: 32 currently-annotated templates surface their description in the manifest. Components without a doc-block emit `description: ""` (not error).

### Task 4.2 — Promote doc-block to a contract for new components

Add `tests/test_doc_block_required_for_new_components.py`: for any template added in this PR or later, doc-block is required. Existing untouched templates are grandfathered.

**Acceptance**: Adding a new template without a doc-block fails CI. The 163 existing templates without one don't fail (opportunistic backfill, per chirp-ui's "envelope conversion" policy).

### Task 4.3 — Document the policy in `AGENTS.md` and `CLAUDE.md`

Add to `AGENTS.md § Done criteria`: "New component → doc-block present (`{#- chirp-ui: ... -#}`)." Add to `CLAUDE.md § Adding a component`: doc-block is step 1.

**Acceptance**: Both files updated in the same PR.

---

## Sprint 5: Generate COMPONENT-OPTIONS.md from the manifest

**Goal**: Stop the 3,594-line drift problem. Hand-authored guides stay; reference tables become projections.

### Task 5.1 — Identify the hand-authored vs. generated boundary

Read `docs/COMPONENT-OPTIONS.md`; classify each section as:
- **Generated** (params/variants/sizes/slots reference tables — most of the file)
- **Guides** (Strict mode, Slot Reference narrative, Macro Slot Context, Icon registry — keep hand-authored)

**Acceptance**: A diff annotation in the PR description showing the split. Estimated: ~3,000 lines generated, ~500 lines hand-authored.

### Task 5.2 — Build the generator

`scripts/build_component_options.py`. Reads the manifest, emits markdown sections wrapped between `<!-- chirpui:generated:start -->` / `<!-- chirpui:generated:end -->` markers so hand-authored content can interleave.

**Files**: `scripts/build_component_options.py` (new), `pyproject.toml`.
**Acceptance**:
- `uv run poe build-docs` regenerates the file.
- `uv run poe build-docs-check` fails if generated sections are stale.
- Hand-authored sections survive a regenerate cycle untouched.

### Task 5.3 — Migrate

Run the generator; commit the new file. Verify the content is at least as complete as the prior hand-authored version (no component lost, no parameter dropped).

**Acceptance**: Manual diff review in PR. Old `COMPONENT-OPTIONS.md` lines preserved or accounted for.

---

## Sprint 6: Plan triage + find CLI

**Goal**: Reduce noise in `docs/`; give agents a way to discover components by purpose.

### Task 6.1 — Sort PLAN-*.md by status

Create `docs/plans/done/` and `docs/plans/`. Move each `PLAN-*.md` into one or the other based on a status-line scan (or per-file confirmation). Update `docs/INDEX.md` to point at both.

**Acceptance**:
- `ls docs/PLAN-*.md` returns nothing (all moved).
- `ls docs/plans/*.md` lists in-flight plans only (~5).
- `ls docs/plans/done/*.md` lists completed plans (~26).
- Old paths redirect via INDEX entries.

### Task 6.2 — `python -m chirp_ui find` CLI

Search the manifest by name + category + description.

```bash
python -m chirp_ui find dashboard
# → metric-card, metric-grid, animated-stat-card, stat, ...
python -m chirp_ui find --category=feedback
# → alert, callout, empty-state, sse-status, ...
```

**Files**: `src/chirp_ui/find.py` (new), `src/chirp_ui/__main__.py` (dispatch).
**Acceptance**:
- `uv run python -m chirp_ui find metric` lists at least `metric-card`, `metric-grid`, `animated-stat-card`.
- Output is a stable, sorted list with `name | category | one-line description`.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Kida `{% def %}` grammar evolves; regex parser breaks | Medium | High | Sprint 0 RFC picks a strategy that survives at least the current minor (0.4.x); pin parser tests to canonical macros (`btn`, `card`, `form`, `metric_card`); preference for kida AST API if exposed. |
| Schema bump (`@1` → `@2`) breaks downstream consumers | Low | High | Invariant 1 — additive only. New fields appear; nothing is removed. Document explicitly in the RFC and in `CHANGELOG.md`. |
| Auto-extracted slots disagree with hand-authored descriptor; tests start failing | Medium | Medium | Sprint 2 task 2.1 — descriptor wins, parser warns. Triaged opportunistically per component, not as a blocker. |
| `manifest.json` shipped in package data goes stale because contributor forgets `poe build-manifest` | High | Medium | Sprint 3 task 3.1 — `poe build-manifest-check` CI gate, same pattern as `poe build-css-check`. |
| Generating COMPONENT-OPTIONS.md drops a hand-authored caveat | Medium | Medium | Sprint 5 task 5.2 — markered regions; hand-authored sections preserved. Manual diff review in Sprint 5 task 5.3. |
| Backfilling 163 doc-blocks is grindy; gets abandoned half-done | High | Low | Sprint 4 task 4.2 — opportunistic policy (per `AGENTS.md` envelope-conversion convention). New templates required; existing grandfathered. No big-bang. |
| `chirp_ui find` becomes a half-built second discovery path | Low | Low | Sprint 6 task 6.2 — minimal scope (search 3 fields). If usage grows, expand later. |

---

## Success Metrics

| Metric | Current (2026-04-20) | After Sprint 3 | After Sprint 6 (Final) |
|--------|---------------------|----------------|------------------------|
| Components with full Python signature in manifest | 0/309 | 309/309 | 309/309 |
| Components with description in manifest | 0/309 | 0/309 | 32/309 (existing doc-blocks); rising opportunistically |
| Components with `provides`/`consumes` in manifest | 0/309 | 24/309 | 24/309 (rising opportunistically) |
| Manifest reachable offline via `from chirp_ui import MANIFEST_PATH` | No | Yes | Yes |
| `COMPONENT-OPTIONS.md` hand-authored lines | 3,594 | 3,594 | ~500 |
| `docs/PLAN-*.md` in active mix | 31 (mixed) | 31 | ~5 in-flight, rest in `done/` |
| Categorical bet (Vision § The flywheel) — agent grounds in registry, not template grep | Partial | Substantial | Complete for params/slots/description |

---

## Relationship to Existing Work

- **`docs/VISION.md § Agent-groundable manifest`** — prerequisite vision; this epic is the first concrete delivery against the "registry as one bet" thesis beyond CSS class coverage.
- **`docs/plans/PLAN-css-scope-and-layer.md`** — parallel; CSS is the *other* projection of the registry. This epic projects the *Python API*; together they make the registry a complete source of truth.
- **`docs/plans/done/PLAN-descriptor-coverage.md`** — prerequisite-ish; raises descriptor coverage from the current ~64% (110/309 are `category=auto`). The two epics can interleave: this one consumes whatever descriptors exist, drift is enforced by parity tests.
- **`docs/PROVIDE-CONSUME-KEYS.md`** — Sprint 2 task 2.3 makes this doc a projection rather than a hand-authored register.
- **`AGENTS.md`** — Sprint 4 task 4.3 amends it. The escape-hatch and done-criteria sections are load-bearing for agents using the new contract.

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-20 | Initial draft | Vibe-coding readiness eval surfaced the descriptor-depth gap as the single highest-leverage move |
