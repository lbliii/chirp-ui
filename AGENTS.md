# AGENTS.md

Chirp-ui ships the component vocabulary that downstream apps render to their end users. A bad macro here becomes a rendering bug, an XSS hole, or a cascade failure in every Chirp app that upgrades. You can't see those apps, and they can't audit what you did. Treat the rules below as safety rules, not style rules.

---

## North star

**Chirpui is a Python vocabulary for UI, not a string vocabulary.** The component registry is the single source of truth; CSS, macros, tests, docs, and the agent manifest are all *projections* of it. Every decision routes back to that: does this keep chirpui introspectable from Python, or does it grow a parallel source of truth the registry can't see? If a change doesn't serve that goal, it isn't worth shipping. See `docs/VISION.md`.

---

## Design philosophy

- **No utility-class vocabulary, ever.** `stack()`, `cluster()`, `grid()`, `frame()`, `block()` are the composition primitives. We do not ship `p-4 mx-auto rounded-lg` equivalents. The moment a utility class lands, the registry stops being the source of truth and we re-enter Tailwind's category at a disadvantage.
- **Every class the CSS ships is registry-cited.** If `chirpui-card__X` is emitted by `card.html`, it appears in the card registry entry's `emits` set and in `_card.css`. Tests assert the three views agree. Unused classes get deleted; hallucinated classes fail CI.
- **Cascade order is public API.** `@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility, app.overrides`. Consumers place overrides in `app.overrides` and win predictably. Don't fight it with specificity.
- **CSS is concat-from-partials.** Edit `src/chirp_ui/templates/css/partials/*.css`, run `poe build-css`, commit both. New components get the `@layer chirpui.component { @scope (.chirpui-X) to (.chirpui-X .chirpui-X) { … } }` envelope — see `docs/PLAN-css-scope-and-layer.md`.
- **Free-threading-compatible tooling only.** Pure-Python build scripts, stdlib-only where possible. Lightning CSS Python bindings and anything else gated on the GIL are out. Python 3.14+ (free-threading-ready) is the floor.
- **No client JS in macros.** Alpine `x-data` attributes only. No `<script>` tags in component templates. Named Alpine components use `Alpine.safeData(name, factory)` and live in `chirpui-alpine.js`. Chirp is the single authority for Alpine injection.
- **Sharp edges are bugs, not taste.** Silent `| safe` on user input, un-validated variants, raw motion/color/spacing values, template-CSS drift, `attrs=""` raw strings — these have cost real consumers real time. CI catches some; the rest is on you.

---

## Stakes

When you change something in chirp-ui, the blast radius is:

- **Template rendering bugs** → consumer apps produce broken HTML to their end users. Debuggable only by the consumer, who can't see inside chirpui's macros. Harm: a dashboard breaks, an admin can't take a destructive action, a user sees a stale state.
- **XSS via `| safe` misuse** → reaches every app that renders the affected component. The `html_attrs`/`Markup` rule is load-bearing; raw string interpolation into attributes is an incident waiting to ship. See `SECURITY.md`.
- **CSS cascade / layer order changes** → consumer overrides in `app.overrides` silently stop winning, or chirpui rules start over-specifying. Documented cascade order is the public API; breaking it is a major version bump, not a drive-by.
- **Template-CSS drift** → `test_template_css_contract.py` exists because undefined classes looked fine in review and failed in the browser. New classes referenced in templates must exist in `chirpui.css` and in the registry's `emits` set.
- **Registry drift** → the agent manifest (`chirp_ui.manifest.build_manifest()`) is what grounds coding agents. If the registry doesn't match what macros emit, agents hallucinate classes that don't exist. This is the one bet; treat it like one.
- **Free-threaded races** → no GIL safety net under 3.14t. Any module-level mutable state (registries, colour caches, warning filters) must be safe under true parallelism.

Chirp-ui is pre-1.0 but shipped — the Bengal ecosystem (kida, chirp, chirp-ui, bengal) uses it, and external consumers are starting to. Calibrate accordingly.

---

## Who reads your output

