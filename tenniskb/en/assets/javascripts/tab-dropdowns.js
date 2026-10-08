// Tab dropdown functionality for MkDocs Material top navigation
// This enables dropdown menus in the top tab bar

(function() {
  'use strict';

  // Initialize when DOM is ready
  function initTabDropdowns() {
    const tabItems = document.querySelectorAll('.md-tabs__item--nested');

    tabItems.forEach(function(item) {
      var toggle = item.querySelector('.md-tabs__toggle');
      var link = item.querySelector('.md-tabs__link');
      var nested = item.querySelector('.md-tabs__nested');

      if (!toggle || !link || !nested) return;

      // Hide the checkbox but keep it functional
      toggle.style.display = 'none';
      toggle.setAttribute('aria-hidden', 'true');

      // Make the label act as the dropdown trigger
      link.setAttribute('role', 'button');
      link.setAttribute('aria-haspopup', 'true');
      link.setAttribute('aria-expanded', 'false');
      link.tabIndex = 0;
      link.style.cursor = 'pointer';

      // Click handler for the label
      link.addEventListener('click', function(e) {
        // Don't prevent default if it's a real link and not a dropdown
        if (nested && nested.children.length > 0) {
          e.preventDefault();
          e.stopPropagation();

          var isExpanded = toggle.checked;
          toggle.checked = !isExpanded;
          updateAriaExpanded(link, !isExpanded);
        }
      });

      // Keyboard support
      link.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          e.stopPropagation();
          var isExpanded = toggle.checked;
          toggle.checked = !isExpanded;
          updateAriaExpanded(link, !isExpanded);
        } else if (e.key === 'Escape') {
          if (toggle.checked) {
            toggle.checked = false;
            updateAriaExpanded(link, false);
            link.focus();
          }
        } else if (e.key === 'ArrowDown') {
          e.preventDefault();
          if (!toggle.checked) {
            toggle.checked = true;
            updateAriaExpanded(link, true);
          }
          // Focus first nested item
          var firstNestedLink = nested.querySelector('.md-tabs__link');
          if (firstNestedLink) firstNestedLink.focus();
        }
      });

      // Handle focus within nested menu
      nested.addEventListener('focusin', function() {
        if (!toggle.checked) {
          toggle.checked = true;
          updateAriaExpanded(link, true);
        }
      });

      // Handle focus out
      item.addEventListener('focusout', function(e) {
        // Check if focus is leaving the entire dropdown
        if (!item.contains(e.relatedTarget)) {
          toggle.checked = false;
          updateAriaExpanded(link, false);
        }
      });

      // Click outside to close
      document.addEventListener('click', function(e) {
        if (!item.contains(e.target) && toggle.checked) {
          toggle.checked = false;
          updateAriaExpanded(link, false);
        }
      });
    });

    function updateAriaExpanded(link, expanded) {
      link.setAttribute('aria-expanded', expanded);
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTabDropdowns);
  } else {
    initTabDropdowns();
  }

  // Also handle MkDocs Material's instant navigation
  // Listen for page changes
  if (typeof history !== 'undefined') {
    var originalPushState = history.pushState;
    history.pushState = function() {
      originalPushState.apply(this, arguments);
      // Re-initialize after a short delay for new content to render
      setTimeout(initTabDropdowns, 100);
    };

    var originalReplaceState = history.replaceState;
    history.replaceState = function() {
      originalReplaceState.apply(this, arguments);
      setTimeout(initTabDropdowns, 100);
    };

    window.addEventListener('popstate', function() {
      setTimeout(initTabDropdowns, 100);
    });
  }

  // Also handle MkDocs Material's instant navigation
  document.addEventListener('DOMContentLoaded', function() {
    // Listen for instant navigation events
    document.addEventListener('md-instant-init', initTabDropdowns);
    document.addEventListener('md-instant-change', initTabDropdowns);
  });

  // Export for manual initialization
  window.initTabDropdowns = initTabDropdowns;
})();