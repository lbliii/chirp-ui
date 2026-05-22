# Steward Questions

These questions capture the design intent and governance details the bootstrap
could not prove from source. Do not invent answers; update the relevant
`AGENTS.md` file only after an SME answer is recorded or the source changes.

## Core Registry And Python API

1. Which names in `chirp_ui.__all__` are intended as stable public API before
   1.0, and which are convenience exports that may still move?
2. What is the minimum repeated-consumer evidence required before layout
   relationship metadata should become a descriptor or manifest field?
3. Which downstream tools currently consume `chirpui-manifest@5`, and what
   migration window do they need for a schema bump?

## Template, CSS, And Behavior

1. Which remaining legacy CSS partials are highest priority for scoped-envelope
   conversion when touched?
2. What browser proof is considered sufficient for visual/layout changes that
   are too small for a full gauntlet run?
3. Which inline `x-data` shapes are still acceptable, and where is the boundary
   for promoting behavior into `chirpui-alpine.js`?

## Bengal Theme

1. Which `chirp-theme` surfaces are foundation acceptance targets versus
   long-term parity targets?
2. Which legacy Bengal palette names must remain as transitional aliases, and
   what would justify removing them?
3. What external Bengal theme consumers, if any, need migration notice for
   theme template or asset hook changes?

## Documentation

1. Which docs are canonical enough that published site mirrors should always
   link back rather than repeat full guidance?
2. What is the intended review gate for moving a candidate example into
   `docs/AGENT-CURATED-SNIPPETS.md`?
3. Which public claims in `README.md` or `docs/VISION.md` are strategic product
   story versus implementation commitments?

## Planning

1. Who decides when a plan moves from active to `docs/plans/done/`?
2. What active-plan count should the docs IA ratchet enforce after the current
   productization saga settles?
3. Which plan types should be issues instead of docs files?

## Published Site

1. Which generated `site/public/` artifacts are expected to be committed, if
   any, versus produced only by Pages?
2. What link-check or public artifact verification should block release, and
   what should remain docs-site CI only?
3. Which site pages need screenshots or browser proof when theme chrome changes?

## Examples And Showcase

1. Which showcase routes are considered canonical examples for new users versus
   visual audit or stress fixtures?
2. What is the minimum runnable proof for a showcase snippet to become
   copyable-curated agent guidance?
3. Which legacy helper usages remain intentionally demonstrated, and which are
   tolerated only until replacement examples land?

## Test Contract

1. Which browser tests are release gates, and which are exploratory or
   local-only stress checks?
2. What is the expected policy for flaky browser tests: quarantine, fix in
   place, or narrow the fixture?
3. Which test fixtures intentionally differ from real Chirp/Kida behavior, and
   why?

## Build Projection

1. Should every generated artifact have both a builder test and a Poe
   `--check` task, or are some projections intentionally script-only?
2. Which builders may use shell commands or external tools, and which must stay
   pure Python/stdlib?
3. What is the intended lifecycle for generated `site/public` artifacts in local
   development versus release?

## CI And Release

1. Should `python-publish.yml` run the same release preflight as `Makefile`
   before building distributions?
2. What PR labels or paths should bypass changelog enforcement, if any?
3. Which dependency updates require manual free-threading review before merge?

## Advisory Agent Artifacts

1. Which advisory personas should participate automatically in `review swarm`,
   and which should be opt-in only?
2. Should advisory agents have tests or fixtures that validate their output
   format against root `AGENTS.md`?
3. What criteria justify adding a new persona instead of expanding an existing
   scoped steward or cross-cutting root section?
