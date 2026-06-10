/**
 * DOM-contract test for the Bengal chirp-theme track enhancements (#142).
 *
 * tracks.js is an IIFE that enhances the bespoke data-file pillar page rendered
 * by `tracks/single.html` (+ `partials/track-sidebar.html` / `track-helpers.html`).
 * Its selectors MUST agree with the "RECONCILED DOM VOCABULARY" those templates
 * emit. This test builds that exact DOM in jsdom, runs tracks.js, and asserts the
 * scroll-spy finds > 0 sections, the announcer reads a non-empty label, the
 * resume banner has a valid insertion point, and track jumps honor
 * prefers-reduced-motion — so the template ↔ JS contract can't silently rot.
 *
 * Mirrors the hooks in:
 *   src/bengal_themes/chirp_theme/templates/tracks/single.html
 *   src/bengal_themes/chirp_theme/templates/partials/track-sidebar.html
 *   src/bengal_themes/chirp_theme/templates/partials/track-helpers.html
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { mockLocalStorage } from "./helpers.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TRACKS_JS_PATH = path.resolve(
  __dirname,
  "../../src/bengal_themes/chirp_theme/assets/js/enhancements/tracks.js"
);
const TRACKS_SRC = readFileSync(TRACKS_JS_PATH, "utf8");

const SECTION_TITLES = ["Get started", "Theming", "App shell"];

/**
 * Build the reconciled track pillar-page DOM (sidebar nav + section blocks +
 * reading column + combined TOC rail), matching what the theme templates emit.
 */
function renderTrackPage(titles = SECTION_TITLES) {
  const sidebarItems = titles
    .map(
      (title, i) => `
        <li class="chirp-theme-track-sidebar__item">
          <a href="#track-section-${i + 1}"
             class="chirpui-list__link chirp-theme-track-sidebar__link"
             data-track-section="${i + 1}"
             data-track-target="#track-section-${i + 1}">
            <span class="chirp-theme-track-sidebar__number">${i + 1}</span>
            <span class="chirp-theme-track-sidebar__title">${title}</span>
          </a>
        </li>`
    )
    .join("");

  const sectionBlocks = titles
    .map(
      (title, i) => `
        <section id="track-section-${i + 1}"
                 class="chirp-theme-track-section"
                 data-track-section="${i + 1}">
          <header class="chirp-theme-track-section__header">
            <span class="chirp-theme-track-section__number">${i + 1}</span>
            <div class="chirp-theme-track-section__heading">
              <h2 class="chirp-theme-track-section__title">${title}</h2>
            </div>
          </header>
          <div class="chirp-theme-track-section__body prose"><p>Lesson ${i + 1}.</p></div>
        </section>`
    )
    .join("");

  const tocGroups = titles
    .map(
      (_t, i) => `
        <div class="toc-group" data-toc-section="${i + 1}"></div>`
    )
    .join("");

  document.body.innerHTML = `
    <div class="chirp-theme-track-layout chirp-theme-track-layout--with-toc"
         data-chirp-theme-surface="track" data-track-id="getting-started">
      <aside class="chirp-theme-track-layout__sidebar">
        <nav class="chirp-theme-track-sidebar" aria-label="Track navigation"
             data-bengal="track-nav" data-track-id="getting-started">
          <ul class="chirp-theme-track-sidebar__list">${sidebarItems}</ul>
        </nav>
      </aside>
      <div class="chirp-theme-track-layout__main">
        <article class="prose chirp-theme-track-layout__article">
          <div class="chirp-theme-track-sections">${sectionBlocks}</div>
        </article>
      </div>
      <aside class="chirp-theme-track-layout__toc">${tocGroups}</aside>
    </div>`;
}

/** Execute the tracks.js IIFE in the current jsdom global scope. */
function loadTracksScript() {
  // tracks.js is a plain IIFE that attaches window.BengalTracks; it is not an
  // ES module, so evaluate it as a script with the jsdom globals in scope.
  // eslint-disable-next-line no-new-func
  new Function(
    "window",
    "document",
    "localStorage",
    "console",
    `${TRACKS_SRC}\n//# sourceURL=tracks.js`
  )(window, document, window.localStorage, console);
}

/** Minimal stand-in for window.BengalUtils (real one lives in utils.js). */
function installBengalUtils() {
  window.BengalUtils = {
    // Run the scroll callback synchronously for deterministic tests.
    throttleScroll: (cb) => cb,
    ready: (cb) => cb(),
  };
}

/** Force a matchMedia result for the reduced-motion query. */
function mockMatchMedia(reduce) {
  window.matchMedia = vi.fn().mockImplementation((query) => ({
    matches: reduce && query.includes("prefers-reduced-motion"),
    media: query,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
  }));
}

let scrollSpy;
let storage;

beforeEach(() => {
  // jsdom does not implement scrollIntoView — spy on it to inspect behavior.
  scrollSpy = vi.fn();
  window.HTMLElement.prototype.scrollIntoView = scrollSpy;
  mockMatchMedia(false);
  installBengalUtils();
  // jsdom's default localStorage lacks .clear(); use a Map-backed mock.
  storage = mockLocalStorage();
});

