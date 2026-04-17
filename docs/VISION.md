# Vision

## The category

> **Tailwind is a string vocabulary interpreted by Node. Chirpui is a Python vocabulary interpreted by Python.**

For a Python developer, that single fact is the category difference. It means the design system — its tokens, variants, slots, contracts, and rendered output — is reachable from the same interpreter running the app. The developer's own toolchain (`ty`, `pytest`, `pyproject.toml`, their IDE, their coding agent) can reason about the UI directly, without a parallel JS build, without round-tripping through a config language they don't use, without drift between what the designer declared and what the tests check.

Tailwind cannot enter this category without becoming a Python library and abandoning the utility-class paradigm. It will not. That leaves the category open.

## Why this matters for Python devs

Tailwind asks a Python developer to:

- Maintain a Node toolchain (`package.json`, `tailwind.config.js`, PostCSS) alongside their Python one.
- Express design decisions in a JavaScript configuration they cannot round-trip through `pyproject.toml`, `ty`, or their test suite.
- Test UI output by asserting on class-name strings — the same class-name strings an AI agent will hallucinate confidently.
- Build their own component layer on top of utilities, because Tailwind has no opinion on what a card is.
- Wire HTMX and Alpine themselves, hitting the same boost / select / form-reset pitfalls every project hits.

Chirpui collapses those into: write Python, render templates, run `uv run poe ci`. The *source of truth* lives where the developer already is.

## The flywheel

Five capabilities compound. Only one is hard; the rest follow.

1. **A type-checked component registry** (the one bet). Every macro exposes its slots, parameters, variants, `provides`/`consumes` keys, and HTMX support as a Python object. Importable, introspectable, versioned.
2. **Tokens in `pyproject.toml`.** Theme, spacing, typography, color tokens declared in Python-native config. CSS generated at install time. One edit round-trips through the whole stack.
3. **Contract verification as a verb.** `registry.verify(rendered_html, contract="dashboard")` returns a typed result. Dashboard maturity, accessibility contracts, composition contracts — all callable from tests or CI.
4. **HTMX- and Alpine-native defaults.** Boost-aware components, auto `hx-select="unset"` on forms inside boosted layouts, fragment islands, SSE / suspense primitives — problems solved once, inherited everywhere.
5. **Agent-groundable manifest.** The registry serializes to a machine-readable manifest an AI coding agent can cite, reducing UI hallucination to near zero. Docs regenerate from the same source.

## What we are not

Not a utility-class expansion. Chirpui uses `stack()`, `cluster()`, `grid()`, `frame()`, `block()` as composition primitives; it does not ship `p-4 mx-auto rounded-lg` equivalents. The discipline is load-bearing — once a utility vocabulary exists, contracts and introspection erode, and we re-enter Tailwind's category at a disadvantage.

Not a React-replacement component system. Chirpui does not own state. It renders HTML and lets HTMX / Alpine handle interactivity. That is the shape that lets it remain a Python vocabulary.

Not a framework. It is an opinionated UI layer on top of `kida-templates` + `bengal-chirp`. Adoption is additive; any Chirp app can use none, some, or all of it.

## The concession

The Tailwind ecosystem — plugins, Tailwind UI, Shadcn ports, landing-page generators, every designer's Figma plugin — is enormous and we will not have it. For prototyping a one-off marketing page, Tailwind is faster. For building a Python-native application whose UI must stay correct over years, chirpui wins by being reachable from Python.

We are choosing *correct, introspectable, small ecosystem* over *unbounded, opaque, large ecosystem*. That choice is the product.

## Decision lens for future PRs

When evaluating a change, ask:

- Does this preserve the property that chirpui is a Python vocabulary, not a string vocabulary?
- Does it make the registry richer, or does it grow a parallel source of truth?
- Can the test suite, `ty`, and a coding agent all reason about it?
- Does it inherit from a contract, or does it reinvent one?

If the answer to any is no, the change belongs somewhere else — or the design needs to bend until the answers are yes.

## Related

- `docs/PLAN-base-layer-hardening.md` — follow-on CSS hardening (preflight-style defaults)
- `CLAUDE.md § Sharp edges — what's been hardened` — institutional memory of solved categories
- `DASHBOARD-MATURITY-CONTRACT.md` — early example of a contract chirpui enforces
- `docs/PROVIDE-CONSUME-KEYS.md` — composition primitives for parent-to-child state flow
