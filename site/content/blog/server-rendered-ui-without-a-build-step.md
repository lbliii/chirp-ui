---
title: Server-rendered UI without a build step
description: Why chirp-ui renders plain HTML first and layers interactivity only where a screen needs it.
date: 2026-01-20
draft: false
weight: 10
lang: en
author: chirp-ui-team
featured: true
tags: [architecture, htmx, alpine]
keywords: [server-rendered, html, htmx, alpine, no build step]
---

chirp-ui starts from a deliberately old-fashioned premise: most of an
interface is just HTML, and HTML is something Python already renders well. The
component library is a set of Kida macros that emit plain markup, styled with
modern CSS. There is no bundler, no hydration pass, and no client framework to
boot before the first paint.

## Render first, enhance second

A page made of `card`, `form`, and `nav` macros is fully usable the moment the
server flushes the response. We add behavior in two narrow places:

- **htmx** for swaps, server-sent events, and fragment navigation.
- **Alpine** for small islands of local state — a disclosure, a toggle, a menu.

Neither is required for the page to work. Disable JavaScript and the forms
still submit, the links still navigate, the content still reads.

## What you get for free

Because the output is real HTML, the platform features come along without extra
work: view-source is legible, the back button behaves, print stylesheets apply,
and assistive technology sees semantic structure instead of a `<div>` soup
assembled at runtime.

The trade is honest. You write a little more on the server and a lot less on the
client, and the screens you ship stay close to the screens you can reason about.
