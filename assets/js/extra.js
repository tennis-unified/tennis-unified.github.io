// Cross-language tab URL fix.
// The mkdocs-static-i18n plugin uses a single shared nav: across all language
// builds, so the cross-language tab's href is the same in both EN and VI.
// At runtime we detect the current language and rewrite the cross-link tab
// to point at the *other* language's site root.
(function () {
  function fixCrossLangTab() {
    var path = window.location.pathname;  // e.g. "/tenniskb/vi/..."
    var isVi = path.indexOf("/vi/") !== -1 || /\/vi(\/|$|\.)/.test(path);
    var crossLinks = document.querySelectorAll(".md-tabs__link[href*='tenniskb/'], .md-nav__link[href*='tenniskb/']");
    crossLinks.forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (isVi) {
        // Currently on VI site -> point cross-link to EN site
        if (href.indexOf("/vi/index.html") !== -1 || href.indexOf("/vi/") !== -1) {
          a.setAttribute("href", "https://henryphamduc.github.io/taichiknowledgebase/");
        }
      } else {
        // Currently on EN site (or root) -> point cross-link to VI site
        if (href.indexOf("/en/index.html") !== -1 || href.indexOf("/en/") !== -1) {
          a.setAttribute("href", "https://henryphamduc.github.io/tenniskb/vi/index.html");
        }
      }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixCrossLangTab);
  } else {
    fixCrossLangTab();
  }
})();

// Adjustable font-size control (A- / A / A+), persisted across pages via
// localStorage so the reading size follows the user from page to page.
(function () {
  var STORAGE_KEY = "tp-font-scale";
  var MIN = 0.8, MAX = 1.6, STEP = 0.1;

  function getScale() {
    var v = parseFloat(localStorage.getItem(STORAGE_KEY));
    return isNaN(v) ? 1 : v;
  }
  function applyScale(scale) {
    document.documentElement.style.setProperty("--tp-font-scale", scale);
  }
  function setScale(scale) {
    scale = Math.round(Math.min(MAX, Math.max(MIN, scale)) * 100) / 100;
    localStorage.setItem(STORAGE_KEY, scale);
    applyScale(scale);
  }

  function initFontControl() {
    applyScale(getScale());

    var wrap = document.createElement("div");
    wrap.className = "tp-font-control";
    wrap.setAttribute("role", "group");
    wrap.setAttribute("aria-label", "Adjust text size");

    var dec = document.createElement("button");
    dec.type = "button";
    dec.textContent = "A-";
    dec.setAttribute("aria-label", "Decrease text size");

    var reset = document.createElement("button");
    reset.type = "button";
    reset.textContent = "A";
    reset.setAttribute("aria-label", "Reset text size");

    var inc = document.createElement("button");
    inc.type = "button";
    inc.textContent = "A+";
    inc.setAttribute("aria-label", "Increase text size");

    dec.addEventListener("click", function () { setScale(getScale() - STEP); });
    reset.addEventListener("click", function () { setScale(1); });
    inc.addEventListener("click", function () { setScale(getScale() + STEP); });

    wrap.appendChild(dec);
    wrap.appendChild(reset);
    wrap.appendChild(inc);
    document.body.appendChild(wrap);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFontControl);
  } else {
    initFontControl();
  }
})();
