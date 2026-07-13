# Print And PDF Contract

The packaged Bengal `chirp-theme` treats print as a complete reading surface,
not a screenshot of the screen layout. The contract is owned jointly by
`assets/css/base/print.css`, the print lifecycle in `assets/js/main.js`, and the
browser-backed fixture in `tests/browser/templates/bengal_print_contract.html`.

## Reader Contract

When a reader prints a page or uses the browser's PDF destination, the theme:

- forces a white paper surface and high-contrast text even from dark mode
- removes navigation, actions, overlays, and other screen-only chrome
- expands authored tabs and closed disclosures, then restores their prior state
- replaces interactive embeds with a short explanation that points readers to
  the online version
- uses the available printable width on A4, Letter, and larger portrait or
  landscape paper
- keeps short code, callout, card, and figure blocks together while allowing
  genuinely tall blocks to paginate instead of clipping or creating large gaps
- repeats table headers, keeps table rows intact, and keeps headings with the
  content they introduce
- underlines links and prints a tracking-free external URL only when the visible
  label is not already that URL
- appends the document title and canonical source URL as print-only provenance
- normalizes visual emphasis into standards-compatible tagged-PDF text during
  printing, then restores the exact authored roles
- preserves legibility when backgrounds are disabled or output is grayscale

The lifecycle-created URL and provenance nodes use DOM text properties rather
than raw HTML. They are removed after printing along with temporary disclosure
and pagination state.

## Tagged PDF Proof

Browser print dialogs control their own PDF feature set, so the theme cannot
promise that every browser's “Save as PDF” output is tagged. The repository
proof generator does request Chromium's tagged-PDF and document-outline modes
explicitly:

```console
uv sync --group browser
uv run playwright install chromium
uv run poe print-pdf-proof
```

The proof task writes to `output/pdf/` and covers three scenarios:

1. Letter paper with print backgrounds
2. A4 paper with print backgrounds disabled
3. Letter paper rendered in grayscale

Each PDF must emit no Poppler structure warnings and contain a structure tree,
language metadata, document outline,
headings, links, table roles, figure semantics, every stress-fixture sentinel,
the sanitized external URL, and the canonical source URL. Poppler then renders
every page to PNG and checks page count, nonblank content, white paper edges,
and grayscale channel parity. `output/pdf/index.html` is the human-review
contact sheet.

The proof task requires Poppler commands (`pdfinfo`, `pdftotext`, and
`pdftoppm`). CI installs those system tools and uploads the PDFs, page rasters,
manifest, and contact sheet as the `bengal-print-pdf-proof` artifact.

## Regression Surface

`tests/browser/test_bengal_print_contract.py` is part of the focused Chromium
smoke suite. It protects print-media computed styles, disclosure restoration,
clean link decoration, source metadata, long-block fragmentation, width across
paper sizes, and tagged/outlined PDF generation. `tests/js/main_print.test.js`
provides the faster lifecycle proof for temporary DOM state.

Changes to print CSS or lifecycle behavior should update the stress fixture and
both proof layers in the same pull request. Review the generated contact sheet
before treating the change as release-ready.
