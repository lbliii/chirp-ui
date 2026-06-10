/**
 * Bengal SSG - Documentation Navigation Enhancement
 *
 * Progressive enhancement for the docs sidebar (`partials/docs-nav.html`).
 *
 * The sidebar works with ZERO JavaScript: every section header (caret button
 * + label link) is rendered ALWAYS visible, and the children region is
 * rendered visible by default so all content is reachable without scripting.
 * `aria-current="page"` marks the active link. This module layers on the
 * disclosure behaviour HTML cannot express on its own:
 *
 *   1. Unique landmark label — the chirp-ui `sidebar()` macro emits a generic
 *      <nav class="chirpui-sidebar"> with no accessible name, which collides
 *      with the surrounding "Documentation catalog" landmarks. We give it a
 *      distinct label so AT users can tell the two navs apart (issue #164,
 *      docs-nav slice).
 *   2. Disclosure toggle — wire each `__toggle` <button> to show/hide its
 *      `aria-controls` children region, keeping aria-expanded + the chevron
 *      rotation in sync. On load, collapse every section that is NOT on the
 *      active trail (the server marks the active branch with `is-active` and
 *      pre-sets the button's aria-expanded="true").
 *   3. Deep-link disclosure — ensure every section ancestor of the active
 *      link is expanded so a bookmarked/deep-linked page reveals its place.
 *
 * Structure note (issue #162 + regression fix): the section label is NOT
 * inside the activatable control. The `__toggle` <button> contains only a
 * decorative caret; the navigable `__summary-link` is its SIBLING in the
 * always-visible `__section-header` row. A *closed* native <details> used to
 * hide everything but the <summary> (`::details-content` is
 * content-visibility:hidden), which made collapsed section labels vanish —
 * this module replaces that with explicit attribute/style toggling and must
 * never wrap a control inside another control.
 *
 * Why inline `style.display` for hiding: the children region
 * (`.chirp-theme-docs-nav__section-links`) is given `display: grid` by a rule
 * in the late `@layer chirp-theme` cascade layer, which beats any rule this
 * theme's component layer (or a bare `[hidden]` UA rule) could add. An inline
 * style wins over every author layer, so we set it directly and keep the
 * `hidden` attribute in sync for semantics.
 */

(function () {
  'use strict';

  var ROOT_SELECTOR = '[data-chirp-theme-doc-nav="catalog"]';
  var SIDEBAR_LABEL = 'Documentation sections';
  var SECTION_SELECTOR = '.chirp-theme-docs-nav__section--has-toggle';
  var TOGGLE_SELECTOR = '.chirp-theme-docs-nav__toggle';

  /**
   * Give the docs-nav sidebar landmark a unique accessible name.
   * @param {HTMLElement|Document} root
   */
  function labelSidebarLandmark(root) {
    var nav = root.querySelector('.chirp-theme-docs-nav.chirpui-sidebar') ||
              root.querySelector('[data-chirp-theme-doc-nav="sections"] .chirpui-sidebar');
    if (nav && !nav.getAttribute('aria-label')) {
      nav.setAttribute('aria-label', SIDEBAR_LABEL);
    }
  }

  /**
   * Find the children region a toggle controls (its aria-controls target,
   * falling back to the section-links sibling within the same section).
   * @param {HTMLElement} toggle
   * @returns {HTMLElement|null}
   */
  function panelFor(toggle) {
    var id = toggle.getAttribute('aria-controls');
    var panel = id ? document.getElementById(id) : null;
    if (panel) return panel;
    var section = toggle.closest(SECTION_SELECTOR);
    return section
      ? section.querySelector(':scope > .chirp-theme-docs-nav__section-links')
      : null;
  }

  /**
   * Expand or collapse a section, keeping aria-expanded, the chevron, the
   * `hidden` attribute, and the inline display in sync.
   * @param {HTMLElement} toggle
   * @param {boolean} expanded
   */
  function setExpanded(toggle, expanded) {
    var panel = panelFor(toggle);
    toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    if (!panel) return;
    if (expanded) {
      panel.hidden = false;
      panel.style.removeProperty('display');
    } else {
      panel.hidden = true;
      // Inline style beats the `@layer chirp-theme` `display: grid` rule.
      panel.style.display = 'none';
    }
  }

  /**
   * Wire each disclosure toggle and set its initial collapsed/expanded state
   * from the server-rendered aria-expanded (true on the active trail).
   * @param {HTMLElement|Document} root
   */
  function initToggles(root) {
    var toggles = root.querySelectorAll(TOGGLE_SELECTOR);
    toggles.forEach(function (toggle) {
      // Mirror the server-rendered expanded state into actual visibility.
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      setExpanded(toggle, expanded);

      if (toggle.dataset.docsNavBound === '1') return;
      toggle.dataset.docsNavBound = '1';
      toggle.addEventListener('click', function () {
        var isOpen = toggle.getAttribute('aria-expanded') === 'true';
        setExpanded(toggle, !isOpen);
      });
    });
  }

  /**
   * Open every section ancestor of the current page's active link so a
   * deep-linked page reveals its place in the tree.
   * @param {HTMLElement|Document} root
   */
  function openActiveTrail(root) {
    var active = root.querySelector(
      '.chirp-theme-docs-nav__summary-link--active,' +
      '.chirp-theme-docs-nav [aria-current="page"],' +
      '.chirp-theme-docs-nav__link.chirpui-sidebar__link--active'
    );
    if (!active) return;

    var node = active.parentElement;
    while (node && !(node.matches && node.matches(ROOT_SELECTOR))) {
      if (node.matches && node.matches(SECTION_SELECTOR)) {
        var toggle = node.querySelector(':scope > .chirp-theme-docs-nav__section-header > ' + TOGGLE_SELECTOR);
        if (toggle && toggle.getAttribute('aria-expanded') !== 'true') {
          setExpanded(toggle, true);
        }
      }
      node = node.parentElement;
    }
  }

  /**
   * Apply all enhancements to a docs-nav root.
   * @param {HTMLElement|Document} root
   */
  function enhance(root) {
    var scope = root || document;
    labelSidebarLandmark(scope);
    initToggles(scope);
    openActiveTrail(scope);
  }

  /** Find every docs-nav root in the document and enhance it. */
  function enhanceAll() {
    var roots = document.querySelectorAll(ROOT_SELECTOR);
    if (roots.length === 0) return;
    roots.forEach(function (root) {
      enhance(root);
    });
  }

  // Register with the Bengal enhancement system. Override the no-op/scroll-spy
  // stub from interactive.js so the real behaviour wins when the element with
  // data-bengal="docs-nav" is discovered.
  if (window.Bengal && window.Bengal.enhance) {
    window.Bengal.enhance.register('docs-nav', function (el) {
      enhance(el || document);
    }, { override: true });
  }

  // Self-bootstrap so the enhancements run even when this module is loaded
  // directly. enhance() is idempotent: toggles carry a `data-docs-nav-bound`
  // guard, and re-applying visibility state is harmless.
  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  }
  ready(enhanceAll);

  // Re-apply after htmx boosted navigation swaps in a fresh sidebar.
  document.addEventListener('htmx:afterSwap', enhanceAll);
})();
