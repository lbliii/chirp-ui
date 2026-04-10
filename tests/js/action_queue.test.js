import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

let mount;
let islands;

beforeEach(() => {
  vi.useFakeTimers();
  islands = mockChirpIslands();
});

afterEach(() => {
  vi.useRealTimers();
  islands.teardown();
});

async function getMountFn() {
  if (!mount) {
    await import("../../src/chirp_ui/templates/islands/action_queue.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "action_queue"
    )?.[1]?.mount;
  }
  return mount;
}

function createActionDOM({ fail = false } = {}) {
  const root = document.createElement("div");
  root.innerHTML = `
    <button data-action-trigger ${fail ? 'data-action-fail="true"' : ""}>Go</button>
    <span data-action-status></span>
  `;
  return root;
}

describe("action_queue", () => {
  it("registers as 'action_queue' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("initializes with idle status", async () => {
    const fn = await getMountFn();
    const root = createActionDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[data-action-status]").textContent).toBe(
      "Ready."
    );
    expect(
      root.querySelector("[data-action-status]").getAttribute("data-status")
    ).toBe("idle");
  });

  it("click sets pending status and disables button", async () => {
    const fn = await getMountFn();
    const root = createActionDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    root.querySelector("[data-action-trigger]").click();

    expect(
      root.querySelector("[data-action-trigger]").hasAttribute("disabled")
    ).toBe(true);
    expect(root.querySelector("[data-action-status]").textContent).toBe(
      "Working..."
    );
    expect(api.emitAction).toHaveBeenCalledWith("action", "pending", {});
  });

  it("resolves to success after 450ms", async () => {
    const fn = await getMountFn();
    const root = createActionDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    root.querySelector("[data-action-trigger]").click();

    // Advance past the 450ms await
    await vi.advanceTimersByTimeAsync(450);

    expect(root.querySelector("[data-action-status]").textContent).toBe(
      "Done."
    );
    expect(
      root.querySelector("[data-action-status]").getAttribute("data-status")
    ).toBe("success");
    expect(api.emitAction).toHaveBeenCalledWith("action", "success", {});
  });

  it("resolves to error when data-action-fail is true", async () => {
    const fn = await getMountFn();
    const root = createActionDOM({ fail: true });
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    root.querySelector("[data-action-trigger]").click();
    await vi.advanceTimersByTimeAsync(450);

    expect(root.querySelector("[data-action-status]").textContent).toBe(
      "Failed. Retry."
    );
    expect(
      root.querySelector("[data-action-status]").getAttribute("data-status")
    ).toBe("error");
    expect(api.emitAction).toHaveBeenCalledWith("action", "error", {});
  });

  it("re-enables button after completion", async () => {
    const fn = await getMountFn();
    const root = createActionDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    root.querySelector("[data-action-trigger]").click();

    expect(
      root.querySelector("[data-action-trigger]").hasAttribute("disabled")
    ).toBe(true);

    await vi.advanceTimersByTimeAsync(450);

    expect(
      root.querySelector("[data-action-trigger]").hasAttribute("disabled")
    ).toBe(false);
  });

  it("uses custom actionId from props", async () => {
    const fn = await getMountFn();
    const root = createActionDOM();
    const api = createMockApi();

    fn(createPayload(root, { actionId: "delete" }), api);

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ actionId: "delete", status: "idle" })
    );

    api.emitAction.mockClear();
    root.querySelector("[data-action-trigger]").click();
    expect(api.emitAction).toHaveBeenCalledWith("delete", "pending", {});
  });

  it("cleanup removes click listener", async () => {
    const fn = await getMountFn();
    const root = createActionDOM();
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    cleanup();
    root.querySelector("[data-action-trigger]").click();

    expect(api.emitAction).not.toHaveBeenCalled();
  });

  it("works without optional DOM nodes", async () => {
    const fn = await getMountFn();
    const root = document.createElement("div"); // no trigger, no status
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    expect(typeof cleanup).toBe("function");
    cleanup();
  });
});
