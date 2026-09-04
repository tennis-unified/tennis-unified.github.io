/* =========================================================================
   Tennis Unified — Dark Mode Toggle
   - Reads saved preference from localStorage
   - Falls back to prefers-color-scheme: dark for first-time visitors
   - Toggles data-theme on <html> + data-md-color-scheme on <body>
   - Updates button label/emoji to reflect current state
   ========================================================================= */

(function () {
  'use strict';

  var STORAGE_KEY = 'tu-darkmode';

  function getInitialTheme() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'dark' || saved === 'light') return saved;
    } catch (e) { /* localStorage may be blocked */ }
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
    // Material's color scheme attribute is set on <body> after DOM is ready.
    var body = document.body;
    if (body) {
      body.setAttribute('data-md-color-scheme', theme === 'dark' ? 'slate' : 'default');
    }
  }

  function updateButton(theme) {
    var btn = document.querySelector('.tu-nav-darkmode');
    if (!btn) return;
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
  }

  // PRE-PAINT: this runs immediately when the script loads. If the script
  // is placed in <head> BEFORE the <link rel="stylesheet"> tags, this
  // sets data-theme before any body content paints, preventing flash.
  var initialTheme = getInitialTheme();
  applyTheme(initialTheme);

  // Click handler + button state — runs after DOM is parsed so the button exists.
  function init() {
    // Re-apply on body now that it exists (handles Material's data-md-color-scheme)
    applyTheme(initialTheme);
    updateButton(initialTheme);

    var btn = document.querySelector('.tu-nav-darkmode');
    if (btn) {
      btn.addEventListener('click', function () {
        var current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        var next = current === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* ignore */ }
        applyTheme(next);
        updateButton(next);
      });
    }

    // Track system preference changes for users who haven't picked manually
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
      else if (mq.addListener) mq.addListener(mqHandler); // older Safari
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
