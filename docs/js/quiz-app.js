/**
 * Quiz app: multi-step flow for GitHub Pages static site.
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

  function renderLength() {
    app.innerHTML = '<section class="page-section quiz-intro">' +
      '<div class="page-banner page-banner--quiz">' +
      '<h1 class="page-title">Career Discovery Quiz</h1>' +
      '<p class="page-intro">How much time do you have?</p>' +
      '</div>' +
      '<div class="quiz-options-cards">' +
      '<div class="card card-link quiz-option-card" data-length="short">' +
      '<span class="card-icon" aria-hidden="true">⏱</span>' +
      '<h2 class="card-title">Short quiz</h2>' +
      '<p class="card-desc">10 questions, about 3 minutes. Quick snapshot of your interests and style—results are less tailored but still useful for exploring.</p>' +
      '<span class="card-cta">Use short quiz →</span></div>' +
      '<div class="card card-link quiz-option-card" data-length="full">' +
      '<span class="card-icon" aria-hidden="true">📋</span>' +
      '<h2 class="card-title">Full quiz</h2>' +
      '<p class="card-desc">25 questions, about 6–7 minutes. More accurate, research-backed match to majors and careers. Best if you want detailed results.</p>' +
      '<span class="card-cta">Use full quiz →</span></div>' +
      '</div>' +
      '<p class="quiz-meta">Short = 10 questions (~3 min). Full = 25 questions (~6–7 min).</p>' +
      '</section>';
    app.querySelectorAll('[data-length]').forEach(function(el) {
      el.addEventListener('click', function() {
        state.quizShort = this.getAttribute('data-length') === 'short';
        state.step = 'path';
        render();
      });
    });
  }

  function renderPath() {
    var lenText = state.quizShort ? 'Short quiz (10 questions) selected.' : 'Full quiz (25 questions) selected.';
    app.innerHTML = '<section class="page-section quiz-intro">' +
      '<div class="page-banner page-banner--quiz">' +
      '<h1 class="page-title">Choose your path</h1>' +
      '<p class="page-intro">' + lenText + '</p>' +
      '</div>' +
      '<div class="quiz-options-cards">' +
      '<div class="card card-link quiz-option-card" data-path="major">' +
      '<span class="card-icon" aria-hidden="true">🎓</span>' +
      '<h2 class="card-title">I have a major in mind</h2>' +
      '<p class="card-desc">Pick your major, then take the quiz. We suggest <strong>jobs within your degree</strong> that match your personality and interests.</p>' +
      '<span class="card-cta">Pick my major & start quiz →</span></div>' +
      '<div class="card card-link quiz-option-card" data-path="explore">' +
      '<span class="card-icon" aria-hidden="true">📚</span>' +
      '<h2 class="card-title">I\'m not sure what I want</h2>' +
      '<p class="card-desc">Take a broader quiz with the same questions. We\'ll suggest <strong>majors and job categories</strong> that fit you, plus sample careers—no major required.</p>' +
      '<span class="card-cta">Explore majors & careers →</span></div>' +
      '</div>' +
      '<p class="quiz-meta"><a href="#" id="quiz-back-length">← Choose a different quiz length</a></p>' +
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
  }

  function renderMajor() {
    app.innerHTML = '<section class="page-section major-selection">' +
      '<h1 class="page-title">What\'s your major (or intended major)?</h1>' +
      '<p class="page-intro">We\'ll suggest roles that fit your degree and your personality. Pick the one closest to what you\'re studying.</p>' +
      '<div class="quiz-loading">Loading majors...</div></section>';
    QuizStatic.getMajors().then(function(majors) {
      var html = '<form class="major-form" id="major-form">' +
        '<p class="major-choose-label">Choose your major</p>' +
        '<div class="major-list-wrapper" id="major-list-wrapper">' +
        '<div class="major-list" id="major-list">';
      majors.forEach(function(m) {
        html += '<button type="button" class="major-option" data-major-key="' + m.key + '" data-major-label="' + m.label + '">' +
          '<span class="major-option-label">' + m.label + '</span>' +
          '<span class="major-option-desc">' + m.desc + '</span></button>';
      });
      html += '</div><div class="major-list-scrollbar" id="major-list-scrollbar" aria-hidden="true">' +
        '<div class="major-list-thumb" id="major-list-thumb"></div></div></div>' +
        '<button type="submit" class="btn btn-primary major-submit-btn" id="major-submit" disabled>Continue to quiz</button>' +
        '</form>';
      app.innerHTML = '<section class="page-section major-selection">' +
        '<h1 class="page-title">What\'s your major (or intended major)?</h1>' +
        '<p class="page-intro">We\'ll suggest roles that fit your degree and your personality. Pick the one closest to what you\'re studying.</p>' +
        html + '</section>';
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
      app.querySelector('.quiz-meta') && app.querySelector('.quiz-meta').remove();
      var back = document.createElement('p');
      back.className = 'quiz-meta';
      back.innerHTML = '<a href="#" id="quiz-back-path">← Choose a different path</a>';
      app.querySelector('section').appendChild(back);
      back.querySelector('a').addEventListener('click', function(e) {
        e.preventDefault();
        state.step = 'path';
        state.majorKey = null;
        state.majorLabel = null;
        render();
      });
      initCustomScrollbar(list, track, thumb);
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
    app.innerHTML = '<section class="page-section quiz-page"><div class="quiz-loading">Loading questions...</div></section>';
    QuizStatic.getQuestions(state.quizShort).then(function(questions) {
      var majorBadge = state.majorKey && state.majorLabel
        ? '<p class="quiz-major-badge">Exploring careers for: <strong>' + state.majorLabel + '</strong></p>'
        : '';

      var html = '<h1 class="page-title">Career Discovery Quiz</h1>' + majorBadge +
        '<p class="page-intro">Answer each question honestly. Questions cover your interests, Big Five personality, teamwork, and work-style preferences. There are no wrong answers.</p>' +
        '<form class="quiz-form" id="quiz-form">';
      questions.forEach(function(q) {
        html += '<fieldset class="quiz-question">' +
          '<legend class="quiz-question-legend">' + q.id + '. ' + q.text + '</legend>' +
          '<ul class="quiz-options">';
        q.options.forEach(function(opt) {
          html += '<li><label class="quiz-option">' +
            '<input type="radio" name="q' + q.id + '" value="' + opt.key + '" required>' +
            '<span class="quiz-option-text">' + opt.label + '</span></label></li>';
        });
        html += '</ul></fieldset>';
      });
      html += '<button type="submit" class="btn btn-primary">See my results</button></form></section>';
      app.innerHTML = html;

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

      var html = '<section class="page-section results-page' + (isExplore ? ' explore-results-page' : '') + '">' +
        '<h1 class="page-title">' + (isExplore ? 'Your majors & career fit' : 'Your Career Suggestions') + '</h1>';

      if (state.fromExploreMajor) {
        html += '<p class="results-from-explore-note">These results use your <strong>explore quiz</strong> answers—no need to retake the quiz.</p>';
      }
      if (majorKey && state.majorLabel) {
        html += '<p class="results-major">Roles that fit <strong>' + state.majorLabel + '</strong> and your interests & personality:</p>';
      } else if (!isExplore) {
        html += '<p class="page-intro">Based on your answers, here are careers that might fit your interests and personality.</p>';
      } else {
        html += '<p class="page-intro">Based on your answers, here are majors and job categories that match your interests and personality—plus sample careers to explore.</p>';
      }

      html += '<div id="quiz-calculating" class="quiz-calculating">' +
        '<div class="quiz-calculating-inner">' +
        '<div class="quiz-calc-spinner"></div>' +
        '<p class="quiz-calc-text">Calculating your profile...</p>' +
        '<p class="quiz-calc-percent" id="quiz-calc-percent">0%</p></div></div>' +
        '<div id="quiz-chart-container" class="quiz-chart-container" style="display:none">' +
        '<h2 class="quiz-chart-title">Your profile at a glance</h2>' +
        '<div class="quiz-chart-wrap">' +
        '<canvas id="quiz-pie-chart" class="quiz-pie-chart" width="280" height="280"></canvas>' +
        '<ul class="quiz-chart-legend" id="quiz-chart-legend"></ul></div></div>' +
        '<script type="application/json" id="quiz-scores-json">' + scoresJson + '</script>';

      if (exploreSummary) {
        html += '<div class="results-summary"><h2 class="results-summary-title">Why these fit you</h2>' +
          '<p class="results-summary-text">' + exploreSummary + '</p></div>';
      }
      if (resultsSummary && !isExplore) {
        html += '<div class="results-summary"><h2 class="results-summary-title">Why these roles fit you</h2>' +
          '<p class="results-summary-text">' + resultsSummary + '</p></div>';
      }

      if (suggestedMajors && suggestedMajors.length) {
        html += '<div class="explore-section"><h2 class="explore-section-title">Suggested majors for you</h2>' +
          '<p class="explore-section-desc">See jobs tailored to each major using your same quiz answers—no need to retake the quiz.</p>' +
          '<ul class="explore-majors-list">';
        suggestedMajors.forEach(function(m) {
          html += '<li class="explore-major-item"><a href="#" class="explore-major-link" data-major-key="' + m[0] + '" data-major-label="' + m[1] + '">' +
            '<span class="explore-major-name">' + m[1] + '</span>' +
            '<span class="explore-major-desc">' + m[2] + '</span>' +
            '<span class="explore-major-cta">See jobs for this major →</span></a></li>';
        });
        html += '</ul></div>';
      }

      html += '<div class="scores-section"><h2>Your top categories</h2><ul class="scores-list">';
      scoresWithNames.forEach(function(s) {
        html += '<li><strong>' + s[2] + '</strong> — ' + s[1] + ' point' + (s[1] !== 1 ? 's' : '') + '. ' + s[3] + '</li>';
      });
      html += '</ul></div>';

      if (suggestions && suggestions.length) {
        var sectionTitle = isExplore ? 'Sample careers that might fit' : '';
        if (isExplore) html += '<div class="explore-section"><h2 class="explore-section-title">' + sectionTitle + '</h2>' +
          '<p class="explore-section-desc">A mix of roles across majors that match your profile.</p>';
        html += '<div class="career-cards">';
        suggestions.forEach(function(s, i) {
          var rank = s.compatibility_rank === 1 ? 'Best match' : '#' + s.compatibility_rank;
          html += '<div class="career-card">' +
            '<span class="career-card-rank">' + rank + '</span>' +
            '<h3 class="career-card-title">' + s.title + '</h3>' +
            '<p class="career-card-desc">' + s.description + '</p>' +
            '<details class="career-learn-more"><summary class="career-learn-more-trigger">' +
            '<span class="career-learn-more-label">Learn more</span>' +
            '<span class="career-learn-more-arrow" aria-hidden="true">▼</span></summary>' +
            '<div class="career-learn-more-content"><p>' + s.learn_more + '</p></div></details></div>';
        });
        html += '</div>';
        if (isExplore) html += '</div>';
      }

      html += '<div class="' + (isExplore ? 'explore-actions' : 'results-actions') + '">';
      if (state.fromExploreMajor) {
        html += '<button type="button" class="btn btn-secondary" id="quiz-back-explore">Back to explore results</button>';
      } else if (isExplore) {
        html += '<button type="button" class="btn btn-secondary" id="quiz-retake-explore">Retake explore quiz</button>';
      }
      html += '<a href="quiz.html" class="btn btn-secondary">' + (state.majorKey ? 'Pick a different major & retake quiz' : 'Back to quiz home') + '</a></div>';
      html += '</section>';

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
    });
  }

  render();
})();
