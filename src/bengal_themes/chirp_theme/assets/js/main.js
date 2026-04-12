/**
 * chirp-theme
 * Minimal runtime helpers for the retained surface.
 */

(function () {
  'use strict';

  const log = window.BengalUtils?.log || (() => {});
  const copyToClipboard = window.BengalUtils?.copyToClipboard || (async () => {});
  const ready = window.BengalUtils?.ready || ((fn) => {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  });

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
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

  function setupCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach((codeBlock) => {
      const pre = codeBlock.parentElement;
      if (!pre || pre.closest('.code-block-wrapper') || pre.querySelector('.code-copy-button')) {
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

  function init() {
    setupSmoothScroll();
    setupExternalLinks();
    setupCodeCopyButtons();
    setupKeyboardDetection();
    log('chirp-theme minimal runtime initialized');
  }

  ready(init);
  window.BengalMain = { cleanup: () => {} };
})();
