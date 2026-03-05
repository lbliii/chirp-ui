# Dashboard Maturity Contract

Benchmark-derived rules for dashboard/CRM-quality interaction patterns. Use these to guide component design and page decisions.

## Product Principles

### 1. One interaction model everywhere

- Same patterns for edit, delete, filter, select, and run actions across pages
- No page-specific ad-hoc interaction style unless there is a hard requirement

### 2. Progressive disclosure over clutter

- Keep default views clean; move advanced controls into trays/popovers/collapsible sections
- Use contextual help (`tooltip`/`popover`) instead of long static explanation blocks

### 3. Explicit action hierarchy

- Per region: 1 primary action, compact secondary actions, protected destructive actions
- Destructive actions must always use explicit confirmation UI (never native `confirm()`)

### 4. Edit affordance clarity

- If editable: either click-to-edit inline or explicit edit mode toggle
- Preserve user confidence with clear save/cancel state and feedback

### 5. Accessible, high-signal visual language

- Strong focus-visible behavior, reduced-motion support, semantic status colors/tokens
- Spacing and elevation communicate structure, not decoration

---

## Action Hierarchy

| Zone | Purpose | Examples |
|------|---------|----------|
| **Primary** | Main CTA for the region | Create, Save, Run |
| **Secondary** | Supporting actions | Edit, Export, Filters |
| **Destructive** | Delete, remove, irreversible | Delete, Remove — always behind `confirm_dialog` |

Use `action_strip`, `command_bar`, `filter_bar` with zones: `chirpui-action-strip__primary`, `chirpui-action-strip__controls`, `chirpui-action-strip__actions`.

---

## Edit Mode Policy

- **Inline edit**: Single-field tweaks (name, title). Use `inline_edit_field` with display + edit mode.
- **Explicit edit**: Multi-field forms. Use edit mode toggle; show Save/Cancel clearly.
- **No ambiguity**: If editable, user must know how to enter and exit edit state.

---

## Confirmation Policy

- **Destructive actions**: Always use `confirm_dialog` (never `hx-confirm` or native `confirm()`).
- **Confirm dialog**: Title + message + Cancel + Confirm (danger variant for destructive).
- **HTMX-friendly**: Use `confirm_url` + `confirm_method` for form submission; trigger via `confirm_trigger` or custom button with `onclick` to `showModal()`.

---

## Tooltip / Popover Usage

- **Tooltip**: Short hint on hover (1–2 lines). Use for icon-only buttons, truncated labels.
- **Popover**: Interactive content (filters, options). Use for controls that need input.
- **Avoid**: Long static blocks; prefer contextual help.

---

## Data Layout and Action Placement

| Rule | When | Where |
|------|------|-------|
| **Section-level actions** | Primary action for the section (Refresh, Auto-detect, Run validation) | `section_header` actions slot (right of title) |
| **Page-level actions** | Create, Install, bulk actions | `page_header` actions or `command_bar` |
| **Field-set layout** | Label + status + value rows | `settings_row_list` + `settings_row` |
| **Key-value only** | Term + detail, no status | `description_list` (horizontal or stacked) |

Use `section` with `{% slot actions %}` for surface + header + content composites. Put section-level buttons in the actions slot, not beneath the content.

---

## Density and Spacing Defaults

- Use `--chirpui-*` tokens for consistent spacing and elevation
- `action_strip` density: `sm` for compact toolbars, `md` for standard
- Table: `chirpui-table--striped` for readability; optional `chirpui-table-wrap--sticky` for sticky headers

---

## Quality Gates (Acceptance Criteria)

| Gate | Criteria |
|------|----------|
| **Interaction consistency** | All core workflows use same edit/confirm/action hierarchy patterns |
| **Accessibility** | Keyboard navigation and focus-visible behavior verified for interactive controls |
| **Motion and feedback** | Reduced-motion respected; loading and success/error feedback always visible |
| **Density and readability** | No visual crowding regressions at common viewport widths |
| **Code quality** | Reduced inline style/JS in page templates in favor of reusable component patterns |

---

## Phase Completion Criteria

- **Phase 0**: Product principles and quality gates documented and approved ✓
- **Phase 1**: New primitives implemented, documented, and test-covered
- **Phase 2**: Chirp guide examples reflect benchmark-aligned patterns
- **Phase 3**: Dori (and similar apps) no longer rely on ad-hoc interaction patterns for core workflows
- **Phase 4**: All quality gates pass for targeted pages
