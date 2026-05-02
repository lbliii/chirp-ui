# chirp-ui: Product Page Patterns from LangChain

## Goal

Turn the design feedback from LangChain's 2026 homepage into ChirpUI-native product-site patterns without expanding the public component surface prematurely.

The target is not to copy the site. The target is to identify the repeatable product-page grammar behind it, express that grammar with existing ChirpUI primitives first, and only add registry-backed components when recipes prove too verbose or too easy to misuse.

Reference observed 2026-05-02: <https://www.langchain.com/>

---

## Design Read

LangChain's page works because each section has a clear product job:

| Page move | Product job | ChirpUI lesson |
|-----------|-------------|----------------|
| Product-aware top nav | Teaches the product taxonomy before navigation | `site_header` needs stronger documented patterns for grouped product links |
| Direct hero claim plus CTAs | States the product promise and sends users to trial/demo | `hero` and `page_hero` need product-site recipes with proof nearby |
| Build / Observe / Evaluate / Deploy strip | Turns lifecycle positioning into navigation | `tabs_panels` plus `feature_section` can become a lifecycle showcase recipe |
| Logo proof band | Builds trust before deep feature copy | `marquee`, `band`, and `cluster` can compose this today |
| Platform feature panels | Pairs feature copy with concrete visual artifacts | `feature_section`, `frame`, `surface`, and `grid` should cover this without new atoms |
| Framework/product cards | Helps users choose among adjacent offerings | `index_card`, `resource_index`, and `bento_grid` need product-card recipes |
| Customer story list | Converts adoption into specific outcomes | A testimonial/use-case card may be worth testing as a pattern |
| Metric proof band | Makes adoption claims scannable | `metric_grid` and `metric_card` already cover this |
| Final CTA band | Restates the offer after proof | `band` should document a canonical CTA composition |

---

## Current ChirpUI Surface

ChirpUI already has most of the atoms and low-level primitives needed:

- **Site shell:** `site_shell`, `site_header`, `site_footer`
- **Hero and sections:** `hero`, `page_hero`, `band`, `feature_section`, `feature_stack`
- **Composition primitives:** `container`, `stack`, `cluster`, `grid`, `frame`, `block`, `layer`
- **Proof and data:** `marquee`, `metric_grid`, `metric_card`, `stat`
- **Navigation/choice:** `tabs_panels`, `route_tabs`, `index_card`, `resource_index`, `bento_grid`
- **Effects:** `aura`, `border_beam`, `spotlight_card`, `reveal_on_scroll`

The gap is a recipe and pattern layer: how to assemble these into polished product pages while staying registry-grounded.

---

## Non-Goals

- Do not add utility classes.
- Do not add new color, size, or variant vocabulary in this plan.
- Do not copy LangChain's brand, copy, assets, or exact visual treatment.
- Do not add a new component until a recipe has been proven too repetitive or too fragile.
- Do not change cascade layer order or the `app.overrides` contract.
- Do not introduce client scripts for marketing interactions. Use Alpine only where existing components already require it.

---

## Proposed Pattern Recipes

### 1. Product Hero With Adjacent Proof

**Use when:** A product page needs a first-viewport claim, primary/secondary CTAs, and immediate trust evidence.

**Compose from:**

- `site_shell`
- `site_header`
- `hero` or `page_hero`
- `cluster` for CTAs and proof chips
- `band` or `marquee` for logo proof

**Recipe shape:**

```kida
{% call site_shell() %}
  {% slot header %}...site_header...{% end %}
  {% call hero(title=product_name, subtitle=value_prop, background="solid") %}
    {% slot actions %}...primary and secondary CTAs...{% end %}
  {% end %}
  {% call band(width="bleed", variant="default") %}
    ...logo proof or compact customer list...
  {% end %}
{% end %}
```

**Acceptance checks:**

- The H1 names the product or literal offer.
- Proof appears before long-form feature copy.
- CTAs use existing `btn` variants only.
- No custom utility classes are required in the recipe.

### 2. Lifecycle Showcase

**Use when:** A product is understood through a sequence of jobs, stages, or modes.

**Compose from:**

- `tabs_panels` for client-side switching
- `feature_section` for copy/media pairing
- `surface` or `frame` for screenshots, code samples, timelines, or metric panels
- `list` or simple prose for feature bullets

