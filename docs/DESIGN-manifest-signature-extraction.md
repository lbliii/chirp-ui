# DESIGN: Manifest Signature Extraction

**Status**: Locked — Sprint 0 of `docs/plans/PLAN-agent-grounding-depth.md`
**Created**: 2026-04-20
**Decisions cover**: parser strategy, schema bump (`@1`→`@2`), packaging mechanism
**One-line summary**: Use `kida.analysis.Template.def_metadata()` for AST-derived fields; tiny regex for comment-only fields; ship a build-time-generated `manifest.json` as package data, gated by a `poe build-manifest-check` CI hook modeled on `poe build-css-check`.

---

## Decision 1 — Parser strategy: kida.analysis (zero parser to maintain)

### Investigation

`kida ≥ 0.6.0` (current pin) ships `kida.analysis` with first-class def introspection:

```python
# kida.analysis.metadata
@dataclass(frozen=True, slots=True)
class DefParamInfo:
    name: str
    annotation: str | None
    has_default: bool
    is_required: bool

@dataclass(frozen=True, slots=True)
class DefMetadata:
    name: str
    template_name: str | None = None
    lineno: int = 0
    params: tuple[DefParamInfo, ...] = ()
    slots: tuple[str, ...] = ()              # named {% slot name %} usages
    has_default_slot: bool = False           # unnamed {% slot %} present
    depends_on: frozenset[str] = frozenset() # context paths read in body
```

Surfaced via `Template.def_metadata() -> dict[str, DefMetadata]`. Empirically verified on `chirpui/metric_grid.html` (using the test stubs from `tests/conftest.py` so chirp-ui filters resolve at compile-time):

```text
metric_card:
  params: [('value', False, True), ('label', False, True),
           ('icon', True, False), ('trend', True, False),
           ('trend_direction', True, False), ('hint', True, False),
           ('href', True, False), ('icon_bg', True, False),
           ('footer_label', True, False), ('footer_href', True, False),
           ('cls', True, False), ('attrs', True, False),
           ('attrs_unsafe', True, False), ('attrs_map', True, False)]
  slots: ()
  has_default_slot: False
metric_grid:
  params: [('cols', True, False), ('gap', True, False), ('cls', True, False)]
  slots: ()
  has_default_slot: False
```

This is exactly the shape the manifest needs. `metric_card`'s empty `slots` is *correct* — that macro doesn't have direct `{% slot %}` calls; it composes `card()`, which is the macro that owns the slot vocabulary. The descriptor's `slots` field stays as the consumer-facing surface; kida's parsed slots become a parity-check signal.

### Decision

**Primary**: use `kida.analysis.Template.def_metadata()` for everything AST-derived: `params`, direct `slots`, `has_default_slot`, `depends_on`, `lineno`, `template_name`.

**Comments-only fallback**: kida's AST drops `{# ... #}` comments. Two pieces of metadata live in comments only:
- `{#- chirp-ui: <description> -#}` — leading doc-block convention (32/195 templates today).
- `{# @provides _key #}` and `{# @consumes _key from: ... #}` — context-flow annotations (24/195 templates today).

For these, parse the raw template source with two small stdlib `re` patterns (~10 LOC total). No third-party parser. No new runtime dependency.

### Why not pure regex on `{% def %}`

Considered. Rejected:
- Multi-line `{% def %}` signatures (`btn` is 4 lines) and default values containing commas (`attrs_map=none`, `cls=""`) make the regex non-trivial; it's the kind of code that almost works.
- Maintenance burden: when kida grammar evolves (already on 0.6.0; pre-1.0), every grammar tweak risks silent breakage.
- We'd be rebuilding what kida already gives us.

### Why not embed kida's full template-resolver

