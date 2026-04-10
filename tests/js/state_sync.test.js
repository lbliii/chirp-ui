import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

let mount;
let islands;

// jsdom defaults to "about:blank" — replaceState only works with same-origin URLs.
// We set the jsdom URL via vitest config (see below) or work around it by
// reading window.location after replaceState calls that state_sync.js makes.

beforeEach(() => {
  islands = mockChirpIslands();
  // Stub history.replaceState to avoid jsdom SecurityError
  vi.spyOn(window.history, "replaceState").mockImplementation(() => {});
});

afterEach(() => {
  islands.teardown();
  vi.restoreAllMocks();
});

async function getMountFn() {
  if (!mount) {
    await import("../../src/chirp_ui/templates/islands/state_sync.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "state_sync"
    )?.[1]?.mount;
  }
  return mount;
}

function createSyncDOM(inputCount = 1) {
  const root = document.createElement("div");
  let inputs = "";
  for (let i = 0; i < inputCount; i++) {
    inputs += `<input data-state-field value="" />\n`;
  }
  root.innerHTML = inputs;
  return root;
}

describe("state_sync", () => {
  it("registers as 'state_sync' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("reads initial value from URL query param", async () => {
    const fn = await getMountFn();
    // Simulate a URL with query param by stubbing location.href
    const originalHref = window.location.href;
    vi.spyOn(window, "location", "get").mockReturnValue({
      ...window.location,
      href: "http://localhost:3000/?value=hello",
    });

    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[data-state-field]").value).toBe("hello");
    expect(api.emitState).toHaveBeenCalledWith({ value: "hello" });
  });

  it("falls back to props.initial when no query param", async () => {
    const fn = await getMountFn();
    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, { initial: "default-val" }), api);

    expect(root.querySelector("[data-state-field]").value).toBe("default-val");
    expect(api.emitState).toHaveBeenCalledWith({ value: "default-val" });
  });

  it("defaults to empty string when no query param or initial", async () => {
    const fn = await getMountFn();
    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(api.emitState).toHaveBeenCalledWith({ value: "" });
  });

  it("input change calls replaceState with updated URL", async () => {
    const fn = await getMountFn();
    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const input = root.querySelector("[data-state-field]");
    input.value = "new-val";
    input.dispatchEvent(new Event("input"));

    expect(window.history.replaceState).toHaveBeenCalled();
    const calledUrl = window.history.replaceState.mock.calls.at(-1)[2];
    expect(calledUrl).toContain("value=new-val");
  });

  it("empty input removes query param from URL", async () => {
    const fn = await getMountFn();
    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, { initial: "old" }), api);

    const input = root.querySelector("[data-state-field]");
    input.value = "";
    input.dispatchEvent(new Event("input"));

    const calledUrl = window.history.replaceState.mock.calls.at(-1)[2];
    expect(calledUrl).not.toContain("value=");
  });

  it("uses custom stateKey and queryParam", async () => {
    const fn = await getMountFn();
    vi.spyOn(window, "location", "get").mockReturnValue({
      ...window.location,
      href: "http://localhost:3000/?q=search-term",
    });

    const root = createSyncDOM();
    const api = createMockApi();

    fn(
      createPayload(root, { stateKey: "search", queryParam: "q" }),
      api
    );

    expect(root.querySelector("[data-state-field]").value).toBe("search-term");
    expect(api.emitState).toHaveBeenCalledWith({ search: "search-term" });
  });

  it("multiple inputs are synced on mount", async () => {
    const fn = await getMountFn();
    vi.spyOn(window, "location", "get").mockReturnValue({
      ...window.location,
      href: "http://localhost:3000/?value=synced",
    });

    const root = createSyncDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const inputs = root.querySelectorAll("[data-state-field]");
    inputs.forEach((input) => {
      expect(input.value).toBe("synced");
    });
  });

  it("emits state on input change", async () => {
    const fn = await getMountFn();
    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitState.mockClear();

    const input = root.querySelector("[data-state-field]");
    input.value = "updated";
    input.dispatchEvent(new Event("input"));

    expect(api.emitState).toHaveBeenCalledWith({ value: "updated" });
  });

  it("cleanup removes input listeners", async () => {
    const fn = await getMountFn();
    const root = createSyncDOM();
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    api.emitState.mockClear();

    cleanup();

    const input = root.querySelector("[data-state-field]");
    input.value = "after-cleanup";
    input.dispatchEvent(new Event("input"));

    expect(api.emitState).not.toHaveBeenCalled();
  });

  it("queryParam defaults to stateKey", async () => {
    const fn = await getMountFn();
    vi.spyOn(window, "location", "get").mockReturnValue({
      ...window.location,
      href: "http://localhost:3000/?filter=active",
    });

    const root = createSyncDOM();
    const api = createMockApi();

    fn(createPayload(root, { stateKey: "filter" }), api);

    expect(root.querySelector("[data-state-field]").value).toBe("active");
    expect(api.emitState).toHaveBeenCalledWith({ filter: "active" });
  });
});
