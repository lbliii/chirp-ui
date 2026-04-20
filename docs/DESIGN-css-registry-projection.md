# DESIGN — CSS as a projection of the Python registry

**Status:** accepted 2026-04-17
**Epic:** `docs/PLAN-css-scope-and-layer.md`
**Purpose:** settle the four cross-sprint decisions so S1–S7 can execute without re-litigation.

## Decision 1 — Layer namespace is `chirpui.*`

Layers are declared in one line at the top of the generated `chirpui.css`:

```css
@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;
```

**Why namespaced (not bare `reset, token, base, component, utility`):**
- A consumer using a `reset` layer in their own app won't collide.
- The namespace mirrors the `chirpui-*` BEM prefix; two-pronged isolation.
- Cost is 7 extra characters per layer declaration — trivial.

Consumers override via the reserved companion name `app.overrides`, declared *after* chirpui's layers so any rule inside wins without specificity tricks:

```css
@layer app.overrides {
    .chirpui-card { border-color: var(--brand-teal); }
}
```

`app.overrides` is not reserved by chirp-ui; consumers may name their layer anything, but the documented recipe uses `app.overrides`.

## Decision 2 — Partials directory is `src/chirp_ui/templates/css/`

```
src/chirp_ui/templates/
    chirpui.css              # GENERATED — do not hand-edit
    css/                     # AUTHORING ROOT
        _layers.css          # layer declaration line only
        _reset.css
        _tokens.css
        _base.css
        components/          # one partial per component
            _card.css
            _btn.css
            …
        _utility.css
```

**Why this path (not `src/chirp_ui/templates/chirpui/css/`):**
- Sits next to `chirpui.css` — the authoring source and its output are siblings, not separated by a namespace directory.
- Already matched by the existing `package-data` glob `"templates/**/*.css"` — no `pyproject.toml` change needed.
- The `chirpui/` namespace inside `templates/` is reserved for Kida macros; CSS is a sibling concern.

## Decision 3 — Concat script API

Pure Python, stdlib only, deterministic byte-for-byte given the same input.

**Inputs:**
1. An ordered manifest of partial filenames (hardcoded list in `scripts/build_chirpui_css.py`, not a separate config file — one less moving part).
2. The partial files themselves.

**Output:**
- `src/chirp_ui/templates/chirpui.css`, containing:
  - A generated-file header comment (committed; warns against hand-edits).
  - Each partial's contents, preceded by a `/* === <relative path> === */` banner.
  - Trailing newline.

