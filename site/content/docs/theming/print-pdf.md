---
title: Print and PDF
description: The chirp-theme contract for readable printouts and tagged PDF proof
draft: false
weight: 45
lang: en
type: doc
keywords: [chirp-theme, print, pdf, accessibility, docs]
category: theming
---

# Print and PDF

The packaged Bengal `chirp-theme` treats print as a complete reading surface,
not a screenshot of the screen layout.

When a reader prints a page or uses a browser's PDF destination, the theme:

- forces a white, high-contrast paper surface even from dark mode
- removes navigation, actions, overlays, and screen-only chrome
- expands tabs and closed disclosures, then restores their prior state
- replaces interactive embeds with a short online-version explanation
- uses the printable width on A4, Letter, and larger paper formats
- keeps short related blocks together but lets genuinely tall code, callout,
  card, and figure blocks paginate instead of clipping
- repeats table headers and keeps headings with the content they introduce
- underlines links and prints cleaned external URLs without tracking parameters
- appends the document title and canonical source URL
- normalizes visual emphasis into standards-compatible tagged-PDF text and
  restores the authored roles after printing
- remains legible with backgrounds disabled and in grayscale

Browser print dialogs control their own PDF feature set, so not every browser's
“Save as PDF” output is guaranteed to be tagged. Chirp UI's repository proof
generator explicitly requests Chromium's tagged-PDF and document-outline modes
and verifies structure, text completeness, paper edges, and raster legibility
across color, background-off, and grayscale scenarios.

The canonical implementation and contributor contract is
[`docs/theming/print-pdf.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/theming/print-pdf.md?plain=1).
