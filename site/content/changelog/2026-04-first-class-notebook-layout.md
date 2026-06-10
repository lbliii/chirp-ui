---
title: "v0.9 — First-class notebook layout"
name: "First-class notebook layout"
status: stable
description: >-
  The notebook template family graduates to a real layout, and the changelog
  single now renders version-grouped change sections from structured
  frontmatter.
date: 2026-04-05
draft: false
weight: 5
lang: en
tags: [theme, content]
keywords: [chirp-theme, changelog, notebook, structured-frontmatter]

added:
  - A `notebook/list.html` index built on the shared `learning_index()` macro.
  - A dogfood notebook page so the notebook layout renders on the live site.
changed:
  - "`tutorial/list.html` now composes the shared `learning_index()` macro instead of an inlined `resource_index` + `content_cards` block."
fixed:
  - Changelog entries can now drive the structured Added/Changed/Fixed sections from frontmatter, exercising the `change_section` path in `changelog/single.html`.
---

This entry populates the **structured changelog frontmatter** path
(`added:` / `changed:` / `fixed:`) so `changelog/single.html` renders labelled,
counted change sections instead of only a Markdown body. Older entries (which
use Markdown `## Added` headings) still render through the body fallback — both
authoring shapes are intended dogfood.
