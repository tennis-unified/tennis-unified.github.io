/* =========================================================================
   Tennis Unified & TennisKB — Dynamic Language Toggle Script
   Switches dynamically between corresponding English and Vietnamese pages:
   - Articles 1-200: /en/articles/EN-xxx <-> /vi/articles/VI-xxx
   - Articles Index: /en/articles/ <-> /vi/articles/
   - Category Pillars: /en/articles/biomechanics/ <-> /vi/articles/co-sinh-hoc/
   - 5 & 10 Pillars: /Tenniskb-5 Pillars/ <-> /vi/Tenniskb-5 Pillars/ (including article.html?p=... params)
   - Site-wide fallbacks: /vi/... <-> /...
   ========================================================================= */

(function () {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  function getLangToggles() {
    return document.querySelectorAll('[data-lang-toggle], a.tu-nav-lang');
  }

  function isVietnamesePage(path) {
    var p = path || window.location.pathname;
    return /^\/?vi(\/|$)/i.test(p) || (document.documentElement && document.documentElement.lang === 'vi');
  }

  function getAuthoritativeAlternate(isVi) {
    var selector = isVi ? 'link[rel="alternate"][hreflang="en"]' : 'link[rel="alternate"][hreflang="vi"]';
    var alt = document.querySelector(selector);
    if (alt) {
      var href = alt.getAttribute('href');
      // Only trust root-relative or full http(s) URLs from <link rel="alternate">
      if (href && (href.charAt(0) === '/' || /^https?:\/\//i.test(href))) {
        return href.replace(/^https?:\/\/[^\/]+/i, '');
      }
    }
    return null;
  }

  function buildTargetUrl(currentPath, currentSearch) {
    currentPath = currentPath || window.location.pathname;
    currentSearch = (currentSearch !== undefined) ? currentSearch : window.location.search;
    var isVi = isVietnamesePage(currentPath);

    // 1. Authoritative <link rel="alternate"> if present on article pages
    var alt = getAuthoritativeAlternate(isVi);
    if (alt) {
      return alt;
    }

    // 2. Individual Article Pages (200 Articles): EN-xxx <-> VI-xxx
    var mEn = currentPath.match(/^(?:\/en)?\/articles\/EN-(.*)$/i);
    if (mEn) {
      return '/vi/articles/VI-' + mEn[1];
    }
    var mVi = currentPath.match(/^\/vi\/articles\/VI-(.*)$/i);
    if (mVi) {
      return '/en/articles/EN-' + mVi[1];
    }

    // 3. Pillar Taxonomy Categories in Articles
    var pillarEnToVi = {
      'biomechanics': 'co-sinh-hoc',
      'neuro-athletics': 'than-kinh',
      'stroke-mechanics': 'cu-danh',
      'tactics': 'chien-thuat',
      'conditioning': 'the-luc'
    };
    var pillarViToEn = {
      'co-sinh-hoc': 'biomechanics',
      'than-kinh': 'neuro-athletics',
      'cu-danh': 'stroke-mechanics',
      'chien-thuat': 'tactics',
      'the-luc': 'conditioning'
    };

    for (var pen in pillarEnToVi) {
      if (currentPath.indexOf('/articles/' + pen) !== -1) {
        return '/vi/articles/' + pillarEnToVi[pen] + '/';
      }
    }
    for (var pvi in pillarViToEn) {
      if (currentPath.indexOf('/vi/articles/' + pvi) !== -1) {
        return '/en/articles/' + pillarViToEn[pvi] + '/';
      }
    }

    // 4. Articles Catalog Main Index
    if (/^\/(?:en\/)?articles\/?$/i.test(currentPath)) {
      return '/vi/articles/';
    }
    if (/^\/vi\/articles\/?$/i.test(currentPath)) {
      return '/en/articles/';
    }

    // 5. 5 Pillars & 10 Pillars Knowledge Bases
    var pillars = ['Tenniskb-5 Pillars', 'Tenniskb-10 Pillars'];
    for (var i = 0; i < pillars.length; i++) {
      var pName = pillars[i];
      if (currentPath.indexOf('/vi/' + pName) !== -1) {
        var enPath = currentPath.replace('/vi/' + pName, '/' + pName);
        var enSearch = currentSearch.replace(/_VN\.md/gi, '_EN.md').replace(/lang=vi/gi, 'lang=en');
        return enPath + enSearch;
      }
      if (currentPath.indexOf('/' + pName) !== -1) {
        var viPath = currentPath.replace('/' + pName, '/vi/' + pName);
        var viSearch = currentSearch.replace(/_EN\.md/gi, '_VN.md').replace(/lang=en/gi, 'lang=vi');
        return viPath + viSearch;
      }
    }

    // 6. General Site Fallback
    var path = currentPath.replace(/^\//, '');
    if (/^vi(\/|$)/i.test(path)) {
      var enFallback = path.replace(/^vi\/?/i, '');
      return '/' + enFallback;
    } else {
      if (path === '' || path === '/') {
        return '/vi/';
      }
      return '/vi/' + path;
    }
  }

  function updateToggleElements() {
    var toggles = getLangToggles();
    if (!toggles || toggles.length === 0) return;

    var currentPath = window.location.pathname;
    var target = buildTargetUrl(currentPath, window.location.search);
    var isVi = isVietnamesePage(currentPath);

    toggles.forEach(function (toggle) {
      toggle.setAttribute('href', target);
      var textEl = toggle.querySelector('.tu-nav-text');
      if (textEl) {
        textEl.textContent = isVi ? 'EN' : 'VI';
      }
      toggle.setAttribute('title', isVi ? 'Switch to English' : 'Chuyển sang Tiếng Việt');
    });

    // Also update any MkDocs header dropdown language links if present
    var targetLang = isVi ? 'en' : 'vi';
    var selectLinks = document.querySelectorAll('.md-select__link[hreflang="' + targetLang + '"]');
    selectLinks.forEach(function (link) {
      link.setAttribute('href', target);
    });
  }

  function init() {
    updateToggleElements();

    // Capture-phase click listener to guarantee latest dynamic target on click
    document.addEventListener('click', function (e) {
      var toggle = e.target && e.target.closest && e.target.closest('[data-lang-toggle], a.tu-nav-lang, .md-select__link');
      if (toggle) {
        var target = buildTargetUrl(window.location.pathname, window.location.search);
        if (target) {
          toggle.setAttribute('href', target);
        }
      }
    }, true);

    // Watch for dynamic head updates (e.g. single-page doc navigation)
    if (window.MutationObserver && document.head) {
      var observer = new MutationObserver(function () {
        updateToggleElements();
      });
      observer.observe(document.head, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