- **App devs migrating from Tailwind/Shadcn** — want Python-reachable components, a working app-shell, and not to wire htmx/Alpine themselves. They read macro docstrings, `COMPONENT-OPTIONS.md`, and tracebacks.
- **Coding agents** — read the manifest and docstrings to ground suggestions. Vague, inconsistent, or missing docstrings propagate hallucinations into every PR those agents open in downstream projects.
- **Contributors** — know Jinja/Python but not our internals. They read `CLAUDE.md`, `docs/INDEX.md`, and a macro or two to get oriented. Onboarding fails when composition primitives aren't obvious.
- **Me (Lawrence)** — read diffs. Put the what in code, the why in the PR. I am the sole author of kida/chirp/chirp-ui; the flywheel is real and reviewer bandwidth is me.

---

## Escape hatches — stop and ask

Forks where I want a check-in, not a judgment call:

- **Adding a utility class.** The bright line. The answer is almost always no. If you think it's yes, ask.
- **Touching `@layer` order** (`chirpui.css` preamble) or the `app.overrides` contract. Public API.
- **New component that isn't clearly a projection of a registry entry.** Sketch the macro, its `emits` set, its `provides`/`consumes` keys, and variants first; ask whether it belongs before writing CSS.
- **New variant, size, or colour vocabulary.** Add to `VARIANT_REGISTRY` / `SIZE_REGISTRY` / `register_colors` first; if the vocabulary itself is new (not just a new value), ask.
- **New runtime dependency.** Must be pure-Python, free-threading-safe, and genuinely load-bearing. Default answer: "reshape an existing primitive."
- **New build/tooling dependency.** Same bar as runtime deps, plus: must work on 3.14t. Lightning CSS Python bindings are already out; so is anything equivalent.
- **New config option / macro parameter on a load-bearing component.** Reshape first. The surface is already large; growing it is a smell. If you add one, update `COMPONENT-OPTIONS.md` in the same PR.
- **Bypassing escaping** (`| safe`, `Markup(...)`, new `attrs_unsafe` consumer). Explain why the input is trusted. Default: use `html_attrs` + `attrs_map`.
- **Changing `provide`/`consume` keys** (`PROVIDE-CONSUME-KEYS.md`). Contract surface across macro boundaries; breaking it breaks consumer templates silently.
- **Big-bang CSS migrations.** Don't. Opportunistic envelope conversion only — when a PR touches a legacy partial, convert that one partial in the same PR. One component per PR. See `docs/PLAN-css-scope-and-layer.md § Migration status`.
- **Public API change** (anything imported from `chirp_ui.__init__`, macro signatures in the registry, `static_path()`, `register_filters()`). Ask whether the break is worth it and add a deprecation path per the policy in `CLAUDE.md`.
- **Dead code you found.** Flag in the PR, let me decide. Unused macros may be load-bearing for a theme, showcase route, or example.
- **Test disagrees with code.** Ask which is authoritative before "fixing" either — especially for `test_template_css_contract.py`, `test_transition_tokens.py`, and the registry-emits parity test. They exist because the code drifted.
- **Adjacent issues found mid-task.** List them in the PR description. Don't fold them in — exception: opportunistic envelope conversion on the partial you're already editing, and refactors renaming a concept across many files (one bundled PR beats churn).

---

## Anti-patterns

Things that look reasonable and are wrong here:

