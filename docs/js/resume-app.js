/**
 * Resume static site app — loads resume-data.json and renders pages.
 */
(function () {
  let DATA = null;

  async function loadData() {
    if (DATA) return DATA;
    try {
      const resp = await fetch('js/resume-data.json');
      if (!resp.ok) throw new Error('Failed to load resume data');
      DATA = await resp.json();
    } catch (e) {
      console.error('Resume data load error:', e);
      DATA = { templates: {}, tips: [] };
    }
    return DATA;
  }

  const HERO_DECOR = {
    shapes: '<div class="hero-shapes" aria-hidden="true"><div class="hero-shape hero-shape--orb hero-shape-1"></div><div class="hero-shape hero-shape--orb hero-shape-2"></div><div class="hero-shape hero-shape--orb hero-shape-3"></div><div class="hero-shape hero-shape--blob hero-shape-4"></div><div class="hero-shape hero-shape--prism hero-shape-5"></div><div class="hero-shape hero-shape--prism hero-shape-6"></div><div class="hero-shape hero-shape--glow hero-shape-7"></div><div class="hero-shape hero-shape--glow hero-shape-8"></div></div>',
    particlesBehind: '<div class="hero-particles hero-particles--behind" aria-hidden="true"><span class="hero-particle hero-particle--s" style="--x: 9%; --y: 16%; --d: 0"></span><span class="hero-particle hero-particle--m" style="--x: 86%; --y: 24%; --d: 0.9"></span><span class="hero-particle hero-particle--s" style="--x: 14%; --y: 46%; --d: 1.6"></span><span class="hero-particle hero-particle--l" style="--x: 76%; --y: 52%; --d: 0.2"></span><span class="hero-particle hero-particle--accent" style="--x: 26%; --y: 32%; --d: 0.4"></span><span class="hero-particle hero-particle--accent hero-particle--s" style="--x: 70%; --y: 44%; --d: 1.5"></span></div>',
    particlesFront: '<div class="hero-particles hero-particles--front" aria-hidden="true"><span class="hero-particle hero-particle--m" style="--x: 28%; --y: 20%; --d: 0.6"></span><span class="hero-particle hero-particle--s" style="--x: 68%; --y: 38%; --d: 1.0"></span><span class="hero-particle hero-particle--accent hero-particle--s" style="--x: 52%; --y: 82%; --d: 0.7"></span></div>'
  };

  function majorCardHTML(key, t, idx) {
    var delayClass = (typeof idx === 'number' && idx < 6) ? ' reveal-delay-' + idx : '';
    return `<a href="resume-template.html?major=${key}" class="resume-major-card reveal${delayClass}" data-keywords="${t.label.toLowerCase()} ${t.focus.toLowerCase()}">
      <span class="resume-major-icon">${t.icon}</span>
      <h3 class="resume-major-label">${t.label}</h3>
      <p class="resume-major-focus">${t.focus}</p>
      <span class="resume-major-cta">View template →</span>
    </a>`;
  }

  /* ---- Resume Home ---- */
  window.renderResumeHome = async function (el) {
    const data = await loadData();
    const templates = data.templates;
    const majorCards = Object.entries(templates).map(([k, t], i) => majorCardHTML(k, t, i)).join('');

    el.innerHTML = `
    <section class="block block--hero block--hero-with-bg resume-hero">
      ${HERO_DECOR.shapes}
      ${HERO_DECOR.particlesBehind}
      <div class="block-inner">
        <p class="hero-badge">Free for students</p>
        <h1 class="block-hero-title">Build a resume that gets you hired</h1>
        <p class="block-hero-sub">Download free, major-specific resume templates designed for students and recent grads. Every major has different expectations—we've got you covered.</p>
        <div class="block-hero-buttons">
          <a href="resume-templates.html" class="btn btn-primary btn-hero-primary">Browse templates <span class="btn-arrow" aria-hidden="true">→</span></a>
          <a href="resume-tips.html" class="btn btn-hero-secondary">Resume tips <span class="btn-arrow btn-arrow--outline" aria-hidden="true">▶</span></a>
        </div>
      </div>
      ${HERO_DECOR.particlesFront}
    </section>
    <section class="block block--dark">
      <div class="block-inner">
        <h2 class="block-title block-title--light reveal" style="text-align:center; margin-bottom: 0.5rem;">What would you like to do?</h2>
        <p class="block-desc block-desc--light reveal" style="text-align:center; margin-bottom: 2.5rem;">Whether you're starting fresh or polishing what you have, we'll help you stand out.</p>
        <div class="resume-options-grid resume-options-grid--3">
          <a href="resume-generate.html" class="resume-option-card reveal">
            <span class="resume-option-icon">✨</span>
            <h3 class="resume-option-title">AI-generated resume</h3>
            <p class="resume-option-desc">Answer a few questions about the role and your background. Our AI creates a tailored resume and delivers it as a PDF.</p>
            <span class="resume-option-cta">Get started →</span>
          </a>
          <a href="resume-templates.html" class="resume-option-card reveal reveal-delay-1">
            <span class="resume-option-icon resume-option-icon--plus" aria-hidden="true">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="14" y="4" width="4" height="24" rx="2" fill="currentColor"/>
                <rect x="4" y="14" width="24" height="4" rx="2" fill="currentColor"/>
              </svg>
            </span>
            <h3 class="resume-option-title">Create a new resume</h3>
            <p class="resume-option-desc">Pick a template tailored to your major, fill in your details, and download a polished, professional resume as a PDF.</p>
            <span class="resume-option-cta">Browse templates →</span>
          </a>
          <a href="resume-ai-tools.html" class="resume-option-card reveal reveal-delay-1">
            <span class="resume-option-icon">📊</span>
            <h3 class="resume-option-title">Perform Resume Gap Analysis</h3>
            <p class="resume-option-desc">Paste your resume and a job posting. Get a match score, missing keywords, and actionable suggestions to improve your fit — powered by AI gap analysis. Plus enhance bullets, summaries, and more.</p>
            <span class="resume-option-cta">Run gap analysis →</span>
          </a>
        </div>
      </div>
    </section>
    <section class="block block--features">
      <div class="block-inner">
        <h2 class="block-title reveal" style="text-align:center; margin-bottom: 0.5rem;">Templates for every major</h2>
        <p class="block-desc reveal" style="text-align:center; margin-bottom: 2.5rem;">Each template is formatted for your field with the right sections, action verbs, and sample content.</p>
        <div class="resume-major-grid">${majorCards}</div>
      </div>
    </section>
    <section class="block block--cream reveal">
      <div class="block-inner block-inner--narrow">
        <h2 class="block-title">Not sure where to start?</h2>
        <p class="block-desc block-desc--why">Take our career quiz to discover which paths match your personality and interests—then come back to build the perfect resume.</p>
        <a href="quiz.html" class="btn btn-primary">Take the career quiz <span class="btn-arrow" aria-hidden="true">→</span></a>
      </div>
    </section>`;

    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  };

  /* ---- Resume Templates list ---- */
  window.renderResumeTemplates = async function (el) {
    const data = await loadData();
    const templates = data.templates;
    const count = Object.keys(templates).length;
    const majorCards = Object.entries(templates).map(([k, t], i) => majorCardHTML(k, t, i)).join('');

    el.innerHTML = `
    <section class="block block--hero block--hero-with-bg resume-hero resume-hero--compact">
      ${HERO_DECOR.shapes}
      ${HERO_DECOR.particlesBehind}
      <div class="block-inner">
        <p class="hero-badge">${count} majors · free downloads</p>
        <h1 class="block-hero-title">Resume Templates by Major</h1>
        <p class="block-hero-sub">Every field has different expectations. Pick your major to get a template with the right sections, formatting, and sample content — ready to download as a PDF.</p>
      </div>
      ${HERO_DECOR.particlesFront}
    </section>
    <section class="block resume-templates-section">
      <div class="block-inner">
        <div class="resume-search-wrap reveal">
          <span class="resume-search-icon" aria-hidden="true">🔍</span>
          <input type="text" class="resume-search-input" id="resume-search" placeholder="Search majors..." autocomplete="off">
        </div>
        <div class="resume-major-grid" id="resume-major-grid">${majorCards}</div>
        <p class="resume-no-results" id="resume-no-results">No templates match your search. Try a different keyword.</p>
        <p class="resume-back-link"><a href="resume-tips.html">Resume tips & advice →</a></p>
      </div>
    </section>`;

    // Search filter
    var input = document.getElementById('resume-search');
    var grid = document.getElementById('resume-major-grid');
    var noResults = document.getElementById('resume-no-results');
    if (input && grid) {
      var cards = grid.querySelectorAll('.resume-major-card');
      input.addEventListener('input', function() {
        var q = this.value.trim().toLowerCase();
        var visible = 0;
        cards.forEach(function(card) {
          var kw = card.getAttribute('data-keywords') || '';
          var match = !q || kw.indexOf(q) !== -1;
          card.style.display = match ? '' : 'none';
          if (match) visible++;
        });
        noResults.style.display = visible === 0 ? 'block' : 'none';
      });
    }

    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  };

  /* ---- Resume Template Detail ---- */
  window.renderResumeDetail = async function (el) {
    const params = new URLSearchParams(window.location.search);
    const majorKey = params.get('major');
    const data = await loadData();
    const t = data.templates[majorKey];

    if (!t) {
      el.innerHTML = '<p style="text-align:center;padding:3rem;">Template not found. <a href="resume-templates.html">Browse all templates</a></p>';
      return;
    }

    function sectionContent(section) {
      if (section === 'Summary') {
        return `<div class="rp-content" contenteditable="true">Results-driven ${t.label} student with experience in ${t.focus.toLowerCase()}. Passionate about making an impact through practical skills and a strong work ethic. Seeking an entry-level position to apply classroom knowledge in a professional setting.</div>`;
      }
      if (section === 'Education' || section === 'Education & Training') {
        return `<div class="rp-content" contenteditable="true"><strong>Bachelor of Science in ${t.label}</strong><br>Your University · Expected May 2026<br>GPA: 3.X/4.0 · Relevant Coursework: [Add your courses]</div>`;
      }
      if (['Technical Skills', 'Skills', 'Tools & Software', 'Skills & Tools', 'Skills & Equipment'].includes(section)) {
        const skillTip = (t.tips || []).find(tip => tip.toLowerCase().includes('tools') || tip.toLowerCase().includes('list') || tip.toLowerCase().includes('include'));
        return `<div class="rp-content" contenteditable="true">${skillTip || 'Add your relevant skills, tools, and software here. Separate technical skills from soft skills for clarity.'}</div>`;
      }
      if (['Certifications', 'Certifications & Licenses', 'Licenses & Certifications'].includes(section)) {
        return `<div class="rp-content" contenteditable="true">List relevant certifications, licenses, and professional training. Include dates earned and issuing organization.</div>`;
      }
      if (['Portfolio', 'Portfolio & Projects'].includes(section)) {
        return `<div class="rp-content" contenteditable="true">Link to your online portfolio (e.g., Behance, Dribbble, GitHub, personal website). List 2–3 key projects with brief descriptions of your role and impact.</div>`;
      }
      const bullets = t.sample_bullets.map(b => `<li>${b}</li>`).join('');
      return `<div class="rp-content" contenteditable="true"><ul>${bullets}</ul></div>`;
    }

    const sectionsHTML = t.sections.map(s => `
      <div class="rp-section">
        <div class="rp-section-title">${s}</div>
        ${sectionContent(s)}
      </div>`).join('');

    const tipsHTML = t.tips.map(tip => `<li>${tip}</li>`).join('');
    const sectionsListHTML = t.sections.map(s => `<li>${s}</li>`).join('');

    el.innerHTML = `
    <section class="block block--hero block--hero-with-bg resume-hero resume-hero--compact">
      ${HERO_DECOR.shapes}
      ${HERO_DECOR.particlesBehind}
      <div class="block-inner">
        <p class="hero-badge">${t.label} · editable template</p>
        <h1 class="block-hero-title">${t.icon} ${t.label} Resume</h1>
        <p class="block-hero-sub">${t.focus} — tailored format and sample content for ${t.label} students.</p>
      </div>
      ${HERO_DECOR.particlesFront}
    </section>
    <section class="block resume-detail-section">
      <div class="block-inner">
        <div class="resume-quickstart reveal" id="resume-quickstart">
          <div class="resume-quickstart-steps">
            <span class="resume-qs-step"><span class="resume-qs-num">1</span> Click any text to edit</span>
            <span class="resume-qs-step"><span class="resume-qs-num">2</span> Add your info</span>
            <span class="resume-qs-step"><span class="resume-qs-num">3</span> Use AI tools to polish</span>
            <span class="resume-qs-step"><span class="resume-qs-num">4</span> Download as PDF</span>
          </div>
        </div>
        <div class="resume-detail-layout">
          <div class="resume-preview-wrap reveal">
            <div class="resume-preview" id="resumePreview">
              <div class="resume-paper">
                <div class="rp-header">
                  <div class="rp-name" contenteditable="true">Your Name</div>
                  <div class="rp-contact" contenteditable="true">email@example.com · (555) 123-4567 · City, State · linkedin.com/in/yourname${majorKey === 'computer_science' ? ' · github.com/yourname' : ''}</div>
                </div>
                ${sectionsHTML}
              </div>
            </div>
            <div class="resume-preview-actions">
              <button class="btn btn-primary" id="downloadPdfBtn">Download as PDF <span aria-hidden="true">↓</span></button>
              <button class="btn btn-teal" id="reviewBtn">Review my resume <span aria-hidden="true">✦</span></button>
              <button class="btn btn-secondary" id="resetBtn">Reset template</button>
            </div>
            <div id="reviewResults" class="review-results" style="display:none;"></div>
          </div>
          <aside class="resume-detail-sidebar reveal reveal-delay-1">
            <div class="resume-sidebar-card">
              <h3 class="ai-sidebar-title">AI Resume Assistant <span class="ai-badge">Free</span></h3>
              <div id="aiKeySetup"></div>
              <div id="aiTools" class="ai-sidebar-wrap"></div>
            </div>
            <div class="resume-sidebar-card resume-sidebar-card--compact">
              <details class="resume-details" open>
                <summary class="resume-details-toggle">Tips for ${t.label}</summary>
                <ul class="resume-sidebar-tips">${tipsHTML}</ul>
              </details>
              <details class="resume-details">
                <summary class="resume-details-toggle">Recommended sections</summary>
                <ol class="resume-sidebar-sections">${sectionsListHTML}</ol>
              </details>
            </div>
            <a href="resume-templates.html" class="btn btn-secondary" style="width:100%; text-align:center;">← Back to all templates</a>
          </aside>
        </div>
      </div>
    </section>`;

    // Quickstart step animation
    var qs = document.getElementById('resume-quickstart');
    if (qs && 'IntersectionObserver' in window) {
      var qsObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            qs.classList.add('is-animated');
            qsObs.unobserve(qs);
          }
        });
      }, { threshold: 0.3 });
      qsObs.observe(qs);
    }

    // PDF download
    const preview = document.getElementById('resumePreview');
    const originalHTML = preview.innerHTML;

    document.getElementById('downloadPdfBtn').addEventListener('click', function () {
      const btn = this;
      btn.textContent = 'Generating PDF...';
      btn.disabled = true;

      function resetBtn() {
        btn.innerHTML = 'Download as PDF <span aria-hidden="true">↓</span>';
        btn.disabled = false;
      }

      function generatePdf() {
        html2pdf().set({
          margin: 1,
          filename: majorKey + '-resume-futurefit.pdf',
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 1, width: 600, height: 500, scrollY: 0 },
          jsPDF: { unit: 'in', orientation: 'portrait' }
        }).from(
          document.querySelector('.resume-paper')
        ).save().then(resetBtn).catch(function(err) {
          console.error('PDF generation error:', err);
          alert('There was an error generating the PDF. Please try again.');
          resetBtn();
        });
      }

      if (typeof html2pdf !== 'undefined') {
        generatePdf();
      } else {
        alert("Could not load PDF library. Please check your internet connection and try again.");
        resetBtn();
        
        /*
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
        //script.onload = generatePdf;
        script.onerror = function () {
          alert('Could not load PDF library. Please check your internet connection and try again.');
          resetBtn();
        };
        document.head.appendChild(script);
        */
      }
    });

    document.getElementById('resetBtn').addEventListener('click', function () {
      if (confirm('Reset the template? Your edits will be lost.')) {
        preview.innerHTML = originalHTML;
      }
    });

    // AI resume review
    var reviewBtn = document.getElementById('reviewBtn');
    var reviewResults = document.getElementById('reviewResults');

    reviewBtn.addEventListener('click', function () {
      var resumeText = preview.querySelector('.resume-paper').innerText.trim();
      if (!resumeText || resumeText.length < 30) {
        alert('Add some content to your resume before reviewing.');
        return;
      }
      if (typeof ResumeAI === 'undefined' || !ResumeAI.canUseAI()) {
        alert('Please set up your AI key in the sidebar first.');
        return;
      }
      reviewBtn.disabled = true;
      reviewBtn.innerHTML = '<span class="gap-btn-spinner"></span> Reviewing...';
      reviewResults.style.display = 'none';

      ResumeAI.reviewResume(resumeText, t.label)
        .then(function (data) {
          renderReview(data);
          reviewResults.style.display = 'block';
          reviewResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(function (e) {
          reviewResults.innerHTML = '<p class="ai-error" style="display:block;">' + (e.message || 'Something went wrong.') + '</p>';
          reviewResults.style.display = 'block';
        })
        .finally(function () {
          reviewBtn.disabled = false;
          reviewBtn.innerHTML = 'Review my resume <span aria-hidden="true">✦</span>';
        });
    });

    function renderReview(data) {
      var scoreColor = data.score >= 70 ? '#7FAF9D' : data.score >= 40 ? '#4FA3A5' : '#C8766A';

      var strengthsHTML = data.strengths.map(function (s) {
        return '<li class="review-strength-item">' + s + '</li>';
      }).join('');

      var improvementsHTML = data.improvements.map(function (imp) {
        return '<div class="review-improvement">' +
          '<div class="review-imp-header"><span class="review-imp-area">' + imp.area + '</span></div>' +
          '<p class="review-imp-issue">' + imp.issue + '</p>' +
          '<p class="review-imp-fix"><strong>Suggestion:</strong> ' + imp.fix + '</p>' +
        '</div>';
      }).join('');

      var missingHTML = data.missing.map(function (m) {
        return '<span class="gap-keyword-tag">' + m + '</span>';
      }).join('');

      reviewResults.innerHTML =
        '<div class="review-header">' +
          '<div class="review-score-ring">' +
            '<canvas id="reviewChart" width="100" height="100"></canvas>' +
            '<span class="review-score-num">' + data.score + '</span>' +
          '</div>' +
          '<div class="review-verdict-wrap">' +
            '<h3 class="review-verdict">' + data.verdict + '</h3>' +
            '<p class="review-verdict-sub">AI reviewed your ' + t.label + ' resume and found ' +
              data.improvements.length + ' area' + (data.improvements.length !== 1 ? 's' : '') + ' to improve.</p>' +
          '</div>' +
        '</div>' +
        (strengthsHTML ? '<div class="review-section"><h4 class="review-section-title review-section-title--good">What\'s working</h4><ul class="review-strengths">' + strengthsHTML + '</ul></div>' : '') +
        (improvementsHTML ? '<div class="review-section"><h4 class="review-section-title review-section-title--fix">Suggested improvements</h4>' + improvementsHTML + '</div>' : '') +
        (missingHTML ? '<div class="review-section"><h4 class="review-section-title">Consider adding</h4><div class="gap-keywords">' + missingHTML + '</div></div>' : '');

      var canvas = document.getElementById('reviewChart');
      if (canvas) {
        var ctx = canvas.getContext('2d');
        var dpr = window.devicePixelRatio || 1;
        var size = 100;
        canvas.width = size * dpr;
        canvas.height = size * dpr;
        canvas.style.width = size + 'px';
        canvas.style.height = size + 'px';
        ctx.scale(dpr, dpr);
        var cx = size / 2, cy = size / 2, r = size / 2 - 8, lw = 10;
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(31,42,68,0.08)'; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.stroke();
        var sweep = (data.score / 100) * Math.PI * 2;
        if (sweep > 0.01) {
          ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + sweep);
          ctx.strokeStyle = scoreColor; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.stroke();
        }
      }
    }

    // AI tools — auto-detect server mode
    if (typeof ResumeAI !== 'undefined') {
      ResumeAI.checkServer().then(function(serverOk) {
        var keyEl = document.getElementById('aiKeySetup');
        if (serverOk) {
          keyEl.appendChild(ResumeAI.createServerBadge());
        } else {
          keyEl.appendChild(ResumeAI.createKeySetup());
        }
        const aiTools = document.getElementById('aiTools');
        aiTools.appendChild(ResumeAI.createBulletEnhancer(t.label));
        aiTools.appendChild(ResumeAI.createSummaryGenerator(t.label));
        aiTools.appendChild(ResumeAI.createSkillsSuggester(t.label));
      });
    }

    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  };

  /* ---- Resume Tips ---- */
  window.renderResumeTips = async function (el) {
    const data = await loadData();
    const tips = data.tips;

    const tipsCards = tips.map((tip, i) => {
      var delayClass = i < 3 ? ' reveal-delay-' + i : '';
      return `
      <div class="resume-tip-card reveal${delayClass}">
        <span class="resume-tip-number" data-target="${i + 1}">${i + 1}</span>
        <h3 class="resume-tip-title">${tip.title}</h3>
        <p class="resume-tip-desc">${tip.desc}</p>
      </div>`;
    }).join('');

    el.innerHTML = `
    <section class="block block--hero block--hero-with-bg resume-hero resume-hero--compact">
      ${HERO_DECOR.shapes}
      ${HERO_DECOR.particlesBehind}
      <div class="block-inner">
        <p class="hero-badge">${tips.length} expert tips</p>
        <h1 class="block-hero-title">Resume Tips & Best Practices</h1>
        <p class="block-hero-sub">Expert advice to help you write a resume that stands out. Whether you're starting from scratch or polishing a draft, these tips will help.</p>
      </div>
      ${HERO_DECOR.particlesFront}
    </section>
    <section class="block resume-tips-section">
      <div class="block-inner">
        <div class="resume-tips-grid" id="resume-tips-grid">${tipsCards}</div>
      </div>
    </section>
    <section class="block block--cream reveal">
      <div class="block-inner block-inner--narrow">
        <h2 class="block-title">Want tips specific to your major?</h2>
        <p class="block-desc block-desc--why">Every field has different resume expectations. Browse our templates to see section recommendations, sample bullets, and formatting advice tailored to your degree.</p>
        <a href="resume-templates.html" class="btn btn-primary">Browse templates by major <span class="btn-arrow" aria-hidden="true">→</span></a>
      </div>
    </section>
    <section class="block resume-verbs-section-block">
      <div class="block-inner">
        <h2 class="block-title reveal" style="text-align:center; margin-bottom: 0.35rem;">Power action verbs</h2>
        <p class="block-desc reveal" style="text-align:center; margin-bottom: 2rem;">Start your bullet points with these strong verbs to make your achievements stand out.</p>
        <div class="resume-verbs-grid">
          <div class="resume-verb-group reveal"><h4 class="resume-verb-category">Leadership</h4><p class="resume-verb-list">Led, Managed, Directed, Supervised, Coordinated, Spearheaded, Mentored, Delegated</p></div>
          <div class="resume-verb-group reveal reveal-delay-1"><h4 class="resume-verb-category">Achievement</h4><p class="resume-verb-list">Achieved, Exceeded, Improved, Increased, Reduced, Streamlined, Resolved, Delivered</p></div>
          <div class="resume-verb-group reveal reveal-delay-2"><h4 class="resume-verb-category">Creation</h4><p class="resume-verb-list">Designed, Developed, Created, Built, Launched, Established, Implemented, Initiated</p></div>
          <div class="resume-verb-group reveal reveal-delay-3"><h4 class="resume-verb-category">Analysis</h4><p class="resume-verb-list">Analyzed, Researched, Evaluated, Assessed, Investigated, Identified, Calculated, Forecasted</p></div>
          <div class="resume-verb-group reveal"><h4 class="resume-verb-category">Communication</h4><p class="resume-verb-list">Presented, Authored, Edited, Negotiated, Collaborated, Advocated, Facilitated, Persuaded</p></div>
          <div class="resume-verb-group reveal reveal-delay-1"><h4 class="resume-verb-category">Technical</h4><p class="resume-verb-list">Programmed, Engineered, Automated, Configured, Debugged, Optimized, Deployed, Integrated</p></div>
        </div>
      </div>
    </section>
    <p class="resume-back-link"><a href="resume.html">← Back to Resume Builder</a></p>`;

    // Tip card animation observer
    var tipCards = document.querySelectorAll('.resume-tip-card');
    if (tipCards.length && 'IntersectionObserver' in window) {
      var tipObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            tipObs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.2 });
      tipCards.forEach(function(card) { tipObs.observe(card); });
    }

    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  };

  /* ---- AI Tools page ---- */
  window.renderResumeAITools = async function (el) {
    el.innerHTML = `
    <section class="block block--hero block--hero-with-bg resume-hero resume-hero--compact">
      ${HERO_DECOR.shapes}
      ${HERO_DECOR.particlesBehind}
      <div class="block-inner">
        <p class="hero-badge">AI-powered · free</p>
        <h1 class="block-hero-title">Resume Gap Analysis</h1>
        <p class="block-hero-sub">See how your resume stacks up against a real job posting. Get an AI-powered match score, find out what's missing, and learn exactly what to add.</p>
      </div>
      ${HERO_DECOR.particlesFront}
    </section>
    <section class="block resume-ai-section">
      <div class="block-inner">
        <div id="aiKeySetup" class="reveal" style="max-width: 600px;"></div>

        <div class="gap-analysis-card reveal">
          <h2 class="gap-analysis-heading">Compare your resume to a job posting</h2>
          <p class="gap-analysis-desc">Paste your resume and a job description below. AI will analyze the overlap and tell you exactly what to improve.</p>
          <div class="ai-tailor-grid">
            <div class="ai-tailor-col">
              <label class="ai-label">Your resume</label>
              <textarea class="ai-textarea ai-textarea-lg" rows="10" placeholder="Paste your full resume text here..." id="gapResume"></textarea>
            </div>
            <div class="ai-tailor-col">
              <label class="ai-label">Job description</label>
              <textarea class="ai-textarea ai-textarea-lg" rows="10" placeholder="Paste the job posting you're targeting..." id="gapJob"></textarea>
            </div>
          </div>
          <button type="button" class="btn btn-primary ai-action-btn ai-tailor-btn" id="gapAnalyzeBtn">Analyze my resume <span class="btn-arrow" aria-hidden="true">→</span></button>
          <p class="ai-error" id="gapError" style="display:none;"></p>
        </div>

        <div id="gapResults" class="gap-results" style="display:none;">
          <div class="gap-results-top">
            <div class="gap-chart-wrap">
              <div class="gap-chart-ring">
                <canvas id="gapChart" width="220" height="220"></canvas>
                <div class="gap-chart-center">
                  <span class="gap-chart-score" id="gapScoreLabel">0%</span>
                  <span class="gap-chart-score-label">match</span>
                </div>
              </div>
            </div>
            <div class="gap-summary-wrap">
              <h3 class="gap-summary-title">Overview</h3>
              <p class="gap-summary-text" id="gapSummaryText"></p>
              <div class="gap-strengths" id="gapStrengths"></div>
            </div>
          </div>
          <div class="gap-section">
            <h3 class="gap-section-title">Missing keywords &amp; skills</h3>
            <p class="gap-section-desc">These appeared in the job description but not in your resume. Adding them can help you pass applicant tracking systems (ATS) and show recruiters you're a fit.</p>
            <div class="gap-keywords" id="gapKeywords"></div>
          </div>
          <div class="gap-section">
            <h3 class="gap-section-title">What to add or change</h3>
            <p class="gap-section-desc">Specific, actionable steps to bring your resume closer to what this role is looking for.</p>
            <ol class="gap-suggestions" id="gapSuggestions"></ol>
          </div>
          <div class="gap-cta-bar">
            <p class="gap-cta-text">Ready to improve your resume? Use the tools below to implement these suggestions.</p>
          </div>
        </div>

        <div class="reveal" style="max-width: 600px; margin-top: 2rem;">
          <h2 class="gap-tools-heading">More AI tools</h2>
          <div id="aiBulletTool"></div>
          <div id="aiSummaryTool" style="margin-top: 0.75rem;"></div>
          <div id="aiSkillsTool" style="margin-top: 0.75rem;"></div>
        </div>
      </div>
    </section>
    <p class="resume-back-link"><a href="resume.html">← Back to Resume Builder</a></p>`;

    /* Wire up gap analysis */
    var analyzeBtn = document.getElementById('gapAnalyzeBtn');
    var errorEl = document.getElementById('gapError');

    analyzeBtn.addEventListener('click', function () {
      var resume = document.getElementById('gapResume').value.trim();
      var job = document.getElementById('gapJob').value.trim();
      if (!resume || !job) {
        errorEl.textContent = 'Please paste both your resume and the job description.';
        errorEl.style.display = 'block';
        return;
      }
      if (typeof ResumeAI === 'undefined' || !ResumeAI.canUseAI()) {
        errorEl.textContent = 'Please save your API key first.';
        errorEl.style.display = 'block';
        return;
      }
      errorEl.style.display = 'none';
      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = '<span class="gap-btn-spinner"></span> Analyzing your resume...';
      document.getElementById('gapResults').style.display = 'none';

      ResumeAI.analyzeGap(resume, job)
        .then(function (data) {
          renderGapResults(data);
          document.getElementById('gapResults').style.display = 'block';
          document.getElementById('gapResults').scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(function (e) {
          errorEl.textContent = e.message || 'Something went wrong. Please try again.';
          errorEl.style.display = 'block';
        })
        .finally(function () {
          analyzeBtn.disabled = false;
          analyzeBtn.innerHTML = 'Analyze my resume <span class="btn-arrow" aria-hidden="true">→</span>';
        });
    });

    function renderGapResults(data) {
      document.getElementById('gapSummaryText').textContent = data.summary;

      var strengthsEl = document.getElementById('gapStrengths');
      if (data.strengths.length) {
        strengthsEl.innerHTML = '<h4 class="gap-strengths-title">What you\'re doing well</h4><ul class="gap-strengths-list">' +
          data.strengths.map(function (s) { return '<li>' + s + '</li>'; }).join('') + '</ul>';
      } else {
        strengthsEl.innerHTML = '';
      }

      var keywordsEl = document.getElementById('gapKeywords');
      keywordsEl.innerHTML = data.missing_keywords.map(function (kw) {
        return '<span class="gap-keyword-tag">' + kw + '</span>';
      }).join('');

      var suggestionsEl = document.getElementById('gapSuggestions');
      suggestionsEl.innerHTML = data.suggestions.map(function (s) {
        return '<li>' + s + '</li>';
      }).join('');

      animateGapChart(data.match_score);
    }

    function animateGapChart(score) {
      var canvas = document.getElementById('gapChart');
      if (!canvas) return;
      var ctx = canvas.getContext('2d');
      var dpr = window.devicePixelRatio || 1;
      var size = 220;
      canvas.width = size * dpr;
      canvas.height = size * dpr;
      canvas.style.width = size + 'px';
      canvas.style.height = size + 'px';
      ctx.scale(dpr, dpr);

      var cx = size / 2;
      var cy = size / 2;
      var radius = size / 2 - 12;
      var lineWidth = 18;
      var startAngle = -Math.PI / 2;
      var duration = 1200;
      var startTime = null;

      var scoreColor = score >= 70 ? '#7FAF9D' : score >= 40 ? '#4FA3A5' : '#C8766A';
      var trackColor = 'rgba(31, 42, 68, 0.08)';
      var labelEl = document.getElementById('gapScoreLabel');

      function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

      function frame(timestamp) {
        if (!startTime) startTime = timestamp;
        var elapsed = timestamp - startTime;
        var progress = Math.min(elapsed / duration, 1);
        var eased = easeOutCubic(progress);
        var currentScore = Math.round(eased * score);
        var sweepAngle = (eased * score / 100) * Math.PI * 2;

        ctx.clearRect(0, 0, size, size);

        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        ctx.strokeStyle = trackColor;
        ctx.lineWidth = lineWidth;
        ctx.lineCap = 'round';
        ctx.stroke();

        if (sweepAngle > 0.01) {
          ctx.beginPath();
          ctx.arc(cx, cy, radius, startAngle, startAngle + sweepAngle);
          ctx.strokeStyle = scoreColor;
          ctx.lineWidth = lineWidth;
          ctx.lineCap = 'round';
          ctx.stroke();
        }

        labelEl.textContent = currentScore + '%';

        if (progress < 1) requestAnimationFrame(frame);
      }

      requestAnimationFrame(frame);
    }

    /* Wire up AI tools */
    if (typeof ResumeAI !== 'undefined') {
      ResumeAI.checkServer().then(function(serverOk) {
        var keyEl = document.getElementById('aiKeySetup');
        if (serverOk) {
          keyEl.appendChild(ResumeAI.createServerBadge());
        } else {
          keyEl.appendChild(ResumeAI.createKeySetup());
        }
        document.getElementById('aiBulletTool').appendChild(ResumeAI.createBulletEnhancer('your major'));
        document.getElementById('aiSummaryTool').appendChild(ResumeAI.createSummaryGenerator('your major'));
        document.getElementById('aiSkillsTool').appendChild(ResumeAI.createSkillsSuggester('your major'));
      });
    }

    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  };
})();
