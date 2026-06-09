/**
 * Track Page Enhancements
 *
 * Features:
 * - Highlights current section in sidebar navigation
 * - Filters TOC to show only current section's items
 * - Progress persistence with localStorage
 * - Marks visited sections with visual indicators
 * - Accessibility: aria-current="step" for screen readers
 *
 * DOM contract (reconciled with tracks/single.html + partials/track-sidebar.html):
 * - nav[data-bengal="track-nav"][data-track-id]   .chirp-theme-track-sidebar
 * - a[data-track-section="N"][data-track-target="#track-section-N"]
 *     .chirp-theme-track-sidebar__link
 *     .chirp-theme-track-sidebar__number  (read for the announcer step number)
 *     .chirp-theme-track-sidebar__title   (read for the announcer section name)
 * - section#track-section-N[data-track-section]   .chirp-theme-track-section
 * - .chirp-theme-track-layout__main   (resume-banner insertion point)
 * - .chirp-theme-track-layout__toc    (combined TOC rail, filtered by section)
 *
 * State attributes set by this script:
 * - data-track-active:    active section link
 * - data-track-visited:   visited section links
 * - data-track-completed: section scrolled fully past
 *
 * See the "RECONCILED DOM VOCABULARY" block at the top of tracks/single.html.
 */

