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

  function getLangToggle() {
    return document.querySelector('[data-lang-toggle]');
  }

  function buildTargetUrl(currentPath) {
    // Strip leading slash for consistency
    var path = currentPath.replace(/^\//, '');

    if (/^vi\//.test(path) || path === 'vi' || path === 'vi/') {
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
    var toggle = getLangToggle();
    if (!toggle) return;

    var currentPath = window.location.pathname;
    var target = buildTargetUrl(currentPath);

    toggle.setAttribute('href', target);

    // Click handler to also save a hint of the page the user wants
    toggle.addEventListener('click', function (e) {
      // Let the link navigate normally — the href is already set.
      // Nothing more to do.
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachToggle);
  } else {
    attachToggle();
  }
})();