**What the script does NOT do:**
- No minification (library is pre-compiled; minifying inside the build hides authoring intent from consumers who inspect the file).
- No source maps (partial filenames are in the banners; that's sufficient).
- No import resolution — partials are opaque byte streams concatenated in manifest order.
- No optimization passes — `chirpui.css` stays a human-readable file.

**Why stdlib-only:**
- Free-threading constraint (see `memory/project_free_threading_tooling_constraint.md`).
- No new runtime deps, no new dev deps, no new supply-chain surface.

**Deterministic:**
- `python scripts/build_chirpui_css.py` twice on the same inputs produces byte-identical output.
- The test in `tests/test_chirpui_css_concat.py` asserts: run-the-build → the committed `chirpui.css` is unchanged.

## Decision 4 — Registry `emits` schema

`ComponentDescriptor` gains one field:

```python
@dataclass(frozen=True, slots=True)
class ComponentDescriptor:
    block: str
    variants: tuple[str, ...] = ()
    sizes: tuple[str, ...] = ()
    modifiers: tuple[str, ...] = ()
    elements: tuple[str, ...] = ()
    slots: tuple[str, ...] = ()
    tokens: tuple[str, ...] = ()
    extra_emits: tuple[str, ...] = ()     # NEW — escape hatch
    template: str = ""

    @property
    def emits(self) -> frozenset[str]:    # NEW — derived
        """Every chirpui-* class the component's CSS can legitimately emit."""
        classes = {f"chirpui-{self.block}"}
        classes |= {f"chirpui-{self.block}__{e}" for e in self.elements}
        classes |= {f"chirpui-{self.block}--{v}" for v in self.variants if v}
        classes |= {f"chirpui-{self.block}--{s}" for s in self.sizes}
        classes |= {f"chirpui-{self.block}--{m}" for m in self.modifiers}
        classes |= set(self.extra_emits)
        return frozenset(classes)
```

**Why a derived property instead of a stored field:**
- The generator is trivial and cannot drift — it *is* the BEM grammar.
- `extra_emits` captures only what the grammar can't express (compound states like `chirpui-card__header-wrap`, internal structural elements not surfaced as BEM elements, etc.).

**Parity test** (S4):
- Parse `.chirpui-<ident>` from every partial.
- `stylesheet_classes ⊆ ⋃ descriptor.emits` AND `⋃ descriptor.emits ⊆ stylesheet_classes`.
- On asymmetric failure, print both diffs so the author knows whether to extend `extra_emits` or delete orphaned CSS.

## Envelope convention (what each component partial looks like)

```css
@layer chirpui.component {
    @scope (.chirpui-NAME) to (.chirpui-NAME .chirpui-NAME) {
        :scope { /* root styles */ }
        .chirpui-NAME__part { /* child styles */ }
        :scope.chirpui-NAME--modifier { /* variant state */ }
    }
}
```

The `to (.chirpui-NAME .chirpui-NAME)` upper boundary clamps each component at the first nested instance of itself — fixes real bleed hazards (card inside card, surface inside surface).

**Migration:** every component touched for any other reason in S6 is converted to this envelope. Not a big-bang.

## Build flow

```
┌─ Authoring ───────────────────────────┐     ┌─ Runtime ─────┐
│ src/chirp_ui/templates/css/           │     │ chirpui.css   │
│   _layers.css                         │     │  (generated,  │
│   _reset.css                          │ ──▶ │   committed,  │
│   _tokens.css                         │     │   shipped)    │
│   _base.css                           │     └───────────────┘
│   components/_card.css   (envelope)   │              │
│   components/_btn.css    (envelope)   │              ▼
│   …                                   │     ┌─────────────────────┐
│   _utility.css                        │     │ Consumer site       │
└────────────────┬──────────────────────┘     │ @layer app.overrides│
                 │                            │   { .chirpui-card … │
                 │                            │   }                 │
                 ▼                            └─────────────────────┘
┌─ Registry ────────────────────────────┐
│ ComponentDescriptor(block="card",     │
│     elements=("header","body",…),     │              Parity
│     variants=("feature","stats",…),   │ ◀────────── test (S4)
│     extra_emits=(…))                  │
│   .emits = {chirpui-card, chirpui-    │
│     card__header, chirpui-card--      │              Manifest
│     feature, …}                       │ ─────────▶  (S7)
└───────────────────────────────────────┘
```

One direction of truth: partials are the CSS source; descriptors are the Python source; the parity test makes them the same set.

## Non-decisions (explicitly out of scope for this epic)

- **Minification / source maps.** If they become load-bearing, a *pure-Python* minifier or a *vendored binary invoked via subprocess* is the answer — not a Python binding to a Rust/C tool. See R6 in the epic.
- **Replacing `chirpui-*` BEM prefix.** The prefix is the public API; `@scope` does not replace it.
- **Shipping a utility class vocabulary.** Explicitly rejected in `docs/VISION.md § What we are not`.
- **Runtime CSS generation.** `chirpui.css` is committed; no runtime build step.

## Related

- `docs/PLAN-css-scope-and-layer.md` — the epic this design supports
- `docs/VISION.md § CSS architecture as a registry projection` — the *why*
- `examples/css-scope-prototype/card.scope.css` — the S5 pilot starting point
