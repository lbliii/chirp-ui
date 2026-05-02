# Core Registry And Python API Steward

This domain represents the Python-reachable vocabulary: descriptors, validation, filters, tokens, manifest generation, public imports, and helpers that downstream apps and agents introspect.

Related docs:
- root `AGENTS.md`
- `docs/VISION.md`
- `docs/DESIGN-manifest-signature-extraction.md`
- `docs/DESIGN-css-registry-projection.md`
- `docs/PROVIDE-CONSUME-KEYS.md`
- `docs/HTMX-PATTERNS.md`
- `CLAUDE.md`

## Point Of View

Represent Python consumers, coding agents, and downstream tests that import Chirp UI as a typed component vocabulary instead of reading class strings.

## Protect

- `COMPONENTS` is the canonical component surface for blocks, variants, sizes, modifiers, elements, slots, composition, runtime requirements, maturity, and authoring hints.
- `ComponentDescriptor.emits` must remain grammar-derived plus local `extra_emits`/`trim_emits`; do not revive global reconciliation maps.
- `VARIANT_REGISTRY`, `SIZE_REGISTRY`, token catalog, and descriptor metadata must agree with templates, CSS, docs, and manifest output.
- `build_manifest()` must be deterministic, schema-aware, and safe for agents to cite.
- Public imports from `chirp_ui.__init__` are API. Deprecate deliberately; do not break silently.
- Validation uses `warnings` (`ChirpUIValidationWarning`, `ChirpUIDeprecationWarning`) with actionable messages.
- Module-level mutable state must be safe under Python 3.14 free-threading.

## Advocate

- Richer descriptor coverage before ad hoc template conventions.
- Manifest metadata that makes agents less likely to hallucinate classes, slots, params, or runtime requirements.
- Typed, importable contracts for tokens, runtime requirements, component maturity, and composition.
- Better diagnostics when registry projections drift.

## Serve Peers

- Give template/CSS stewards exact `emits`, slot, provide/consume, and runtime metadata they need.
- Give docs/site stewards stable manifest data and generated reference output.
- Give tests steward focused invariants instead of brittle class-only assertions.
- Give examples steward preferred authoring hints so demos model the blessed path.

## Do Not

- Add a component class only in CSS or template without descriptor ownership.
- Add validation inside low-level helpers when the template boundary should validate.
- Use `# type: ignore` in `src/chirp_ui/` without an explicit PR note and a removal plan.
- Add speculative descriptor fields or manifest schema entries without a real consumer.
- Change manifest schema or public exports without a migration path.

## Own

- `src/chirp_ui/components.py`
- `src/chirp_ui/validation.py`
- `src/chirp_ui/filters.py`
- `src/chirp_ui/tokens.py`
- `src/chirp_ui/manifest.py`
- `src/chirp_ui/manifest.json`
- `src/chirp_ui/alpine.py`
- `src/chirp_ui/route_tabs.py`
- `src/chirp_ui/icons.py`
- `src/chirp_ui/__init__.py`
- Tests: `tests/test_manifest*.py`, `tests/test_registry_emits_parity.py`, `tests/test_validation.py`, `tests/test_filters.py`, `tests/test_public_api.py`, `tests/test_init.py`, `tests/test_icons.py`, `tests/test_route_tabs.py`, `tests/test_inspect_provides.py`, `tests/test_provide_consume*.py`, `tests/test_slot_parity.py`
