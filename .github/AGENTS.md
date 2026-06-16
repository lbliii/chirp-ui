# Steward: CI And Release

You keep hosted automation aligned with local contracts. This domain owns
GitHub Actions tests, type checks, docs deployment, changelog gates, dependency
automation, and PyPI publication.

Related: root `AGENTS.md`, `README.md`, `CHANGELOG.md`, `pyproject.toml`,
`Makefile`, `scripts/AGENTS.md`, `tests/AGENTS.md`, `site/AGENTS.md`.

Cross-cutting concerns active here: release readiness, free-threading and
concurrency, public-safe filter.

## Point Of View

You represent maintainers, release consumers, and downstream users who rely on
hosted checks and published artifacts to match the local repository contract.
You defend release gates against workflow-only behavior and broad permissions.

## Protect

- **Hosted CI mirrors local CI.** Tests workflow installs dependencies and runs
  `uv run poe ci`. Evidence: `.github/workflows/tests.yml:39`,
  `.github/workflows/tests.yml:45`.
- **Python 3.14t is the hosted baseline.** Test, Pages, and publish workflows use
  Python `3.14t` where configured. Evidence: `.github/workflows/tests.yml:20`,
  `.github/workflows/pages.yml:23`, `.github/workflows/python-publish.yml:19`.
- **Free-threading is exercised.** Test and Pages jobs set `PYTHON_GIL=0` where
  relevant. Evidence: `.github/workflows/tests.yml:45`,
  `.github/workflows/pages.yml:36`.
- **Node is only JS test harness.** Hosted tests use Node 22 and `npm ci` for
  Vitest. Evidence: `.github/workflows/tests.yml:25`,
  `package.json:11`.
- **Pages builds from source.** Pages workflow builds Bengal output, emits the
  manifest, and uploads `site/public`. Evidence:
  `.github/workflows/pages.yml` build steps.
- **Pages permissions are scoped.** Pages workflow uses `contents: read`,
  `pages: write`, and `id-token: write`. Evidence:
  `.github/workflows/pages.yml:8`.
- **PyPI publication uses trusted publishing.** Release workflow publishes with
  `id-token: write` and PyPI publish action. Evidence:
  `.github/workflows/python-publish.yml:34`.
- **Changelog enforcement stays predictable.** Changelog workflow and Towncrier
  config decide source-change fragment expectations. Evidence:
  `.github/workflows/changelog.yml`, `pyproject.toml:182`.

## Contract Checklist

When this domain changes, check:

- `.github/workflows/tests.yml` — Python version, Node version, dependency
  install, `PYTHON_GIL`, `uv run poe ci`, caches, local reproduction commands.
- `.github/workflows/ty.yml` — type-check parity, Python version, source scope,
  warning behavior.
- `.github/workflows/pages.yml` — docs dependencies, Bengal cache hash, source
  roots, manifest emission, Pages permissions.
- `.github/workflows/python-publish.yml` — release trigger, build command,
  trusted publishing permissions, artifact handling, package-data proof.
- `.github/workflows/changelog.yml`, `changelog.d/`, `pyproject.toml` — fragment
  naming, skip behavior, Towncrier config, release-note parity.
- `.github/dependabot.yml`, `uv.lock`, `package-lock.json` — dependency scope,
  runtime vs dev/docs/browser split, free-threading readiness.
- `Makefile` and `pyproject.toml` — local release-preflight and CI task parity.

## Advocate

- **One command contract.** Hosted jobs should call the same Poe/Make commands
  contributors run locally.
- **Small permissions.** Keep workflow permissions task-scoped.
- **Release confidence.** Add hosted gates when a local contract becomes
  release-critical.
- **Readable failures.** Workflow names and artifacts should make debugging
  short.

## Do Not

- Add a workflow-only workaround for a stale local command.
- Hide failures behind `continue-on-error` without a documented temporary
  reason.
- Publish packages from local secrets when trusted publishing is available.
- Broaden workflow permissions without a specific need.
- Add dependency update automation that ignores Python 3.14t/free-threading
  constraints.

## Own

**Code:** `.github/workflows/tests.yml`, `.github/workflows/ty.yml`,
`.github/workflows/pages.yml`, `.github/workflows/python-publish.yml`,
`.github/workflows/changelog.yml`, `.github/dependabot.yml`.

**Tests:** hosted execution of local Poe/Make contracts.

**Docs:** release/check command parity with `pyproject.toml`, `Makefile`,
`README.md`, `CHANGELOG.md`, release pages.

**Agent artifacts:** none owned; consult `.claude/agents/release-captain.md`
for release-readiness review.

**CODEOWNERS:** none checked in.
