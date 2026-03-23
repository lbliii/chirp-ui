---
title: Security
description: "| safe", html_attrs, and XSS considerations
draft: false
weight: 44
lang: en
type: doc
keywords: [chirp-ui, security, xss, html_attrs]
icon: shield
---

# Security

## `| safe`

chirp-ui uses `| safe` only where outputs are trusted or pre-escaped. **`attrs`** string escape hatches in several macros pass through raw HTML — **never** pass user-controlled strings.

## `html_attrs`

- **Mapping input** — keys and values are HTML-escaped. Prefer **`attrs_map`** / dicts for HTMX attributes.
- **Raw string input** — passed through unescaped. Caller responsibility.

## Recommendations

1. Prefer **`attrs_map`** over raw **`attrs`** strings.
2. Never pass user input to **`attrs`** or **`meta`** without sanitization.
3. Streaming markdown content should be from **trusted** sources.

## Tests

`tests/test_filters.py` includes **`TestHtmlAttrsXss`** for mapping vs raw-string behavior.

Full audit table: [SECURITY.md](https://github.com/lbliii/chirp-ui/blob/main/SECURITY.md).

## Related

- [Filters](../reference/filters.md)
