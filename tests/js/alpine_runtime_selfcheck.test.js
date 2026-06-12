/**
 * Unit coverage for the chirpui-alpine.js runtime self-check (issue #189).
 *
 * chirpui-alpine.js is a global IIFE, not an ES module, so we read its source
 * and evaluate it in the jsdom global. The guard turns a silently-disabled
 * Alpine (every component inert, clean console) into a loud console warning.
 */
import fs from "node:fs";
import path from "node:path";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

const SRC = fs.readFileSync(
  path.resolve(process.cwd(), "src/chirp_ui/templates/chirpui-alpine.js"),
  "utf8",
);

function loadRuntime() {
  // The IIFE guards re-entry via this flag; clear it so each load runs fully.
  delete window.__chirpuiAlpineRuntimeLoaded;
  // Indirect eval runs in the global scope where window/document are defined.
  (0, eval)(SRC);
}

describe("chirpui-alpine runtime self-check (#189)", () => {
  let warn;

  beforeEach(() => {
    vi.useFakeTimers();
    document.body.innerHTML = "";
    delete window.Alpine;
    warn = vi.spyOn(console, "warn").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.useRealTimers();
    warn.mockRestore();
    delete window.Alpine;
    delete window.__chirpuiAlpineRuntimeLoaded;
  });

  it("warns once (and only once) when Alpine never loads", () => {
    // First eval in this file's jsdom, so no stale listeners can interfere
    // with the "only once" assertion.
    document.body.innerHTML =
      '<button x-data="chirpuiDialogTarget()">Open</button>';
    loadRuntime();

    vi.advanceTimersByTime(1600);

    const message = warn.mock.calls[0][0];
    expect(message).toContain("Alpine.js never initialized");
    expect(message).toContain("INERT");
    expect(message).toContain("/dist/cdn.min.js");

    // Re-checks on later htmx swaps must not double-warn.
    document.dispatchEvent(new Event("htmx:afterSettle"));
    document.dispatchEvent(new Event("htmx:afterSettle"));
    expect(warn).toHaveBeenCalledTimes(1);
  });

  it("stays silent when Alpine initializes normally", () => {
    document.body.innerHTML =
      '<button x-data="chirpuiDialogTarget()">Open</button>';
    loadRuntime();

    // Simulate Alpine booting after the runtime loaded.
    window.Alpine = { version: "3.0.0", data() {}, store() {} };
    document.dispatchEvent(new Event("alpine:init"));

    vi.advanceTimersByTime(1600);

    expect(warn).not.toHaveBeenCalled();
  });

  it("stays silent when no chirp-ui Alpine components are present", () => {
    // Anonymous x-data only needs Alpine core, not chirpui-alpine.js — and the
    // app may not use Alpine at all; the runtime must not cry wolf.
    document.body.innerHTML = '<div x-data="{ open: false }"></div>';
    loadRuntime();

    vi.advanceTimersByTime(1600);

    expect(warn).not.toHaveBeenCalled();
  });
});
