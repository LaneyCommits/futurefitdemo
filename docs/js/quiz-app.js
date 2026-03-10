/**
 * Quiz app: multi-step flow for GitHub Pages static site.
 * Updated to match the ExploringU design system (gradient hero, modern cards, reveal animations).
 */
(function() {
  var app = document.getElementById('quiz-app');
  if (!app) return;

  var state = {
    step: 'length',
    quizShort: null,
    path: null,
    majorKey: null,
    majorLabel: null,
    answers: [],
    fromExploreMajor: null
  };

  function render() {
    if (state.step === 'length') renderLength();
    else if (state.step === 'path') renderPath();
    else if (state.step === 'major') renderMajor();
    else if (state.step === 'questions') renderQuestions();
    else if (state.step === 'results') renderResults();
  }

  function triggerReveal() {
    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  }

  function renderLength() {
    app.innerHTML =
      '<section class="block block--hero block--hero-with-bg quiz-hero">' +
        '<div class="block-inner">' +
          '<p class="hero-badge">3–7 minutes · free · no sign-up</p>' +
          '<h1 class="block-hero-title">Career Discovery Quiz</h1>' +
          '<p class="block-hero-sub">Find careers that match your personality, interests, and strengths — not just what\'s trending. Pick a quiz length to get started.</p>' +
        '</div>' +
      '</section>' +
      '<section class="block quiz-choices-section">' +
        '<div class="block-inner">' +
          '<h2 class="quiz-choices-heading reveal">How much time do you have?</h2>' +
          '<div class="quiz-choice-cards">' +
            '<div class="quiz-choice-card reveal" data-length="short">' +
              '<div class="quiz-choice-icon">⏱</div>' +
              '<h3 class="quiz-choice-title">Short quiz</h3>' +
              '<p class="quiz-choice-time">~3 minutes · 10 questions</p>' +
              '<p class="quiz-choice-desc">A fast snapshot of your career interests. Great if you\'re curious but short on time.</p>' +
              '<span class="quiz-choice-cta">Start short quiz <span class="btn-arrow" aria-hidden="true">→</span></span>' +
            '</div>' +
            '<div class="quiz-choice-card quiz-choice-card--featured reveal reveal-delay-1" data-length="full">' +
              '<div class="quiz-choice-badge">Recommended</div>' +
              '<div class="quiz-choice-icon">📋</div>' +
              '<h3 class="quiz-choice-title">Full quiz</h3>' +
              '<p class="quiz-choice-time">~6–7 minutes · 25 questions</p>' +
              '<p class="quiz-choice-desc">More accurate, research-backed results. Covers personality, teamwork, and job preferences for a fuller picture.</p>' +
              '<span class="quiz-choice-cta">Start full quiz <span class="btn-arrow" aria-hidden="true">→</span></span>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</section>';

    app.querySelectorAll('[data-length]').forEach(function(el) {
      el.addEventListener('click', function() {
        state.quizShort = this.getAttribute('data-length') === 'short';
        state.step = 'path';
        render();
      });
    });
    triggerReveal();
  }

  function renderPath() {
    var lenText = state.quizShort ? 'Short quiz · 10 questions' : 'Full quiz · 25 questions';
    app.innerHTML =
      '<section class="block block--hero block--hero-with-bg quiz-hero">' +
        '<div class="block-inner">' +
          '<p class="hero-badge">' + lenText + '</p>' +
          '<h1 class="block-hero-title">Choose your path</h1>' +
          '<p class="block-hero-sub">You don\'t need to know your major to get started. That\'s the whole point.</p>' +
        '</div>' +
      '</section>' +
      '<section class="block quiz-choices-section">' +
        '<div class="block-inner">' +
          '<div class="quiz-choice-cards">' +
            '<div class="quiz-choice-card reveal" data-path="major">' +
              '<div class="quiz-choice-icon">🎓</div>' +
              '<h3 class="quiz-choice-title">I have a major in mind</h3>' +
              '<p class="quiz-choice-desc">Pick your major, then take the quiz. You\'ll get <strong>job suggestions that fit both your degree and your personality.</strong></p>' +
              '<span class="quiz-choice-cta">Pick my major & start <span class="btn-arrow" aria-hidden="true">→</span></span>' +
            '</div>' +
            '<div class="quiz-choice-card reveal reveal-delay-1" data-path="explore">' +
              '<div class="quiz-choice-icon">🧭</div>' +
              '<h3 class="quiz-choice-title">I\'m not sure what I want</h3>' +
              '<p class="quiz-choice-desc">Take the quiz without choosing a major. We\'ll suggest <strong>majors and job categories that fit you</strong>, plus sample careers to explore.</p>' +
              '<span class="quiz-choice-cta">Explore majors & careers <span class="btn-arrow" aria-hidden="true">→</span></span>' +
            '</div>' +
          '</div>' +
          '<p class="quiz-back-link"><a href="#" id="quiz-back-length">← Change quiz length</a></p>' +
        '</div>' +
      '</section>';

    app.querySelectorAll('[data-path]').forEach(function(el) {
      el.addEventListener('click', function() {
        state.path = this.getAttribute('data-path');
        if (state.path === 'major') {
          state.step = 'major';
          render();
        } else {
          state.step = 'questions';
          render();
        }
      });
    });
    app.querySelector('#quiz-back-length').addEventListener('click', function(e) {
      e.preventDefault();
      state.step = 'length';
      state.quizShort = null;
      state.path = null;
      render();
    });
    triggerReveal();
  }

  function renderMajor() {
    app.innerHTML =
      '<section class="block block--hero block--hero-with-bg quiz-hero quiz-hero--compact">' +
        '<div class="block-inner">' +
          '<p class="hero-badge">Step 2 of 3</p>' +
          '<h1 class="block-hero-title">Pick your major</h1>' +
          '<p class="block-hero-sub">We\'ll suggest roles that fit your degree and your personality. Pick the one closest to what you\'re studying.</p>' +
        '</div>' +
      '</section>' +
      '<section class="block quiz-major-section">' +
        '<div class="block-inner">' +
          '<div class="quiz-loading">Loading majors…</div>' +
        '</div>' +
      '</section>';

    QuizStatic.getMajors().then(function(majors) {
      var majorSection = app.querySelector('.quiz-major-section .block-inner');
      var html =
        '<form class="major-form" id="major-form">' +
          '<p class="major-choose-label reveal">Choose your major</p>' +
          '<div class="major-list-wrapper" id="major-list-wrapper">' +
            '<div class="major-list" id="major-list">';
      majors.forEach(function(m) {
        html +=
          '<button type="button" class="major-option" data-major-key="' + m.key + '" data-major-label="' + m.label + '">' +
            '<span class="major-option-label">' + m.label + '</span>' +
            '<span class="major-option-desc">' + m.desc + '</span>' +
          '</button>';
      });
      html +=
            '</div>' +
            '<div class="major-list-scrollbar" id="major-list-scrollbar" aria-hidden="true">' +
              '<div class="major-list-thumb" id="major-list-thumb"></div>' +
            '</div>' +
          '</div>' +
          '<button type="submit" class="btn btn-primary major-submit-btn" id="major-submit" disabled>Continue to quiz</button>' +
        '</form>' +
        '<p class="quiz-back-link"><a href="#" id="quiz-back-path">← Choose a different path</a></p>';
      majorSection.innerHTML = html;

      var hidden = document.createElement('input');
      hidden.type = 'hidden';
      hidden.name = 'major';
      hidden.id = 'major-hidden';
      hidden.value = '';
      app.querySelector('#major-form').insertBefore(hidden, app.querySelector('.major-choose-label'));
      var list = document.getElementById('major-list');
      var track = document.getElementById('major-list-scrollbar');
      var thumb = document.getElementById('major-list-thumb');
      var submitBtn = document.getElementById('major-submit');
      var options = list.querySelectorAll('.major-option');

      function selectMajor(key, label) {
        hidden.value = key;
        state.majorKey = key;
        state.majorLabel = label;
        submitBtn.disabled = !key;
        options.forEach(function(opt) {
          opt.classList.toggle('selected', opt.getAttribute('data-major-key') === key);
        });
      }
      options.forEach(function(opt) {
        opt.addEventListener('click', function() {
          selectMajor(this.getAttribute('data-major-key'), this.getAttribute('data-major-label'));
        });
      });
      app.querySelector('#major-form').addEventListener('submit', function(e) {
        e.preventDefault();
        if (hidden.value) {
          state.step = 'questions';
          render();
        }
      });
      app.querySelector('#quiz-back-path').addEventListener('click', function(e) {
        e.preventDefault();
        state.step = 'path';
        state.majorKey = null;
        state.majorLabel = null;
        render();
      });
      initCustomScrollbar(list, track, thumb);
      triggerReveal();
    });
  }

  function initCustomScrollbar(list, track, thumb) {
    function updateThumb() {
      var sh = list.scrollHeight, ch = list.clientHeight;
      if (ch >= sh) { thumb.style.display = 'none'; return; }
      thumb.style.display = 'block';
      var trackH = track.clientHeight;
      var thumbH = Math.max(24, (ch / sh) * trackH);
      var maxTop = trackH - thumbH;
      var top = (list.scrollTop / (sh - ch)) * maxTop;
      thumb.style.height = thumbH + 'px';
      thumb.style.top = top + 'px';
    }
    list.addEventListener('scroll', updateThumb);
    updateThumb();
    window.addEventListener('resize', updateThumb);
    var dragging = false, startY, startScrollTop;
    thumb.addEventListener('mousedown', function(e) {
      e.preventDefault();
      dragging = true;
      startY = e.clientY;
      startScrollTop = list.scrollTop;
    });
    track.addEventListener('mousedown', function(e) {
      if (e.target === thumb) return;
      e.preventDefault();
      var trackRect = track.getBoundingClientRect();
      var frac = (e.clientY - trackRect.top) / trackRect.height;
      list.scrollTop = frac * (list.scrollHeight - list.clientHeight);
    });
    document.addEventListener('mousemove', function(e) {
      if (!dragging) return;
      var dy = e.clientY - startY;
      var trackH = track.clientHeight;
      var thumbH = thumb.offsetHeight;
      var maxTop = trackH - thumbH;
      var sh = list.scrollHeight - list.clientHeight;
      if (maxTop <= 0) return;
      var scrollDelta = (dy / maxTop) * sh;
      list.scrollTop = Math.max(0, Math.min(list.scrollHeight - list.clientHeight, startScrollTop + scrollDelta));
    });
    document.addEventListener('mouseup', function() { dragging = false; });
  }

  function renderQuestions() {
    app.innerHTML = '<section class="block quiz-questions-section"><div class="block-inner"><div class="quiz-loading">Loading questions…</div></div></section>';
    QuizStatic.getQuestions(state.quizShort).then(function(questions) {
      var majorBadge = state.majorKey && state.majorLabel
        ? '<div class="quiz-major-pill">📎 ' + state.majorLabel + '</div>'
        : '';
      var pathLabel = state.path === 'explore' ? 'Explore mode' : (state.majorLabel || 'Career quiz');
      var total = questions.length;

      var html =
        '<section class="block block--hero block--hero-with-bg quiz-hero quiz-hero--compact">' +
          '<div class="block-inner">' +
            '<p class="hero-badge">' + pathLabel + ' · ' + total + ' questions</p>' +
            '<h1 class="block-hero-title">Let\'s find your fit</h1>' +
            '<p class="block-hero-sub">Answer honestly — there are no wrong answers. We\'ll match you to careers based on your personality, interests, and work style.</p>' +
          '</div>' +
        '</section>' +
        '<section class="block quiz-questions-section">' +
          '<div class="block-inner">' +
            majorBadge +
            '<div class="quiz-progress-wrap">' +
              '<div class="quiz-progress-bar"><div class="quiz-progress-fill" id="quiz-progress-fill" style="width:0%"></div></div>' +
              '<span class="quiz-progress-text" id="quiz-progress-text">0 of ' + total + '</span>' +
            '</div>' +
            '<form class="quiz-form" id="quiz-form">';

      questions.forEach(function(q, idx) {
        html +=
          '<fieldset class="quiz-question reveal" data-q-idx="' + idx + '">' +
            '<legend class="quiz-question-legend">' + (idx + 1) + '. ' + q.text + '</legend>' +
            '<ul class="quiz-options">';
        q.options.forEach(function(opt) {
          html +=
            '<li><label class="quiz-option">' +
              '<input type="radio" name="q' + q.id + '" value="' + opt.key + '" required>' +
              '<span class="quiz-option-text">' + opt.label + '</span>' +
            '</label></li>';
        });
        html += '</ul></fieldset>';
      });

      html +=
              '<button type="submit" class="btn btn-primary quiz-submit-btn">See my results <span class="btn-arrow" aria-hidden="true">→</span></button>' +
            '</form>' +
          '</div>' +
        '</section>';

      app.innerHTML = html;
      window.scrollTo(0, 0);

      var progressFill = document.getElementById('quiz-progress-fill');
      var progressText = document.getElementById('quiz-progress-text');
      app.querySelector('#quiz-form').addEventListener('change', function() {
        var answered = app.querySelectorAll('.quiz-form input[type="radio"]:checked').length;
        var pct = Math.round((answered / total) * 100);
        progressFill.style.width = pct + '%';
        progressText.textContent = answered + ' of ' + total;
      });

      app.querySelector('#quiz-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var answers = [];
        questions.forEach(function(q) {
          var inp = app.querySelector('input[name="q' + q.id + '"]:checked');
          if (inp) answers.push(inp.value);
        });
        if (answers.length < questions.length) return;
        state.answers = answers;
        state.step = 'results';
        render();
      });
      triggerReveal();
    });
  }

  function renderResults() {
    var isExplore = state.path === 'explore' || state.fromExploreMajor;
    var majorKey = state.fromExploreMajor || state.majorKey;

    QuizStatic.loadData().then(function() {
      var scoreTuples = QuizStatic.scoreQuiz(state.answers);
      var scoresWithNames = QuizStatic.buildScoresWithNames(scoreTuples);
      var scoresJson = JSON.stringify(scoresWithNames.map(function(s) { return { name: s[2], score: s[1] }; }));

      var suggestions, resultsSummary, suggestedMajors, exploreSummary;
      if (isExplore && !majorKey) {
        suggestedMajors = QuizStatic.getSuggestedMajors(scoreTuples, 6);
        suggestions = QuizStatic.getTopCareers(scoreTuples, null, 12);
        exploreSummary = QuizStatic.getExploreSummary(scoresWithNames, suggestedMajors);
      } else {
        suggestions = QuizStatic.getTopCareers(scoreTuples, majorKey, 6);
        var majorLabel = state.majorLabel || (majorKey ? (suggestedMajors && suggestedMajors.find(function(m) { return m[0] === majorKey; })) ? suggestedMajors.find(function(m) { return m[0] === majorKey; })[1] : null : null);
        if (!majorLabel && majorKey) {
          QuizStatic.getMajorByKey(majorKey).then(function(m) {
            if (m) state.majorLabel = m.label;
          });
        }
        resultsSummary = QuizStatic.getResultsSummary(scoresWithNames, suggestions, state.majorLabel || (majorKey ? '' : null));
      }

      var heroTitle = isExplore ? 'Your majors & career fit' : 'Your Career Matches';
      var heroBadge = state.fromExploreMajor ? 'Explore quiz results'
        : (majorKey && state.majorLabel ? state.majorLabel : (isExplore ? 'Explore mode' : 'Career quiz results'));

      var html =
        '<section class="block block--hero block--hero-with-bg quiz-hero">' +
          '<div class="block-inner">' +
            '<p class="hero-badge">' + heroBadge + '</p>' +
            '<h1 class="block-hero-title">' + heroTitle + '</h1>';

      if (state.fromExploreMajor) {
        html += '<p class="block-hero-sub">These results use your explore quiz answers — no need to retake the quiz.</p>';
      } else if (majorKey && state.majorLabel) {
        html += '<p class="block-hero-sub">Roles that fit <strong>' + state.majorLabel + '</strong> and your interests & personality.</p>';
      } else if (!isExplore) {
        html += '<p class="block-hero-sub">Based on your answers, here are careers that match your interests and personality.</p>';
      } else {
        html += '<p class="block-hero-sub">Based on your answers, here are majors and job categories that match you — plus sample careers to explore.</p>';
      }

      html +=
          '</div>' +
        '</section>';

      html +=
        '<section class="block quiz-results-section">' +
          '<div class="block-inner">' +
            '<div id="quiz-calculating" class="quiz-calculating">' +
              '<div class="quiz-calculating-inner">' +
                '<div class="quiz-calc-spinner"></div>' +
                '<p class="quiz-calc-text">Calculating your profile…</p>' +
                '<p class="quiz-calc-percent" id="quiz-calc-percent">0%</p>' +
              '</div>' +
            '</div>' +
            '<div id="quiz-chart-container" class="quiz-chart-container" style="display:none">' +
              '<h2 class="quiz-chart-title reveal">Your profile at a glance</h2>' +
              '<div class="quiz-chart-wrap">' +
                '<canvas id="quiz-pie-chart" class="quiz-pie-chart" width="280" height="280"></canvas>' +
                '<ul class="quiz-chart-legend" id="quiz-chart-legend"></ul>' +
              '</div>' +
            '</div>' +
            '<script type="application/json" id="quiz-scores-json">' + scoresJson + '</script>';

      if (exploreSummary) {
        html +=
          '<div class="results-summary reveal">' +
            '<h2 class="results-summary-title">Why these fit you</h2>' +
            '<p class="results-summary-text">' + exploreSummary + '</p>' +
          '</div>';
      }
      if (resultsSummary && !isExplore) {
        html +=
          '<div class="results-summary reveal">' +
            '<h2 class="results-summary-title">Why these roles fit you</h2>' +
            '<p class="results-summary-text">' + resultsSummary + '</p>' +
          '</div>';
      }

      if (suggestedMajors && suggestedMajors.length) {
        html +=
          '<div class="explore-section reveal">' +
            '<h2 class="explore-section-title">Suggested majors for you</h2>' +
            '<p class="explore-section-desc">See jobs tailored to each major using your same quiz answers — no need to retake the quiz.</p>' +
            '<ul class="explore-majors-list">';
        suggestedMajors.forEach(function(m) {
          html +=
            '<li class="explore-major-item">' +
              '<a href="#" class="explore-major-link" data-major-key="' + m[0] + '" data-major-label="' + m[1] + '">' +
                '<span class="explore-major-name">' + m[1] + '</span>' +
                '<span class="explore-major-desc">' + m[2] + '</span>' +
                '<span class="explore-major-cta">See jobs for this major →</span>' +
              '</a>' +
            '</li>';
        });
        html += '</ul></div>';
      }

      html +=
            '<div class="scores-section reveal">' +
              '<h2>Your top categories</h2>' +
              '<ul class="scores-list">';
      scoresWithNames.forEach(function(s) {
        html += '<li><strong>' + s[2] + '</strong> — ' + s[1] + ' point' + (s[1] !== 1 ? 's' : '') + '. ' + s[3] + '</li>';
      });
      html += '</ul></div>';

      if (suggestions && suggestions.length) {
        var sectionTitle = isExplore ? 'Sample careers that might fit' : 'Your top career matches';
        html +=
          '<div class="' + (isExplore ? 'explore-section' : '') + ' reveal">' +
            '<h2 class="' + (isExplore ? 'explore-section-title' : 'results-careers-title') + '">' + sectionTitle + '</h2>';
        if (isExplore) html += '<p class="explore-section-desc">A mix of roles across majors that match your profile.</p>';
        html += '<div class="career-cards">';
        suggestions.forEach(function(s, i) {
          var rank = s.compatibility_rank === 1 ? 'Best match' : '#' + s.compatibility_rank;
          var delayClass = i < 6 ? ' reveal reveal-delay-' + (i % 3) : '';
          html +=
            '<div class="career-card' + delayClass + '">' +
              '<span class="career-card-rank">' + rank + '</span>' +
              '<h3 class="career-card-title">' + s.title + '</h3>' +
              '<p class="career-card-desc">' + s.description + '</p>' +
              '<details class="career-learn-more">' +
                '<summary class="career-learn-more-trigger">' +
                  '<span class="career-learn-more-label">Learn more</span>' +
                  '<span class="career-learn-more-arrow" aria-hidden="true">▼</span>' +
                '</summary>' +
                '<div class="career-learn-more-content"><p>' + s.learn_more + '</p></div>' +
              '</details>' +
            '</div>';
        });
        html += '</div>';
        if (isExplore) html += '</div>';
      }

      html +=
        '<section class="quiz-results-actions reveal">';
      if (state.fromExploreMajor) {
        html += '<button type="button" class="btn btn-secondary" id="quiz-back-explore">← Back to explore results</button>';
      } else if (isExplore) {
        html += '<button type="button" class="btn btn-secondary" id="quiz-retake-explore">Retake explore quiz</button>';
      }
      html +=
          '<a href="quiz.html" class="btn btn-secondary">' + (state.majorKey ? 'Pick a different major & retake quiz' : 'Back to quiz home') + '</a>' +
          '<a href="resume.html" class="btn btn-primary">Build your resume <span class="btn-arrow" aria-hidden="true">→</span></a>' +
        '</section>';

      html +=
          '</div>' +
        '</section>';

      app.innerHTML = html;
      window.scrollTo(0, 0);

      if (state.fromExploreMajor) {
        app.querySelector('#quiz-back-explore').addEventListener('click', function() {
          state.fromExploreMajor = null;
          state.majorKey = null;
          state.majorLabel = null;
          state.step = 'results';
          state.path = 'explore';
          render();
        });
      }
      if (document.getElementById('quiz-retake-explore')) {
        app.querySelector('#quiz-retake-explore').addEventListener('click', function() {
          state.path = 'explore';
          state.step = 'questions';
          state.answers = [];
          render();
        });
      }
      app.querySelectorAll('.explore-major-link').forEach(function(a) {
        a.addEventListener('click', function(e) {
          e.preventDefault();
          state.fromExploreMajor = this.getAttribute('data-major-key');
          state.majorKey = state.fromExploreMajor;
          state.majorLabel = this.getAttribute('data-major-label');
          state.step = 'results';
          render();
        });
      });

      var chartScript = document.createElement('script');
      chartScript.src = 'js/quiz-results-chart.js';
      document.body.appendChild(chartScript);
      triggerReveal();
    });
  }

  render();
})();