Considered for `slots`-via-composition (e.g. surface `card`'s slots when `metric_card` is queried). Rejected for Sprint 1: the registry's hand-authored `slots` field already serves that purpose, and conflating direct vs. transitive slots makes the manifest field ambiguous. Sprint 2 keeps direct slots from kida and treats the descriptor field as the consumer-facing override.

### Free-threading safety

`kida` ships `_Py_mod_gil = 0` and the `BlockAnalyzer` docstring states "Thread-safe: Stateless analyzers, creates new result objects." The manifest builder does not share kida `Template` instances across threads anyway — manifest generation is build-time, single-threaded. No GIL-gated dependencies introduced.

### Worked example: `btn`

```text
btn:
  params: [
    ('label', False, True),
    ('variant', True, False), ('size', True, False),
    ('loading', True, False), ('type', True, False),
    ('href', True, False), ('icon', True, False), ('cls', True, False),
    ('attrs', True, False), ('attrs_unsafe', True, False), ('attrs_map', True, False),
    ('hx', True, False),
    ('hx_get', True, False), ('hx_post', True, False), ('hx_put', True, False),
    ('hx_patch', True, False), ('hx_delete', True, False),
    ('hx_target', True, False), ('hx_swap', True, False),
    ('hx_trigger', True, False), ('hx_include', True, False), ('hx_select', True, False),
    ('hx_ext', True, False), ('hx_vals', True, False),
    ('disabled', True, False), ('data_action', True, False), ('aria_label', True, False),
  ]
  slots: ()
  has_default_slot: False
  depends_on: frozenset({'_bar_density', '_suspense_busy'})  # — also gives us 'consumes' for free
```

Note: `depends_on` appears to give us `consumes` automatically — the AST already tracks which context paths the macro reads. Sprint 2 should evaluate using `depends_on` as the source for `consumes` instead of regex on annotations. Annotations remain useful for *human-readable comment-cited intent*, but the AST is authoritative for what's actually read.

---

## Decision 2 — Schema bump: `chirpui-manifest@1` → `chirpui-manifest@2` (additive only)

### New fields per component

```jsonc
{
  "metric-card": {
    // === existing @1 fields, unchanged ===
    "block": "metric-card",
    "category": "data-display",
    "template": "metric_grid.html",
    "variants": [], "sizes": [], "modifiers": [],
    "elements": [...], "slots": [...], "tokens": [],
    "extra_emits": [], "emits": [...],

    // === new @2 fields ===
    "macro": "metric_card",                     // macro identifier in the template; null for descriptors with no template
    "params": [                                 // from kida DefParamInfo
      {"name": "value", "has_default": false, "is_required": true},
      {"name": "label", "has_default": false, "is_required": true},
      {"name": "icon",  "has_default": true,  "is_required": false},
      // ... 11 more
    ],
    "description": "Overview/KPI wrappers for dashboard-style pages...",  // from {#- chirp-ui: ... -#} block; "" if absent
    "provides": ["_card_variant"],              // hand-authored {# @provides _key #} comment annotations
    "consumes": ["_bar_density", "_suspense_busy"],  // from kida DefMetadata.depends_on (filtered to underscore-prefixed keys)
    "has_default_slot": false,                  // from kida DefMetadata; true when {% slot %} (unnamed) appears
    "lineno": 16                                // source line of {% def %} — useful for editor jump-to-def
  }
}
```

### Field semantics

| Field | Source | Type | Empty value | Notes |
|-------|--------|------|-------------|-------|
| `macro` | template AST | `str \| null` | `null` | Null when descriptor has no template (e.g. CSS-only `auto` category). |
| `params` | kida `DefParamInfo` | array of `{name, has_default, is_required}` | `[]` | `is_required = !has_default`. Annotation field omitted in @2 (kida always emits `null` here today). |
| `description` | regex on raw source | `str` | `""` | Stripped & dedented. First paragraph of the `{#- chirp-ui: ... -#}` doc-block. Newlines collapsed to spaces in a planned `description_short` future field — out of scope for @2. |
| `provides` | regex on raw source | `array[str]` | `[]` | Sourced from `{# @provides _key — consumed by: ... #}` annotations. Sorted. |
| `consumes` | kida `depends_on` (filtered to keys starting with `_`) | `array[str]` | `[]` | Authoritative source is the AST, not the annotation. Annotation comment becomes a documentation aid; manifest publishes the AST truth. |
| `has_default_slot` | kida `DefMetadata` | `bool` | `false` | |
| `lineno` | kida `DefMetadata` | `int` | `0` | |

### Migration story for downstream consumers

- **@1 schema consumers** (none external known today; `site/public/chirpui.manifest.json` consumers internal): unaffected. Every @1 field keeps its meaning. New fields are ignored by code that doesn't know about them. JSON ordering (`sort_keys=True`) means added keys interleave alphabetically — does not shift existing keys' position.
- **`stats` block**: gains optional aggregate counts (`components_with_params`, `components_with_description`) — additive.
- **Tests**: `tests/test_manifest_schema.py` (new) asserts `schema == "chirpui-manifest@2"` and that every component has at least the @1 fields. `@1` snapshot tests, if any, get a one-line bump.

### What's deliberately NOT in @2

Kept out to limit blast radius:
- **Param annotations** (`DefParamInfo.annotation`). Kida emits `null` today; surface when kida starts populating it.
- **Per-param defaults** (literal value of `=none`, `=""`). Encoding defaults as JSON is its own can of worms (kida nodes vs JSON-safe representation). Defer until a consumer asks.
- **Transitive slots** (slots inherited from composed macros, e.g. `metric_card` → `card`). Requires walking `Include`/`FuncCall` graph; out of Sprint 1's scope. The descriptor's hand-authored `slots` covers consumer-facing API for now.
- **Source-of-truth markers**. Whether a field is "auto-extracted" vs "hand-authored" is implicit (params/description/consumes auto; variants/sizes/modifiers/slots hand). Not worth a field today.

### Schema version policy

`chirpui-manifest@N` is a string discriminator, not a semver. Additive changes increment N. A hypothetical breaking change (removing/repurposing a field) would be `@3` and ship simultaneously with a deprecation cycle on `@2`. We follow the same "deprecation policy" model as the rest of chirp-ui (`CLAUDE.md § Deprecation policy`).

### Invariant preserved

Determinism (per `chirp_ui/manifest.py` docstring): `python -m chirp_ui.manifest --json` produces byte-identical output across runs. New fields use `sort_keys=True`-friendly types (lists sorted at emission, dicts ordered alphabetically). Verified by extending the existing determinism test.

---

## Decision 3 — Packaging mechanism: build-time JSON, mirror the CSS pattern

### Pattern reference

The CSS build is the proven precedent in this repo (`scripts/build_chirpui_css.py`, `pyproject.toml § build-css` / `build-css-check`):

```toml
build-css       = { cmd = "python scripts/build_chirpui_css.py",          help = "..." }
build-css-check = { cmd = "python scripts/build_chirpui_css.py --check",  help = "Fail if chirpui.css is stale relative to partials" }
```

The manifest follows the same shape. Same script style (pure-Python, stdlib-only, deterministic). Same `--check` semantics (regenerate in memory, diff, exit non-zero on drift). Same CI gate inclusion (`poe ci` runs both build checks).

### File location

```
src/chirp_ui/manifest.json     # generated, COMMITTED, shipped as package data
scripts/build_manifest.py      # writes manifest.json; --check fails on drift
```

`manifest.json` lives next to other generated assets (`chirpui.css`). Hatch's wheel build already includes everything under `src/chirp_ui/`, so no additional `tool.hatch.build.targets.wheel.include` needed — it ships automatically.

### Public API surface

Added to `src/chirp_ui/__init__.py`:

```python
from functools import cache
from importlib.resources import as_file, files

MANIFEST_PATH = files("chirp_ui").joinpath("manifest.json")

@cache
def load_manifest() -> dict[str, object]:
    """Return the chirp-ui component manifest as a dict (cached after first call).

    Schema: chirpui-manifest@2. See docs/plans/PLAN-agent-grounding-depth.md.

    Example:
        from chirp_ui import load_manifest
        m = load_manifest()
        print(m["components"]["metric-card"]["params"])
    """
    import json
    with as_file(MANIFEST_PATH) as p:
        return json.loads(p.read_text(encoding="utf-8"))
```

`__all__` gains `"MANIFEST_PATH"` and `"load_manifest"`.

### Why build-time, not lazy runtime build

Considered: skip the committed JSON, build on first `load_manifest()` call. Rejected:
- A user installing `chirp-ui` shouldn't need kida and the chirp-ui filter stubs at *call* time just to read the manifest. The build needs a working compile environment (filters registered); shipping pre-built decouples consumer code from the build dependencies.
- Determinism is easier to audit when the artifact is in git.
- Matches the CSS pattern; one less mental model.
- An agent doing zero-shot grounding can `pip install chirp-ui` and immediately read `MANIFEST_PATH` — no Environment construction, no template resolver wiring.

### CI gate

`poe build-manifest-check` joins `build-css-check` in the `ci` task list. Drift fails CI with a clear message:

```
manifest.json is stale relative to component templates.
Run: poe build-manifest
```

### Free-threading safety

`functools.cache` on a no-arg function is GIL-free under PEP 703 (the cache is a single-slot dict updated atomically; `@cache` uses an internal lock). Acceptable.

`importlib.resources.files()` is thread-safe and ships with stdlib.

The build script itself runs single-threaded. No shared mutable state during generation.

---

## Open questions (out of Sprint 0)

These surfaced during investigation. Logged here so they get explicit treatment, not lost:

1. **Should `consumes` come from `depends_on` (AST) or from `@consumes` annotations (comment)?** Recommendation: **AST is authoritative** in the manifest; annotations stay as documentation aids. Sprint 2 task 2.2 confirms with empirical comparison across 24 annotated templates.
2. **Filter for `depends_on`**: kida's `depends_on` includes *all* context reads, not just provide/consume. We need to filter to underscore-prefixed keys (the convention in chirp-ui per `CLAUDE.md § Provided context keys`). Sprint 2 codifies this.
3. **Doc-block parsing**: the `{#- chirp-ui: ... -#}` convention currently has an informal multi-line shape — first line is the title, subsequent lines describe usage. For Sprint 4, capture the full block as `description`; future schema version may split into `summary` and `details`.
4. **Param defaults in @3?** If a consumer asks for default values (e.g. to render docs showing `cols=3`), revisit. Today nobody asks.

---

## Acceptance — Sprint 0 done

- [x] Strategy decision recorded (Decision 1).
- [x] Schema diff specified (Decision 2 — full table + worked example).
- [x] Packaging path picked (Decision 3 — mirrors CSS, named CI gate).
- [x] Worked example for `btn` and `metric_card` produced (Decision 1).
- [x] Free-threading constraint addressed in each decision.

Sprint 1 may begin against this RFC.
