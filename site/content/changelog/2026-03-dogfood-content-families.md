---
title: "Dogfood content for every template family"
description: The site now ships real blog, tutorial, resume, author, and changelog pages.
date: 2026-03-20
draft: false
weight: 10
lang: en
tags: [content, theme]
keywords: [chirp-theme, dogfood, blog, tutorial, resume, changelog]
---

## Added

Every shipped template family now has live content, so each family renders on
the public site instead of returning a 404:

- A **blog** with three posts and a team author.
- A two-step **tutorial** with a progress stepper.
- A one-page **resume** profile.
- An **authors** index and profile page.
- This **changelog**.

## Why

The templates existed but had nothing to render. Standing up minimal, real
content makes the capabilities discoverable from navigation and guards them with
a build test, so a future change that breaks a family fails CI instead of
shipping quietly.
