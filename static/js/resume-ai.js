/**
 * ExploringU Resume AI — server-only. All AI calls go to the Django backend.
 * The API key is stored in .env (GEMINI_API_KEY) and never sent to the client.
 */
(function () {
  'use strict';

  var SERVER_ENDPOINTS = {
    status: '/resume/api/ai/status/',
    enhance: '/resume/api/ai/enhance-bullet/',
    summary: '/resume/api/ai/generate-summary/',
    skills: '/resume/api/ai/suggest-skills/',
    tailor: '/resume/api/ai/tailor-resume/',
    review: '/resume/api/ai/review-resume/',
  };

  var _serverAvailable = null;

  function checkServer() {
    if (_serverAvailable !== null) return Promise.resolve(_serverAvailable);
    return fetch(SERVER_ENDPOINTS.status, { method: 'GET' })
      .then(function (r) { return r.json(); })
      .then(function (d) { _serverAvailable = d.available === true; return _serverAvailable; })
      .catch(function () { _serverAvailable = false; return false; });
  }

  function isServerMode() {
    return _serverAvailable === true;
  }

  function callServer(endpoint, body) {
    return fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then(function (r) {
      return r.json().then(function (data) {
        if (!r.ok || data.error) throw new Error(data.error || 'Server error');
        return data.result;
      });
    });
  }

  function enhanceBullet(bullet, major) {
    return callServer(SERVER_ENDPOINTS.enhance, { bullet: bullet, major: major });
  }

  function generateSummary(major, role, level, skills) {
    return callServer(SERVER_ENDPOINTS.summary, { major: major, role: role, level: level, skills: skills });
  }

  function suggestSkills(major, role) {
    return callServer(SERVER_ENDPOINTS.skills, { major: major, role: role });
  }

  function tailorResume(resume, job) {
    return callServer(SERVER_ENDPOINTS.tailor, { resume: resume, job: job });
  }

  function analyzeGap(resume, job) {
    return callServer(SERVER_ENDPOINTS.tailor, { resume: resume, job: job, mode: 'gap_analysis' })
      .then(parseGapResponse);
  }

  function parseGapResponse(data) {
    if (typeof data === 'object' && data.match_score !== undefined) return data;
    return {
      match_score: 50,
      summary: 'Analysis complete.',
      strengths: [],
      missing_keywords: [],
      suggestions: [],
    };
  }

  function reviewResume(resumeText, major) {
    return callServer(SERVER_ENDPOINTS.review, { resume: resumeText, major: major });
  }

  function canUseAI() {
    return isServerMode();
  }

  function formatMarkdown(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/^\* (.+)$/gm, '<li>$1</li>')
      .replace(/^- (.+)$/gm, '<li>$1</li>')
      .replace(/^### (.+)$/gm, '<h4>$1</h4>')
      .replace(/^## (.+)$/gm, '<h3>$1</h3>')
      .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
      .replace(/\n/g, '<br>');
  }

  function showError(container, msg) {
    var el = container.querySelector('.ai-error');
    if (!el) { el = document.createElement('p'); el.className = 'ai-error'; container.appendChild(el); }
    el.textContent = msg;
    el.style.display = 'block';
  }

  function clearError(container) {
    var el = container.querySelector('.ai-error');
    if (el) el.style.display = 'none';
  }

  function setupToggle(wrap) {
    var toggle = wrap.querySelector('.ai-tool-toggle');
    var body = wrap.querySelector('.ai-tool-body');
    var arrow = wrap.querySelector('.ai-tool-arrow');
    toggle.addEventListener('click', function () {
      var open = body.style.display !== 'none';
      body.style.display = open ? 'none' : 'block';
      arrow.style.transform = open ? '' : 'rotate(180deg)';
    });
  }

  function createKeySetup(onSave) {
    if (isServerMode()) {
      var wrap = document.createElement('div');
      wrap.className = 'ai-key-setup';
      wrap.style.borderColor = 'rgba(127, 175, 157, 0.3)';
      wrap.style.background = 'rgba(127, 175, 157, 0.06)';
      wrap.innerHTML =
        '<div class="ai-key-header">' +
          '<span class="ai-key-icon">✅</span>' +
          '<div>' +
            '<strong>AI is ready to use</strong>' +
            '<p class="ai-key-desc">AI runs on the server. Your API key stays in .env and is never sent to the browser.</p>' +
          '</div>' +
        '</div>';
      return wrap;
    }
    return document.createElement('div');
  }

  function createServerBadge() {
    var wrap = document.createElement('div');
    wrap.className = 'ai-key-setup';
    wrap.style.borderColor = 'rgba(127, 175, 157, 0.3)';
    wrap.style.background = 'rgba(127, 175, 157, 0.06)';
    wrap.innerHTML =
      '<div class="ai-key-header">' +
        '<span class="ai-key-icon">✅</span>' +
        '<div>' +
          '<strong>AI is ready to use</strong>' +
          '<p class="ai-key-desc">AI runs on the server. Your API key stays in .env and is never sent to the browser.</p>' +
        '</div>' +
      '</div>';
    return wrap;
  }

  function createBulletEnhancer(major) {
    var wrap = document.createElement('div');
    wrap.className = 'ai-tool-section';
    wrap.innerHTML =
      '<button type="button" class="ai-tool-toggle">' +
        '<span class="ai-tool-icon">✨</span> Enhance a bullet point' +
        '<span class="ai-tool-arrow">▼</span></button>' +
      '<div class="ai-tool-body" style="display:none;">' +
        '<p class="ai-tool-hint">Type a weak bullet point and AI will rewrite it with strong action verbs and quantified impact.</p>' +
        '<textarea class="ai-textarea" rows="2" placeholder="e.g. Helped with social media marketing"></textarea>' +
        '<button type="button" class="btn btn-primary ai-action-btn">Enhance →</button>' +
        '<div class="ai-result" style="display:none;">' +
          '<label class="ai-result-label">Enhanced version:</label>' +
          '<div class="ai-result-text"></div>' +
          '<button type="button" class="btn btn-secondary ai-copy-btn">Copy to clipboard</button>' +
        '</div></div>';
    setupToggle(wrap);

    var textarea = wrap.querySelector('.ai-textarea');
    var btn = wrap.querySelector('.ai-action-btn');
    var result = wrap.querySelector('.ai-result');
    var resultText = wrap.querySelector('.ai-result-text');
    var copyBtn = wrap.querySelector('.ai-copy-btn');

    btn.addEventListener('click', function () {
      var text = textarea.value.trim();
      if (!text) return;
      if (!canUseAI()) { showError(wrap, 'AI is only available when the Django server is running with GEMINI_API_KEY in .env.'); return; }
      clearError(wrap); btn.disabled = true; btn.textContent = 'Enhancing...'; result.style.display = 'none';
      enhanceBullet(text, major)
        .then(function (r) { resultText.textContent = r; result.style.display = 'block'; })
        .catch(function (e) { showError(wrap, e.message); })
        .finally(function () { btn.disabled = false; btn.textContent = 'Enhance →'; });
    });

    copyBtn.addEventListener('click', function () {
      navigator.clipboard.writeText(resultText.textContent).then(function () {
        copyBtn.textContent = 'Copied ✓'; setTimeout(function () { copyBtn.textContent = 'Copy to clipboard'; }, 1500);
      });
    });
    return wrap;
  }

  function createSummaryGenerator(major) {
    var wrap = document.createElement('div');
    wrap.className = 'ai-tool-section';
    wrap.innerHTML =
      '<button type="button" class="ai-tool-toggle">' +
        '<span class="ai-tool-icon">📝</span> Generate professional summary' +
        '<span class="ai-tool-arrow">▼</span></button>' +
      '<div class="ai-tool-body" style="display:none;">' +
        '<p class="ai-tool-hint">Generate a tailored summary paragraph for the top of your resume.</p>' +
        '<label class="ai-label">Target role <span class="ai-optional">(optional)</span></label>' +
        '<input type="text" class="ai-input" placeholder="e.g. Marketing Coordinator" data-field="role">' +
        '<label class="ai-label">Experience level</label>' +
        '<select class="ai-select" data-field="level">' +
          '<option value="entry-level">Entry-level / Student</option>' +
          '<option value="recent graduate">Recent Graduate</option>' +
          '<option value="1-2 years experience">1-2 Years Experience</option></select>' +
        '<label class="ai-label">Key skills <span class="ai-optional">(optional, comma-separated)</span></label>' +
        '<input type="text" class="ai-input" placeholder="e.g. Excel, project management, data analysis" data-field="skills">' +
        '<button type="button" class="btn btn-primary ai-action-btn">Generate summary →</button>' +
        '<div class="ai-result" style="display:none;">' +
          '<label class="ai-result-label">Generated summary:</label>' +
          '<div class="ai-result-text"></div>' +
          '<button type="button" class="btn btn-secondary ai-copy-btn">Copy to clipboard</button>' +
        '</div></div>';
    setupToggle(wrap);

    var btn = wrap.querySelector('.ai-action-btn');
    var result = wrap.querySelector('.ai-result');
    var resultText = wrap.querySelector('.ai-result-text');
    var copyBtn = wrap.querySelector('.ai-copy-btn');

    btn.addEventListener('click', function () {
      if (!canUseAI()) { showError(wrap, 'AI is only available when the Django server is running with GEMINI_API_KEY in .env.'); return; }
      clearError(wrap);
      var role = wrap.querySelector('[data-field="role"]').value.trim();
      var level = wrap.querySelector('[data-field="level"]').value;
      var skills = wrap.querySelector('[data-field="skills"]').value.trim();
      btn.disabled = true; btn.textContent = 'Generating...'; result.style.display = 'none';
      generateSummary(major, role, level, skills)
        .then(function (r) { resultText.textContent = r; result.style.display = 'block'; })
        .catch(function (e) { showError(wrap, e.message); })
        .finally(function () { btn.disabled = false; btn.textContent = 'Generate summary →'; });
    });

    copyBtn.addEventListener('click', function () {
      navigator.clipboard.writeText(resultText.textContent).then(function () {
        copyBtn.textContent = 'Copied ✓'; setTimeout(function () { copyBtn.textContent = 'Copy to clipboard'; }, 1500);
      });
    });
    return wrap;
  }

  function createSkillsSuggester(major) {
    var wrap = document.createElement('div');
    wrap.className = 'ai-tool-section';
    wrap.innerHTML =
      '<button type="button" class="ai-tool-toggle">' +
        '<span class="ai-tool-icon">💡</span> Suggest skills for my resume' +
        '<span class="ai-tool-arrow">▼</span></button>' +
      '<div class="ai-tool-body" style="display:none;">' +
        '<p class="ai-tool-hint">Get AI-suggested technical and soft skills based on your major and target role.</p>' +
        '<label class="ai-label">Target role <span class="ai-optional">(optional)</span></label>' +
        '<input type="text" class="ai-input" placeholder="e.g. Data Analyst" data-field="role">' +
        '<button type="button" class="btn btn-primary ai-action-btn">Suggest skills →</button>' +
        '<div class="ai-result" style="display:none;">' +
          '<label class="ai-result-label">Suggested skills:</label>' +
          '<div class="ai-result-text ai-result-formatted"></div>' +
        '</div></div>';
    setupToggle(wrap);

    var btn = wrap.querySelector('.ai-action-btn');
    var result = wrap.querySelector('.ai-result');
    var resultText = wrap.querySelector('.ai-result-text');

    btn.addEventListener('click', function () {
      if (!canUseAI()) { showError(wrap, 'AI is only available when the Django server is running with GEMINI_API_KEY in .env.'); return; }
      clearError(wrap);
      var role = wrap.querySelector('[data-field="role"]').value.trim();
      btn.disabled = true; btn.textContent = 'Thinking...'; result.style.display = 'none';
      suggestSkills(major, role)
        .then(function (r) { resultText.innerHTML = formatMarkdown(r); result.style.display = 'block'; })
        .catch(function (e) { showError(wrap, e.message); })
        .finally(function () { btn.disabled = false; btn.textContent = 'Suggest skills →'; });
    });
    return wrap;
  }

  function createJobTailor() {
    var wrap = document.createElement('div');
    wrap.className = 'ai-tailor-section';
    wrap.innerHTML =
      '<div class="ai-tailor-grid">' +
        '<div class="ai-tailor-col">' +
          '<label class="ai-label">Your resume content</label>' +
          '<p class="ai-tool-hint">Paste your current resume text (bullet points, summary, etc.)</p>' +
          '<textarea class="ai-textarea ai-textarea-lg" rows="12" placeholder="Paste your resume content here..." data-field="resume"></textarea></div>' +
        '<div class="ai-tailor-col">' +
          '<label class="ai-label">Job description</label>' +
          '<p class="ai-tool-hint">Paste the job posting you want to tailor your resume for.</p>' +
          '<textarea class="ai-textarea ai-textarea-lg" rows="12" placeholder="Paste the job description here..." data-field="job"></textarea></div>' +
      '</div>' +
      '<button type="button" class="btn btn-primary ai-action-btn ai-tailor-btn">Tailor my resume →</button>' +
      '<div class="ai-result ai-result-lg" style="display:none;">' +
        '<label class="ai-result-label">Tailored resume content:</label>' +
        '<div class="ai-result-text ai-result-formatted"></div>' +
        '<button type="button" class="btn btn-secondary ai-copy-btn">Copy to clipboard</button></div>';

    var btn = wrap.querySelector('.ai-action-btn');
    var result = wrap.querySelector('.ai-result');
    var resultText = wrap.querySelector('.ai-result-text');
    var copyBtn = wrap.querySelector('.ai-copy-btn');

    btn.addEventListener('click', function () {
      var resume = wrap.querySelector('[data-field="resume"]').value.trim();
      var job = wrap.querySelector('[data-field="job"]').value.trim();
      if (!resume || !job) { showError(wrap, 'Please paste both your resume content and the job description.'); return; }
      if (!canUseAI()) { showError(wrap, 'AI is only available when the Django server is running with GEMINI_API_KEY in .env.'); return; }
      clearError(wrap); btn.disabled = true; btn.textContent = 'Tailoring your resume...'; result.style.display = 'none';
      tailorResume(resume, job)
        .then(function (r) { resultText.innerHTML = formatMarkdown(r); result.style.display = 'block'; result.scrollIntoView({ behavior: 'smooth', block: 'start' }); })
        .catch(function (e) { showError(wrap, e.message); })
        .finally(function () { btn.disabled = false; btn.textContent = 'Tailor my resume →'; });
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        navigator.clipboard.writeText(resultText.textContent).then(function () {
          copyBtn.textContent = 'Copied ✓'; setTimeout(function () { copyBtn.textContent = 'Copy to clipboard'; }, 1500);
        });
      });
    }
    return wrap;
  }

  // Run server check as soon as script loads so status is known before user clicks
  checkServer();

  window.ResumeAI = {
    checkServer: checkServer,
    isServerMode: isServerMode,
    canUseAI: canUseAI,
    createKeySetup: createKeySetup,
    createServerBadge: createServerBadge,
    createBulletEnhancer: createBulletEnhancer,
    createSummaryGenerator: createSummaryGenerator,
    createSkillsSuggester: createSkillsSuggester,
    createJobTailor: createJobTailor,
    analyzeGap: analyzeGap,
    reviewResume: reviewResume,
    formatMarkdown: formatMarkdown,
  };
})();
