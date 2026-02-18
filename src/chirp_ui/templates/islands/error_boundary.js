import { readProps, registerPrimitive, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const boundaryId = String(props.boundaryId || payload.id || payload.name);
  const fallback = root.querySelector("[data-error-fallback]");
  const reset = root.querySelector("[data-error-reset]");
  const body = root.querySelector("[data-error-body]");

  const showFallback = () => {
    fallback?.removeAttribute("hidden");
    body?.setAttribute("hidden", "hidden");
    setState(payload, api, { boundaryId, state: "error" });
  };

  const clearFallback = () => {
    fallback?.setAttribute("hidden", "hidden");
    body?.removeAttribute("hidden");
    setState(payload, api, { boundaryId, state: "healthy" });
  };

  const onError = (event) => {
    const detail = event.detail || {};
    const targetId = detail.id || null;
    if (targetId && payload.id && targetId !== payload.id) {
      return;
    }
    if (detail.name && detail.name !== payload.name && !detail.error) {
      return;
    }
    showFallback();
  };

  const onReset = () => clearFallback();

  document.addEventListener("chirp:island:error", onError);
  reset?.addEventListener("click", onReset);
  clearFallback();

  return () => {
    document.removeEventListener("chirp:island:error", onError);
    reset?.removeEventListener("click", onReset);
  };
}

registerPrimitive("error_boundary", { mount });
