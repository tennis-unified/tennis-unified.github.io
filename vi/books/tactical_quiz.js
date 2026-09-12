/* =========================================================================
   tactical_quiz.js
   Interactive Quiz Runner for Tennis Scenario Decisions
   ========================================================================= */

(function() {
  "use strict";

  function initTacticalQuizzes(root) {
    root = root || document;
    const widgets = root.querySelectorAll('.tu-quiz-widget');

    widgets.forEach(widget => {
      if (widget.dataset.quizBound) return;
      widget.dataset.quizBound = "1";

      const options = widget.querySelectorAll('.tu-quiz-opt');
      const feedback = widget.querySelector('.tu-quiz-feedback');
      const resetBtn = widget.querySelector('.tu-quiz-reset-btn');

      options.forEach(opt => {
        opt.addEventListener('click', () => {
          if (opt.classList.contains('disabled')) return;

          const isCorrect = opt.dataset.correct === "true";
          const explanation = opt.dataset.explanation || "";

          // Mark all disabled
          options.forEach(o => o.classList.add('disabled'));

          if (isCorrect) {
            opt.classList.add('correct');
            feedback.className = 'tu-quiz-feedback show-correct';
            feedback.innerHTML = `<strong><i class="fa-solid fa-circle-check"></i> CHÍNH XÁC!</strong><br>${explanation}`;
          } else {
            opt.classList.add('incorrect');
            // Also reveal the correct one
            options.forEach(o => {
              if (o.dataset.correct === "true") o.classList.add('correct');
            });
            feedback.className = 'tu-quiz-feedback show-incorrect';
            feedback.innerHTML = `<strong><i class="fa-solid fa-circle-xmark"></i> CHƯA CHÍNH XÁC:</strong><br>${explanation}`;
          }
        });
      });

      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          options.forEach(o => {
            o.classList.remove('disabled', 'correct', 'incorrect');
          });
          feedback.className = 'tu-quiz-feedback';
          feedback.innerHTML = '';
        });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initTacticalQuizzes(document));
  } else {
    initTacticalQuizzes(document);
  }

  window.initTacticalQuizzes = initTacticalQuizzes;
})();
