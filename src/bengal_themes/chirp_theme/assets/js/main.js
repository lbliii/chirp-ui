/**
 * chirp-theme
 * Minimal runtime helpers for the retained surface.
 */

(function () {
  'use strict';

  let printOpenedDetails = [];
  let printDecoratedLinks = [];
  let printLinkUrlElements = [];
  let printBreakableElements = [];
  let printMetadataElement = null;
  let printPrepared = false;

  const PRINT_TRACKING_PARAMETERS = new Set([
    'dclid',
    'fbclid',
    'gclid',
    'mc_cid',
    'mc_eid',
    'msclkid',
  ]);

  const log = window.BengalUtils?.log || (() => {});
  const copyToClipboard = window.BengalUtils?.copyToClipboard || (async () => {});
  const ready = window.BengalUtils?.ready || ((fn) => {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  });

  /**
   * Returns true when the user has requested reduced motion.
   * Single source of truth for scroll/animation behavior across theme JS —
   * other modules reuse this via window.BengalMain.prefersReducedMotion()
   * instead of duplicating their own matchMedia query.
   */
  function prefersReducedMotion() {
    return typeof window.matchMedia === 'function'
      && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /**
   * scrollIntoView behavior that collapses to 'auto' (instant) when the user
   * prefers reduced motion. The CSS `scroll-behavior` reset does not cover the
   * explicit JS option, so guard each call site through here.
   */
  function scrollBehavior() {
    return prefersReducedMotion() ? 'auto' : 'smooth';
  }

  function setupSmoothScroll() {
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach((anchor) => {
      anchor.addEventListener('click', (event) => {
        const href = anchor.getAttribute('href');
        if (!href || href === '#') {
          return;
        }

        const target = document.getElementById(href.slice(1));
        if (!target) {
          return;
        }

        event.preventDefault();
        target.scrollIntoView({ behavior: scrollBehavior(), block: 'start' });
        history.pushState(null, '', href);
        if (!target.hasAttribute('tabindex')) {
          target.setAttribute('tabindex', '-1');
        }
        target.focus({ preventScroll: true });
      });
    });
  }

  function setupExternalLinks() {
    const links = document.querySelectorAll('a[href]');
    links.forEach((link) => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
        return;
      }

      let isExternal = false;
      try {
        isExternal = new URL(href, window.location.href).origin !== window.location.origin;
      } catch {
        return;
      }

      if (!isExternal) {
        return;
      }

      const label = (link.textContent || '').trim();
      link.setAttribute('data-external', 'true');
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
      if (label) {
        link.setAttribute('aria-label', `${label} (opens in new tab)`);
      }
    });
  }

  function cleanPrintUrl(href) {
    try {
      const url = new URL(href, window.location.href);
      if (url.protocol !== 'http:' && url.protocol !== 'https:') {
        return null;
      }

      url.username = '';
      url.password = '';
      url.hash = '';
      Array.from(url.searchParams.keys()).forEach((key) => {
        const normalizedKey = key.toLowerCase();
        if (normalizedKey.startsWith('utm_') || PRINT_TRACKING_PARAMETERS.has(normalizedKey)) {
          url.searchParams.delete(key);
        }
      });
      return url.href;
    } catch {
      return null;
    }
  }

  function normalizedUrlLabel(value) {
    return value.trim().replace(/^https?:\/\//, '').replace(/\/$/, '');
  }

  function preparePrintLinks() {
    printDecoratedLinks = [];
    printLinkUrlElements = [];
    document.querySelectorAll('main a[href]').forEach((link) => {
      const cleanUrl = cleanPrintUrl(link.href);
      if (!cleanUrl || new URL(cleanUrl).origin === window.location.origin) {
        return;
      }

      const label = normalizedUrlLabel(link.textContent || '');
      if (label && label === normalizedUrlLabel(cleanUrl)) {
        return;
      }

      link.setAttribute('data-print-href', cleanUrl);
      printDecoratedLinks.push(link);
      const printedUrl = document.createElement('span');
      printedUrl.className = 'print-link-url print-only';
      printedUrl.textContent = ` (${cleanUrl})`;
      link.after(printedUrl);
      printLinkUrlElements.push(printedUrl);
    });
  }

  function preparePrintBreaks() {
    printBreakableElements = [];
    const candidates = document.querySelectorAll(
      'main :is(pre, .chirpui-callout, .callout, figure, .card, .feature-card, .callout-card)'
    );
    candidates.forEach((element) => {
      if (element.scrollHeight <= 500) {
        return;
      }
      element.setAttribute('data-print-breakable', 'true');
      printBreakableElements.push(element);
    });
  }

  function preparePrintMetadata() {
    const content = document.querySelector('main article') || document.querySelector('main');
    if (!content) {
      return;
    }

    const canonical = document.querySelector('link[rel="canonical"]')?.href
      || window.location.href;
    const cleanUrl = cleanPrintUrl(canonical);
    if (!cleanUrl) {
      return;
    }

    const metadata = document.createElement('div');
    metadata.className = 'print-document-meta print-only';
    metadata.setAttribute('role', 'note');
    metadata.setAttribute('aria-label', 'Printed document information');
    metadata.setAttribute('data-print-generated', 'true');

    const title = document.createElement('span');
    title.className = 'print-document-meta__title';
    title.textContent = document.title;

    const source = document.createElement('span');
    source.className = 'print-document-meta__source';
    source.textContent = 'Source: ';

    const link = document.createElement('a');
    link.href = cleanUrl;
    link.textContent = cleanUrl;
    source.append(link);
    metadata.append(title, source);
    content.append(metadata);
    printMetadataElement = metadata;
  }

  function setupCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach((codeBlock) => {
      const pre = codeBlock.parentElement;
      if (!pre || pre.closest('.code-block-wrapper') || pre.querySelector('.code-copy-button')) {
        return;
      }
      // Skip chirp-ui's own code blocks: code_block(copy=true) already ships a
      // `.chirpui-code-block-wrapper` + `.chirpui-code-block__copy` button.
      // Re-wrapping them inserts a stray `.code-block-wrapper` ahead of the
      // member's docstring example, hijacking the first-code-block selector.
      if (pre.classList.contains('chirpui-code-block')
        || pre.closest('.chirpui-code-block-wrapper')) {
        return;
      }

      const highlightTable = pre.closest('.highlighttable');
      const languageMatch = codeBlock.className.match(/language-(\w+)|hljs-(\w+)/);
      const language = (languageMatch?.[1] || languageMatch?.[2] || '').toUpperCase();

      const button = document.createElement('button');
      button.className = 'code-copy-button copy-success-burst';
      button.setAttribute('aria-label', 'Copy');
      button.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span>Copy</span>
      `;

      if (highlightTable) {
        const highlightWrapper = highlightTable.closest('.highlight');
        if (!highlightWrapper) {
          return;
        }
        highlightWrapper.classList.add('has-copy-button');
        button.classList.add('code-copy-button--absolute');
        highlightWrapper.appendChild(button);
      } else {
        const header = document.createElement('div');
        header.className = 'code-header-inline';
        const label = document.createElement('span');
        if (language) {
          label.className = 'code-language';
          label.textContent = language;
        }
        header.append(label, button);

        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        const nonEmptyLines = (codeBlock.textContent || '')
          .split('\n')
          .map((line) => line.trim())
          .filter(Boolean);
        if (
          nonEmptyLines.length <= 1
          && codeBlock.closest(
            '.chirp-theme-reference-description, .chirp-theme-reference-member__description'
          )
        ) {
          wrapper.classList.add('code-block-wrapper--specimen');
        }

        ['gradient-border', 'gradient-border-subtle', 'gradient-border-strong', 'fluid-border', 'fluid-combined']
          .forEach((className) => {
            if (pre.classList.contains(className)) {
              pre.classList.remove(className);
              wrapper.classList.add(className);
            }
          });

        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.append(pre, header);
      }

      button.addEventListener('click', async (event) => {
        event.preventDefault();
        try {
          await copyToClipboard(codeBlock.textContent || '');
          button.classList.add('copied');
          button.setAttribute('aria-label', 'Code copied!');
          button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>Copied!</span>
          `;
        } catch (error) {
          log('Failed to copy code:', error);
          button.setAttribute('aria-label', 'Failed to copy');
        }

        window.setTimeout(() => {
          button.classList.remove('copied');
          button.setAttribute('aria-label', 'Copy');
          button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
          `;
        }, 2000);
      });
    });
  }

  function setupKeyboardDetection() {
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Tab') {
        document.body.classList.add('user-is-tabbing');
      }
    });
    document.addEventListener('mousedown', () => {
      document.body.classList.remove('user-is-tabbing');
    });
  }

  /**
   * Native closed <details> descendants are omitted from Chromium PDF layout
   * even when print CSS computes the content as display:block. Open authored
   * main-content disclosures for the print lifecycle, then restore their
   * original state after the browser finishes printing.
   */
  function preparePrint() {
    if (printPrepared) {
      return;
    }

    printPrepared = true;

    printOpenedDetails = Array.from(document.querySelectorAll('main details:not([open])'));
    printOpenedDetails.forEach((details) => {
      details.open = true;
    });
    preparePrintLinks();
    preparePrintBreaks();
    preparePrintMetadata();
  }

  function restorePrint() {
    printOpenedDetails.forEach((details) => {
      if (details.isConnected) {
        details.open = false;
      }
    });
    printOpenedDetails = [];
    printDecoratedLinks.forEach((link) => {
      if (link.isConnected) {
        link.removeAttribute('data-print-href');
      }
    });
    printDecoratedLinks = [];
    printLinkUrlElements.forEach((element) => element.remove());
    printLinkUrlElements = [];
    printBreakableElements.forEach((element) => {
      if (element.isConnected) {
        element.removeAttribute('data-print-breakable');
      }
    });
    printBreakableElements = [];
    printMetadataElement?.remove();
    printMetadataElement = null;
    printPrepared = false;
  }

  window.addEventListener('beforeprint', preparePrint);
  window.addEventListener('afterprint', restorePrint);

  function init() {
    setupSmoothScroll();
    setupExternalLinks();
    setupCodeCopyButtons();
    setupKeyboardDetection();
    log('chirp-theme minimal runtime initialized');
  }

  ready(init);
  window.BengalMain = {
    cleanup: () => {},
    prefersReducedMotion,
    scrollBehavior,
  };
})();
