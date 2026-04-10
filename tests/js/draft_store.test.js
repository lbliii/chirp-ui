import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import {
  mockChirpIslands,
  mockLocalStorage,
  createPayload,
  createMockApi,
} from "./helpers.js";

let mount;
let islands;
let storage;

beforeEach(() => {
  vi.useFakeTimers();
  islands = mockChirpIslands();
  storage = mockLocalStorage();
});

afterEach(() => {
  vi.useRealTimers();
  islands.teardown();
  storage.teardown();
});

async function getMountFn() {
  if (!mount) {
    await import("../../src/chirp_ui/templates/islands/draft_store.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "draft_store"
    )?.[1]?.mount;
  }
  return mount;
}

function createDraftDOM() {
  const root = document.createElement("div");
  root.innerHTML = `
    <input data-draft-field name="title" value="" />
    <textarea data-draft-field name="body"></textarea>
    <span data-draft-saved-at></span>
  `;
  return root;
}

describe("draft_store", () => {
  it("registers as 'draft_store' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("restores fields from localStorage on mount", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    // Pre-populate localStorage
    storage.store.set(
      "chirp:draft:draft",
      JSON.stringify({
        savedAt: "2026-04-10T12:00:00Z",
        data: { title: "Hello", body: "World" },
      })
    );

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[name=title]").value).toBe("Hello");
    expect(root.querySelector("[name=body]").value).toBe("World");
    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ draftKey: "draft", restored: true })
    );
  });

  it("does not restore when no localStorage key exists", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[name=title]").value).toBe("");
    // savedAt node shows "never"
    expect(root.querySelector("[data-draft-saved-at]").textContent).toBe(
      "never"
    );
  });

  it("persists to localStorage after 250ms debounce", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    fn(createPayload(root, { draftKey: "myform" }), api);

    const titleInput = root.querySelector("[name=title]");
    titleInput.value = "Draft title";
    titleInput.dispatchEvent(new Event("input"));

    // Not yet persisted
    expect(storage.store.has("chirp:draft:myform")).toBe(false);

    // Advance past debounce
    vi.advanceTimersByTime(250);

    expect(storage.store.has("chirp:draft:myform")).toBe(true);
    const stored = JSON.parse(storage.store.get("chirp:draft:myform"));
    expect(stored.data.title).toBe("Draft title");
    expect(stored.savedAt).toBeTruthy();
  });

  it("debounce cancels previous timer on rapid input", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    fn(createPayload(root, { draftKey: "rapid" }), api);

    const titleInput = root.querySelector("[name=title]");

    titleInput.value = "first";
    titleInput.dispatchEvent(new Event("input"));
    vi.advanceTimersByTime(100); // not yet

    titleInput.value = "second";
    titleInput.dispatchEvent(new Event("input"));
    vi.advanceTimersByTime(100); // still not yet (reset)

    titleInput.value = "third";
    titleInput.dispatchEvent(new Event("input"));
    vi.advanceTimersByTime(250); // NOW fires

    const stored = JSON.parse(storage.store.get("chirp:draft:rapid"));
    expect(stored.data.title).toBe("third");
  });

  it("handles corrupted JSON gracefully", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    storage.store.set("chirp:draft:draft", "not valid json{{{");

    // Should not throw
    fn(createPayload(root, {}), api);

    expect(root.querySelector("[data-draft-saved-at]").textContent).toBe(
      "never"
    );
  });

  it("uses data-draft-field attribute as fallback key", async () => {
    const fn = await getMountFn();
    const root = document.createElement("div");
    root.innerHTML = `
      <input data-draft-field="custom_key" value="" />
      <span data-draft-saved-at></span>
    `;
    const api = createMockApi();

    fn(createPayload(root, { draftKey: "custom" }), api);

    const input = root.querySelector("[data-draft-field=custom_key]");
    input.value = "val";
    input.dispatchEvent(new Event("input"));
    vi.advanceTimersByTime(250);

    const stored = JSON.parse(storage.store.get("chirp:draft:custom"));
    expect(stored.data.custom_key).toBe("val");
  });

  it("emits save action on persist", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    fn(createPayload(root, { draftKey: "act" }), api);
    api.emitAction.mockClear();

    root.querySelector("[name=title]").value = "x";
    root.querySelector("[name=title]").dispatchEvent(new Event("input"));
    vi.advanceTimersByTime(250);

    expect(api.emitAction).toHaveBeenCalledWith("save", "success", {
      draftKey: "act",
    });
  });

  it("cleanup removes listeners and clears timer", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    const cleanup = fn(createPayload(root, { draftKey: "cl" }), api);
    api.emitState.mockClear();

    const titleInput = root.querySelector("[name=title]");
    titleInput.value = "pending";
    titleInput.dispatchEvent(new Event("input"));

    cleanup();

    // Advance timers — persist should NOT fire after cleanup
    vi.advanceTimersByTime(500);
    expect(storage.store.has("chirp:draft:cl")).toBe(false);
  });

  it("snapshots multiple fields", async () => {
    const fn = await getMountFn();
    const root = createDraftDOM();
    const api = createMockApi();

    fn(createPayload(root, { draftKey: "multi" }), api);

    root.querySelector("[name=title]").value = "T";
    root.querySelector("[name=body]").value = "B";
    root.querySelector("[name=title]").dispatchEvent(new Event("input"));
    vi.advanceTimersByTime(250);

    const stored = JSON.parse(storage.store.get("chirp:draft:multi"));
    expect(stored.data.title).toBe("T");
    expect(stored.data.body).toBe("B");
  });
});
