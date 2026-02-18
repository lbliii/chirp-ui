import { readProps, registerPrimitive, setAction, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  let count = Number(props.seed || 0);
  const root = payload.element;
  const valueNode = root.querySelector("[data-counter-value]");
  const plus = root.querySelector("[data-counter-plus]");
  const minus = root.querySelector("[data-counter-minus]");

  const render = () => {
    if (valueNode) {
      valueNode.textContent = String(count);
    }
    setState(payload, api, { count });
  };

  const inc = () => {
    count += 1;
    render();
    setAction(payload, api, "increment", "success");
  };
  const dec = () => {
    count -= 1;
    render();
    setAction(payload, api, "decrement", "success");
  };

  plus?.addEventListener("click", inc);
  minus?.addEventListener("click", dec);
  render();

  return () => {
    plus?.removeEventListener("click", inc);
    minus?.removeEventListener("click", dec);
  };
}

registerPrimitive("counter-widget", { mount });
