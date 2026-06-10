/**
 * Reduced-motion contract for the Bengal chirp-theme back-to-top button (#164).
 *
 * enhancements/interactive.js is a plain IIFE that prefers window.BengalUtils
 * but degrades gracefully when it is absent. On click, the floating
 * back-to-top button calls window.scrollTo({ top: 0, behavior }). CSS
 * `scroll-behavior` does NOT override an explicit `behavior:'smooth'` option,
 * so the smooth/auto choice must be made in JS. This test asserts that choice
 * honors prefers-reduced-motion: 'auto' (instant) when the user asked to
 * reduce motion, 'smooth' otherwise. It also confirms the module reuses the
 * shared BengalUtils.prefersReducedMotion() helper rather than duplicating a
 * matchMedia read.
 *
 * Mirrors:
 *   src/bengal_themes/chirp_theme/assets/js/enhancements/interactive.js
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const INTERACTIVE_JS_PATH = path.resolve(
  __dirname,
  "../../src/bengal_themes/chirp_theme/assets/js/enhancements/interactive.js"
);
const INTERACTIVE_SRC = readFileSync(INTERACTIVE_JS_PATH, "utf8");

/** Render the floating back-to-top control the theme templates emit. */
function renderBackToTop() {
  document.body.innerHTML = `
    <button type="button" class="back-to-top chirp-theme-floating-top">Top</button>
    <footer><span class="chirp-theme-footer__rule-mark"></span></footer>`;
}

/** Execute interactive.js in the current jsdom global scope. */
function loadInteractiveScript() {
  // eslint-disable-next-line no-new-func
  new Function(
    "window",
    "document",
    "console",
    `${INTERACTIVE_SRC}\n//# sourceURL=interactive.js`
  )(window, document, console);
}

/**
 * Stub window.matchMedia so a `(prefers-reduced-motion: reduce)` query returns
 * `reduced`. Returns a teardown that restores the previous value.
 */
function stubReducedMotion(reduced) {
  const prev = window.matchMedia;
  window.matchMedia = vi.fn((query) => ({
    matches: reduced && query.includes("prefers-reduced-motion"),
    media: query,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }));
  return () => {
    window.matchMedia = prev;
  };
}

/**
 * Minimal stand-in for window.BengalUtils. prefersReducedMotion is the real
 * contract: read matchMedia('(prefers-reduced-motion: reduce)').
 */
function installBengalUtils() {
  window.BengalUtils = {
    log: () => {},
    throttleScroll: (cb) => cb,
    debounce: (cb) => cb,
    ready: (cb) => cb(),
    prefersReducedMotion: () =>
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  };
}

let restoreMatchMedia;

beforeEach(() => {
  // jsdom does not implement these scroll APIs — stub them.
  window.scrollTo = vi.fn();
  window.requestAnimationFrame = (cb) => {
    cb();
    return 0;
  };
  installBengalUtils();
  renderBackToTop();
});

afterEach(() => {
  if (window.BengalInteractive) {
    window.BengalInteractive.cleanup();
    delete window.BengalInteractive;
  }
  delete window.BengalUtils;
  if (restoreMatchMedia) {
    restoreMatchMedia();
    restoreMatchMedia = undefined;
  }
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

describe("interactive.js back-to-top reduced-motion", () => {
  it("smooth-scrolls when reduced motion is NOT requested", () => {
    restoreMatchMedia = stubReducedMotion(false);
    loadInteractiveScript();

    document.querySelector(".back-to-top").click();

    expect(window.scrollTo).toHaveBeenCalledWith(
      expect.objectContaining({ top: 0, behavior: "smooth" })
    );
  });

  it("jumps instantly (behavior:auto) when reduced motion IS requested", () => {
    restoreMatchMedia = stubReducedMotion(true);
    loadInteractiveScript();

    document.querySelector(".back-to-top").click();

    expect(window.scrollTo).toHaveBeenCalledWith(
      expect.objectContaining({ top: 0, behavior: "auto" })
    );
    // Never animate for reduced-motion users.
    const behaviors = window.scrollTo.mock.calls.map((c) => c[0].behavior);
    expect(behaviors).not.toContain("smooth");
  });

  it("adds the reduce-motion class on init when reduced motion is requested", () => {
    restoreMatchMedia = stubReducedMotion(true);
    loadInteractiveScript();
    expect(
      document.documentElement.classList.contains("reduce-motion")
    ).toBe(true);
  });
});
