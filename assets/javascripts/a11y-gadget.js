/* =========================================================================
   Accessibility Gadget — Tennis Unified
   Vanilla JS, no dependencies. Builds the floating toggle + panel, persists
   user preferences to localStorage under 'a11y-gadget-settings', and applies
   state via classes on <html>.
   ========================================================================= */
(function () {
  'use strict';

  var STORAGE_KEY = 'a11y-gadget-settings';
  var VERSION = 1;

  var DEFAULTS = {
    fontSize: 2,        // 1..4
    contrast: 'default', // 'default' | 'high' | 'dark' | 'sepia'
    underlineLinks: false,
    highlightHeadings: false,
    reduceMotion: false,
    isOpen: false
  };

  var FONT_SIZE_LABELS = { 1: 'A-', 2: 'A', 3: 'A+', 4: 'A++' };

  var CONTRAST_LABELS = {
    default: 'Default',
    high:    'High Contrast',
    dark:    'Dark',
    sepia:   'Sepia'
  };

  function loadSettings() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return Object.assign({}, DEFAULTS);
      var parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== 'object') return Object.assign({}, DEFAULTS);
      if (parsed.__v !== VERSION) return Object.assign({}, DEFAULTS);
      // Merge with defaults so missing keys default
      var merged = Object.assign({}, DEFAULTS, parsed);
      // Validate fields
      merged.fontSize   = Math.min(4, Math.max(1, parseInt(merged.fontSize, 10) || 2));
      merged.contrast   = CONTRAST_LABELS[merged.contrast] ? merged.contrast : 'default';
      merged.underlineLinks = !!merged.underlineLinks;
      merged.highlightHeadings = !!merged.highlightHeadings;
      merged.reduceMotion = !!merged.reduceMotion;
      merged.isOpen = !!merged.isOpen;
      return merged;
    } catch (err) {
      return Object.assign({}, DEFAULTS);
    }
  }

  function saveSettings(s) {
    try {
      var toSave = Object.assign({ __v: VERSION }, s);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
    } catch (err) {
      /* ignore quota errors */
    }
  }

  function applySettings(s) {
    var html = document.documentElement;

    // --- Font size ---
    html.classList.remove('a11y-fontsize-1', 'a11y-fontsize-2', 'a11y-fontsize-3', 'a11y-fontsize-4');
    html.classList.add('a11y-fontsize-' + s.fontSize);

    // --- Contrast ---
    html.classList.remove('a11y-contrast-high', 'a11y-contrast-dark', 'a11y-contrast-sepia');
    if (s.contrast && s.contrast !== 'default') {
      html.classList.add('a11y-contrast-' + s.contrast);
    }

    // --- Underline links ---
    html.classList.toggle('a11y-underline-links', !!s.underlineLinks);

    // --- Highlight headings ---
    html.classList.toggle('a11y-highlight-headings', !!s.highlightHeadings);

    // --- Reduce motion ---
    html.classList.toggle('a11y-reduce-motion', !!s.reduceMotion);

    // --- Panel open state ---
    var root = document.getElementById('a11y-gadget');
    if (root) root.classList.toggle('is-open', !!s.isOpen);

    // --- Reflect state in form controls ---
    syncControls(s);
  }

  function syncControls(s) {
    var root = document.getElementById('a11y-gadget');
    if (!root) return;
    // Font size buttons
    var sizeBtns = root.querySelectorAll('[data-a11y-action="set-fontsize"]');
    sizeBtns.forEach(function (btn) {
      var v = parseInt(btn.getAttribute('data-a11y-value'), 10);
      btn.setAttribute('aria-pressed', v === s.fontSize ? 'true' : 'false');
    });
    // Contrast buttons
    var contrastBtns = root.querySelectorAll('[data-a11y-action="set-contrast"]');
    contrastBtns.forEach(function (btn) {
      var v = btn.getAttribute('data-a11y-value');
      btn.setAttribute('aria-pressed', v === s.contrast ? 'true' : 'false');
    });
    // Toggles
    setSwitch(root, 'a11y-underline-links-toggle', s.underlineLinks);
    setSwitch(root, 'a11y-highlight-headings-toggle', s.highlightHeadings);
    setSwitch(root, 'a11y-reduce-motion-toggle', s.reduceMotion);
  }

  function setSwitch(root, id, on) {
    var el = root.querySelector('#' + id);
    if (!el) return;
    el.checked = !!on;
    el.setAttribute('aria-checked', on ? 'true' : 'false');
  }

  function update(patch) {
    var s = loadSettings();
    Object.keys(patch).forEach(function (k) { s[k] = patch[k]; });
    saveSettings(s);
    applySettings(s);
  }

  function buildPanelHTML(s) {
    var sizeBtns = [1, 2, 3, 4].map(function (v) {
      var pressed = v === s.fontSize ? 'true' : 'false';
      return '<button type="button" class="a11y-btn" data-a11y-action="set-fontsize" ' +
             'data-a11y-value="' + v + '" aria-pressed="' + pressed + '" ' +
             'aria-label="Font size ' + FONT_SIZE_LABELS[v] + '">' +
             FONT_SIZE_LABELS[v] + '</button>';
    }).join('');

    var contrastBtns = ['default', 'high', 'dark', 'sepia'].map(function (v) {
      var pressed = v === s.contrast ? 'true' : 'false';
      return '<button type="button" class="a11y-btn" data-a11y-action="set-contrast" ' +
             'data-a11y-value="' + v + '" aria-pressed="' + pressed + '" ' +
             'aria-label="Contrast ' + CONTRAST_LABELS[v] + '">' +
             CONTRAST_LABELS[v] + '</button>';
    }).join('');

    var html = '' +
      '<div id="a11y-gadget" role="region" aria-label="Accessibility settings">' +
        '<button type="button" class="a11y-toggle" aria-expanded="' + (s.isOpen ? 'true' : 'false') + '" ' +
                'aria-controls="a11y-panel" aria-label="Open accessibility menu" title="Accessibility">' +
        '</button>' +
        '<div class="a11y-panel" id="a11y-panel" role="dialog" aria-label="Accessibility settings">' +
          '<h2>Accessibility</h2>' +
          '<p class="a11y-intro">Adjust how this site looks. Settings are saved on your device.</p>' +

          '<div class="a11y-row">' +
            '<span class="a11y-label" id="a11y-label-fontsize">Font size</span>' +
            '<div class="a11y-buttons" role="group" aria-labelledby="a11y-label-fontsize">' +
              sizeBtns +
            '</div>' +
          '</div>' +

          '<div class="a11y-row">' +
            '<span class="a11y-label" id="a11y-label-contrast">Contrast</span>' +
            '<div class="a11y-buttons" role="group" aria-labelledby="a11y-label-contrast">' +
              contrastBtns +
            '</div>' +
          '</div>' +

          '<div class="a11y-row a11y-toggle-row">' +
            '<label for="a11y-underline-links-toggle" class="a11y-label" style="margin-bottom:0;">Underline links</label>' +
            '<span class="a11y-switch">' +
              '<input type="checkbox" id="a11y-underline-links-toggle" role="switch" aria-label="Underline links">' +
              '<span class="a11y-slider" aria-hidden="true"></span>' +
            '</span>' +
          '</div>' +

          '<div class="a11y-row a11y-toggle-row">' +
            '<label for="a11y-highlight-headings-toggle" class="a11y-label" style="margin-bottom:0;">Highlight headings</label>' +
            '<span class="a11y-switch">' +
              '<input type="checkbox" id="a11y-highlight-headings-toggle" role="switch" aria-label="Highlight headings">' +
              '<span class="a11y-slider" aria-hidden="true"></span>' +
            '</span>' +
          '</div>' +

          '<div class="a11y-row a11y-toggle-row">' +
            '<label for="a11y-reduce-motion-toggle" class="a11y-label" style="margin-bottom:0;">Reduce motion</label>' +
            '<span class="a11y-switch">' +
              '<input type="checkbox" id="a11y-reduce-motion-toggle" role="switch" aria-label="Reduce motion">' +
              '<span class="a11y-slider" aria-hidden="true"></span>' +
            '</span>' +
          '</div>' +

          '<button type="button" class="a11y-reset" data-a11y-action="reset">Reset all settings</button>' +
        '</div>' +
      '</div>';

    return html;
  }

  function insertSkipLink() {
    if (document.querySelector('.a11y-skip-link')) return;
    var link = document.createElement('a');
    link.href = '#main-content, main, .md-content, .md-main';
    link.className = 'a11y-skip-link';
    link.textContent = 'Skip to main content';
    document.body.insertBefore(link, document.body.firstChild);
  }

  function attachEventHandlers(root) {
    // Toggle button
    root.querySelector('.a11y-toggle').addEventListener('click', function () {
      var s = loadSettings();
      update({ isOpen: !s.isOpen });
      var toggle = root.querySelector('.a11y-toggle');
      toggle.setAttribute('aria-expanded', s.isOpen ? 'true' : 'false');
    });

    // Font size buttons (event delegation)
    root.addEventListener('click', function (e) {
      var t = e.target.closest('[data-a11y-action]');
      if (!t) return;
      var action = t.getAttribute('data-a11y-action');
      var value = t.getAttribute('data-a11y-value');
      if (action === 'set-fontsize') {
        update({ fontSize: parseInt(value, 10) });
      } else if (action === 'set-contrast') {
        update({ contrast: value });
      } else if (action === 'reset') {
        try { localStorage.removeItem(STORAGE_KEY); } catch (err) {}
        applySettings(Object.assign({}, DEFAULTS));
      }
    });

    // Switches
    var underlineEl = root.querySelector('#a11y-underline-links-toggle');
    underlineEl.addEventListener('change', function () {
      update({ underlineLinks: underlineEl.checked });
    });

    var headingEl = root.querySelector('#a11y-highlight-headings-toggle');
    headingEl.addEventListener('change', function () {
      update({ highlightHeadings: headingEl.checked });
    });

    var motionEl = root.querySelector('#a11y-reduce-motion-toggle');
    motionEl.addEventListener('change', function () {
      update({ reduceMotion: motionEl.checked });
    });

    // Close panel when clicking outside
    document.addEventListener('click', function (e) {
      var s = loadSettings();
      if (!s.isOpen) return;
      if (root.contains(e.target)) return;
      update({ isOpen: false });
      root.querySelector('.a11y-toggle').setAttribute('aria-expanded', 'false');
    });

    // Escape key closes the panel
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var s = loadSettings();
        if (s.isOpen) {
          update({ isOpen: false });
          root.querySelector('.a11y-toggle').setAttribute('aria-expanded', 'false');
          root.querySelector('.a11y-toggle').focus();
        }
      }
    });
  }

  function init() {
    insertSkipLink();
    var s = loadSettings();
    // Mount gadget UI
    var mount = document.createElement('div');
    mount.innerHTML = buildPanelHTML(s);
    var root = mount.firstChild;
    document.body.appendChild(root);
    attachEventHandlers(root);
    applySettings(s);
  }

  // Boot when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
