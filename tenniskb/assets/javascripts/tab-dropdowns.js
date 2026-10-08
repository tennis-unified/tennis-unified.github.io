// Tab dropdown functionality for MkDocs Material top navigation
// This enables dropdown menus in the top tab bar

(function() {
  'use strict';

  function initTabDropdowns() {
    const tabItems = document.querySelectorAll('.md-tabs__item--nested');

    tabItems.forEach(function(item) {
      var toggle = item.querySelector('.md-tabs__toggle');
      var link = item.querySelector('.md-tabs__link');
      var nested = item.querySelector('.md-tabs__nested');

      if (!toggle || !link || !nested) return;

      toggle.style.display = 'none';
      toggle.setAttribute('aria-hidden', 'true');

      link.setAttribute('role', 'button');
      link.setAttribute('aria-haspopup', 'true');
      link.setAttribute('aria-expanded', 'false');
      link.tabIndex = 0;
      link.style.cursor = 'pointer';

      link.addEventListener('click', function(e) {
        if (nested && nested.children.length > 0) {
          e.preventDefault();
          e.stopPropagation();

          var isExpanded = toggle.checked;
          toggle.checked = !isExpanded;
          updateAriaExpanded(link, !isExpanded);
        }
      });

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
          var firstNestedLink = nested.querySelector('.md-tabs__link');
          if (firstNestedLink) firstNestedLink.focus();
        }
      });

      nested.addEventListener('focusin', function() {
        if (!toggle.checked) {
          toggle.checked = true;
          updateAriaExpanded(link, true);
        }
      });

      item.addEventListener('focusout', function(e) {
        if (!item.contains(e.relatedTarget)) {
          toggle.checked = false;
          updateAriaExpanded(link, false);
        }
      });

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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTabDropdowns);
  } else {
    initTabDropdowns();
  }

  if (typeof history !== 'undefined') {
    var originalPushState = history.pushState;
    history.pushState = function() {
      originalPushState.apply(this, arguments);
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

  document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('md-instant-init', initTabDropdowns);
    document.addEventListener('md-instant-change', initTabDropdowns);
  });

  window.initTabDropdowns = initTabDropdowns;
})();
