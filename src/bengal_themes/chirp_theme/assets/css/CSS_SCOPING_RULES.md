# Bengal CSS Scoping Rules

**Version:** 1.0  
**Date:** October 8, 2025  
**Status:** Active Standard

---

## Core Principle

**Every CSS selector must be scoped to prevent unintended side effects.**

---

## The Scoping Hierarchy

```
1. Component scope    → .dropdown { ... }
2. Content type scope → .prose.api-content { ... }
3. Element scope      → .dropdown-content ul { ... }
```

**Never write bare element selectors outside of base styles.**

---

## Rule 1: Content Type Scoping

### **Problem:**
```css
/* ❌ BAD: Affects ALL prose content */
.prose p + ul {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}
```

### **Solution:**
```css
/* ✅ GOOD: Scoped to specific content type */
.prose.api-content p + ul {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}
```

### **Content Type Classes:**

Use these on the root `.prose` element:

```css
.prose.api-content     /* Auto-generated API documentation */
.prose.reference       /* API reference listings */
.prose.tutorial        /* User tutorials */
.prose.blog-post       /* Blog articles */
.prose.guide           /* How-to guides */
```

**When to use:** Any style specific to a content type.

---

## Rule 2: Component Content Scoping

### **Problem:**
```css
/* ❌ BAD: What if there's a .card inside .dropdown? */
.dropdown-content ul { ... }
.card-body ul { ... }
/* These conflict! */
```

### **Solution: Direct scoping**
```css
/* ✅ GOOD: Direct child selector */
.dropdown-content > ul { ... }
.dropdown-content > ol { ... }
```

**When to use:** Scope each component's content directly so a nested
component (e.g. a `.card` inside a `.dropdown`) can't inherit the wrong list
styling.

---

## Rule 3: Specificity Levels

### **Level 1: Base (Lowest Specificity)**
```css
/* base/reset.css, base/typography.css */
ul, ol { margin: 0; padding: 0; }
```

**Rule:** Only for CSS reset and foundational styles.

---

### **Level 2: Prose Typography**
```css
/* base/typography.css */
.prose ul { list-style-type: disc; }
.prose ol { list-style-type: decimal; }
```

**Rule:** General markdown/HTML content styling.

---

### **Level 3: Content Type Overrides**
```css
/* components/api-docs.css */
.prose.api-content p + ul {
  /* API-specific list styling */
}
```

**Rule:** Content-type specific variations.

---

### **Level 4: Component Scoping**
```css
/* components/dropdown.css */
.dropdown-content ul {
  /* Dropdown-specific list styling */
}
```

**Rule:** Component-specific needs.

---

### **Level 5: Component State (Highest)**
```css
/* components/dropdown.css */
.dropdown-content.is-empty ul {
  /* Special state styling */
}
```

**Rule:** State-based overrides.

---

## Rule 4: The Cascade Chain

**Order matters!** Imports in `style.css` must follow this order:

```css
/* 1. Tokens (variables) */
@import 'tokens/foundation.css';
@import 'tokens/semantic.css';

/* 2. Base (element resets) */
@import 'base/reset.css';
@import 'base/typography.css';

/* 3. Composition (layout primitives) */
@import 'composition/layouts.css';

/* 4. Components (most specific) */
@import 'components/...';

/* 5. Pages (page-specific overrides) */
@import 'pages/...';
```

**Why:** Later imports override earlier ones. Components must come after base styles.

---

## Rule 5: Selector Naming Convention

### **Component Structure:**
```css
.component-name           /* Block */
.component-name__element  /* Element (optional BEM-style) */
.component-name--modifier /* Modifier/variant */
```

### **Examples:**
```css
.dropdown                 /* Component */
.dropdown-content         /* Sub-element (or .dropdown__content) */
.dropdown--minimal        /* Variant */
.dropdown.is-open         /* State */
```

### **Content Areas:**
```css
.component-content        /* Generic content */
.component-body          /* Main content area */
.component-text          /* Text-only area */
```

---

## Rule 6: When to Use .prose

### **✅ Use .prose when:**
- Content comes from markdown
- Content is user-generated HTML
- You want standard typography styles

### **❌ Don't use .prose when:**
- Building UI components (navigation, buttons, etc.)
- Creating layout structures
- Styling application chrome

### **Example:**
```html
<!-- ✅ GOOD: User content -->
<article class="prose">
  {{ content }}
</article>

<!-- ❌ BAD: UI component -->
<nav class="prose">
  <ul>...</ul>
</nav>

<!-- ✅ GOOD: UI component -->
<nav class="site-nav">
  <ul>...</ul>
</nav>
```

---

## Rule 7: Defensive CSS

### **Always assume conflicts will happen.**

### **Bad (fragile):**
```css
.prose ul {
  background: var(--color-surface);
}
```

**Problem:** What if an admonition contains a list?

### **Good (defensive):**
```css
/* API docs: Only style direct children */
.prose.api-content > ul {
  background: var(--color-surface);
}

/* OR: Use specific context */
.prose.api-content p + ul {
  background: var(--color-surface);
}
```

