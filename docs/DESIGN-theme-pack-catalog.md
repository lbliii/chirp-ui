# DESIGN: Theme Pack Catalog

**Status:** Sprint 3 implementation started
**Created:** 2026-05-11
**Purpose:** define curated theme packs without forking component CSS.

## Decision

Curated Chirp UI theme packs are token-only CSS resources plus immutable Python
metadata. They are discoverable through a read-only package contract before any
write/export workflow exists.

Theme packs may set `--chirpui-*` tokens. They may not define component
selectors, utility classes, or private visual systems.

## Package Shape

Theme CSS lives under the Chirp UI static root so existing asset serving can
expose it:

```text
src/chirp_ui/templates/themes/<name>.css
```

Each pack must include:

- `:root` defaults when useful.
- `[data-theme="light"]`.
- `[data-theme="dark"]`.
- `[data-theme="system"]` inside `prefers-color-scheme` media queries.

Theme CSS should use a dedicated layer loaded after `chirpui.css`, for example:

```css
@layer app.theme {
    [data-theme="light"] {
        --chirpui-bg: oklch(0.985 0.004 248);
    }
}
```

## Metadata Shape

Preferred Python shape:

```python
@dataclass(frozen=True, slots=True)
class ThemePack:
    name: str
    label: str
    path: str
    description: str = ""
    modes: tuple[str, ...] = ("light", "dark", "system")
    maturity: str = "experimental"
```

The catalog must be immutable: tuples, frozen dataclasses, no mutable global
registries.

## Public Discovery

First public surface:

- A read-only list API.
- Projection into `get_library_contract()` if the host needs asset discovery.
- Projection into the manifest if agents need theme-aware guidance.

Initial catalog names:

- `atlas`
- `ember`
- `sage`

Do not add write/export commands until a separate design covers destination,
overwrite policy, source format, generated-file headers, and token validation.

## Token Contract

Theme packs may override only cataloged `--chirpui-*` tokens. New tokens must be
added to `TOKEN_CATALOG` and projected into the manifest before a pack uses
them.

Legacy Bengal `--color-*` aliases may exist only as transitional derived
aliases where retained Bengal CSS still requires them. New packs should author
the `--chirpui-*` contract first.

## Bengal Theme Mapping

The packaged Bengal `chirp-theme` keeps its entry point:

```text
chirp-theme = "bengal_themes.chirp_theme"
```

Theme packs do not replace the Bengal theme package. The catalog must either
map Bengal palette names to shared theme-pack names or explicitly mark Bengal
palette controls as transitional aliases.

## Required Proof

- Package-data/resource tests for every theme CSS file.
- Deterministic theme list ordering.
- Token-only scanner that rejects `.chirpui-*` selectors and non-token
  component rules.
- CSS syntax tests.
- Manifest/library contract tests if projected.
- Browser visual QA across light, dark, and system mode on desktop and mobile.

## Stop-And-Ask Items

- Adding a write/export command.
- Adding a new public theme-pack field.
- Changing Bengal theme entry points or storage keys.
- Allowing theme packs to contain component selectors.

## Non-Goals

- Utility classes.
- Component-specific theme overrides.
- Dynamic runtime CSS generation.
- New build dependencies.
