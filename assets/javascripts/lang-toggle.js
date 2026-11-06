/* =========================================================================
   Tennis Unified & TennisKB — Dynamic Language Toggle Script (v3)
   Switches dynamically between corresponding English and Vietnamese pages.

   Language detection is SEGMENT-AWARE: a page is Vietnamese iff one of its
   path segments is exactly "vi" (at any position), not only at the start.
   This fixes subtrees such as /tenniskb/vi/ <-> /tenniskb/en/ and
   /tnkb/vi/ <-> /tnkb/en/, where the language directory is nested.

   Priority when computing the counterpart URL:
     1. An explicit data-lang-href written on the element at build time
        (authoritative — overrides everything below).
     2. A <link rel="alternate" hreflang="..."> in <head>.
     3. A .md-select__link[hreflang="..."] written by MkDocs. This is the
        CURATED counterpart and may legitimately be a sibling article when
        no 1:1 translation exists. v2 clobbered it with a computed URL.
     4. Article / pillar heuristics.
     5. General SEGMENT-AWARE swap:
          - /vi/x           <-> /x
          - /en/x           <-> /vi/x
          - /tenniskb/vi/x  <-> /tenniskb/en/x (nested directory swap)
          - /<section>/x    -> /vi/<section>/x (MAIN SITE, root prefix)
          - /tenniskb/x     -> /tenniskb/vi/x  (nested subtrees only)

   v3 fixes the 404 class: v2's step 7 spliced "vi" at segment 2 for EVERY
   main-site page, producing /fundamentals/vi/footwork/<slug>/ (404). The
   main site uses the ROOT-PREFIXED /vi/... form; only /tenniskb/ and /tnkb/
   use the nested form. A HEAD-probe guard also walks computed targets up to
   the nearest existing ancestor, so an unauthored target can never land the
   reader on a 404. Authored targets (steps 1-3) are trusted and are not
   probed, so the common case has no extra network round-trip.
   ========================================================================= */

