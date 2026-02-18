/**
 * Interactive career quiz – one-question-at-a-time wizard, option animations,
 * smooth progress, and micro-interactions.
 */
(function() {
  'use strict';

  var form = document.getElementById('quiz-form');
  var total = parseInt(document.body.dataset.quizTotal || '0', 10);
  var wizardMode = document.body.classList.contains('quiz-wizard-mode');

  function initProgress() {
    var fill = document.getElementById('quiz-progress-fill');
    var text = document.getElementById('quiz-progress-text');
    if (!form || !fill || !text) return;

    var submitBtn = form.querySelector('.quiz-submit-btn');
    function update() {
      var answered = form.querySelectorAll('input[type="radio"]:checked').length;
      var pct = total > 0 ? Math.round((answered / total) * 100) : 0;
      fill.style.width = pct + '%';
      text.textContent = answered + ' of ' + total;
      if (submitBtn) submitBtn.classList.toggle('is-ready', answered === total);
    }
    form.addEventListener('change', update);
    update();
  }

  function initOptionCards() {
    var options = document.querySelectorAll('.quiz-option');
    options.forEach(function(label) {
      var input = label.querySelector('input[type="radio"]');
      if (!input) return;

      function select() {
        options.forEach(function(opt) { opt.classList.remove('is-selected'); });
        label.classList.add('is-selected');
        if (wizardMode) {
          var fieldset = label.closest('fieldset');
          if (fieldset) {
            setTimeout(function() {
              fieldset.classList.add('answered');
              var next = fieldset.nextElementSibling;
              if (next && next.matches('fieldset')) {
                next.classList.add('next-reveal');
                next.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }, 300);
          }
        }
      }

      label.addEventListener('click', function(e) {
        if (e.target === input) return;
        select();
      });
      input.addEventListener('change', select);
      if (input.checked) label.classList.add('is-selected');
    });
  }

  function initWizardMode() {
    if (!form || !wizardMode) return;

    var questions = form.querySelectorAll('fieldset.quiz-question');
    if (questions.length === 0) return;

    questions.forEach(function(q, i) {
      if (i > 0) q.classList.add('quiz-question-hidden');
    });

    questions.forEach(function(q) {
      var answered = q.querySelector('input[type="radio"]:checked');
      if (answered) {
        q.classList.remove('quiz-question-hidden');
        q.classList.add('answered');
        var idx = Array.prototype.indexOf.call(questions, q);
        for (var j = 0; j <= idx; j++) questions[j].classList.remove('quiz-question-hidden');
      }
    });
  }

  function init() {
    initProgress();
    initOptionCards();
    initWizardMode();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
