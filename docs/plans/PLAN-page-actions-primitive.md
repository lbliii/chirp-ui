# chirp-ui: Page Actions Primitive Investigation

Status: active investigation, no public API authorized
Date: 2026-05-23
Depends on:

- [PLAN-application-chrome-system.md](PLAN-application-chrome-system.md)
- [../BENGAL-THEME-ANATOMY.md](../BENGAL-THEME-ANATOMY.md)
- [../DROPDOWN-ANATOMY.md](../DROPDOWN-ANATOMY.md)
- [../MODAL-ANATOMY.md](../MODAL-ANATOMY.md)
- [../PUBLIC-SURFACE-STABILIZATION.md](../PUBLIC-SURFACE-STABILIZATION.md)

## Goal

Decide whether Chirp UI should promote a narrow page-actions primitive for
page-local commands such as copy URL, open/copy LLM text, AI handoff, share,
and app-supplied page tools.

This plan does not authorize `page_actions()`, a descriptor, emitted classes,
CSS, JavaScript runtime, manifest changes, or generated docs. It is the
contract work required before asking for a public API change.

## Why This Candidate

The application-chrome evidence-ledger synthesis identified page actions as a
narrow candidate because Bengal docs pages already repeat a useful shape:
actions live near the page title, use a native popover, expose copy/LLM/AI
handoff hooks, and must stay reachable without turning the whole docs shell into
a generic `docs_shell()` macro.

This is not a generic shell problem. It is a page-local command surface problem.

## Existing Primitives Tried

| Existing surface | What it solves | Why it is not the whole contract |
|---|---|---|
| `page_hero` actions slot | Places actions near page title and metadata. | Does not define command anatomy, copy behavior, AI handoff hooks, or empty-slot behavior. |
| `dropdown_menu` | Provides command-menu anatomy and item events. | Does not define page URL, LLM text, external assistant, or copy-to-clipboard semantics. |
| `share_menu` | Provides legacy social sharing links and copy link affordance. | It is a social-share menu, not a page-command surface; it lacks LLM text and app command semantics. |
| `action_bar` | Provides visible social/content actions. | It is an inline row, not a title-adjacent overflow/popover surface. |
| Bengal `page_actions` partial | Proves the theme-owned target shape. | It uses theme selectors and Bengal static scripts; it is not a registry-owned Chirp UI contract. |

## Reference Evidence Scan

Current scan result: the promotion gate is not satisfied. Bengal docs/reference
pages are the only qualifying implementation context for copy URL, LLM text,
AI handoff, and title-adjacent page actions together. This is not a userbase
gate; it means we must build or identify a scenario-complete non-Bengal
reference implementation before proposing `page_actions()`.

| Evidence | Current Shape | Counts Toward Promotion? | Reason |
|---|---|---:|---|
| Bengal docs/reference page actions | Native popover near page hero/reference header with copy URL, open/copy LLM text, and AI handoff hooks. | Partial | Packaged theme pressure, but theme selectors and static scripts are not Chirp UI registry API. |
| Forum site pattern detail page | Uses `share_menu` and `action_bar` for thread/post sharing, replies, votes, follows, watches, and reports. | No | Social/forum actions prove `share_menu` and `action_bar`; they do not need LLM text, AI handoff, or title-adjacent page-command semantics. |
| Component showcase social/layout examples | Demonstrate `share_menu` and `action_bar` in isolated examples. | No | Showcase examples are useful visual/API proof but not scenario-complete implementation repetition. |
| Product/media pattern docs | Mention share or secondary actions in recipes. | No | Recipe prose does not prove a repeated rendered page-action contract. |
| Existing `share_menu` component | Provides social-share links and copy-link affordance. | No | It remains the compatibility/social sharing surface; it should not be counted as evidence for a new page-command primitive. |

Implementation evidence still needed:

- one non-Bengal scenario-complete app, example, or packaged integration with a
  page or object header that needs copy URL plus at least one non-social page
  command,
- evidence that `page_hero` actions, `dropdown_menu`, `share_menu`, and
  `action_bar` were tried or considered,
- a written gap showing why the remaining need is page-local command anatomy
  rather than social sharing, generic dropdown actions, or shell composition,
