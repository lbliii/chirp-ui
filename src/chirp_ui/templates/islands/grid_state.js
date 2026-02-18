import { readProps, registerPrimitive, setAction, setState } from "/static/islands/foundation.js";

function mount(payload, api) {
  const props = readProps(payload);
  const root = payload.element;
  const stateKey = String(props.stateKey || "grid");
  const filterInput = root.querySelector("[data-grid-filter]");
  const sortBtn = root.querySelector("[data-grid-sort]");
  const rows = Array.from(root.querySelectorAll("[data-grid-row]"));
  let selected = new Set();
  let asc = true;
  let currentFilter = "";

  const render = () => {
    rows.forEach((row) => {
      const text = (row.textContent || "").toLowerCase();
      const visible = !currentFilter || text.includes(currentFilter);
      row.hidden = !visible;
      const checkbox = row.querySelector("[data-grid-select]");
      if (checkbox) {
        checkbox.checked = selected.has(row.getAttribute("data-grid-id") || "");
      }
    });
    setState(payload, api, {
      stateKey,
      filter: currentFilter,
      selected: Array.from(selected),
      sort: asc ? "asc" : "desc",
    });
  };

  const onFilter = () => {
    currentFilter = String(filterInput?.value || "").trim().toLowerCase();
    render();
  };

  const onSort = () => {
    asc = !asc;
    rows.sort((a, b) => {
      const left = (a.textContent || "").toLowerCase();
      const right = (b.textContent || "").toLowerCase();
      return asc ? left.localeCompare(right) : right.localeCompare(left);
    });
    const body = root.querySelector("[data-grid-body]");
    rows.forEach((row) => body?.appendChild(row));
    setAction(payload, api, "sort", "success", { direction: asc ? "asc" : "desc" });
    render();
  };

  const rowHandlers = [];
  rows.forEach((row) => {
    const checkbox = row.querySelector("[data-grid-select]");
    if (!checkbox) return;
    const rowId = row.getAttribute("data-grid-id") || "";
    const onChange = () => {
      if (checkbox.checked) {
        selected.add(rowId);
      } else {
        selected.delete(rowId);
      }
      setAction(payload, api, "select", "success", { count: selected.size });
      render();
    };
    checkbox.addEventListener("change", onChange);
    rowHandlers.push([checkbox, onChange]);
  });

  filterInput?.addEventListener("input", onFilter);
  sortBtn?.addEventListener("click", onSort);
  render();

  return () => {
    filterInput?.removeEventListener("input", onFilter);
    sortBtn?.removeEventListener("click", onSort);
    rowHandlers.forEach(([el, fn]) => el.removeEventListener("change", fn));
  };
}

registerPrimitive("grid_state", { mount });