- **Utility classes.** No `chirpui-p-4`, no `chirpui-flex`, no `chirpui-text-center`. Use composition macros.
- **Raw CSS values instead of tokens.** Hardcoded hex colors, `font-weight: 600`, `transition: 200ms ease`, `z-index: 9999`, `padding: 12px`. Motion tokens are enforced by `test_transition_tokens.py`; the rest is on you. Use `--chirpui-{duration,easing,color,on,weight,z,spacing,radius}-*`.
- **Template classes without a CSS definition.** `test_template_css_contract.py` will fail. If a class is visual, define it in the matching partial and cite it in the registry.
- **`<script>` tags inside macro templates.** Named controllers go in `chirpui-alpine.js` via `Alpine.safeData`. Inline `x-data` is fine for tiny one-state widgets only; anything involving `$refs`, `$nextTick`, keyboard handling, `localStorage`, or viewport measurement moves out.
- **`| safe` on user-controlled input.** Use `html_attrs` + `attrs_map` (escaping), or `Markup` on already-escaped output. `attrs=""` raw strings are deprecated — migrate to `attrs_unsafe` (explicit) or `attrs_map` (safe).
- **`try: ... except Exception: pass`** around validation. Chirp-ui uses `warnings`, not `logging`, for dev feedback. Let warnings fire; consumers filter with `-W`. Silencing them hides the footgun for everyone downstream.
- **`# type: ignore` in `src/chirp_ui/`.** Target is zero. `ty` is fast and Rust-based; there's no excuse. If you have to, own it in the PR.
- **Speculative macro parameters** for "future flexibility." If no consumer template uses it, don't add it. Parameters are easier to add than to remove — and `COMPONENT-OPTIONS.md` entries rot.
- **Defensive validation inside internal filters/helpers.** Validate at the template boundary (`validate_variant`, `validate_size`, `sanitize_color`); internal code trusts its callers.
- **Macro name collisions with context variable names.** `route_tabs` the macro vs `route_tabs` the context var silently shadow each other. Verb-prefix macros (`render_route_tabs`), noun-name context vars (`route_tabs`). See `docs/ANTI-FOOTGUNS.md § Kida Macros`.
- **Refactoring during a bug fix.** Separate PR. Exception: the refactor *is* the fix, or it's an opportunistic envelope conversion on a partial you're already touching (one partial, called out in the PR description).
- **Re-triaging sharp edges listed in `CLAUDE.md`.** The table is institutional memory. If you see an entry, it's solved; don't "fix" it again.

---

## Done criteria

A change is done when all of these hold:

- [ ] `uv run poe ci` is green — lint + format + CSS build check + `ty` + tests.
- [ ] `test_template_css_contract.py`, `test_transition_tokens.py`, and the registry-emits parity test pass. No new classes without matching CSS; no raw motion values.
- [ ] If you added/changed a macro: the registry entry reflects the new slots/params/variants, and the agent manifest rebuilds cleanly (`python -m chirp_ui.manifest --json`).
- [ ] If you added a CSS class: it's cited in the registry `emits` set and in the matching partial — not hand-appended to `chirpui.css`, which is generated.
- [ ] Tests exercise the *interesting* path: at least one non-default variant, default-fallback behaviour for invalid variants, and the slot-composition shape for new macros.
- [ ] Provide/consume keys on new macros are annotated with `@provides` / `@consumes` in the template and listed in `docs/PROVIDE-CONSUME-KEYS.md`.
- [ ] Public API changed or macro deprecated → entry in `COMPONENT-OPTIONS.md` (and `CLAUDE.md § Deprecation policy` if user-facing), migration note if breaking.
- [ ] Error messages and warnings tell the reader what to do next, not just what went wrong. `ChirpUIValidationWarning` / `ChirpUIDeprecationWarning` are the right channels — not `print`, not `logging`.
- [ ] PR description explains *why*. The diff explains what.

"Tests pass" is not "done." The test suite covers structural shape and cascade order; feature correctness is on you. UI changes that can't be verified in a browser should say so explicitly in the PR rather than claim success.

---

## Review and assimilation

- **I read diff-first, description-second.** Tight diff + clear why merges fast; sprawling diff gets questions.
- **One component / one concern per PR.** If the diff needs section headers, it's two PRs. Exceptions: refactors renaming a concept across many files, and opportunistic envelope conversion on partials you're already editing (call it out in the description).
- **Commit style:** see `git log`. `feat(...):`/`fix:`/`refactor:`/`docs:` prefixes, imperative, body = motivation.
- **Don't trailing-summary me.** If the diff is readable, I can read it.
- **Flag surprises.** Unused classes, unused macros, variants/sizes that differ across components, orphaned providers (wire them, don't remove — see `docs/PROVIDE-CONSUME-KEYS.md`), tests that look wrong. Put it in the PR description. Don't fix silently, don't ignore.

---

## When this file is wrong

It will be. Tell me. The worst outcome is that it sits here for a year contradicting how the project actually works. Updates to `AGENTS.md` are a first-class PR — short, focused, and welcome.