**Recipe shape:**

```kida
{% call tabs_container(active="build") %}
  {{ tab_button("build", "Build", active=true) }}
  {{ tab_button("observe", "Observe") }}
  {{ tab_button("evaluate", "Evaluate") }}
  {{ tab_button("deploy", "Deploy") }}

  {% call tab_panel("build", active=true) %}
    {% call feature_section(layout="balanced") %}
      {% slot title %}Build agents with clear control{% end %}
      ...body...
      {% slot media %}...surface with product artifact...{% end %}
    {% end %}
  {% end %}
{% end %}
```

**Acceptance checks:**

- Each tab describes a job, not a visual style.
- Media is a concrete product artifact: screenshot, trace, config, table, code, or workflow state.
- The default active panel renders useful content without JavaScript.
- Existing `tabs_panels` Alpine behavior remains the only client behavior.

### 3. Proof Band

**Use when:** A page needs customer logos, ecosystem names, integrations, or adoption claims.

**Compose from:**

- `band`
- `marquee` for long repeating logo/name strips
- `cluster` for short proof sets
- `metric_grid` for quantified proof

**Recipe shape:**

```kida
{% call band(width="bleed", variant="elevated") %}
  {{ section_header("Trusted by teams building production agents") }}
  {{ marquee(items=customer_names, speed="slow") }}
{% end %}
```

**Acceptance checks:**

- Text alternatives exist when logos are images.
- Motion respects existing marquee behavior and reduced-motion CSS.
- Repeated proof does not duplicate source data in templates if the app already owns the list.

### 4. Product Choice Grid

**Use when:** A product family has multiple tools, frameworks, modules, or entry points.

**Compose from:**

- `grid` or `bento_grid`
- `index_card`
- `resource_index` when search/filter is needed
- `badge` for maturity, audience, or runtime labels

**Recipe shape:**

```kida
{% call grid(cols=3, gap="lg") %}
  {% for item in products %}
    {{ index_card(href=item.href, title=item.name, description=item.summary, badge=item.kind) }}
  {% endfor %}
{% end %}
```

**Acceptance checks:**

- Cards explain decision criteria, not just names.
- Use `resource_index` only when filtering/search is part of the page job.
- Avoid bespoke card modifiers until repeated usage proves a registry-backed product card is necessary.

### 5. Customer Story Strip

**Use when:** A product page needs specific outcomes from real users.

**Compose from now:**

- `grid`
- `card`
- `badge`
- `metric_card` for numeric outcomes

**Potential future component:** `story_card`

Only add `story_card` if at least two real pages need the same structure:

- customer name
- short outcome headline
- optional metric
- short summary
- href
- optional logo/avatar slot

**Acceptance checks before adding a component:**

- Existing `card` composition requires repeated structural classes across pages.
- The registry entry can cite all emitted classes.
- The macro can avoid unsafe rich text and raw attribute strings.

### 6. CTA Band

**Use when:** A page has finished a proof sequence and needs one final action.

**Compose from:**

- `band`
- `stack`
- `cluster`
- `btn`

**Recipe shape:**

```kida
{% call band(width="bleed", variant="accent") %}
  {% call stack(gap="md") %}
    <h2>Start building with LangSmith</h2>
    <p>...</p>
    {% call cluster() %}
      {{ btn("Start building", variant="primary") }}
      {{ btn("Get a demo", variant="ghost") }}
    {% end %}
  {% end %}
{% end %}
```

**Acceptance checks:**

- One primary action, one optional secondary action.
- No section-level card wrapper inside the band.
- Copy is specific to the product page, not generic framework language.

---

## Implementation Plan

### Phase 1: Document Recipes (completed 2026-05-02)

Add product-page recipes to docs without changing component APIs.

| File | Action |
|------|--------|
| `docs/PRODUCT-PAGE-PATTERNS.md` | Added recipe documentation for product hero, lifecycle, proof, product choice, customer story, and CTA sections |
| `docs/PRIMITIVES.md` | Added a short product-page compositions pointer after the blessed primitives section |
| `docs/INDEX.md` | Indexed the recipe doc under Patterns |
| `docs/plans/PLAN-product-page-patterns-from-langchain.md` | Kept this plan as the active roadmap |

**Done when:**

