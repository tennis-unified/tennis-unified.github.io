/* =========================================================================
   court-diagram.js
   Bộ điều khiển tooltip dùng chung cho mọi sơ đồ chiến thuật SVG.
   Đọc dữ liệu từ thuộc tính data-tt-* trên các phần tử .ball-path và
   .player-marker, hiển thị hộp tooltip HTML định vị theo con trỏ / phím Tab.

   Cách nhúng (đặt sau khi các SVG đã có trong DOM):
     <script src="/assets/js/court-diagram.js"></script>

   Thuộc tính dữ liệu hỗ trợ trên mỗi phần tử có class "ball-path" hoặc
   "player-marker":
     data-tt-title   : tiêu đề hộp tooltip
     data-tt-speed   : tốc độ bóng (ví dụ "95 km/h")
     data-tt-depth   : độ sâu cú đánh (ví dụ "Sâu, cách baseline 0.5m")
     data-tt-angle   : góc mở (ví dụ "Chéo sân, góc 28°")
     data-tt-note    : ghi chú chiến thuật ngắn (tuỳ chọn)
   ========================================================================= */
(function () {
  "use strict";

  function initCourtDiagrams(root) {
    root = root || document;

    let tooltip = document.querySelector(".cd-tooltip");
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.className = "cd-tooltip";
      tooltip.setAttribute("role", "tooltip");
      document.body.appendChild(tooltip);
    }

    function buildTooltipHTML(el) {
      const title = el.getAttribute("data-tt-title");
      const speed = el.getAttribute("data-tt-speed");
      const depth = el.getAttribute("data-tt-depth");
      const angle = el.getAttribute("data-tt-angle");
      const note = el.getAttribute("data-tt-note");
      if (!title && !speed && !depth && !angle && !note) return null;

      let html = "";
      if (title) html += `<strong>${title}</strong>`;
      if (speed) html += `<div class="cd-tooltip-row"><span>Tốc độ</span><span>${speed}</span></div>`;
      if (depth) html += `<div class="cd-tooltip-row"><span>Độ sâu</span><span>${depth}</span></div>`;
      if (angle) html += `<div class="cd-tooltip-row"><span>Góc mở</span><span>${angle}</span></div>`;
      if (note) html += `<div style="margin-top:4px;">${note}</div>`;
      return html;
    }

    function showTooltip(el, clientX, clientY) {
      const html = buildTooltipHTML(el);
      if (!html) return;
      tooltip.innerHTML = html;
      tooltip.classList.add("visible");
      positionTooltip(clientX, clientY);
    }

    function positionTooltip(clientX, clientY) {
      const pad = 14;
      const rect = tooltip.getBoundingClientRect();
      let x = clientX + pad;
      let y = clientY + pad;
      if (x + rect.width > window.innerWidth - 8) x = clientX - rect.width - pad;
      if (y + rect.height > window.innerHeight - 8) y = clientY - rect.height - pad;
      tooltip.style.left = Math.max(8, x) + "px";
      tooltip.style.top = Math.max(8, y) + "px";
    }

    function hideTooltip() {
      tooltip.classList.remove("visible");
    }

    const targets = root.querySelectorAll(".ball-path, .player-marker");
    targets.forEach((el) => {
      if (el.dataset.ttBound) return;
      el.dataset.ttBound = "1";

      if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "0");

      el.addEventListener("mouseenter", (e) => showTooltip(el, e.clientX, e.clientY));
      el.addEventListener("mousemove", (e) => positionTooltip(e.clientX, e.clientY));
      el.addEventListener("mouseleave", hideTooltip);

      el.addEventListener("focus", () => {
        const box = el.getBoundingClientRect();
        showTooltip(el, box.left + box.width / 2, box.top);
      });
      el.addEventListener("blur", hideTooltip);
    });
  }

  document.addEventListener("DOMContentLoaded", () => initCourtDiagrams(document));

  // Cho phép gọi lại thủ công nếu sơ đồ được chèn động (ví dụ sau khi fetch nội dung chương).
  window.initCourtDiagrams = initCourtDiagrams;
})();
