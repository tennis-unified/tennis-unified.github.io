/**
 * Tennis Unified - Universal Language Toggle Script
 * Dynamically switches between English and Vietnamese for any page.
 * Supports:
 * - Dynamic article renderer (Tenniskb-5 Pillars/article.html?p=...)
 * - Landing pages (Tenniskb-5 Pillars/ <-> vi/Tenniskb-5 Pillars/)
 * - Subcategory pillars (/en/articles/pillar/ <-> /vi/articles/tru-cot/)
 * - Static articles (/en/articles/EN-.../ <-> /vi/articles/VI-.../)
 * - Canonical <link rel="alternate"> overrides
 * - Fallback path-based translation
 */

(function () {
  'use strict';

  var pillarMapEnToVi = {
    'biomechanics': 'co-sinh-hoc',
    'neuro-athletics': 'than-kinh',
    'stroke-mechanics': 'cu-danh',
    'tactics': 'chien-thuat',
    'conditioning': 'the-luc'
  };

  var pillarMapViToEn = {
    'co-sinh-hoc': 'biomechanics',
    'than-kinh': 'neuro-athletics',
    'cu-danh': 'stroke-mechanics',
    'chien-thuat': 'tactics',
    'the-luc': 'conditioning'
  };

  function getLangToggles() {
    return document.querySelectorAll('[data-lang-toggle]');
  }

  function getAlternateUrl(targetLang) {
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + targetLang + '"]');
    if (alt && alt.getAttribute('href')) {
      return alt.getAttribute('href');
    }
    return null;
  }

  function buildTargetUrl(currentPath) {
    var rawPath = currentPath || window.location.pathname;
    var decodedPath = '';
    try {
      decodedPath = decodeURIComponent(rawPath);
    } catch (e) {
      decodedPath = rawPath;
    }
    var search = window.location.search || '';
    var isVi = /^\/?vi(\/|$)/i.test(decodedPath);
    var targetLang = isVi ? 'en' : 'vi';

    // 1. DYNAMIC ARTICLE RENDERER (Tenniskb-5 Pillars/article.html?p=...)
    if (decodedPath.indexOf('Tenniskb-5 Pillars') !== -1 || decodedPath.indexOf('article.html') !== -1) {
      var params = new URLSearchParams(search);
      var p = params.get('p');
      if (p) {
        if (isVi) {
          // VI -> EN: ART-xxx_..._VN.md -> ART-xxx_..._EN.md
          var enFile = p.replace(/_VN\.md$/i, '_EN.md').replace(/_vi\.md$/i, '_en.md');
          return '/Tenniskb-5 Pillars/article.html?p=' + encodeURIComponent(enFile) + '&lang=en';
        } else {
          // EN -> VI: ART-xxx_..._EN.md -> ART-xxx_..._VN.md
          var viFile = p.replace(/_EN\.md$/i, '_VN.md').replace(/_en\.md$/i, '_vi.md');
          return '/vi/Tenniskb-5 Pillars/article.html?p=' + encodeURIComponent(viFile) + '&lang=vi';
        }
      }
      // If on article.html without ?p=, default to ART-001
      if (/article\.html$/i.test(decodedPath)) {
        if (isVi) {
          return '/Tenniskb-5 Pillars/article.html?p=ART-001_GRF_TriPlanar_EN.md&lang=en';
        } else {
          return '/vi/Tenniskb-5 Pillars/article.html?p=ART-001_GRF_TriPlanar_VN.md&lang=vi';
        }
      }
      // Landing page of Tenniskb-5 Pillars
      if (/^\/?(en\/)?Tenniskb-5 Pillars\/?$/i.test(decodedPath)) {
        return '/vi/Tenniskb-5 Pillars/';
      }
      if (/^\/?vi\/Tenniskb-5 Pillars\/?$/i.test(decodedPath)) {
        return '/Tenniskb-5 Pillars/';
      }
    }

    // 2. PILLAR SUBCATEGORY MAPPING
    var enPillarMatch = decodedPath.match(/^\/?en\/articles\/([a-z0-9-]+)\/?$/i);
    if (enPillarMatch) {
      var enPillar = enPillarMatch[1].toLowerCase();
      if (pillarMapEnToVi[enPillar]) {
        return '/vi/articles/' + pillarMapEnToVi[enPillar] + '/';
      }
    }
    var viPillarMatch = decodedPath.match(/^\/?vi\/articles\/([a-z0-9-]+)\/?$/i);
    if (viPillarMatch) {
      var viPillar = viPillarMatch[1].toLowerCase();
      if (pillarMapViToEn[viPillar]) {
        return '/en/articles/' + pillarMapViToEn[viPillar] + '/';
      }
    }

    // 3. STATIC ARTICLES MAPPING
    var enArtMatch = decodedPath.match(/^\/?en\/articles\/(EN-[^\/]+)\/?$/i);
    if (enArtMatch) {
      var altSlug = enArtMatch[1].replace(/^EN-/i, 'VI-');
      return '/vi/articles/' + altSlug + '/';
    }
    var viArtMatch = decodedPath.match(/^\/?vi\/articles\/(VI-[^\/]+)\/?$/i);
    if (viArtMatch) {
      var altSlug = viArtMatch[1].replace(/^VI-/i, 'EN-');
      return '/en/articles/' + altSlug + '/';
    }

    // 4. CHECK <link rel="alternate"> (AUTHORITATIVE FOR STATIC PAGES)
    var alt = getAlternateUrl(targetLang);
    if (alt) {
      return alt;
    }

    // 5. GENERAL ROUTING FALLBACKS
    var path = decodedPath.replace(/^\//, '');

    if (isVi) {
      var enPath = path.replace(/^vi\//i, '').replace(/^vi$/i, '');
      return enPath ? '/' + enPath : '/';
    } else {
      if (path === '' || path === 'index.html') {
        return '/vi/';
      }
      var cleanPath = path.replace(/^en\//i, '');
      return '/vi/' + cleanPath;
    }
  }

  function attachToggle() {
    var currentPath = window.location.pathname;
    var decodedPath = '';
    try {
      decodedPath = decodeURIComponent(currentPath);
    } catch(e) {
      decodedPath = currentPath;
    }
    var isVi = /^\/?vi(\/|$)/i.test(decodedPath);
    var target = buildTargetUrl(currentPath);

    var toggles = getLangToggles();
    if (toggles && toggles.length > 0) {
      toggles.forEach(function (toggle) {
        toggle.setAttribute('href', target);
        var textEl = toggle.querySelector('.tu-nav-text');
        if (textEl) {
          textEl.textContent = isVi ? 'English' : 'Tiếng Việt';
        }
        toggle.setAttribute('title', isVi ? 'Switch to English' : 'Chuyển sang Tiếng Việt');
      });
    }

    // Also update any dropdown links with matching hreflang
    var targetLang = isVi ? 'en' : 'vi';
    var selectLinks = document.querySelectorAll('.md-select__link[hreflang="' + targetLang + '"]');
    selectLinks.forEach(function (link) {
      link.setAttribute('href', target);
    });
  }

  // Intercept click on any language toggle link in capture phase to guarantee latest dynamic parameters
  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('[data-lang-toggle], .md-select__link');
    if (!toggle) return;

    var currentPath = window.location.pathname;
    var dynamicTarget = buildTargetUrl(currentPath);
    if (dynamicTarget) {
      toggle.setAttribute('href', dynamicTarget);
    }
  }, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachToggle);
  } else {
    attachToggle();
  }
})();
