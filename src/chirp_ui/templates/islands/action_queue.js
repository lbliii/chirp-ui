import { readProps, registerPrimitive, setAction, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const actionId = String(props.actionId || "action");
  const statusNode = root.querySelector("[data-action-status]");
  const trigger = root.querySelector("[data-action-trigger]");

  const render = (status, message) => {
    if (statusNode) {
      statusNode.textContent = message;
      statusNode.setAttribute("data-status", status);
    }
    setState(payload, api, { actionId, status, message });
  };

  const run = async () => {
    trigger?.setAttribute("disabled", "disabled");
    render("pending", "Working...");
    setAction(payload, api, actionId, "pending");
    await new Promise((resolve) => window.setTimeout(resolve, 450));
    const shouldFail = trigger?.getAttribute("data-action-fail") === "true";
    if (shouldFail) {
      render("error", "Failed. Retry.");
      setAction(payload, api, actionId, "error");
    } else {
      render("success", "Done.");
      setAction(payload, api, actionId, "success");
    }
    trigger?.removeAttribute("disabled");
  };

  trigger?.addEventListener("click", run);
  render("idle", "Ready.");

  return () => {
    trigger?.removeEventListener("click", run);
  };
}

registerPrimitive("action_queue", { mount });
