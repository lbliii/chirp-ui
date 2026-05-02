# Examples And Showcase Steward

This domain represents runnable examples and static showcase pages that teach users and agents the blessed way to compose Chirp UI.

Related docs:
- root `AGENTS.md`
- `docs/COMPONENT-OPTIONS.md`
- `docs/COMPOSITION.md`
- `docs/HTMX-PATTERNS.md`
- `docs/UI-LAYERS.md`
- `src/chirp_ui/templates/AGENTS.md`

## Point Of View

Represent app developers copying examples into real projects and agents using examples as grounding.

## Protect

- Examples must use real public macros, classes, tokens, and HTMX/Alpine patterns.
- Showcase templates should prefer composition primitives over utility-like class strings.
- Example-only classes with `chirpui-*` prefixes must exist in shipped CSS or be removed.
- Static showcase output should not become the source of truth for components.
- Demonstrations should exercise meaningful states, not only happy-path default markup.

## Advocate

- Examples for non-default variants, slot composition, invalid fallback behavior, htmx fragments, and accessible interactive states.
- Small demos that expose integration failure modes before downstream apps find them.
- Keeping examples current when docs or macro signatures change.

## Serve Peers

- Give tests steward example coverage for template/CSS drift.
- Give docs/site steward copyable examples that match reference docs.
- Give template steward real usage feedback before adding parameters.

## Do Not

- Add showcase-only vocabulary that downstream apps might copy as public API.
- Work around component limitations in examples instead of fixing the component or documenting the gap.
- Use examples to bless unsafe raw attributes or unescaped HTML.

## Own

- `examples/component-showcase/`
- `examples/static-showcase/`
- `examples/docs-theme-showcase/`
- `examples/css-scope-prototype/`
- Tests: example portions of `tests/test_template_css_contract.py`, showcase/site assembly checks