- Docs show how to build each pattern from existing registry-cited components.
- No new classes, variants, or tokens are introduced.
- Examples use `stack`, `cluster`, `grid`, `frame`, `block`, `band`, and existing components.

### Phase 2: Build a Showcase Fixture (completed 2026-05-02)

Create one internal showcase page that exercises the recipes against real HTML.

Implemented locations:

- `tests/browser/templates/product_page_patterns.html`
- `tests/browser/test_product_page_patterns.py`
- `/product-page-patterns` route in `tests/browser/app.py`

**Done when:**

- The page renders the six recipes with realistic placeholder data.
- Browser tests verify no mobile horizontal overflow.
- The fixture uses only existing public macros and component classes.

### Phase 3: Promote Repeated Recipes

After the showcase and at least one consumer page use the same recipe, decide whether any pattern deserves a macro.

Candidate macros, gated by evidence:

| Candidate | Default answer | Promotion trigger |
|-----------|----------------|-------------------|
| `logo_cloud` | Built 2026-05-02 | Accessible proof bands are common and stable enough to ship proactively |
| `lifecycle_showcase` | Recipe only | Repeated `tabs_panels` + `feature_section` markup becomes error-prone |
| `story_card` | Built 2026-05-02 | Customer outcome cards are common and stable enough to ship proactively |
| `site_nav_group` | Maybe | Product nav grouping cannot be expressed cleanly with current `site_header` slots |
| `cta_band` | Recipe only | `band` + `stack` + `cluster` proves too verbose in multiple pages |

**Done when:**

- Any promoted macro has a `ComponentDescriptor`.
- Emitted classes are in the registry and matching CSS partial.
- Template doc-block, tests, and manifest projection are updated.
- `COMPONENT-OPTIONS.md` documents new params only after the API is real.

### Phase 4: Polish Existing Components

Only after recipe validation, refine existing components where the recipe exposes friction.

Possible refinements:

- `site_header`: document grouped navigation patterns before adding new macros.
- `feature_section`: check whether existing `layout` values cover lifecycle/media cases.
- `marquee`: audit logo/image accessibility and reduced-motion behavior.
- `band`: verify CTA/proof sections do not require app-owned chrome classes.
- `index_card`: verify product-choice cards have enough slots or params without becoming speculative.

**Done when:**

- Refinements remain token-based and registry-cited.
- No raw CSS values are added.
- Existing tests for template/CSS/registry parity remain green.

---

## Testing Strategy

For recipe-only phases:

- Run docs checks if docs examples become test-covered.
- Add browser fixture coverage if a showcase template is added.
- Check responsive behavior at phone and desktop widths.

For any future macro/component promotion:

- `test_template_css_contract.py`
- `test_transition_tokens.py`
- Registry-emits parity test
- Manifest rebuild: `python -m chirp_ui.manifest --json`
- Focused component render tests in `tests/test_components.py`
- Browser smoke coverage for the showcase route

Full done criteria remain `uv run poe ci`.

---

## Steward Notes

- **Registry steward:** New macros require descriptors before CSS/classes ship.
- **Rendering steward:** Marketing recipes must keep user text escaped and use `attrs_map` for attributes.
- **Theme steward:** Product-page polish should use existing tokens before proposing new ones.
- **Docs steward:** Recipes must describe shipped contracts, not aspirational APIs.
- **Planning steward:** Keep this plan active until recipes are either documented or promoted into concrete component plans.
- **Site steward:** If exposed on the docs site, examples must render cleanly in the published site shell.

---

## Not Now

- A generic landing-page builder.
- A Shadcn/Tailwind-style marketing section library.
- Brand-specific LangChain visual mimicry.
- New animation primitives for marketing pages.
- New utility classes for spacing, typography, or alignment.
- A public `product_*` namespace before there is usage evidence.

---

## Open Questions

- Should product-page recipes live in a new `docs/PRODUCT-PAGE-PATTERNS.md`, or as sections in existing `PRIMITIVES.md` / `COMPOSITION.md`?
- Should the first showcase live under browser tests only, or should it become part of the docs site?
- Do downstream apps need image/logo handling in ChirpUI, or should app templates own brand assets entirely?
- Is `site_nav_group` a real component need, or can `site_header` slots plus documented structure cover it?
