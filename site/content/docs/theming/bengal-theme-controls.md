---
title: Bengal theme controls anatomy
description: Packaged chirp-theme hooks for theme menus, search, mobile nav, TOC, and docs tabs
draft: false
weight: 36
lang: en
type: doc
keywords: [chirp-theme, Bengal theme, search modal, mobile nav, theme controls]
category: theming
---

# Bengal theme controls anatomy

The packaged `chirp-theme` ships static-site controls for appearance menus,
search, mobile navigation, docs navigation, table-of-contents tracking, and
content tabs.

These are **Bengal theme partial and asset hooks**, not registry-owned Chirp UI
component macros. App-level component contracts still come from the Chirp UI
component registry, macros, generated CSS, and manifest.

The full rendered contract, selectors, browser-owned behavior, JavaScript
exports, and proof locations live in the canonical source guide:
[`docs/BENGAL-THEME-ANATOMY.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/BENGAL-THEME-ANATOMY.md?plain=1).