afterEach(() => {
  if (window.BengalTracks) {
    window.BengalTracks.cleanup();
    delete window.BengalTracks;
  }
  storage.teardown();
  document.body.innerHTML = "";
  document.getElementById("track-live-region")?.remove();
  vi.restoreAllMocks();
});

describe("tracks.js DOM contract", () => {
  it("finds > 0 sections on the reconciled pillar page (does not early-return)", () => {
    renderTrackPage();
    loadTracksScript();

    expect(window.BengalTracks).toBeDefined();
    // init() ran via ready(); a missing contract would leave it at -1 forever.
    expect(window.BengalTracks.getCurrentSection()).toBeGreaterThanOrEqual(0);
  });

  it("marks the track nav as enhanced (selector matched the data-bengal hook)", () => {
    renderTrackPage();
    loadTracksScript();

    const nav = document.querySelector('[data-bengal="track-nav"]');
    expect(nav.getAttribute("data-enhanced")).toBe("true");
  });

  it("early-returns cleanly when no sections exist", () => {
    document.body.innerHTML = `
      <nav data-bengal="track-nav" data-track-id="empty"></nav>`;
    loadTracksScript();

    const nav = document.querySelector('[data-bengal="track-nav"]');
    expect(nav.hasAttribute("data-enhanced")).toBe(false);
    expect(window.BengalTracks.getCurrentSection()).toBe(-1);
  });

  it("announcer reads a NON-EMPTY label from the sidebar __title hook", () => {
    vi.useFakeTimers();
    renderTrackPage();
    loadTracksScript();
    // Announce is debounced 300ms inside updateCurrentSection().
    vi.advanceTimersByTime(400);

    const liveRegion = document.getElementById("track-live-region");
    expect(liveRegion).not.toBeNull();
    expect(liveRegion.textContent.trim()).not.toBe("");
    // The announcer reads the sidebar __title hook, so it names a real section
    // (which one depends on layout; in jsdom rects are 0 → last section wins).
    // The regression we guard is an EMPTY label, so assert it contains a title.
    expect(SECTION_TITLES.some((t) => liveRegion.textContent.includes(t))).toBe(
      true
    );
    vi.useRealTimers();
  });

  it("resume banner has a valid insertion point (the reading column)", () => {
    vi.useFakeTimers();
    // Seed progress so checkResume() decides to show the banner.
    window.localStorage.setItem(
      "bengal_track_progress_getting-started",
      JSON.stringify({ visited: [1], lastSection: 1 })
    );
    renderTrackPage();
    loadTracksScript();
    // checkResume() is scheduled 500ms after init.
    vi.advanceTimersByTime(600);

    const main = document.querySelector(".chirp-theme-track-layout__main");
    const banner = main.querySelector(".track-resume-banner");
    // A missing/renamed insertion point would leave the banner unattached.
    expect(banner).not.toBeNull();
    // The resume label is read from a sidebar __title hook → never empty, and
    // names a real section (which one depends on jsdom's zero-rect layout).
    const resumeBtn = banner.querySelector(".track-resume-button");
    expect(resumeBtn.textContent.replace(/Resume:/, "").trim()).not.toBe("");
    expect(SECTION_TITLES.some((t) => resumeBtn.textContent.includes(t))).toBe(
      true
    );
    vi.useRealTimers();
  });

  it("resume jump uses SMOOTH scroll by default", () => {
    vi.useFakeTimers();
    window.localStorage.setItem(
      "bengal_track_progress_getting-started",
      JSON.stringify({ visited: [1], lastSection: 1 })
    );
    renderTrackPage();
    loadTracksScript();
    vi.advanceTimersByTime(600);

    document.querySelector(".track-resume-button").click();
    expect(scrollSpy).toHaveBeenCalledWith({ behavior: "smooth" });
    vi.useRealTimers();
  });

  it("resume jump is INSTANT under prefers-reduced-motion (#164 slice)", () => {
    vi.useFakeTimers();
    mockMatchMedia(true);
    window.localStorage.setItem(
      "bengal_track_progress_getting-started",
      JSON.stringify({ visited: [1], lastSection: 1 })
    );
    renderTrackPage();
    loadTracksScript();
    vi.advanceTimersByTime(600);

    document.querySelector(".track-resume-button").click();
    expect(scrollSpy).toHaveBeenCalledWith({ behavior: "auto" });
    vi.useRealTimers();
  });

  it("prefers a shared BengalUtils.prefersReducedMotion helper when present", () => {
    vi.useFakeTimers();
    // Simulate the #164 utils.js helper being available; matchMedia stays false
    // so we prove the helper (returning true) wins over the local fallback.
    window.BengalUtils.prefersReducedMotion = () => true;
    window.localStorage.setItem(
      "bengal_track_progress_getting-started",
      JSON.stringify({ visited: [1], lastSection: 1 })
    );
    renderTrackPage();
    loadTracksScript();
    vi.advanceTimersByTime(600);

    document.querySelector(".track-resume-button").click();
    expect(scrollSpy).toHaveBeenCalledWith({ behavior: "auto" });
    vi.useRealTimers();
  });
});
