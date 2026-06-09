/**
 * Bengal SSG - Documentation Navigation Enhancement
 *
 * Progressive enhancement for the docs sidebar (`partials/docs-nav.html`).
 *
 * The sidebar works with ZERO JavaScript: expand/collapse is native
 * <details>/<summary>, the active trail is pre-opened server-side via the
 * `open` attribute, and `aria-current="page"` marks the active link. This
 * module only layers on polish that HTML cannot express on its own:
 *
 *   1. Unique landmark label — the chirp-ui `sidebar()` macro emits a generic
 *      <nav class="chirpui-sidebar"> with no accessible name, which collides
 *      with the surrounding "Documentation catalog" landmarks. We give it a
 *      distinct label so AT users can tell the two navs apart (issue #164,
 *      docs-nav slice).
 *   2. Deep-link disclosure — when a page is reached via a bookmark/deep link,
 *      ensure every <details> ancestor of the active link is open. The template
 *      already does this for the in-trail path; this is a runtime safety net.
 *
 * Structure note (issue #162): the disclosure <summary> is toggle-only and the
 * section link is its SIBLING, so there is no nested-interactive control. This
 * module must NOT re-introduce one — it only reads structure and sets
 * attributes, it never wraps controls.
 */

(function () {
  'use strict';

  var ROOT_SELECTOR = '[data-chirp-theme-doc-nav="catalog"]';
  var SIDEBAR_LABEL = 'Documentation sections';

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
   * Open every <details> ancestor of the current page's active link so a
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
      if (node.tagName === 'DETAILS' && !node.open) {
        node.open = true;
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
  // directly (the disclosure toggle is native and needs no JS, so this is
  // purely additive and safe to run more than once — it is idempotent).
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
