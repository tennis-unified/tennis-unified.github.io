/* =========================================================================
   Tennis Unified — Language Toggle Script
   Reads the current page URL and switches to the corresponding VI or EN page.

   Strategy:
   - If the current URL contains /vi/, switch to EN (strip /vi/)
   - Otherwise, switch to VI (insert /vi/)
   - If the EN version of the current page doesn't exist, fall back to /vi/ or / home.
   ========================================================================= */

(function () {
  'use strict';

  function getLangToggles() {
    return document.querySelectorAll('[data-lang-toggle]');
  }

  function buildTargetUrl(currentPath) {
    // Strip leading slash for consistency
    var path = currentPath.replace(/^\//, '');

    if (/^vi(\/|$)/.test(path)) {
      // Currently on VI page -> switch to EN (strip /vi/)
      var enPath = path.replace(/^vi\/?/, '');
      return '/' + enPath;
    } else {
      // Currently on EN page -> switch to VI
      if (path === '' || path === '/') {
        return '/vi/';
      }
      return '/vi/' + path;
    }
  }

  function attachToggle() {
    var toggles = getLangToggles();
    if (!toggles || toggles.length === 0) return;

    var currentPath = window.location.pathname;
    var target = buildTargetUrl(currentPath);
    var isVi = /^vi(\/|$)/.test(currentPath.replace(/^\//, ''));

    toggles.forEach(function (toggle) {
      toggle.setAttribute('href', target);
      var textEl = toggle.querySelector('.tu-nav-text');
      if (textEl) {
        textEl.textContent = isVi ? 'English' : 'Tiếng Việt';
      }
      toggle.setAttribute('title', isVi ? 'Switch to English' : 'Chuyển sang Tiếng Việt');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachToggle);
  } else {
    attachToggle();
  }
})();
