/**
 * ExploringU Resume AI — auto-detects server mode vs client mode.
 *
 * Server mode (Django): Calls /resume/api/ai/* endpoints. No API key needed by users.
 * Client mode (GitHub Pages): Falls back to direct Gemini calls with user's own key.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'exploringu_gemini_key';
  var GEMINI_MODEL = 'gemini-2.0-flash';
  var GEMINI_API = 'https://generativelanguage.googleapis.com/v1beta/models/' + GEMINI_MODEL + ':generateContent';

  /* Default key for the static site so AI works out of the box */
  var DEFAULT_KEY = 'AIzaSyDa1nPd3toFkz7GK2kxEBJo0BhsC-XsNzA';

  /* Server endpoints (Django) */
  var SERVER_ENDPOINTS = {
    status: '/resume/api/ai/status/',
    enhance: '/resume/api/ai/enhance-bullet/',
    summary: '/resume/api/ai/generate-summary/',
    skills: '/resume/api/ai/suggest-skills/',
    tailor: '/resume/api/ai/tailor-resume/',
  };

  var _serverAvailable = null; // null = not checked, true/false after check

  /* ---- Mode detection ---- */

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

  /* ---- Client-side key management (fallback) ---- */

  function getClientKey() { return localStorage.getItem(STORAGE_KEY) || DEFAULT_KEY || ''; }
  function setClientKey(key) { localStorage.setItem(STORAGE_KEY, key.trim()); }
  function hasClientKey() { return getClientKey().length > 10; }

  /* ---- API calls ---- */

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

  function callGeminiDirect(prompt) {
    var key = getClientKey();
    if (!key) return Promise.reject(new Error('No API key set'));
    return fetch(GEMINI_API + '?key=' + encodeURIComponent(key), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.7, maxOutputTokens: 1024 },
      })
    }).then(function (r) {
      if (!r.ok) return r.json().then(function (e) { throw new Error((e.error && e.error.message) || 'API error'); });
      return r.json();
    }).then(function (d) {
      if (!d.candidates || !d.candidates[0]) throw new Error('No response');
      return d.candidates[0].content.parts[0].text;
    });
  }

  /* ---- Feature: Enhance bullet ---- */

  function enhanceBullet(bullet, major) {
    if (isServerMode()) {
      return callServer(SERVER_ENDPOINTS.enhance, { bullet: bullet, major: major });
    }
    var prompt = 'You are an expert resume writer for ' + (major || 'college') + ' students. ' +
      'Rewrite this resume bullet point to be more impactful. Use a strong action verb, ' +
      'add specificity, and quantify results where possible. Keep it to ONE concise bullet point (one sentence). ' +
      'Return ONLY the improved bullet point, no explanation or extra text.\n\nOriginal: ' + bullet;
    return callGeminiDirect(prompt).then(function (t) { return t.replace(/^[-•*]\s*/, '').trim(); });
  }

  /* ---- Feature: Generate summary ---- */

  function generateSummary(major, role, level, skills) {
    if (isServerMode()) {
      return callServer(SERVER_ENDPOINTS.summary, { major: major, role: role, level: level, skills: skills });
    }
    var prompt = 'You are an expert resume writer. Write a professional resume summary (2-3 sentences) for a ' +
      level + ' ' + major + ' student' + (role ? ' targeting a ' + role + ' role' : '') + '. ' +
      (skills ? 'Key skills: ' + skills + '. ' : '') +
      'Make it confident, specific, and tailored. Return ONLY the summary paragraph, no labels or explanation.';
    return callGeminiDirect(prompt).then(function (t) { return t.trim(); });
  }

  /* ---- Feature: Suggest skills ---- */

  function suggestSkills(major, role) {
    if (isServerMode()) {
      return callServer(SERVER_ENDPOINTS.skills, { major: major, role: role });
    }
    var prompt = 'You are a career advisor for ' + major + ' students. ' +
      (role ? 'The student is targeting a ' + role + ' role. ' : '') +
      'List 12-15 relevant skills they should include on their resume, separated into ' +
      '"Technical Skills" and "Soft Skills" categories. Format as two short lists. ' +
      'Return ONLY the skill lists, no extra explanation. Use bullet points.';
    return callGeminiDirect(prompt).then(function (t) { return t.trim(); });
  }

  /* ---- Feature: Tailor to job ---- */

  function tailorResume(resume, job) {
    if (isServerMode()) {
      return callServer(SERVER_ENDPOINTS.tailor, { resume: resume, job: job });
    }
    var prompt = 'You are an expert resume consultant. A student has the following resume content and wants to tailor it ' +
      'to a specific job posting. Rewrite their resume content to better match the job description by:\n' +
      '1. Incorporating relevant keywords from the job posting\n' +
      '2. Reordering bullet points to highlight the most relevant experience\n' +
      '3. Strengthening bullet points with action verbs and quantified results\n' +
      '4. Keeping the same overall structure\n\n' +
      'Return ONLY the improved resume content, formatted with clear section headers and bullet points. ' +
      'Do not include any explanation or commentary.\n\n' +
      '--- RESUME CONTENT ---\n' + resume + '\n\n--- JOB DESCRIPTION ---\n' + job;
    return callGeminiDirect(prompt).then(function (t) { return t.trim(); });
  }

  /* ---- Feature: Gap analysis ---- */

  function analyzeGap(resume, job) {
    var prompt = 'You are an expert resume consultant and hiring manager. Analyze how well the following resume matches ' +
      'the job description. Return your analysis as a JSON object with EXACTLY this structure (no markdown, no code fences, ONLY raw JSON):\n' +
      '{\n' +
      '  "match_score": <number 0-100 representing overall match percentage>,\n' +
      '  "summary": "<1-2 sentence overview of how well the resume matches>",\n' +
      '  "strengths": ["<strength 1>", "<strength 2>", ...],\n' +
      '  "missing_keywords": ["<keyword 1>", "<keyword 2>", ...],\n' +
      '  "suggestions": ["<actionable suggestion 1>", "<actionable suggestion 2>", ...]\n' +
      '}\n\n' +
      'Rules:\n' +
      '- match_score should reflect realistic alignment (most students score 30-70)\n' +
      '- strengths: 2-4 things the resume already does well for this role\n' +
      '- missing_keywords: 4-8 specific skills, tools, or keywords from the job posting missing from the resume\n' +
      '- suggestions: 3-5 specific, actionable things the student could add or change to improve their match\n' +
      '- Return ONLY the JSON object, nothing else\n\n' +
      '--- RESUME ---\n' + resume + '\n\n--- JOB DESCRIPTION ---\n' + job;

    if (isServerMode()) {
      return callServer(SERVER_ENDPOINTS.tailor, { resume: resume, job: job, mode: 'gap_analysis' })
        .then(parseGapResponse);
    }
    return callGeminiDirect(prompt).then(parseGapResponse);
  }

  function parseGapResponse(text) {
    if (typeof text === 'object' && text.match_score !== undefined) return text;
    var cleaned = text.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
    try {
      var parsed = JSON.parse(cleaned);
      if (typeof parsed.match_score !== 'number') parsed.match_score = 50;
      parsed.match_score = Math.max(0, Math.min(100, parsed.match_score));
      if (!Array.isArray(parsed.strengths)) parsed.strengths = [];
      if (!Array.isArray(parsed.missing_keywords)) parsed.missing_keywords = [];
      if (!Array.isArray(parsed.suggestions)) parsed.suggestions = [];
      if (!parsed.summary) parsed.summary = 'Analysis complete.';
      return parsed;
    } catch (e) {
      return {
        match_score: 50,
        summary: cleaned.substring(0, 200),
        strengths: [],
        missing_keywords: [],
        suggestions: [cleaned]
      };
    }
  }

  /* ---- Feature: Full resume review ---- */

  function reviewResume(resumeText, major) {
    var prompt = 'You are an expert resume reviewer and career counselor for ' + (major || 'college') + ' students. ' +
      'Review the following resume and provide detailed, actionable feedback. ' +
      'Return your review as a JSON object with EXACTLY this structure (no markdown, no code fences, ONLY raw JSON):\n' +
      '{\n' +
      '  "score": <number 0-100 representing overall resume quality>,\n' +
      '  "verdict": "<one short phrase like \'Strong foundation, needs polish\' or \'Great start — a few tweaks will make it shine\'>",\n' +
      '  "strengths": ["<strength 1>", "<strength 2>", ...],\n' +
      '  "improvements": [\n' +
      '    {"area": "<section or aspect>", "issue": "<what\'s wrong>", "fix": "<specific suggestion>"},\n' +
      '    ...\n' +
      '  ],\n' +
      '  "missing": ["<thing they should add 1>", "<thing they should add 2>", ...]\n' +
      '}\n\n' +
      'Rules:\n' +
      '- score: be realistic (most student resumes score 40-75)\n' +
      '- strengths: 2-3 things done well\n' +
      '- improvements: 3-5 specific issues with concrete fixes (e.g. "Your bullet about social media should quantify reach")\n' +
      '- missing: 2-4 sections or items they should consider adding\n' +
      '- Be encouraging but honest. This is for a student.\n' +
      '- Return ONLY the JSON object, nothing else\n\n' +
      '--- RESUME ---\n' + resumeText;

    return callGeminiDirect(prompt).then(parseReviewResponse);
  }

  function parseReviewResponse(text) {
    if (typeof text === 'object' && text.score !== undefined) return text;
    var cleaned = text.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
    try {
      var parsed = JSON.parse(cleaned);
      if (typeof parsed.score !== 'number') parsed.score = 50;
      parsed.score = Math.max(0, Math.min(100, parsed.score));
      if (!parsed.verdict) parsed.verdict = 'Review complete';
      if (!Array.isArray(parsed.strengths)) parsed.strengths = [];
      if (!Array.isArray(parsed.improvements)) parsed.improvements = [];
      if (!Array.isArray(parsed.missing)) parsed.missing = [];
      return parsed;
    } catch (e) {
      return {
        score: 50,
        verdict: 'Review complete',
        strengths: [],
        improvements: [{ area: 'General', issue: 'Could not parse structured feedback', fix: cleaned.substring(0, 300) }],
        missing: []
      };
    }
  }

  /* ---- UI Helpers ---- */

  function canUseAI() {
    return isServerMode() || hasClientKey();
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

  /* ---- UI: Key setup (only shown in client mode) ---- */

  function createKeySetup(onSave) {
    /* If a default key is present, AI works automatically — show ready badge */
    if (DEFAULT_KEY && DEFAULT_KEY.length > 10 && !localStorage.getItem(STORAGE_KEY)) {
      var readyWrap = document.createElement('div');
      readyWrap.className = 'ai-key-setup';
      readyWrap.style.borderColor = 'rgba(127, 175, 157, 0.3)';
      readyWrap.style.background = 'rgba(127, 175, 157, 0.06)';
      readyWrap.innerHTML =
        '<div class="ai-key-header">' +
          '<span class="ai-key-icon">✅</span>' +
          '<div>' +
            '<strong>AI is ready to use</strong>' +
            '<p class="ai-key-desc">AI features are powered by Google Gemini. No setup needed — just use the tools below.</p>' +
          '</div>' +
        '</div>';
      return readyWrap;
    }

    var wrap = document.createElement('div');
    wrap.className = 'ai-key-setup';
    wrap.innerHTML =
      '<div class="ai-key-header">' +
        '<span class="ai-key-icon">🔑</span>' +
        '<div>' +
          '<strong>Connect your free AI</strong>' +
          '<p class="ai-key-desc">Enter your free Google Gemini API key to unlock AI features. ' +
          'Your key stays in your browser and is never sent to our servers.</p>' +
        '</div>' +
      '</div>' +
      '<a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener" class="ai-key-link">' +
        'Get a free API key from Google AI Studio →</a>' +
      '<div class="ai-key-input-row">' +
        '<input type="password" class="ai-key-input" placeholder="Paste your Gemini API key" value="' + (localStorage.getItem(STORAGE_KEY) || '') + '">' +
        '<button type="button" class="btn btn-primary ai-key-save">Save key</button>' +
      '</div>';

    wrap.querySelector('.ai-key-save').addEventListener('click', function () {
      var val = wrap.querySelector('.ai-key-input').value.trim();
      if (!val) return;
      setClientKey(val);
      this.textContent = 'Saved ✓';
      this.style.background = 'var(--sage)';
      var btn = this;
      setTimeout(function () { btn.textContent = 'Save key'; btn.style.background = ''; }, 2000);
      if (onSave) onSave();
    });

    return wrap;
  }

  /* ---- UI: Server-mode ready badge ---- */

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
          '<p class="ai-key-desc">AI features are powered by Google Gemini. No setup needed — just use the tools below.</p>' +
        '</div>' +
      '</div>';
    return wrap;
  }

  /* ---- UI Components for each feature ---- */

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
      if (!canUseAI()) { showError(wrap, 'Please save your API key first.'); return; }
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
      if (!canUseAI()) { showError(wrap, 'Please save your API key first.'); return; }
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
      if (!canUseAI()) { showError(wrap, 'Please save your API key first.'); return; }
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
      if (!canUseAI()) { showError(wrap, 'Please save your API key first.'); return; }
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

  /* ---- Public API ---- */

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
