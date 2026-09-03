/* =========================================================================
   Tennis Unified & TNKBGAP — Universal Dark Mode Toggle
   - Synchronizes:
     1. documentElement[data-theme="dark"]
     2. body[data-md-color-scheme="slate" | "default"]
     3. .tu-nav-darkmode buttons (☀️ Light Mode / 🌙 Dark Mode)
     4. MkDocs Material header palette toggle inputs & labels
     5. localStorage 'tu-darkmode'
     6. prefers-color-scheme media query
   ========================================================================= */

(function () {
  'use strict';

  var STORAGE_KEY = 'tu-darkmode';

  function getInitialTheme() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'dark' || saved === 'light') return saved;
    } catch (e) {}
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  function applyTheme(theme) {
    var html = document.documentElement;
    if (theme === 'dark') {
      html.setAttribute('data-theme', 'dark');
    } else {
      html.removeAttribute('data-theme');
    }

    var body = document.body;
    if (body) {
      body.setAttribute('data-md-color-scheme', theme === 'dark' ? 'slate' : 'default');
    }

    syncMaterialPalette(theme);
  }

  function syncMaterialPalette(theme) {
    var p0 = document.getElementById('__palette_0'); // light input
    var p1 = document.getElementById('__palette_1'); // dark input
    if (p0 && p1) {
      if (theme === 'dark') {
        p1.checked = true;
        p0.checked = false;
      } else {
        p0.checked = true;
        p1.checked = false;
      }
    }
    var l0 = document.querySelector('label[for="__palette_0"]'); // Switch to light
    var l1 = document.querySelector('label[for="__palette_1"]'); // Switch to dark
    if (l0 && l1) {
      if (theme === 'dark') {
        l0.removeAttribute('hidden');
        l0.style.display = 'inline-block';
        l1.setAttribute('hidden', '');
        l1.style.display = 'none';
      } else {
        l1.removeAttribute('hidden');
        l1.style.display = 'inline-block';
        l0.setAttribute('hidden', '');
        l0.style.display = 'none';
      }
    }
  }

  function updateButton(theme) {
    var btns = document.querySelectorAll('.tu-nav-darkmode');
    btns.forEach(function (btn) {
      var emoji = btn.querySelector('.tu-nav-emoji');
      var text = btn.querySelector('.tu-nav-text');
      if (theme === 'dark') {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        btn.setAttribute('title', 'Light Mode');
        if (emoji) emoji.textContent = '☀️';
        if (text) text.textContent = 'Light Mode';
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
        btn.setAttribute('title', 'Dark Mode');
        if (emoji) emoji.textContent = '🌙';
        if (text) text.textContent = 'Dark Mode';
      }
    });
  }

  // PRE-PAINT: set data-theme immediately on script load to prevent flash
  var initialTheme = getInitialTheme();
  applyTheme(initialTheme);

  function toggleTheme() {
    var current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    var next = current === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(STORAGE_KEY, next); } catch (e) {}
    applyTheme(next);
    updateButton(next);
  }

  function init() {
    applyTheme(initialTheme);
    updateButton(initialTheme);

    // Event delegation for .tu-nav-darkmode click
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.tu-nav-darkmode');
      if (btn) {
        e.preventDefault();
        toggleTheme();
      }
    });

    // Sync with Material palette icon clicks
    document.addEventListener('click', function (e) {
      var lbl = e.target.closest('label[for^="__palette_"]');
      if (lbl) {
        setTimeout(function () {
          var p1 = document.getElementById('__palette_1');
          var next = (p1 && p1.checked) ? 'dark' : 'light';
          try { localStorage.setItem(STORAGE_KEY, next); } catch (err) {}
          applyTheme(next);
          updateButton(next);
        }, 20);
      }
    });

    // Track system preference changes
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var mqHandler = function (e) {
        var saved;
        try { saved = localStorage.getItem(STORAGE_KEY); } catch (err) { saved = null; }
        if (saved !== 'dark' && saved !== 'light') {
          var sysTheme = e.matches ? 'dark' : 'light';
          applyTheme(sysTheme);
          updateButton(sysTheme);
        }
      };
      if (mq.addEventListener) mq.addEventListener('change', mqHandler);
      else if (mq.addListener) mq.addListener(mqHandler);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
