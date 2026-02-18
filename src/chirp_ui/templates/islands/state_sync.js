import { readProps, registerPrimitive, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const stateKey = String(props.stateKey || "value");
  const queryParam = String(props.queryParam || stateKey);
  const url = new URL(window.location.href);
  const initial = url.searchParams.get(queryParam) ?? String(props.initial || "");
  const inputs = root.querySelectorAll("[data-state-field]");
  const state = { [stateKey]: initial };

  const syncInputs = (next) => {
    inputs.forEach((el) => {
      if ("value" in el) {
        el.value = next;
      }
    });
  };

  const update = (nextValue) => {
    state[stateKey] = nextValue;
    const nextUrl = new URL(window.location.href);
    if (nextValue) {
      nextUrl.searchParams.set(queryParam, nextValue);
    } else {
      nextUrl.searchParams.delete(queryParam);
    }
    window.history.replaceState({}, "", nextUrl.toString());
    setState(payload, api, state);
  };

  const handlers = [];
  inputs.forEach((el) => {
    const onInput = () => update("value" in el ? String(el.value) : "");
    el.addEventListener("input", onInput);
    handlers.push([el, onInput]);
  });

  syncInputs(initial);
  setState(payload, api, state);

  return () => {
    handlers.forEach(([el, fn]) => el.removeEventListener("input", fn));
  };
}

registerPrimitive("state_sync", { mount });
