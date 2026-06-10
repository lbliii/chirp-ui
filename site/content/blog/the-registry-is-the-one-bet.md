---
title: The registry is the one bet
description: Why chirp-ui validates variants and sizes against a registry instead of trusting free-form strings.
date: 2026-03-12
draft: false
weight: 30
lang: en
author: chirp-ui-team
tags: [design, validation, components]
keywords: [registry, variant, size, validation, strict mode]
---

Most component libraries accept a `variant="primary"` string and hope you typed
it correctly. chirp-ui makes a different bet: every variant and size is checked
against a registry at render time.

## What the registry buys

If you pass `variant="primry"`, you do not silently get a default-styled button
with no warning. In development you get a `ChirpUIValidationWarning` pointing at
the typo; in strict mode (`set_strict(True)`) it escalates to a `ValueError` so
a bad value fails the test suite instead of shipping.

The vocabulary lives in Python — `VARIANT_REGISTRY` and `SIZE_REGISTRY` — not in
a wall of utility classes. That is the whole thesis: a *Python* vocabulary for
UI, not a string vocabulary you assemble by hand and debug in the browser.

## Falling back, not falling over

Unknown values do not crash a production render. They warn and fall back to the
component's documented default, so a stray typo degrades gracefully while still
being loud enough to catch. You opt into hard failures only where you want them
— usually CI — by flipping strict mode on.

It is a small constraint that pays for itself the first time a refactor renames
a variant and the registry tells you every call site that needs updating.
