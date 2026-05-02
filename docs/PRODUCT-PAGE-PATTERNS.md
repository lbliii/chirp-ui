# Product Page Patterns

ChirpUI product pages should be built from named composition primitives and registry-backed components, not page-specific utility classes. These recipes cover the product-site patterns identified from the LangChain homepage review on 2026-05-02.

Use these as starting points for marketing pages, docs homes, product family pages, and launch pages. If a recipe becomes repeated and fragile across real pages, promote it into a component plan with a registry entry, CSS partial, tests, and `COMPONENT-OPTIONS.md` updates.

---

## Imports

Most examples use this shared import set:

```kida
{% from "chirpui/site_shell.html" import site_shell %}
{% from "chirpui/site_header.html" import site_header, site_nav_link %}
{% from "chirpui/site_footer.html" import site_footer, footer_column, footer_link %}
{% from "chirpui/hero.html" import hero %}
{% from "chirpui/band.html" import band %}
{% from "chirpui/button.html" import btn %}
{% from "chirpui/layout.html" import container, stack, cluster, grid, frame, section_header %}
{% from "chirpui/logo_cloud.html" import logo_cloud %}
{% from "chirpui/marquee.html" import marquee %}
{% from "chirpui/feature_section.html" import feature_section %}
{% from "chirpui/tabs_panels.html" import tabs_container, tab_button, tab_panel %}
{% from "chirpui/surface.html" import surface %}
{% from "chirpui/index_card.html" import index_card %}
{% from "chirpui/card.html" import card %}
{% from "chirpui/story_card.html" import story_card %}
{% from "chirpui/metric_grid.html" import metric_grid, metric_card %}
```

Keep imports in the nearest layout or page template that owns the composition. For HTMX fragments, follow the import guidance in [COMPOSITION.md](COMPOSITION.md).

---

## Product Hero With Adjacent Proof

Use this when a product page needs a first-viewport claim, one primary action, one optional secondary action, and proof before long-form feature copy.

```kida
{% call site_shell() %}
  {% slot header %}
    {% call site_header(current_path=current_path) %}
      {% slot brand %}Acme Agents{% end %}
      {% slot nav %}
        {{ site_nav_link("/platform", "Platform", match="prefix") }}
        {{ site_nav_link("/docs", "Docs", match="prefix") }}
        {{ site_nav_link("/pricing", "Pricing", match="exact") }}
      {% end %}
      {% slot tools %}
        {{ btn("Get a demo", href="/demo", variant="ghost") }}
        {{ btn("Start building", href="/start", variant="primary") }}
      {% end %}
    {% end %}
  {% end %}

  {% call hero(title="Acme Agents", subtitle="Observe, evaluate, and deploy production agents.", background="solid") %}
    {% slot actions %}
      {% call cluster() %}
        {{ btn("Start building", href="/start", variant="primary") }}
        {{ btn("Get a demo", href="/demo", variant="ghost") }}
      {% end %}
    {% end %}
  {% end %}

  {% call band(width="bleed", variant="default") %}
    {% call container() %}
      {{ logo_cloud(items=customer_logos, label="Customers using Acme Agents") }}
    {% end %}
  {% end %}
{% end %}
```

Checks:

- The H1 names the product or literal offer.
- The proof band appears before deep feature copy.
- CTAs use existing `btn` variants.
- The page does not introduce app-owned layout classes for the core structure.

---

## Lifecycle Showcase

Use this when the product is best understood as a sequence of jobs, such as Build, Observe, Evaluate, and Deploy.

```kida
{% call tabs_container(active="build") %}
  {{ tab_button("build", "Build", active=true) }}
  {{ tab_button("observe", "Observe") }}
  {{ tab_button("evaluate", "Evaluate") }}
  {{ tab_button("deploy", "Deploy") }}

  {% call tab_panel("build", active=true) %}
    {% call feature_section(layout="balanced") %}
      {% slot eyebrow %}Build{% end %}
      {% slot title %}Design agent workflows with clear control{% end %}
      <p>Give teams a shared place to define steps, tools, and review points.</p>
      {% slot media %}
        {% call surface(variant="muted") %}
          {% call stack(gap="sm") %}
            <strong>Workflow draft</strong>
            <p>Plan -> retrieve context -> call tools -> request review -> respond.</p>
          {% end %}
        {% end %}
      {% end %}
    {% end %}
  {% end %}

  {% call tab_panel("observe") %}
    {% call feature_section(layout="balanced") %}
      {% slot eyebrow %}Observe{% end %}
      {% slot title %}Trace every run as a timeline{% end %}
      <p>Show each step, model call, tool result, and handoff in order.</p>
      {% slot media %}
        {% call surface(variant="muted") %}
          Trace timeline placeholder
        {% end %}
      {% end %}
    {% end %}
  {% end %}
{% end %}
```

Checks:

