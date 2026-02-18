import { readProps, registerPrimitive, setAction, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const stateKey = String(props.stateKey || "wizard");
  const configuredSteps = Array.isArray(props.steps) ? props.steps : [];
  const stepNodes = Array.from(root.querySelectorAll("[data-wizard-step]"));
  const stepIds = stepNodes.map((el, idx) => el.getAttribute("data-step-id") || configuredSteps[idx] || String(idx + 1));
  const nextBtn = root.querySelector("[data-wizard-next]");
  const prevBtn = root.querySelector("[data-wizard-prev]");
  const status = root.querySelector("[data-wizard-status]");
  let index = 0;

  const render = () => {
    stepNodes.forEach((node, idx) => {
      if (idx === index) {
        node.removeAttribute("hidden");
      } else {
        node.setAttribute("hidden", "hidden");
      }
    });
    prevBtn?.toggleAttribute("disabled", index === 0);
    nextBtn?.toggleAttribute("disabled", index >= stepNodes.length - 1);
    if (status) {
      status.textContent = `Step ${index + 1} of ${stepNodes.length}`;
    }
    setState(payload, api, {
      stateKey,
      step: stepIds[index] || String(index + 1),
      index,
      total: stepNodes.length,
    });
  };

  const onNext = () => {
    if (index >= stepNodes.length - 1) return;
    index += 1;
    setAction(payload, api, "next", "success", { step: stepIds[index] });
    render();
  };
  const onPrev = () => {
    if (index <= 0) return;
    index -= 1;
    setAction(payload, api, "prev", "success", { step: stepIds[index] });
    render();
  };

  nextBtn?.addEventListener("click", onNext);
  prevBtn?.addEventListener("click", onPrev);
  render();

  return () => {
    nextBtn?.removeEventListener("click", onNext);
    prevBtn?.removeEventListener("click", onPrev);
  };
}

registerPrimitive("wizard_state", { mount });