(function () {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  var LANG_SEG = /^(vi|en)$/i;
  var NESTED_ROOTS = { 'tenniskb': 1, 'tnkb': 1 };

  var pillarEnToVi = {
    'biomechanics': 'co-sinh-hoc',
    'neuro-athletics': 'than-kinh',
    'stroke-mechanics': 'cu-danh',
    'tactics': 'chien-thuat',
    'conditioning': 'the-luc'
  };
  var pillarViToEn = {};
  for (var pk in pillarEnToVi) {
    if (Object.prototype.hasOwnProperty.call(pillarEnToVi, pk)) {
      pillarViToEn[pillarEnToVi[pk]] = pk;
    }
  }

  function getLangToggles() {
    return document.querySelectorAll('[data-lang-toggle], a.tu-nav-lang');
  }

  // Index of a path segment that is exactly 'vi' or 'en' (any position), else -1.
  function langSegmentIndex(path) {
    var parts = path.split('/');
    for (var i = 0; i < parts.length; i++) {
      if (LANG_SEG.test(parts[i])) return i;
    }
    return -1;
  }

  function isVietnamesePath(path) {
    var i = langSegmentIndex(path);
    if (i !== -1) return /^vi$/i.test(path.split('/')[i]);
    return false;
  }

  // Authoritative, build-time target written on the element itself.
  function getExplicitTarget(el) {
    var h = el.getAttribute('data-lang-href');
    if (h && (h.charAt(0) === '/' || /^https?:\/\//i.test(h))) {
      return h.replace(/^https?:\/\/[^\/]+/i, '');
    }
    return null;
  }

  // Resolve any authored href to an absolute pathname. Rejects MkDocs'
  // href="./" self-links, which are NOT language counterparts.
  function toPath(href) {
    if (!href) return null;
    var p;
    if (/^https?:\/\//i.test(href)) p = href.replace(/^https?:\/\/[^\/]+/i, '');
    else if (href.charAt(0) === '/') p = href;
    else {
      try { p = new URL(href, window.location.href).pathname; }
      catch (e) { return null; }
    }
    if (!p) return null;
    p = p.split('#')[0].split('?')[0] || '/';
    if (p === window.location.pathname) return null;
    return p;
  }

  function resolveAlt(lang) {
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
    return alt ? toPath(alt.getAttribute('href')) : null;
  }

  // MkDocs writes the curated counterpart into the header language selector.
  // It is the ONLY correct source for pages with no 1:1 translation.
  function resolveSelectAlt(lang) {
    var links = document.querySelectorAll('.md-select__link[hreflang="' + lang + '"]');
    for (var i = 0; i < links.length; i++) {
      var p = toPath(links[i].getAttribute('href'));
      if (p) return p;
    }
    return null;
  }

  function computeTarget(currentPath, currentSearch) {
    currentPath = currentPath || window.location.pathname;
    currentSearch = (currentSearch !== undefined) ? currentSearch : window.location.search;
    var lang = isVietnamesePath(currentPath) ? 'en' : 'vi';

    // 1-2. Authoritative <link rel="alternate" hreflang> if present.
    var alt = resolveAlt(lang);
    if (alt) return { url: alt, authored: true };

    // 3. Curated MkDocs language selector (v2 used to OVERWRITE this).
    var sel = resolveSelectAlt(lang);
    if (sel) return { url: sel, authored: true };

    // 4. Individual Article Pages (200 Articles): EN-xxx <-> VI-xxx
    var mEn = currentPath.match(/^(?:\/en)?\/articles\/EN-(.*)$/i);
    if (mEn) return { url: '/vi/articles/VI-' + mEn[1], authored: false };
    var mVi = currentPath.match(/^\/vi\/articles\/VI-(.*)$/i);
    if (mVi) return { url: '/en/articles/EN-' + mVi[1], authored: false };

    // 5. Pillar Taxonomy Categories in Articles
    for (var pen in pillarEnToVi) {
      if (Object.prototype.hasOwnProperty.call(pillarEnToVi, pen) &&
          currentPath.indexOf('/articles/' + pen) !== -1) {
        return { url: '/vi/articles/' + pillarEnToVi[pen] + '/', authored: false };
      }
    }
    for (var pvi in pillarViToEn) {
      if (Object.prototype.hasOwnProperty.call(pillarViToEn, pvi) &&
          currentPath.indexOf('/vi/articles/' + pvi) !== -1) {
        return { url: '/en/articles/' + pillarViToEn[pvi] + '/', authored: false };
      }
    }

    // 6. Articles Catalog Main Index
    if (/^\/(?:en\/)?articles\/?$/i.test(currentPath)) {
      return { url: '/vi/articles/', authored: false };
    }
    if (/^\/vi\/articles\/?$/i.test(currentPath)) {
      return { url: '/en/articles/', authored: false };
    }

    // 7. 5 Pillars & 10 Pillars Knowledge Bases
    var pillars = ['Tenniskb-5 Pillars', 'Tenniskb-10 Pillars'];
    for (var p = 0; p < pillars.length; p++) {
      var pName = pillars[p];
      if (currentPath.indexOf('/vi/' + pName) !== -1) {
        var enPath = currentPath.replace('/vi/' + pName, '/' + pName);
        var enSearch = currentSearch.replace(/_VN\.md/gi, '_EN.md').replace(/lang=vi/gi, 'lang=en');
        return { url: enPath + enSearch, authored: false };
      }
      if (currentPath.indexOf('/' + pName) !== -1) {
        var viPath = currentPath.replace('/' + pName, '/vi/' + pName);
        var viSearch = currentSearch.replace(/_EN\.md/gi, '_VN.md').replace(/lang=en/gi, 'lang=vi');
        return { url: viPath + viSearch, authored: false };
      }
    }

    // 8. General fallback — SEGMENT-AWARE swap (fixes /tenniskb/vi/ etc.)
    var parts = currentPath.split('/');
    var idx = langSegmentIndex(currentPath);
    if (idx !== -1) {
      var cur = parts[idx].toLowerCase();
      // A language segment at index 1 means a ROOT-LEVEL prefix (/vi/x, /en/x).
      if (idx === 1) {
        if (cur === 'vi') {
          return { url: '/' + parts.slice(2).join('/'), authored: false };
        }
        parts[1] = 'vi';
        return { url: parts.join('/'), authored: false };
      }
      parts[idx] = (cur === 'vi') ? 'en' : 'vi';
      return { url: parts.join('/'), authored: false };
    }

    // 9. No language segment -> treat as EN.
    if (currentPath === '/' || currentPath === '') {
      return { url: '/vi/', authored: false };
    }
    var root = (parts[1] || '').toLowerCase();
    if (NESTED_ROOTS[root]) {
      var nested = parts.slice();
      nested.splice(2, 0, 'vi');           // /tenniskb/x -> /tenniskb/vi/x
      return { url: nested.join('/'), authored: false };
    }
    // MAIN SITE: root-prefixed. v2 produced /<section>/vi/... -> 404.
    return { url: '/vi' + currentPath, authored: false };
  }

  // ---- existence guard for computed (unauthored) targets ----------------
  var state = {
    path: null, url: null, authored: false, verified: null, pending: null
  };

  function ancestorCandidates(p) {
    var clean = (p || '').split('#')[0].split('?')[0];
    var segs = clean.split('/').filter(function (s) { return s.length > 0; });
    var out = [clean];
    for (var i = segs.length; i >= 1; i--) {
      var c = '/' + segs.slice(0, i).join('/') + '/';
      if (out.indexOf(c) === -1) out.push(c);
    }
    if (out.indexOf('/') === -1) out.push('/');
    return out;
  }

  function probe(list, i, done) {
    if (i >= list.length) return done(list[0]);
    var c = list[i];
    fetch(c, { method: 'HEAD', credentials: 'same-origin' })
      .then(function (r) {
        if (r.ok) done(c);
        else probe(list, i + 1, done);
      })
      .catch(function () { probe(list, i + 1, done); });
  }

  function verify(url) {
    if (!url || state.authored || typeof window.fetch !== 'function') {
      return Promise.resolve(url);
    }
    var list = ancestorCandidates(url);
    return new Promise(function (resolve) {
      var settled = false;
      var timer = setTimeout(function () {
        if (!settled) { settled = true; resolve(url); }
      }, 2500);
      probe(list, 0, function (good) {
        if (!settled) {
          settled = true;
          clearTimeout(timer);
          resolve(good);
        }
      });
    });
  }

  function applyHref(url) {
    if (!url) return;
    var isVi = isVietnamesePath(window.location.pathname);
    var toggles = getLangToggles();
    for (var i = 0; i < toggles.length; i++) {
      var el = toggles[i];
      el.setAttribute('href', getExplicitTarget(el) || url);
      var textEl = el.querySelector('.tu-nav-text');
      if (textEl) textEl.textContent = isVi ? 'EN' : 'VI';
      el.setAttribute('title', isVi ? 'Switch to English' : 'Chuyển sang Tiếng Việt');
    }

    // Never clobber a valid authored MkDocs selector link; only repair
    // selector links that are empty or self-referential (href="./").
    var targetLang = isVi ? 'en' : 'vi';
    var selectLinks = document.querySelectorAll(
      '.md-select__link[hreflang="' + targetLang + '"]');
    for (var j = 0; j < selectLinks.length; j++) {
      if (!toPath(selectLinks[j].getAttribute('href'))) {
        selectLinks[j].setAttribute('href', url);
      }
    }
  }

  function updateToggleElements() {
    if (state.path === window.location.pathname && state.url) {
      applyHref(state.verified || state.url);
      return;
    }
    state.path = window.location.pathname;
    state.verified = null;
    state.pending = null;
    var t = computeTarget(state.path, window.location.search);
    state.url = t.url;
    state.authored = t.authored;
    applyHref(state.url);
    if (!state.authored && state.url) {
      state.pending = verify(state.url).then(function (good) {
        state.verified = good;
        if (good !== state.url) applyHref(good);
        return good;
      });
    } else {
      state.verified = state.url;
    }
  }

  function init() {
    updateToggleElements();

    // Capture-phase click listener: if verification is still in flight, wait
    // for it rather than navigating to an unchecked (possibly 404) URL.
    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey ||
          e.ctrlKey || e.shiftKey || e.altKey) return;
      var el = e.target && e.target.closest && e.target.closest(
        '[data-lang-toggle], a.tu-nav-lang, .md-select__link');
      if (!el) return;
      var explicit = getExplicitTarget(el);
      if (explicit) {
        el.setAttribute('href', explicit);
        return;
      }
      // Authored MkDocs selector links are already correct — leave them alone.
      if (el.classList && el.classList.contains('md-select__link') &&
          toPath(el.getAttribute('href'))) return;
      if (state.verified) {
        el.setAttribute('href', state.verified);
        return;
      }
      if (!state.pending) return;
      e.preventDefault();
      state.pending.then(function () {
        window.location.assign(state.verified || state.url);
      });
    }, true);

    // Watch for dynamic head updates (e.g. single-page doc navigation).
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