- Tab labels describe product jobs, not visual styles.
- Each panel pairs copy with a concrete product artifact: screenshot, trace, table, config, code, or workflow state.
- The default active panel renders useful content before Alpine initializes.
- No custom client script is added.

---

## Proof Band

Use this for customer logos, ecosystem names, integration lists, or adoption claims.
Use `logo_cloud` for accessible image or text logos, and reserve `marquee`
for long repeating text strips.

```kida
{% call band(width="bleed", variant="elevated") %}
  {% call container() %}
    {% call stack(gap="md") %}
      {{ section_header("Trusted by teams shipping production agents") }}
      {{ logo_cloud(items=customer_logos, label="Customers using Acme Agents") }}
    {% end %}
  {% end %}
{% end %}
```

For quantified proof, pair the same band with `metric_grid`:

```kida
{% call band(width="bleed", variant="elevated") %}
  {% call container() %}
    {% call metric_grid(cols=3) %}
      {{ metric_card(value="100M+", label="Monthly downloads") }}
      {{ metric_card(value="6K+", label="Active customers") }}
      {{ metric_card(value="5", label="Fortune 10 customers") }}
    {% end %}
  {% end %}
{% end %}
```

Checks:

- Image logos have text alternatives through `logo_cloud` item names or explicit `alt` values.
- Repeated proof data comes from app-owned lists, not duplicated template literals.
- Motion remains limited to existing `marquee` behavior.

---

## Product Choice Grid

Use this when a page needs to explain related products, frameworks, modules, or entry points.

```kida
{% call container() %}
  {% call stack(gap="lg") %}
    {{ section_header("Choose the right framework") }}

    {% call grid(cols=3, gap="lg") %}
      {% for item in products %}
        {{ index_card(href=item.href, title=item.name, description=item.summary, badge=item.kind) }}
      {% endfor %}
    {% end %}
  {% end %}
{% end %}
```

Use `resource_index` instead when search, filters, selection state, or mutation feedback are part of the page job.

Checks:

- Cards explain decision criteria, not only product names.
- The grid owns repetition; cards own navigation.
- New card variants wait until repeated real pages prove the need.

---

## Customer Story Strip

Use this when a page needs specific outcomes from real users.

```kida
{% call container() %}
  {% call stack(gap="lg") %}
    {{ section_header("Learn from teams running agents in production") }}

    {% call grid(cols=3, gap="lg") %}
      {% for story in stories %}
        {{ story_card(
          customer=story.customer,
          outcome=story.outcome,
          summary=story.summary,
          href=story.href,
          metric=story.metric | default(none)
        ) }}
      {% endfor %}
    {% end %}
  {% end %}
{% end %}
```

Use `card` directly only when a story needs page-specific structure outside the
standard customer, outcome, metric, summary, and CTA regions.

Checks:

- Outcome copy is specific and measurable when possible.
- The whole-card link is used only when the footer does not need independent controls.
- Logo images have text alternatives through `logo_alt` or the customer name.

---

## CTA Band

Use this after proof and feature explanation, not as a substitute for the hero.

```kida
{% call band(width="bleed", variant="accent") %}
  {% call container() %}
    {% call stack(gap="md") %}
      <h2>Start building with Acme Agents</h2>
      <p>Improve each step of the agent development lifecycle from one platform.</p>
      {% call cluster() %}
        {{ btn("Start building", href="/start", variant="primary") }}
        {{ btn("Get a demo", href="/demo", variant="ghost") }}
      {% end %}
    {% end %}
  {% end %}
{% end %}
```

Checks:

- Use one primary action and at most one secondary action.
- Do not put a card inside the CTA band for section chrome.
- Copy is specific to the product or offer.

---

## When To Add A Component

Keep these recipes as documentation until repeated usage proves otherwise. A promoted component must satisfy the normal ChirpUI contract:

- `ComponentDescriptor` entry exists before CSS/classes ship.
- Template doc-block describes the macro.
- Emitted classes are present in the registry and matching CSS partial.
- Tests cover default rendering, a non-default path, invalid fallback behavior where relevant, and slot composition.
- `COMPONENT-OPTIONS.md` documents real public params after the API exists.
- Changelog fragment explains the user-facing behavior.

Likely candidates, in priority order:

| Candidate | Default | Promote when |
|-----------|---------|--------------|
| `site_nav_group` | Recipe | Grouped product navigation cannot be expressed cleanly with `site_header` slots |
| `lifecycle_showcase` | Recipe | `tabs_panels` plus `feature_section` markup becomes repeated and error-prone |
| `logo_cloud` | Built | Accessible proof bands are common and stable enough to ship proactively |
| `story_card` | Built | Customer outcome cards are common and stable enough to ship proactively |
| `cta_band` | Recipe | `band` plus `stack` plus `cluster` proves too verbose in multiple pages |

Do not add a generic landing-page builder or utility-class vocabulary.
