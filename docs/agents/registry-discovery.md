# Registry Discovery

**Status:** active reference  
**Scope:** Finding Chirp UI components, primitives, patterns, maturity labels, and registry metadata from an installed package

The component registry is the source of truth. Discovery should start from the
manifest and `find` helpers instead of guessing macro names, CSS classes, slots,
or maturity status.

## Two Layers Of Agent Discovery

Chirp applications and the Chirp UI component library expose different MCP
surfaces. Use both when an agent needs to understand an application and choose
the component vocabulary used to change it.

| Question | MCP surface | Read-only tools | Use it for |
|---|---|---|---|
| What routes and hypermedia contracts does this application ship? | Chirp's Milo-backed MCP server (`chirp --mcp`) | `check`, `diff`, `routes` | Inspecting an app import, validating route/template/target contracts, or comparing the app contract with a git baseline. |
| Which Chirp UI surface should the application use? | Chirp UI's manifest MCP server (`chirp-ui mcp`) | `find_components`, `get_component`, `list_categories` | Searching the installed component registry, inspecting one manifest entry, or narrowing discovery by category. |

Start with Chirp when the question contains application state: which handler
owns a route, whether an HTMX target resolves, or what changed in the compiled
app contract. Then use Chirp UI when the question is about authoring vocabulary:
which component or primitive exists, whether it is preferred or experimental,
which slots it exposes, and which runtime it requires.

The Chirp UI MCP server reads the installed `chirpui-manifest@5`; it does not
load or validate a Chirp application. Conversely, Chirp's app inspection tools
do not replace component-level registry discovery. See Chirp 0.10's
[CLI and Milo MCP agent-inspection reference](https://lbliii.github.io/chirp/docs/reference/cli/)
for the app import boundary, MCP allowlist, and structured results.

## CLI

Use `python -m chirp_ui find` for local human and agent discovery. It searches
the installed manifest by component name, BEM block, category, maturity,
authoring hint, role, and description.

```bash
python -m chirp_ui find metric
python -m chirp_ui find --category=feedback
python -m chirp_ui find --authoring=preferred
python -m chirp_ui find --maturity=experimental
python -m chirp_ui find --role=pattern --maturity=experimental --details
```

Default output is intentionally compact:

```text
metric-card  data-display  Metric card
metric-grid  data-display  Metric grid/card
```

Use `--details` when choosing or auditing a surface. It shows existing manifest
metadata without changing the manifest schema:

```bash
python -m chirp_ui find token-input --details
```

Detailed output includes:

- name
- category
- maturity
- authoring
- role
- macro
- template
- runtime requirements
- slots
- summary

## Common Audits

Preferred primitives:

```bash
python -m chirp_ui find --role=primitive --authoring=preferred --details
```

Experimental public surfaces:

```bash
python -m chirp_ui find --maturity=experimental --details
```

Recipe-first patterns:

```bash
python -m chirp_ui find --role=pattern --maturity=experimental --details
```

Compatibility helpers:

```bash
python -m chirp_ui find --authoring=compatibility --details
```

## Python Helpers

Use the Python helpers when tools or tests need structured manifest entries.

```python
from chirp_ui import load_manifest
from chirp_ui.find import (
    components_by_authoring,
    components_by_maturity,
    components_by_role,
    detailed_search,
    preferred_components,
)

manifest = load_manifest()

preferred = preferred_components(manifest=manifest)
experimental_patterns = components_by_role(
    "pattern",
    manifest=manifest,
    maturity="experimental",
)
legacy_helpers = components_by_authoring("compatibility", manifest=manifest)
token_rows = detailed_search(manifest, "token-input")
```

The helpers return data from the shipped manifest. They do not validate rendered
HTML, generate snippets, or authorize promotion. Use
[PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md) for maturity
decisions and [DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md)
for behavior-bearing promotion evidence.

## Labels

Discovery exposes labels that already exist in the manifest:

| Field | Meaning |
|---|---|
| `maturity` | Stability state such as `stable`, `experimental`, `legacy`, or `internal`. |
| `authoring` | Agent/developer guidance such as `preferred`, `available`, `compatibility`, or `internal`. |
| `role` | Surface shape such as `primitive`, `component`, `pattern`, `effect`, or `infrastructure`. |
| `category` | Product family such as `layout`, `feedback`, `form`, `navigation`, or `data-display`. |

Do not infer `recipe-only` from a name alone. Recipe-first decisions live in
[PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md) and are
usually represented as `role=pattern`, `maturity=experimental`, and
non-preferred authoring until repeated consumers prove a public API.

## Boundaries

- `find` is discovery, not validation.
- In plain terms: find is discovery, not validation.
- `find --details` is local CLI output, not a generated artifact.
- In plain terms: find --details is local CLI output, not a generated artifact.
- The manifest schema remains `chirpui-manifest@5`.
- New descriptor fields, manifest schema fields, or public extension protocols
  still require a separate design plan and stop-and-ask review.