---

## Rule 8: Scoping Checklist

Before adding a new CSS rule, ask:

- [ ] Is this scoped to a component?
- [ ] Will this affect nested components?
- [ ] Is this specific to a content type?
- [ ] Will this conflict with existing styles?
- [ ] Is the selector as specific as needed, no more?

---

## Rule 9: Anti-Patterns to Avoid

### **❌ Don't:**

1. **Bare element selectors in components:**
   ```css
   /* ❌ In components/dropdown.css */
   ul { list-style: none; }
   ```

2. **Overly broad .prose selectors:**
   ```css
   /* ❌ Too broad */
   .prose ul { border: 1px solid red; }
   ```

3. **Important cascades:**
   ```css
   /* ❌ Fighting specificity */
   .prose ul { list-style: disc !important; }
   ```

4. **Deep nesting:**
   ```css
   /* ❌ Too specific, hard to override */
   .prose .card .dropdown-content ul li a { ... }
   ```

### **✅ Do:**

1. **Scoped component selectors:**
   ```css
   /* ✅ In components/dropdown.css */
   .dropdown-content ul { list-style: none; }
   ```

2. **Content-type specific selectors:**
   ```css
   /* ✅ Properly scoped */
   .prose.api-content ul { border: 1px solid red; }
   ```

3. **Direct child selectors for shared patterns:**
   ```css
   /* ✅ Won't leak into nested components */
   .dropdown-content > ul { list-style: disc; }
   ```

4. **Shallow, specific selectors:**
   ```css
   /* ✅ Just right */
   .dropdown-content > ul { ... }
   ```

---

## Quick Reference

### **What to use where:**

| Location | Selector Style | Example |
|----------|---------------|---------|
| `base/reset.css` | Bare elements | `ul, ol { ... }` |
| `base/typography.css` | `.prose elements` | `.prose ul { ... }` |
| `components/*.css` | `.component elements` | `.dropdown ul { ... }` |
| Content-specific | `.prose.type elements` | `.prose.api-content ul { ... }` |

---

## Examples

### **Example 1: Adding a new component**

```css
/* components/callout.css */

/* Component base */
.callout {
  padding: var(--space-4);
  border-radius: var(--radius-md);
}

/* Content area - scope lists to the body directly */
.callout-body ul {
  padding-left: var(--space-8);
  list-style-type: disc;
}

/* Variant */
.callout--warning {
  background: var(--color-warning-bg);
}
```

```html
<div class="callout callout--warning">
  <div class="callout-body">
    <!-- User content here -->
  </div>
</div>
```

---

### **Example 2: Content-type specific styling**

```css
/* components/tutorial-docs.css */

/* Only affects tutorial content */
.prose.tutorial h2 {
  /* Add step numbers */
  counter-increment: step;
}

.prose.tutorial h2::before {
  content: "Step " counter(step) ": ";
  color: var(--color-primary);
}

/* Tutorial-specific lists */
.prose.tutorial > ul {
  /* Checklist style */
  list-style-type: "✓ ";
}
```

---

### **Example 3: Nested components**

```css
/* components/dropdown.css */

/* Dropdown styles */
.dropdown-content ul {
  padding-left: var(--space-6);
  list-style-type: disc;
}

/* But: What if dropdown contains a card? */
/* Solution: Use direct child selector */
.dropdown-content > ul {
  /* Only affects direct children */
}
```

---

## Enforcement

### **Manual Review:**
- Every PR with CSS changes must follow these rules
- Reviewer checks scoping on new selectors

### **Automated (Future):**
- Stylelint rules
- CSS validator in CI
- Scope checker script

---

## Migration Path

For existing code:

1. **Audit:** Find all `.prose` selectors outside `typography.css`
2. **Scope:** Add appropriate content-type class (`.api-content`, etc.)
3. **Refactor:** Scope shared patterns with direct child selectors (`.component-content > ul`)
4. **Test:** Verify no visual regressions
5. **Document:** Update component docs with scoping requirements

---

## Questions?

**Q: Do I need to scope utility classes?**  
A: No. Utilities like `.flex`, `.mt-4` are intentionally global.

**Q: What if I need to override prose styles in a component?**  
A: Use a more specific selector:
```css
.dropdown-content .prose ul {
  /* Override .prose ul */
}
```

**Q: Can I use `!important`?**  
A: Only as a last resort, and document why.

**Q: How do I handle dark mode?**  
A: Scope dark mode the same way:
```css
[data-theme="dark"] .prose.api-content ul { ... }
```

**Q: What about responsive styles?**  
A: Keep the same scoping:
```css
@media (max-width: 768px) {
  .prose.api-content ul { ... }
}
```

---

## Related Documents

- [CSS Architecture Review](../plan/completed/CSS_ARCHITECTURE_REVIEW.md)
- [Component Fixes](../plan/completed/CSS_COMPONENT_FIXES_2025-10-08.md)
- [Theme README](./README.md)

---

**Remember:** When in doubt, scope it! It's easier to loosen scoping later than to fix conflicts.