- browser proof for trigger placement, popover containment, keyboard/focus, and
  overflow before public API work begins.

## Non-Bengal Reference Candidate Scan

Scan date: 2026-05-23

Result: no existing non-Bengal page qualifies as the second reference
implementation yet. The best next move is a scenario-complete first-party
reference page that tries current primitives first, then records whether a
page-actions gap remains.

| Candidate | Current Signals | Existing Primitives To Try | Qualifies Now? | Decision |
|---|---|---|---:|---|
| Component showcase Streaming & AI page | Has LLM/SSE context, assistant messages, copy buttons, model cards, and a stable page header. | `page_header` actions, `dropdown_menu`, `share_menu`, `action_bar`, existing `copy_button`. | No | Best candidate for a private fixture because it could need copy demo URL plus open/copy transcript or prompt text, but the current page does not repeat Bengal's title-adjacent page-action shape. |
| Component showcase catalog/detail routes | Have browsable resource/detail context and existing command/search surfaces. | `page_hero` actions, `dropdown_menu`, `action_bar`, `share_menu`. | No | Useful for generic page tools, but there is no LLM text or AI handoff need. |
| Forum site pattern detail page | Has thread/post sharing, replies, votes, watches, reports, and social share affordances. | Existing `share_menu` and `action_bar`. | No | Confirms the social/action-bar boundary; it should not be counted as page-actions pressure. |
| Product/media pattern pages | Have public content actions and share-adjacent recipes. | `share_menu`, `action_bar`, `dropdown_menu`. | No | Pattern prose is not reference implementation evidence and does not need AI/LLM actions. |
| Bengal docs/reference pages | Have copy URL, open/copy LLM text, and AI handoff in a title-adjacent native popover. | Bengal theme partial plus static enhancement script. | Partial | Still the only qualifying implementation context, but theme selectors and static scripts are not Chirp UI API. |

Candidate fixture rule:

- Start with the Streaming & AI page family only if the scenario naturally needs
  copy current URL plus open/copy transcript, prompt, or LLM sample text.
- Use existing `page_header` actions, `dropdown_menu`, `share_menu`,
  `action_bar`, and `copy_button` before sketching any new macro.
- If those primitives suffice, close the candidate as no-new-API evidence.
- If they fail, record the exact missing anatomy: trigger placement, command
  grouping, copy/fetch behavior, status feedback, external link safety,
  keyboard/focus, and responsive containment.
- Keep the fixture private/copyable until browser proof shows the repeated gap
  is not Bengal-specific.

## Private Candidate Fixture

Status: implemented as test evidence only, no public API authorized.

Fixture:

- route: `/page-actions-candidate`
- template: `tests/browser/templates/page_actions_candidate_page.html`
- browser proof: `tests/browser/test_page_actions_candidate.py`

What the fixture proves:

- A Streaming & AI page can place page-local tools in `page_header` actions
  using existing `dropdown_menu` and `share_menu`.
- `action_bar` and `copy_button` can cover visible local actions and known-text
  copy behavior without a new macro.
- The fixture can expose non-social commands such as open prompt text and copy
  sample text while staying outside Bengal theme selectors.
- Phone, tablet, and desktop widths can keep the candidate trigger region
  visible without document-level horizontal overflow.
- A deliberately long non-social dropdown command can stay contained at 320px
  without a new page-actions primitive or component CSS.

What the fixture does not prove:

- It does not prove that `page_actions()` should exist.
- It does not provide URL/LLM text/AI handoff semantics as one owned Chirp UI
  contract.
- It does not add a descriptor, macro, emitted class, CSS partial, generated
  CSS, manifest entry, generated component options, runtime controller, docs
  page, or changelog.
- It does not count as qualifying implementation evidence until a
  scenario-complete reference implementation records a repeated gap after
  existing primitives are tried.

Fixture decision:

| Question | Current Answer |
|---|---|
| Do existing primitives render the candidate shape? | Yes, as a private fixture. |
| Is there enough evidence for public API promotion? | No. |
| Is the next slice implementation or analysis? | Analysis: inspect fixture behavior and record whether the remaining gap is real. |
| What would unlock promotion? | A second independent reference implementation that repeats copy URL plus non-social page commands after trying this fixture pattern. |

