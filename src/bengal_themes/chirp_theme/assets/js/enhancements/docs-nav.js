/**
 * Bengal SSG - Documentation Navigation Enhancement
 *
 * Progressive enhancement for the docs sidebar (`partials/docs-nav.html`).
 *
 * The sidebar is fully functional with ZERO JavaScript. Each collapsible
 * section is a native <details> whose <summary> CONTAINS the navigable
 * section label, so the label stays painted whether the section is collapsed
 * or open — a closed <details> hides only its NON-summary content. The server
 * seeds the `open` attribute from the active trail, so a deep-linked page
 * arrives with its branch already expanded. The native disclosure marker is
 * suppressed in CSS (no caret) per the owner's preference. `aria-current`
 * marks the active link. No toggle wiring is needed.
 *
 * This module layers on the two niceties HTML cannot express on its own:
 *
 *   1. Unique landmark label — the chirp-ui `sidebar()` macro emits a generic
 *      <nav class="chirpui-sidebar"> with no accessible name, which collides
 *      with the surrounding "Documentation catalog" landmarks. We give it a
 *      distinct label so AT users can tell the two navs apart (issue #164,
 *      docs-nav slice).
 *   2. Active-link scroll — bring the current page's link into view inside the
 *      scrollable sidebar on load, so a deep-linked page reveals its place
 *      without manual scrolling.
 */

(function () {
  'use strict';

  var ROOT_SELECTOR = '[data-chirp-theme-doc-nav="catalog"]';
  var SIDEBAR_LABEL = 'Documentation sections';
  var ACTIVE_SELECTOR =
    '.chirp-theme-docs-nav__summary-link--active,' +
    '.chirp-theme-docs-nav [aria-current="page"],' +
    '.chirp-theme-docs-nav__link.chirpui-sidebar__link--active';

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
   * Scroll the active link into view inside the scrollable sidebar so a
   * deep-linked page reveals its place in the tree. Best-effort and silent.
   * @param {HTMLElement|Document} root
   */
  function scrollActiveIntoView(root) {
    var active = root.querySelector(ACTIVE_SELECTOR);
    if (!active || active.dataset.docsNavScrolled === '1') return;
    active.dataset.docsNavScrolled = '1';
    if (typeof active.scrollIntoView === 'function') {
      active.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    }
  }

  /**
   * Apply all enhancements to a docs-nav root. Idempotent: the landmark label
   * is only set when absent and the scroll runs once per active link.
   * @param {HTMLElement|Document} root
   */
  function enhance(root) {
    var scope = root || document;
    labelSidebarLandmark(scope);
    scrollActiveIntoView(scope);
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
  // directly. enhance() is idempotent.
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
