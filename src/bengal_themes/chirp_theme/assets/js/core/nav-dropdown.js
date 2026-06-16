/**
 * Navigation Dropdown Handler
 *
 * Pattern: HOVER MENU (see COMPONENT-PATTERNS.md)
 * - Trigger: Hover (mouseenter/mouseleave)
 * - State: data-state="open|closed" attributes
 * - Positioning: CSS absolute within parent
 *
 * This pattern is intentionally different from popover-based menus because
 * navigation dropdowns use hover, not click. Native popover is click-only.
 */

(function() {
  'use strict';

  /**
   * Initialize navigation dropdowns
   */
  function initNavDropdowns() {
    const navItems = document.querySelectorAll('.nav-main > li');

    navItems.forEach(function(navItem) {
      const submenu = navItem.querySelector('.submenu');
      // Support both <a> links and <span class="nav-dropdown-trigger"> for dropdown-only items
      const navLink = navItem.querySelector(':scope > a') || navItem.querySelector(':scope > .nav-dropdown-trigger');

      if (!submenu || !navLink) {
        return;
      }

      // Skip if already initialized to prevent duplicate event listeners
      if (navItem.dataset.dropdownInit) {
        return;
      }
      navItem.dataset.dropdownInit = 'true';

      // Mark nav item as having dropdown
      navItem.classList.add('has-dropdown');

      // Initialize state attributes (Supabase/Radix pattern)
      navItem.setAttribute('data-state', 'closed');
      navLink.setAttribute('data-state', 'closed');

      // Add ARIA attributes for accessibility
      navLink.setAttribute('aria-haspopup', 'true');
      navLink.setAttribute('aria-expanded', 'false');
      navLink.setAttribute('aria-controls', submenu.id || `submenu-${Math.random().toString(36).substr(2, 9)}`);

      if (!submenu.id) {
        submenu.id = navLink.getAttribute('aria-controls');
      }

      let isOpen = false;
      let hoverTimeout = null;

      /**
       * Open dropdown
       */
      function openDropdown() {
        if (isOpen) return;

        isOpen = true;
        navItem.setAttribute('data-state', 'open');
        navLink.setAttribute('data-state', 'open');
        navLink.setAttribute('aria-expanded', 'true');

        // Close other dropdowns
        document.querySelectorAll('.nav-main > li[data-state="open"]').forEach(function(item) {
          if (item !== navItem) {
            const otherSubmenu = item.querySelector('.submenu');
            const otherLink = item.querySelector('a');
            item.setAttribute('data-state', 'closed');
            if (otherLink) {
              otherLink.setAttribute('data-state', 'closed');
              otherLink.setAttribute('aria-expanded', 'false');
            }
          }
        });
      }

      /**
       * Close dropdown
       */
      function closeDropdown() {
        if (!isOpen) return;

        isOpen = false;
        navItem.setAttribute('data-state', 'closed');
        navLink.setAttribute('data-state', 'closed');
        navLink.setAttribute('aria-expanded', 'false');
      }

      /**
       * Toggle dropdown
       */
      function toggleDropdown() {
        if (isOpen) {
          closeDropdown();
        } else {
          openDropdown();
        }
      }

      // Mouse events
      navItem.addEventListener('mouseenter', function() {
        clearTimeout(hoverTimeout);
        openDropdown();
      });

      navItem.addEventListener('mouseleave', function() {
        hoverTimeout = setTimeout(function() {
          closeDropdown();
        }, 150); // Small delay to allow moving to dropdown
      });

      // Keep dropdown open when hovering over it
      submenu.addEventListener('mouseenter', function() {
        clearTimeout(hoverTimeout);
        openDropdown();
      });

      submenu.addEventListener('mouseleave', function() {
        hoverTimeout = setTimeout(function() {
          closeDropdown();
        }, 150);
      });

      // Click navigates to the link (Supabase pattern: hover opens, click navigates)
      // No preventDefault - allow normal link behavior
      // Dropdown is controlled by hover, not click

      // Keyboard navigation
      navLink.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleDropdown();
        } else if (e.key === 'ArrowDown') {
          e.preventDefault();
          openDropdown();
          // Focus first item in dropdown
          const firstLink = submenu.querySelector('a');
          if (firstLink) {
            firstLink.focus();
          }
        } else if (e.key === 'Escape') {
          closeDropdown();
          navLink.focus();
        }
      });

      // Keyboard navigation within dropdown
      const dropdownLinks = submenu.querySelectorAll('a');
      dropdownLinks.forEach(function(link, index) {
        link.addEventListener('keydown', function(e) {
          if (e.key === 'ArrowDown') {
            e.preventDefault();
            const nextLink = dropdownLinks[index + 1] || dropdownLinks[0];
            if (nextLink) nextLink.focus();
          } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prevLink = dropdownLinks[index - 1] || navLink;
            prevLink.focus();
          } else if (e.key === 'Escape') {
            closeDropdown();
            navLink.focus();
          } else if (e.key === 'Home') {
            e.preventDefault();
            dropdownLinks[0]?.focus();
          } else if (e.key === 'End') {
            e.preventDefault();
            dropdownLinks[dropdownLinks.length - 1]?.focus();
          }
        });
      });

      // Close on outside click
      document.addEventListener('click', function(e) {
        if (!navItem.contains(e.target)) {
          closeDropdown();
        }
      });

      // Close on window resize (mobile)
      window.addEventListener('resize', function() {
        if (window.innerWidth < 768) {
          closeDropdown();
        }
      });
    });
  }

  /**
   * Initialize Chirp UI navbar dropdowns rendered as native details elements.
   */
  function initChirpNavbarDropdowns() {
    const dropdowns = document.querySelectorAll('.chirp-theme-shell__nav-dropdown');

    dropdowns.forEach(function(dropdown) {
      const trigger = dropdown.querySelector(':scope > .chirpui-navbar-dropdown__trigger');
      const menu = dropdown.querySelector(':scope > .chirpui-navbar-dropdown__menu');

      if (!trigger || !menu || dropdown.dataset.dropdownInit) {
        return;
      }

      dropdown.dataset.dropdownInit = 'true';
      trigger.setAttribute('aria-haspopup', 'true');
      trigger.setAttribute('aria-expanded', dropdown.open ? 'true' : 'false');

      // Section-overview href: the dropdown menu carries a link to its section
      // root (e.g. /docs/). On hover-capable pointers the menu is revealed via
      // CSS :hover/:focus-within, so the <summary> click is free to NAVIGATE to
      // the section root instead of merely toggling (Supabase pattern: hover
      // opens, click navigates). Touch / no-hover devices keep the native
      // <details> toggle so the menu stays reachable.
      const overviewLink = menu.querySelector('[data-chirp-theme-mega-overview]');
      const overviewHref = overviewLink ? overviewLink.getAttribute('href') : null;

      if (!menu.id) {
        menu.id = `navbar-menu-${Math.random().toString(36).slice(2, 9)}`;
      }
      trigger.setAttribute('aria-controls', menu.id);

      let closeTimer = null;
      const hoverMedia = window.matchMedia('(hover: hover) and (pointer: fine)');

      function closeOtherDropdowns() {
        document.querySelectorAll('.chirp-theme-shell__nav-dropdown[open]').forEach(function(other) {
          if (other !== dropdown) {
            other.removeAttribute('open');
            other.querySelector(':scope > .chirpui-navbar-dropdown__trigger')
              ?.setAttribute('aria-expanded', 'false');
          }
        });
      }

      function openDropdown() {
        clearTimeout(closeTimer);
        closeOtherDropdowns();
        dropdown.setAttribute('open', '');
        trigger.setAttribute('aria-expanded', 'true');
      }

      function closeDropdown() {
        clearTimeout(closeTimer);
        dropdown.removeAttribute('open');
        trigger.setAttribute('aria-expanded', 'false');
      }

      function queueClose() {
        clearTimeout(closeTimer);
        closeTimer = setTimeout(closeDropdown, 140);
      }

      dropdown.addEventListener('pointerenter', function(event) {
        if (hoverMedia.matches && event.pointerType !== 'touch') {
          openDropdown();
        }
      });

      dropdown.addEventListener('pointerleave', function(event) {
        if (hoverMedia.matches && event.pointerType !== 'touch') {
          queueClose();
        }
      });

      dropdown.addEventListener('focusin', openDropdown);
      dropdown.addEventListener('focusout', function(event) {
        if (!dropdown.contains(event.relatedTarget)) {
          queueClose();
        }
      });

      dropdown.addEventListener('toggle', function() {
        trigger.setAttribute('aria-expanded', dropdown.open ? 'true' : 'false');
        if (dropdown.open) {
          closeOtherDropdowns();
        }
      });

      // Navigate to the section root on click/Enter when a hover-capable
      // pointer is present (the menu is already revealed by :hover, so the
      // toggle is redundant). preventDefault stops the native <details> toggle.
      function navigateToOverview() {
        if (overviewHref) {
          window.location.assign(overviewHref);
          return true;
        }
        return false;
      }

      trigger.addEventListener('click', function(event) {
        if (overviewHref && hoverMedia.matches) {
          event.preventDefault();
          navigateToOverview();
        }
      });

      trigger.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowDown') {
          event.preventDefault();
          openDropdown();
          menu.querySelector('a')?.focus();
        } else if (event.key === 'Enter' && overviewHref) {
          // Enter activates the trigger as a link to the section root.
          event.preventDefault();
          navigateToOverview();
        } else if (event.key === 'Escape') {
          closeDropdown();
          trigger.focus();
        }
      });

      menu.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
          closeDropdown();
          trigger.focus();
        }
      });
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initNavDropdowns();
      initChirpNavbarDropdowns();
    });
  } else {
    initNavDropdowns();
    initChirpNavbarDropdowns();
  }
})();