## Fixture Analysis

Analysis date: 2026-05-23

Decision: keep page actions in investigation. The fixture shows existing
primitives can render a credible Streaming & AI page-action candidate, but it
does not prove a public `page_actions()` API gap.

| Behavior | Existing Primitive Outcome | Remaining Gap | API Signal |
|---|---|---|---|
| Title-adjacent placement | `page_header` actions can hold `dropdown_menu` and `share_menu` in a compact header. | Layout works, but ownership is split across independent primitives. | Weak: composition is acceptable. |
| Grouped non-social commands | `dropdown_menu` can expose open prompt text, copy sample text, and review links. | Generic menu actions do not own clipboard/fetch status or LLM/AI semantics. | Medium only if a second reference implementation repeats those semantics. |
| Social/canonical URL share | `share_menu` covers copy/social URL affordances. | It remains a social-share compatibility surface, not a page-command primitive. | Weak: do not replace it yet. |
| Known-text copy | `copy_button` copies a known prompt string and shows local feedback. | It does not fetch LLM text, copy the current page URL, or coordinate with a page command menu. | Medium only for an eventual runtime question. |
| Visible local actions | `action_bar` covers inline visible actions. | It is not title-adjacent overflow and does not group page-level commands. | Weak: boundary is clear. |
| Responsive containment | Browser proof covers 320, 390, 768, and 1024 widths without document overflow. | A future owned popover would still need viewport, focus, and long-label proof. | Good fixture proof, not API proof. |

Current gap classification:

- Real gap: there is no single owned contract for page URL, LLM text fetch/copy,
  AI handoff, grouped page commands, status feedback, and external link safety.
- Not yet a promotion gap: the fixture is still one artificial non-Bengal
  candidate, not a scenario-complete reference implementation.
- Practical next step: keep the fixture as regression/evidence, then build or
  identify a scenario-complete reference implementation that repeats the same
  need after trying this composition.

Next-slice options from this analysis:

| Slice | Purpose | Promotion Risk |
|---|---|---|
| Fixture gap notes | Add comments/docs around what the fixture cannot express with current primitives. | Low; docs/test only. |
| Private behavior stress | Added browser proof for copy feedback, prompt text route, long labels, and dropdown containment. | Closed for the current private fixture; still not API proof. |
| Reference implementation design | Use external design-system patterns and Bengal pressure to define a non-Bengal app/docs/reference page with copy URL plus non-social commands. | Low; evidence gathering. |
| Public API proposal | Draft a promotion proposal only after a second reference implementation repeats the gap. | High; stop and ask first. |

Private behavior stress result:

- `tests/browser/test_page_actions_candidate.py` verifies the prompt text route,
  `copy_button` feedback, long dropdown command visibility, menu containment at
  320px, and no document-level horizontal overflow.
- The stress result strengthens the existing-primitives recipe, not the public
  API case. A future owned primitive would still need focus, status, fetch,
  external-link, and AI handoff proof after a second reference implementation exists.

## Reference Evidence Search

Search date: 2026-05-23

Result: no second qualifying scenario-complete non-Bengal reference
implementation exists in the repository yet. Page actions should remain in
investigation while the next application-chrome slice moves to another
candidate or builds deliberate reference evidence from external market patterns.

Search scope:

- `docs/`
- `examples/`
- `tests/browser/templates/`
- `tests/browser/app.py`
- `src/chirp_ui/templates/`
- excluded Bengal theme templates and this plan to avoid counting the original
  theme pressure or self-references

Qualifying criteria:

- page or object header placement,
- copy current/canonical URL,
- at least one non-social page command,
- LLM text, prompt/transcript, AI handoff, or another page-local command
  semantic beyond generic menu/share/social actions,
- evidence that existing `page_header`, `page_hero`, `dropdown_menu`,
  `share_menu`, `action_bar`, and `copy_button` were tried or considered.

Search findings:

