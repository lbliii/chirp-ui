import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mockChirpIslands, createPayload, createMockApi } from "./helpers.js";

let mount;
let islands;

beforeEach(() => {
  islands = mockChirpIslands();
});

afterEach(() => {
  islands.teardown();
});

async function getMountFn() {
  if (!mount) {
    await import("../../src/chirp_ui/templates/islands/wizard_state.js");
    mount = islands.register.mock.calls.find(
      (c) => c[0] === "wizard_state"
    )?.[1]?.mount;
  }
  return mount;
}

function createWizardDOM(stepCount = 3) {
  const root = document.createElement("div");
  let steps = "";
  for (let i = 0; i < stepCount; i++) {
    steps += `<div data-wizard-step data-step-id="step-${i + 1}">Step ${i + 1}</div>\n`;
  }
  root.innerHTML = `
    ${steps}
    <button data-wizard-prev>Prev</button>
    <button data-wizard-next>Next</button>
    <span data-wizard-status></span>
  `;
  return root;
}

describe("wizard_state", () => {
  it("registers as 'wizard_state' primitive", async () => {
    const fn = await getMountFn();
    expect(fn).toBeTypeOf("function");
  });

  it("starts at index 0 showing first step", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    const steps = root.querySelectorAll("[data-wizard-step]");
    expect(steps[0].hasAttribute("hidden")).toBe(false);
    expect(steps[1].hasAttribute("hidden")).toBe(true);
    expect(steps[2].hasAttribute("hidden")).toBe(true);
  });

  it("emits initial state with step, index, total", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(api.emitState).toHaveBeenCalledWith({
      stateKey: "wizard",
      step: "step-1",
      index: 0,
      total: 3,
    });
  });

  it("prev button is disabled at index 0", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[data-wizard-prev]").disabled).toBe(true);
  });

  it("next button is disabled at last index", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(1);
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(root.querySelector("[data-wizard-next]").disabled).toBe(true);
  });

  it("next advances to step 2", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitState.mockClear();
    api.emitAction.mockClear();

    root.querySelector("[data-wizard-next]").click();

    const steps = root.querySelectorAll("[data-wizard-step]");
    expect(steps[0].hasAttribute("hidden")).toBe(true);
    expect(steps[1].hasAttribute("hidden")).toBe(false);
    expect(steps[2].hasAttribute("hidden")).toBe(true);

    expect(api.emitAction).toHaveBeenCalledWith("next", "success", {
      step: "step-2",
    });
    expect(api.emitState).toHaveBeenCalledWith({
      stateKey: "wizard",
      step: "step-2",
      index: 1,
      total: 3,
    });
  });

  it("prev goes back to step 1", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    root.querySelector("[data-wizard-next]").click();
    api.emitAction.mockClear();

    root.querySelector("[data-wizard-prev]").click();

    const steps = root.querySelectorAll("[data-wizard-step]");
    expect(steps[0].hasAttribute("hidden")).toBe(false);
    expect(steps[1].hasAttribute("hidden")).toBe(true);

    expect(api.emitAction).toHaveBeenCalledWith("prev", "success", {
      step: "step-1",
    });
  });

  it("next at last step is a no-op", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(2);
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    root.querySelector("[data-wizard-next]").click(); // now at index 1 (last)
    api.emitState.mockClear();
    api.emitAction.mockClear();

    root.querySelector("[data-wizard-next]").click(); // should be no-op

    expect(api.emitAction).not.toHaveBeenCalled();
  });

  it("prev at first step is a no-op", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(2);
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    root.querySelector("[data-wizard-prev]").click(); // already at 0

    expect(api.emitAction).not.toHaveBeenCalled();
  });

  it("status text shows 'Step X of Y'", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    fn(createPayload(root, {}), api);
    expect(root.querySelector("[data-wizard-status]").textContent).toBe(
      "Step 1 of 3"
    );

    root.querySelector("[data-wizard-next]").click();
    expect(root.querySelector("[data-wizard-status]").textContent).toBe(
      "Step 2 of 3"
    );
  });

  it("uses index as step ID fallback when no data-step-id", async () => {
    const fn = await getMountFn();
    const root = document.createElement("div");
    root.innerHTML = `
      <div data-wizard-step>A</div>
      <div data-wizard-step>B</div>
      <button data-wizard-next>Next</button>
      <button data-wizard-prev>Prev</button>
    `;
    const api = createMockApi();

    fn(createPayload(root, {}), api);

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ step: "1" })
    );

    root.querySelector("[data-wizard-next]").click();
    expect(api.emitState).toHaveBeenLastCalledWith(
      expect.objectContaining({ step: "2" })
    );
  });

  it("uses props.steps for step IDs when data-step-id absent", async () => {
    const fn = await getMountFn();
    const root = document.createElement("div");
    root.innerHTML = `
      <div data-wizard-step>A</div>
      <div data-wizard-step>B</div>
      <button data-wizard-next>Next</button>
      <button data-wizard-prev>Prev</button>
    `;
    const api = createMockApi();

    fn(createPayload(root, { steps: ["intro", "confirm"] }), api);

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ step: "intro" })
    );
  });

  it("custom stateKey is reflected in state", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(2);
    const api = createMockApi();

    fn(createPayload(root, { stateKey: "onboarding" }), api);

    expect(api.emitState).toHaveBeenCalledWith(
      expect.objectContaining({ stateKey: "onboarding" })
    );
  });

  it("cleanup removes button listeners", async () => {
    const fn = await getMountFn();
    const root = createWizardDOM(3);
    const api = createMockApi();

    const cleanup = fn(createPayload(root, {}), api);
    api.emitAction.mockClear();

    cleanup();
    root.querySelector("[data-wizard-next]").click();

    expect(api.emitAction).not.toHaveBeenCalled();
  });
});
