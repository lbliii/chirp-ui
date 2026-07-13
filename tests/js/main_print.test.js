/**
 * Print-lifecycle regression proof for the Bengal chirp-theme runtime.
 *
 * Mirrors:
 *   src/bengal_themes/chirp_theme/assets/js/main.js
 */
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MAIN_JS_PATH = path.resolve(
  __dirname,
  "../../src/bengal_themes/chirp_theme/assets/js/main.js"
);
const MAIN_SRC = readFileSync(MAIN_JS_PATH, "utf8");

function loadMainScript() {
  // eslint-disable-next-line no-new-func
  new Function(
    "window",
    "document",
    "navigator",
    `${MAIN_SRC}\n//# sourceURL=main.js`
  )(window, document, window.navigator);
}

beforeEach(() => {
  document.body.innerHTML = `
    <main>
      <details id="closed"><summary>Closed</summary><p>Printable body</p></details>
      <details id="open" open><summary>Open</summary><p>Open body</p></details>
    </main>
    <details id="outside"><summary>Outside main</summary><p>Outside body</p></details>
  `;
});

afterEach(() => {
  delete window.BengalMain;
  document.body.innerHTML = "";
});

describe("main.js print lifecycle", () => {
  it("temporarily opens main disclosures and restores only their original state", () => {
    loadMainScript();

    window.dispatchEvent(new Event("beforeprint"));
    window.dispatchEvent(new Event("beforeprint"));

    expect(document.getElementById("closed").open).toBe(true);
    expect(document.getElementById("open").open).toBe(true);
    expect(document.getElementById("outside").open).toBe(false);

    window.dispatchEvent(new Event("afterprint"));

    expect(document.getElementById("closed").open).toBe(false);
    expect(document.getElementById("open").open).toBe(true);
    expect(document.getElementById("outside").open).toBe(false);
  });
});