| Candidate | Evidence Found | Why It Does Not Qualify |
|---|---|---|
| Private `/page-actions-candidate` fixture | Uses `page_header`, `dropdown_menu`, `share_menu`, `action_bar`, `copy_button`, prompt text route, copy feedback, long labels, and dropdown containment proof. | Artificial evidence fixture, not a scenario-complete reference implementation; it proves current primitives can model the scenario. |
| Dense object chrome browser fixture | Uses several `dropdown_menu` command surfaces near dense object context. | Commands are object/workflow tools, not copy URL plus LLM/prompt/AI handoff semantics. |
| Application chrome route fixtures | Use `page_header`, route tabs, breadcrumbs, command bars, page tools, and shell actions. | They prove app chrome composition and response ownership, not page-local copy/LLM actions. |
| Gauntlet command surfaces | Stress dropdowns, command bars, edge menus, long labels, and overflow. | Browser stress evidence only; not a page/object header reference implementation with URL/LLM actions. |
| Forum site patterns | Use `share_menu` and `action_bar` for replies, votes, reports, follows, watches, and social sharing. | Confirms the social/action boundary; no LLM text, AI handoff, or page-local command group. |
| Product/media pattern pages | Mention share-adjacent actions, assistant panels, and content actions. | Pattern prose and visual recipes, not rendered reference implementation repetition. |
| Streaming showcase page | Has LLM/SSE context and copy controls. | The current public showcase page does not place copy URL plus non-social commands in a title-adjacent page-action surface. |

Decision after search:

- Keep `page_actions()` unauthorized.
- Keep the private fixture as regression and evidence for existing primitive
  composition.
- Do not count forum/social, dense object command menus, gauntlet stress cases,
  or recipe prose as page-actions promotion evidence.
- The next useful implementation slice should not be a public page-actions API.
  Either build a scenario-complete external-pattern-backed reference
  implementation or move to the next readiness queue candidate such as linked
  nav-tree/sidebar semantics.

Reference implementation evidence intake:

| Evidence Field | Required Record |
|---|---|
| Implementation identity | Scenario-complete non-Bengal app, package, or docs/reference route family; private fixtures and pattern prose do not qualify. |
| Existing primitives tried | `page_header` or `page_hero` actions, `dropdown_menu`, `share_menu`, `action_bar`, and `copy_button` where applicable. |
| Repeated gap | Exact page-local behavior still missing after composition, such as copy current URL, fetch/copy LLM text, AI handoff, grouped non-social commands, or status feedback. |
| Proof | Browser or server proof that the page tried current primitives and still needs repeated app-owned glue. |
| Boundary | Explicit no-authorization note for `page_actions()`, descriptors, CSS, manifest, generated options, runtime, docs, and changelog until the promotion gate is satisfied. |
| Decision | Keep as recipe evidence, gather another reference implementation, or stop and ask for an explicit public API/design plan. |

Disqualifiers:

- private `/page-actions-candidate` fixture by itself,
- Bengal page actions by themselves,
- social sharing that `share_menu` already covers,
- dense object command menus without URL/LLM/AI semantics,
- copy buttons for known local text without page-level command grouping,
- visual preference for title-adjacent actions without a repeated behavior gap.

## Candidate Contract Shape

A future primitive, if accepted, should be narrower than a shell:

| Contract | Candidate requirement |
|---|---|
| Surface | Page-local actions attached to page header, hero, reference header, or object context. |
| Anatomy | Trigger, native popover/menu panel, header/summary, action items, sections, optional app-provided items. |
| Semantics | Native `[popover]` where browser support is sufficient; fallback strategy must be explicit if required. |
| Built-in actions | Candidate built-ins are copy URL, open LLM text, copy LLM text, and external AI handoff. |
| Extension | App-supplied actions should be structured data or explicit slots, not raw JavaScript strings. |
| Runtime | Copy behavior and AI handoff must live in a named Chirp UI runtime module, not inline scripts. |
| Escaping | URLs, labels, assistant IDs, prompts, and data hooks must render through normal template escaping and attribute helpers. |
| Keyboard/focus | Popover trigger and items must be keyboard reachable; Escape/light dismiss must be browser-owned or tested in the fallback. |
| Responsive | The trigger must fit compact headers; the popover must stay inside the viewport at phone, tablet, and desktop widths. |