(function() {
  'use strict';

  // Ensure utils are available
  if (!window.BengalUtils) {
    console.error('BengalUtils not loaded - tracks.js requires utils.js');
    return;
  }

  const { throttleScroll, ready } = window.BengalUtils;

  /**
   * Resolve a reduced-motion check. Prefers a shared BengalUtils helper
   * (added by the nav-landmarks/#164 work) and falls back to a local
   * matchMedia read so tracks.js stays correct even when loaded standalone.
   */
  function prefersReducedMotion() {
    if (typeof window.BengalUtils.prefersReducedMotion === 'function') {
      return window.BengalUtils.prefersReducedMotion();
    }
    return (
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    );
  }

  /**
   * scrollIntoView that honors prefers-reduced-motion: smooth animation for
   * everyone else, an instant jump for users who asked to reduce motion.
   * (The tracks.js slice of #164 — CSS `scroll-behavior` does not affect an
   * explicit `behavior:'smooth'` option, so it must be chosen in JS.)
   */
  function scrollToElement(el) {
    if (!el) return;
    el.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
  }

  // ============================================================================
  // Constants
  // ============================================================================

  const STORAGE_KEY_PREFIX = 'bengal_track_progress_';

  const SELECTORS = {
    trackNav: '[data-bengal="track-nav"]',
    // Sidebar section links live inside the track nav; scope the lookup so we
    // do not match the section <section data-track-section> blocks themselves.
    trackSection: 'a[data-track-section]',
    // Pillar-page section blocks emitted by track_section_block (single.html).
    sectionTarget: '.chirp-theme-track-section[data-track-section]',
    // Resume banner insertion point: the center reading column.
    trackContent: '.chirp-theme-track-layout__main',
    // Combined-TOC right rail, filtered to the active section.
    tocSidebar: '.chirp-theme-track-layout__toc',
    // Only select top-level section groups (not nested groups within sections)
    tocSectionGroup: '.toc-group[data-toc-section]',
    // Label/number text inside each sidebar link (read by the announcer).
    navLabel: '.chirp-theme-track-sidebar__title',
    navNumber: '.chirp-theme-track-sidebar__number'
  };

  // ============================================================================
  // State
  // ============================================================================

  let trackNav = null;
  let trackId = null;
  let trackSections = [];
  let sidebarLinks = [];
  let tocGroups = [];
  let tocSidebar = null;
  let currentSectionIndex = -1;
  let scrollHandler = null;
  let progress = { visited: [], lastSection: 0 };

  // ============================================================================
  // Progress Persistence
  // ============================================================================

  /**
   * Get storage key for current track
   */
  function getStorageKey() {
    return STORAGE_KEY_PREFIX + (trackId || 'default');
  }

  /**
   * Load progress from localStorage
   */
  function loadProgress() {
    try {
      const stored = localStorage.getItem(getStorageKey());
      if (stored) {
        const parsed = JSON.parse(stored);
        progress = {
          visited: Array.isArray(parsed.visited) ? parsed.visited : [],
          lastSection: typeof parsed.lastSection === 'number' ? parsed.lastSection : 0
        };
      }
    } catch (e) {
      // localStorage not available or corrupted
      progress = { visited: [], lastSection: 0 };
    }
  }

  /**
   * Save progress to localStorage
   */
  function saveProgress() {
    try {
      localStorage.setItem(getStorageKey(), JSON.stringify(progress));
    } catch (e) {
      // localStorage not available or full
    }
  }

  /**
   * Mark a section as visited
   */
  function markSectionVisited(sectionIndex) {
    if (!progress.visited.includes(sectionIndex)) {
      progress.visited.push(sectionIndex);
      saveProgress();
    }

    // Update DOM
    const link = sidebarLinks[sectionIndex];
    if (link && !link.hasAttribute('data-track-visited')) {
      link.setAttribute('data-track-visited', '');
    }
  }

  /**
   * Check if a section has been scrolled past (completed)
   */
  function updateCompletedSections() {
    const viewportOffset = 150;

    trackSections.forEach((section, index) => {
      const rect = section.getBoundingClientRect();
      const link = sidebarLinks[index];

      // Section is completed if its bottom is above the viewport offset
      // (meaning user has scrolled past it)
      if (rect.bottom < viewportOffset && link) {
        if (!link.hasAttribute('data-track-completed')) {
          link.setAttribute('data-track-completed', '');
          markSectionVisited(index);
        }
      }
    });
  }

  /**
   * Restore visited state from saved progress
   */
  function restoreVisitedState() {
    progress.visited.forEach(index => {
      const link = sidebarLinks[index];
      if (link) {
        link.setAttribute('data-track-visited', '');
      }
    });
  }

  // ============================================================================
  // Section Detection
  // ============================================================================

  /**
   * Find which section is currently in view
   */
  function getCurrentSectionIndex() {
    const viewportOffset = 150;

    for (let i = trackSections.length - 1; i >= 0; i--) {
      const section = trackSections[i];
      const rect = section.getBoundingClientRect();
      if (rect.top <= viewportOffset) {
        return i;
      }
    }

    return 0;
  }

  /**
   * Update UI to reflect current section
   */
  function updateCurrentSection() {
    const newIndex = getCurrentSectionIndex();

    // Update completed sections (scrolled past)
    updateCompletedSections();

    // Only update active state if changed
    if (newIndex === currentSectionIndex) return;

    const previousIndex = currentSectionIndex;
    currentSectionIndex = newIndex;

    // Save last viewed section for "resume" functionality
    progress.lastSection = currentSectionIndex;
    saveProgress();

    // Mark current section as visited
    markSectionVisited(currentSectionIndex);

    // Update sidebar navigation
    sidebarLinks.forEach((link, index) => {
      if (index === currentSectionIndex) {
        // Active section
        link.setAttribute('data-track-active', '');
        link.setAttribute('aria-current', 'step');
        link.classList.add('is-active');
      } else {
        // Inactive sections
        link.removeAttribute('data-track-active');
        link.removeAttribute('aria-current');
        link.classList.remove('is-active');
      }
    });

    // Update TOC filtering
    if (tocSidebar) {
      tocSidebar.setAttribute('data-track-filtering', 'true');
      tocSidebar.setAttribute('data-track-active-section', currentSectionIndex + 1);

      tocGroups.forEach((group, index) => {
        if (index === currentSectionIndex) {
          group.setAttribute('data-toc-active', '');
        } else {
          group.removeAttribute('data-toc-active');
        }
      });
    }

    // Announce section change to screen readers (non-intrusively)
    announceToScreenReader(currentSectionIndex);
  }

  // ============================================================================
  // Accessibility
  // ============================================================================

  let announceTimeout = null;

  /**
   * Announce section change to screen readers via live region
   */
  function announceToScreenReader(sectionIndex) {
    // Debounce announcements to avoid spam during fast scrolling
    if (announceTimeout) {
      clearTimeout(announceTimeout);
    }

    announceTimeout = setTimeout(() => {
      const link = sidebarLinks[sectionIndex];
      if (!link) return;

      const label = link.querySelector(SELECTORS.navLabel);
      const number = link.querySelector(SELECTORS.navNumber);
      // Fall back to the link's own text so the announcer is never empty even
      // if the title/number sub-spans are missing.
      const sectionName = (label ? label.textContent : link.textContent).trim();
      const sectionNum = number ? number.textContent.trim() : sectionIndex + 1;

      // Create or update live region
      let liveRegion = document.getElementById('track-live-region');
      if (!liveRegion) {
        liveRegion = document.createElement('div');
        liveRegion.id = 'track-live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'visually-hidden';
        document.body.appendChild(liveRegion);
      }

      liveRegion.textContent = `Section ${sectionNum}: ${sectionName}`;
    }, 300);
  }

  // ============================================================================
  // Resume Functionality
  // ============================================================================

  /**
   * Check if user should be prompted to resume
   */
  function checkResume() {
    // Only show resume if user has progress and isn't already at that section
    if (progress.lastSection > 0 && progress.visited.length > 0) {
      const currentScroll = window.scrollY;

      // Only show if user is near the top of the page
      if (currentScroll < 200) {
        showResumePrompt();
      }
    }
  }

  /**
   * Show resume prompt
   */
  function showResumePrompt() {
    const targetSection = trackSections[progress.lastSection];
    if (!targetSection) return;

    const link = sidebarLinks[progress.lastSection];
    const label = link ? link.querySelector(SELECTORS.navLabel) : null;
    const sectionName = label
      ? label.textContent.trim()
      : (link ? link.textContent.trim() : `Section ${progress.lastSection + 1}`);

    // Create resume banner
    const banner = document.createElement('div');
    banner.className = 'track-resume-banner';
    banner.setAttribute('role', 'status');
    banner.innerHTML = `
      <span class="track-resume-text">Continue where you left off?</span>
      <button class="track-resume-button" type="button">
        Resume: ${sectionName}
      </button>
      <button class="track-resume-dismiss" type="button" aria-label="Dismiss">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 6L6 18M6 6l12 12"/>
        </svg>
      </button>
    `;

    // Add to page — the center reading column of the pillar-page shell.
    const trackContent = document.querySelector(SELECTORS.trackContent);
    if (trackContent) {
      trackContent.insertBefore(banner, trackContent.firstChild);
    }

    // Handle resume click
    banner.querySelector('.track-resume-button').addEventListener('click', () => {
      scrollToElement(targetSection);
      banner.remove();
    });

    // Handle dismiss
    banner.querySelector('.track-resume-dismiss').addEventListener('click', () => {
      banner.classList.add('track-resume-banner--dismissed');
      setTimeout(() => banner.remove(), 300);
    });

    // Auto-dismiss after scroll
    const dismissOnScroll = () => {
      if (window.scrollY > 300) {
        banner.classList.add('track-resume-banner--dismissed');
        setTimeout(() => banner.remove(), 300);
        window.removeEventListener('scroll', dismissOnScroll);
      }
    };
    window.addEventListener('scroll', dismissOnScroll, { passive: true });
  }

  // ============================================================================
  // Initialization
  // ============================================================================

  /**
   * Initialize track enhancements
   */
  function initTracks() {
    // Find track navigation
    trackNav = document.querySelector(SELECTORS.trackNav);
    if (!trackNav) return;

    // Get track ID for localStorage
    trackId = trackNav.getAttribute('data-track-id') || window.location.pathname;

    // Cache DOM elements
    trackSections = Array.from(document.querySelectorAll(SELECTORS.sectionTarget));
    sidebarLinks = Array.from(trackNav.querySelectorAll(SELECTORS.trackSection));
    tocSidebar = document.querySelector(SELECTORS.tocSidebar);
    tocGroups = tocSidebar ? Array.from(tocSidebar.querySelectorAll(SELECTORS.tocSectionGroup)) : [];

    if (!trackSections.length) return;

    // Load saved progress
    loadProgress();

    // Restore visited state
    restoreVisitedState();

    // Mark as enhanced
    trackNav.setAttribute('data-enhanced', 'true');

    // Set up scroll listener
    scrollHandler = throttleScroll(updateCurrentSection);
    window.addEventListener('scroll', scrollHandler, { passive: true });

    // Initial update
    updateCurrentSection();

    // Check for resume prompt (delayed to avoid flash)
    setTimeout(checkResume, 500);

    // Handle click on sidebar links
    sidebarLinks.forEach((link, index) => {
      link.addEventListener('click', () => {
        currentSectionIndex = -1; // Force update
        setTimeout(updateCurrentSection, 100);
      });
    });
  }

  /**
   * Cleanup function
   */
  function cleanup() {
    if (scrollHandler) {
      window.removeEventListener('scroll', scrollHandler);
      scrollHandler = null;
    }
    if (trackNav) {
      trackNav.removeAttribute('data-enhanced');
    }
    if (announceTimeout) {
      clearTimeout(announceTimeout);
    }
  }

  /**
   * Reset progress for current track
   */
  function resetProgress() {
    progress = { visited: [], lastSection: 0 };
    saveProgress();

    // Clear DOM state
    sidebarLinks.forEach(link => {
      link.removeAttribute('data-track-visited');
      link.removeAttribute('data-track-completed');
    });
  }

  // ============================================================================
  // Auto-initialize
  // ============================================================================

  ready(initTracks);

  window.addEventListener('contentLoaded', initTracks);

  // Register with Bengal enhancement system to prevent 404 from lazy-loader
  // trying to load 'track-nav.js' when it sees data-bengal="track-nav"
  if (window.Bengal && window.Bengal.enhance) {
    window.Bengal.enhance.register('track-nav', function(el) {
      // Enhancement handled by initTracks() - just mark as enhanced
      // The element is already processed since tracks.js runs on DOMContentLoaded
    });
  }

  // Export for debugging and testing
  window.BengalTracks = {
    init: initTracks,
    cleanup: cleanup,
    resetProgress: resetProgress,
    getCurrentSection: () => currentSectionIndex,
    getProgress: () => ({ ...progress })
  };
})();
