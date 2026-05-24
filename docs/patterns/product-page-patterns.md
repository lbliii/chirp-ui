# Product Page Patterns

Status: recipe guidance

Use these recipes for marketing pages, docs homes, product-family pages, and
launch pages. They compose shipped Chirp UI primitives; they do not authorize a
landing-page builder, product-specific shell, or utility-class vocabulary.

## Starting Surface

Common imports:

```kida
{% from "chirpui/site_shell.html" import site_shell %}
{% from "chirpui/site_header.html" import site_header, site_nav_link %}
{% from "chirpui/site_footer.html" import site_footer, footer_column, footer_link %}
{% from "chirpui/hero.html" import hero %}
{% from "chirpui/band.html" import band %}
{% from "chirpui/button.html" import btn %}
{% from "chirpui/cta_band.html" import cta_band %}
{% from "chirpui/layout.html" import container, stack, cluster, grid, frame, section_header %}
{% from "chirpui/logo_cloud.html" import logo_cloud %}
{% from "chirpui/feature_section.html" import feature_section %}
{% from "chirpui/tabs_panels.html" import tabs_container, tab_button, tab_panel %}
{% from "chirpui/index_card.html" import index_card %}
{% from "chirpui/story_card.html" import story_card %}
{% from "chirpui/metric_grid.html" import metric_grid, metric_card %}
```

Keep imports in the nearest layout or page template that owns the composition.
For HTMX fragments, follow [composition](../fundamentals/composition.md).

## Recipe Matrix

| Pattern | Use When | Compose With | Checks |
|---|---|---|---|
| Product hero with adjacent proof | The first viewport needs a product name, clear promise, primary action, and immediate trust signal. | `site_shell`, `site_header`, `hero`, `cluster`, `btn`, `band`, `logo_cloud`. | H1 names the product or offer; proof appears before deep feature copy; no page-owned layout classes. |
| Lifecycle showcase | The product is understood as a sequence such as Build, Observe, Evaluate, Deploy. | `tabs_container`, `tab_button`, `tab_panel`, `feature_section`, `surface`, `stack`. | Tab labels are jobs; each panel shows a real artifact; default content works before Alpine. |
| Proof band | The page needs logos, ecosystem proof, adoption metrics, or customer evidence. | `band`, `container`, `section_header`, `logo_cloud`, `metric_grid`, `metric_card`, `marquee`. | Logos have text alternatives; repeated proof comes from data; motion stays in existing `marquee`. |
| Product choice grid | Users need to compare products, frameworks, modules, or entry points. | `container`, `stack`, `grid`, `index_card`; use `resource_index` when search/filter state matters. | Cards explain decision criteria; grid owns repetition; cards own navigation. |
| Customer story strip | The page needs specific user outcomes. | `container`, `stack`, `grid`, `story_card`; use `card` only for truly custom story structure. | Outcomes are specific; whole-card links avoid nested controls; logos have alt text. |
| CTA band | The page needs a closing action after proof and explanation. | `cta_band`. | One primary action, at most one secondary action; no card inside CTA chrome; copy names the offer. |

## Minimal Skeleton

```kida
{% call site_shell() %}
  {% slot header %}
    {% call site_header(current_path=current_path) %}
      {% slot brand %}Acme Agents{% end %}
      {% slot nav %}
        {{ site_nav_link("/platform", "Platform", match="prefix") }}
        {{ site_nav_link("/docs", "Docs", match="prefix") }}
      {% end %}
    {% end %}
  {% end %}

  {% call hero(title="Acme Agents", subtitle="Observe, evaluate, and deploy production agents.") %}
    {% slot actions %}
      {% call cluster(gap="sm") %}
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

## Promotion Gates

Keep recipes as documentation until repeated usage proves a component would
remove real duplication.

| Candidate | Default | Promote when |
|---|---|---|
| `site_nav_group` | Recipe | Grouped product navigation cannot be expressed cleanly with `site_header` slots. |
| `lifecycle_showcase` | Built | Default lifecycle tabs plus feature panels repeat across real pages. |
| `logo_cloud` | Built | Accessible proof bands are common and stable enough to ship proactively. |
| `story_card` | Built | Customer outcome cards remain stable across real pages. |
| `cta_band` | Built | CTA sections are common and stable enough to ship proactively. |

A promoted component needs a descriptor, emitted-class coverage, CSS partial,
template docs, tests, generated docs, and changelog collateral.