## Open Design Questions

- Should the public name be `page_actions`, `page_action_menu`, or a more
  general command/share name?
- Should Chirp UI ship copy URL / LLM text helpers as built-ins, or should apps
  provide every action explicitly?
- Should AI assistant links be built-in presets, or only app-provided items?
- What is the non-JavaScript fallback for copy actions and AI handoff?
- Should this compose `dropdown_menu`, or should it use native popover anatomy
  directly to avoid menu-button claims Chirp UI does not publish yet?
- How does it coexist with `share_menu` without creating two confusing share
  APIs?

## Non-Authorizing API Sketch

This sketch is evaluation input only. Do not copy it into templates, generated docs, examples, or downstream code as a supported API.

Provisional macro shape:

```kida
{% from "chirpui/page_actions.html" import page_actions %}

{{ page_actions(
  title="Page actions",
  url=page_url,
  llm_text_url=llm_txt_url,
  actions=[
    {"type": "copy-url", "label": "Copy URL"},
    {"type": "open-url", "label": "Open LLM text", "href": llm_txt_url},
    {"type": "copy-url", "label": "Copy LLM text", "url": llm_txt_url},
    {"type": "ai-handoff", "label": "Ask ChatGPT", "assistant": "chatgpt", "href": chatgpt_url},
  ],
) }}
```

Candidate parameters:

| Parameter | Required | Candidate meaning |
|---|---:|---|
| `title` | no | Accessible/menu header label; defaults to a localized "Page actions". |
| `label` | no | Visible trigger text; can be hidden at compact widths by CSS, not by removing the accessible name. |
| `url` | yes for built-in copy URL | Canonical page URL used by copy/share actions. |
| `llm_text_url` | no | Canonical LLM text endpoint used by open/copy LLM text and AI handoff actions. |
| `actions` | no | Structured action item list; defaults are not decided. |
| `id` | no | Stable popover id; generated fallback must avoid duplicate ids. |
| `placement` | no | Popover alignment hint, not a layout system. |
| `cls` / `attrs_map` | no | Standard extension points if the public API follows existing macro conventions. |

Candidate action item shape:

| Field | Applies to | Candidate meaning |
|---|---|---|
| `type` | all items | One of `copy-url`, `open-url`, `copy-text-url`, `ai-handoff`, `custom-link`, `custom-button`, or `separator`. |
| `label` | visible items | Rendered label and accessible name source unless `aria_label` overrides it. |
| `url` | copy/open actions | URL copied to clipboard or fetched for text. |
| `href` | links and AI handoff | Destination URL for native link behavior. |
| `assistant` | AI handoff | Explicit assistant id; no behavior may be inferred from the label. |
| `icon` | visible items | Semantic icon name from the Chirp UI icon system, not raw SVG. |
| `method` | custom buttons | Optional app action identifier; must not become inline JavaScript. |
| `attrs_map` | advanced items | Escaped attribute extension map; raw unsafe attributes require a separate design. |

Candidate slots:

| Slot | Purpose | Boundary |
|---|---|---|
| `trigger` | Override trigger content while preserving trigger attributes. | Slot content must not own `popovertarget` or click behavior. |
| `header` | Add short title/help text inside the popover. | No interactive controls unless explicitly designed. |
| `actions` | Append app-specific action rows. | Prefer structured items first; slot is for markup that cannot fit the item schema. |
| `footer` | Optional low-priority metadata or help link. | Must not become a second command region. |

Candidate runtime contract:

- Use native `[popover]` for open/close, light dismiss, Escape, and top-layer
  behavior when browser support is sufficient.
- Add a named Chirp UI runtime controller only for clipboard status, fetching
  LLM text, and AI handoff preparation.
- Runtime event hooks, if any, should be namespaced such as
  `chirpui:page-action-copy` and `chirpui:page-action-error`.
- Copy and AI handoff state must be scoped to the component root; no global
  mutable state or per-frame work.
- No inline scripts, no server-provided JavaScript snippets, and no label-based behavior inference.

Coexistence decision for this investigation:

