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

  function getAlternateUrl(targetLang) {
    var link = document.querySelector('link[rel="alternate"][hreflang="' + targetLang + '"]');
    if (link) {
      var href = link.getAttribute('href');
      if (href) return href;
    }
    return null;
  }

  function buildTargetUrl(currentPath) {
    var isVi = /^\/?vi(\/|$)/.test(currentPath);
    var targetLang = isVi ? 'en' : 'vi';

    // 1. Authoritative check from <link rel="alternate">
    var alt = getAlternateUrl(targetLang);
    if (alt) {
      return alt;
    }

    // 2. Specific routes and fallbacks
    var path = currentPath.replace(/^\//, '');

    if (isVi) {
      // Currently on VI page -> switch to EN
      if (/^vi\/articles(\/.*)?$/.test(path)) {
        return '/' + path.replace(/^vi\/articles/, 'en/articles');
      }
      var enPath = path.replace(/^vi\/?/, '');
      return '/' + (enPath || '');
    } else {
      // Currently on EN page -> switch to VI
      if (/^en\/articles(\/.*)?$/.test(path)) {
        return '/' + path.replace(/^en\/articles/, 'vi/articles');
      }
      if (/^articles(\/.*)?$/.test(path)) {
        return '/vi/' + path;
      }
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
    var isVi = /^\/?vi(\/|$)/.test(currentPath);
    var target = buildTargetUrl(currentPath);

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
