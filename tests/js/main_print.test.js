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
  document.head.innerHTML = `
    <title>Print contract</title>
    <link rel="canonical" href="https://docs.example.com/guide/?utm_source=test#section">
  `;
  document.body.innerHTML = `
    <main>
      <details id="closed"><summary>Closed</summary><p>Printable body</p></details>
      <details id="open" open><summary>Open</summary><p>Open body</p></details>
      <p><a id="named-link" href="https://user:secret@example.com/reference?UTM_Source=test&mode=full#part">Reference</a></p>
      <p><a id="url-link" href="https://example.com/path/">https://example.com/path/</a></p>
      <pre id="long-code"><code>Long code</code></pre>
    </main>
    <details id="outside"><summary>Outside main</summary><p>Outside body</p></details>
  `;
  Object.defineProperty(document.getElementById("long-code"), "scrollHeight", {
    configurable: true,
    value: 700,
  });
});

afterEach(() => {
  delete window.BengalMain;
  document.head.innerHTML = "";
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
    expect(document.querySelectorAll("[data-print-generated]")).toHaveLength(1);
    expect(document.getElementById("long-code").dataset.printBreakable).toBe("true");

    window.dispatchEvent(new Event("afterprint"));

    expect(document.getElementById("closed").open).toBe(false);
    expect(document.getElementById("open").open).toBe(true);
    expect(document.getElementById("outside").open).toBe(false);
    expect(document.querySelector("[data-print-generated]")).toBeNull();
    expect(document.getElementById("long-code").dataset.printBreakable).toBeUndefined();
  });

  it("prints useful external URLs without tracking noise or duplicate URL labels", () => {
    loadMainScript();

    window.dispatchEvent(new Event("beforeprint"));

    expect(document.getElementById("named-link").dataset.printHref).toBe(
      "https://example.com/reference?mode=full"
    );
    expect(document.querySelector(".print-link-url").textContent).toBe(
      " (https://example.com/reference?mode=full)"
    );
    expect(document.getElementById("url-link").dataset.printHref).toBeUndefined();
    expect(document.querySelector(".print-document-meta__title").textContent).toBe(
      "Print contract"
    );
    expect(document.querySelector(".print-document-meta__source a").textContent).toBe(
      "https://docs.example.com/guide/"
    );

    window.dispatchEvent(new Event("afterprint"));

    expect(document.getElementById("named-link").dataset.printHref).toBeUndefined();
    expect(document.querySelector(".print-link-url")).toBeNull();
  });
});