- `share_menu` remains the social-share compatibility surface.
- `dropdown_menu` remains a generic command/select/split menu family.
- A future page-actions primitive should own page URL, LLM text, AI handoff,
  and page-local command semantics only if the promotion gate is satisfied.

## Proof Matrix For Promotion

| Proof Area | Required proof before public API |
|---|---|
| Registry and manifest | Descriptor with maturity/authoring/role, emitted classes, runtime requirements, and manifest projection tests. |
| Template anatomy | Render tests for trigger, popover, sections, built-in items, custom items, empty action list, ids, labels, and slots. |
| Escaping and security | Tests for escaped labels, URLs, assistant ids, prompts, `attrs_map`, external links with `rel="noopener noreferrer"`, and no inline script payloads. |
| Runtime | JS/browser tests for copy URL, copy LLM text, fetch failure, status reset, AI handoff, and event hooks. |
| Keyboard and focus | Browser tests for trigger focus, Tab order, Escape/light dismiss, focus return, and keyboard activation of each item type. |
| Responsive and overflow | Browser tests at 320, 390, 768, 1024, and desktop widths for compact trigger, popover containment, long labels, and no document-level horizontal overflow. |
| CSS and tokens | CSS partial plus generated CSS proof for layers, tokens, control height, focus ring, reduced motion, and no theme-only selectors. |
| Docs and examples | `COMPONENT-OPTIONS.md`, durable docs, published docs bridge, copyable example, migration note for `share_menu` boundaries, and changelog fragment. |

## Promotion Gate

Do not implement a public macro until all of these are true:

- Bengal plus one additional independent reference implementation repeat the
  page-local action shape.
- The additional implementation tries `page_hero` actions, `dropdown_menu`,
  `share_menu`, and `action_bar`, and records the remaining gap.
- A draft API names macro parameters, slots, action item shape, event hooks,
  runtime requirements, and escape boundaries.
- Render tests cover trigger/menu anatomy, built-in actions, app-provided
  actions, empty states, escaping, and strict undefined behavior.
- Browser tests cover popover open/close, keyboard reachability, copy success and failure states, external link behavior, responsive containment, and no
  document-level horizontal overflow.
- Security review covers clipboard behavior, external assistant links,
  `rel="noopener noreferrer"`, and no inline script payloads.
- Collateral plan includes descriptor, macro, CSS partial, generated CSS,
  manifest, generated component options, docs, examples, browser proof, and
  changelog.

## Not Now

- Do not add `page_actions()` in this investigation slice.
- Do not move Bengal `.chirp-theme-page-actions*` selectors into `chirpui-*`
  classes.
- Do not add generated manifest fields or anatomy metadata.
- Do not bake a vendor AI assistant list into Chirp UI without an explicit
  public API decision.
- Do not replace `share_menu` until migration and compatibility are designed.
- Do not use this candidate to justify `application_chrome()`,
  `catalog_shell()`, or `docs_shell()`.

## Next Slice Options

| Slice | Output | Proof |
|---|---|---|
| Reference implementation design | Define one non-Bengal page-action reference implementation and existing primitives to try. | Docs test pins implementation evidence and non-authorization boundary. |
| API sketch | Draft macro/action item shapes without touching code. | Plan test pins parameters, slots, runtime, and escaping questions. |
| Prototype fixture | Build a private browser fixture using existing primitives only. | Browser proof for placement, popover containment, copy hooks, and overflow. |
| Promotion PR | Add the actual public component only after the gate is satisfied. | Full component contract proof and generated collateral. |

## Steward Notes

Consulted stewards: Planning, Documentation, Test Contract, Bengal Theme, and
Application Chrome.

Accepted findings:

- Treat Bengal page actions as real theme pressure but not enough for registry
  promotion alone.
- Keep the candidate narrow: page-local commands, not shell composition.
- Preserve existing `share_menu`, `dropdown_menu`, and `page_hero` boundaries.
- Require browser proof because native popover, clipboard, focus, and overflow
  are browser-owned risks.

Deferred findings:

- Public macro naming.
- Built-in AI assistant presets.
- Runtime module shape.
- Migration path from `share_menu` or Bengal page-actions hooks.
