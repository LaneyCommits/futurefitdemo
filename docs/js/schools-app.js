/**
 * Schools finder static site app — loads schools-data.json and renders the page.
 */
(function () {
  var MAJOR_LABELS = {
    business: 'Business & Management',
    computer_science: 'Computer Science & IT',
    engineering: 'Engineering',
    health_sciences: 'Health Sciences & Nursing',
    humanities: 'Humanities',
    social_sciences: 'Social Sciences',
    arts_design: 'Arts & Design',
    education: 'Education',
    environmental: 'Environmental & Sustainability',
    communications: 'Communications & Media',
    law: 'Law & Criminal Justice',
    agriculture: 'Agriculture & Natural Resources',
    hospitality: 'Hospitality & Tourism',
    real_estate: 'Real Estate & Property',
    sports_recreation: 'Sports & Recreation',
    trades_construction: 'Skilled Trades & Construction'
  };

  var US_STATES = [
    ['AL','Alabama'],['AK','Alaska'],['AZ','Arizona'],['AR','Arkansas'],['CA','California'],
    ['CO','Colorado'],['CT','Connecticut'],['DE','Delaware'],['FL','Florida'],['GA','Georgia'],
    ['HI','Hawaii'],['ID','Idaho'],['IL','Illinois'],['IN','Indiana'],['IA','Iowa'],
    ['KS','Kansas'],['KY','Kentucky'],['LA','Louisiana'],['ME','Maine'],['MD','Maryland'],
    ['MA','Massachusetts'],['MI','Michigan'],['MN','Minnesota'],['MS','Mississippi'],
    ['MO','Missouri'],['MT','Montana'],['NE','Nebraska'],['NV','Nevada'],['NH','New Hampshire'],
    ['NJ','New Jersey'],['NM','New Mexico'],['NY','New York'],['NC','North Carolina'],
    ['ND','North Dakota'],['OH','Ohio'],['OK','Oklahoma'],['OR','Oregon'],['PA','Pennsylvania'],
    ['RI','Rhode Island'],['SC','South Carolina'],['SD','South Dakota'],['TN','Tennessee'],
    ['TX','Texas'],['UT','Utah'],['VT','Vermont'],['VA','Virginia'],['WA','Washington'],
    ['WV','West Virginia'],['WI','Wisconsin'],['WY','Wyoming'],['DC','District of Columbia']
  ];

  var COST_BRACKETS = [
    {key:'low',label:'Under $15k',low:0,high:15000},
    {key:'mid',label:'$15k – $30k',low:15000,high:30000},
    {key:'high',label:'$30k – $50k',low:30000,high:50000},
    {key:'premium',label:'$50k+',low:50000,high:999999}
  ];

  window.renderSchoolsPage = async function (el) {
    var resp = await fetch('js/schools-data.json');
    var SCHOOLS = await resp.json();

    var params = new URLSearchParams(window.location.search);
    var preselect = params.get('major') || '';

    var majorOpts = Object.entries(MAJOR_LABELS).map(function(e) {
      return '<option value="' + e[0] + '"' + (e[0] === preselect ? ' selected' : '') + '>' + e[1] + '</option>';
    }).join('');

    var stateOpts = US_STATES.map(function(s) {
      return '<option value="' + s[0] + '">' + s[1] + '</option>';
    }).join('');

    var costOpts = COST_BRACKETS.map(function(c) {
      return '<option value="' + c.key + '" data-low="' + c.low + '" data-high="' + c.high + '">' + c.label + '</option>';
    }).join('');

    var heroShapes = '<div class="hero-shapes" aria-hidden="true"><div class="hero-shape hero-shape--orb hero-shape-1"></div><div class="hero-shape hero-shape--orb hero-shape-2"></div><div class="hero-shape hero-shape--orb hero-shape-3"></div><div class="hero-shape hero-shape--blob hero-shape-4"></div><div class="hero-shape hero-shape--prism hero-shape-5"></div><div class="hero-shape hero-shape--prism hero-shape-6"></div><div class="hero-shape hero-shape--glow hero-shape-7"></div><div class="hero-shape hero-shape--glow hero-shape-8"></div></div>';
    var heroParticlesBehind = '<div class="hero-particles hero-particles--behind" aria-hidden="true"><span class="hero-particle hero-particle--s" style="--x: 9%; --y: 16%; --d: 0"></span><span class="hero-particle hero-particle--m" style="--x: 86%; --y: 24%; --d: 0.9"></span><span class="hero-particle hero-particle--s" style="--x: 14%; --y: 46%; --d: 1.6"></span><span class="hero-particle hero-particle--l" style="--x: 76%; --y: 52%; --d: 0.2"></span><span class="hero-particle hero-particle--accent" style="--x: 26%; --y: 32%; --d: 0.4"></span><span class="hero-particle hero-particle--accent hero-particle--s" style="--x: 70%; --y: 44%; --d: 1.5"></span></div>';
    var heroParticlesFront = '<div class="hero-particles hero-particles--front" aria-hidden="true"><span class="hero-particle hero-particle--m" style="--x: 28%; --y: 20%; --d: 0.6"></span><span class="hero-particle hero-particle--s" style="--x: 68%; --y: 38%; --d: 1.0"></span><span class="hero-particle hero-particle--accent hero-particle--s" style="--x: 52%; --y: 82%; --d: 0.7"></span></div>';

    el.innerHTML = `
    <section class="block block--hero block--hero-with-bg schools-hero">
      ${heroShapes}
      ${heroParticlesBehind}
      <div class="block-inner">
        <p class="hero-badge">${SCHOOLS.length} schools · 16 majors · free</p>
        <h1 class="block-hero-title">Find the right school for you</h1>
        <p class="block-hero-sub">Filter by major, location, cost, and school type to find colleges that fit your goals — not just what's trending.</p>
      </div>
      ${heroParticlesFront}
    </section>
    <section class="block schools-content-section">
      <div class="block-inner">
        ${preselect ? '<div class="schools-quiz-badge reveal" id="schools-quiz-badge"><span class="schools-quiz-badge-icon">🎯</span><span class="schools-quiz-badge-text">Showing schools strong in <strong id="quiz-major-label">' + (MAJOR_LABELS[preselect] || preselect) + '</strong> based on your quiz results</span><button type="button" class="schools-quiz-badge-clear" id="clear-quiz-filter" title="Clear filter">✕</button></div>' : ''}
        <div class="schools-filters reveal" id="schools-filters">
          <div class="schools-filter-group">
            <label class="schools-filter-label" for="filter-major">Major</label>
            <select class="schools-filter-select" id="filter-major"><option value="">All majors</option>${majorOpts}</select>
          </div>
          <div class="schools-filter-group">
            <label class="schools-filter-label" for="filter-state">State</label>
            <select class="schools-filter-select" id="filter-state"><option value="">Any state</option>${stateOpts}</select>
          </div>
          <div class="schools-filter-group">
            <label class="schools-filter-label" for="filter-cost">Cost (in-state tuition)</label>
            <select class="schools-filter-select" id="filter-cost"><option value="">Any cost</option>${costOpts}</select>
          </div>
          <div class="schools-filter-group">
            <label class="schools-filter-label" for="filter-type">School type</label>
            <select class="schools-filter-select" id="filter-type"><option value="">All types</option><option value="public">Public</option><option value="private">Private</option></select>
          </div>
        </div>
        <div class="schools-results-bar reveal" id="schools-results-bar">
          <span class="schools-results-count" id="schools-count">${SCHOOLS.length} schools</span>
          <button type="button" class="schools-clear-btn" id="clear-all-btn">Clear filters</button>
        </div>
        <div class="schools-grid" id="schools-grid"></div>
        <p class="schools-no-results" id="schools-no-results" style="display:none;">No schools match your filters. Try broadening your search.</p>
      </div>
    </section>
    <section class="block block--cream reveal">
      <div class="block-inner block-inner--narrow">
        <h2 class="block-title">Not sure what major to pick?</h2>
        <p class="block-desc block-desc--why">Take our career quiz to discover which fields match your personality and interests — then come back to find schools that are strong in those areas.</p>
        <a href="quiz.html" class="btn btn-primary">Take the career quiz <span class="btn-arrow" aria-hidden="true">→</span></a>
      </div>
    </section>`;

    var grid = document.getElementById('schools-grid');
    var countEl = document.getElementById('schools-count');
    var noResults = document.getElementById('schools-no-results');
    var filterMajor = document.getElementById('filter-major');
    var filterState = document.getElementById('filter-state');
    var filterCost = document.getElementById('filter-cost');
    var filterType = document.getElementById('filter-type');
    var clearAllBtn = document.getElementById('clear-all-btn');
    var quizBadge = document.getElementById('schools-quiz-badge');
    var clearQuiz = document.getElementById('clear-quiz-filter');
    var quizMajorLabel = document.getElementById('quiz-major-label');

    function formatCost(n) {
      if (n >= 1000) return '$' + (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1) + 'k';
      return '$' + n;
    }

    var LIGHT_PILL_MAJORS = { business: 1, health_sciences: 1, education: 1, computer_science: 1, communications: 1, law: 1 };
    function majorPills(majors) {
      return majors.map(function(m) {
        var lightClass = LIGHT_PILL_MAJORS[m] ? ' school-major-pill--light' : '';
        return '<span class="school-major-pill' + lightClass + '">' + (MAJOR_LABELS[m] || m) + '</span>';
      }).join('');
    }

    function schoolCard(s, idx) {
      var typeBadge = s.type === 'public'
        ? '<span class="school-type-badge school-type-badge--public">Public</span>'
        : '<span class="school-type-badge school-type-badge--private">Private</span>';
      var delayClass = idx < 6 ? ' reveal-delay-' + (idx % 3) : '';
      var imgTag = s.image ? '<img class="school-card-image" src="' + s.image + '" alt="' + s.name + ' campus" loading="lazy">' : '';
      return '<div class="school-card reveal' + delayClass + '">' +
        imgTag +
        '<div class="school-card-body">' +
        '<div class="school-card-top">' + typeBadge + '<span class="school-accept-badge">' + s.acceptance_rate + '% accept</span></div>' +
        '<h3 class="school-card-name">' + s.name + '</h3>' +
        '<p class="school-card-location">' + s.city + ', ' + s.state + '</p>' +
        '<p class="school-card-highlight">' + s.highlight + '</p>' +
        '<div class="school-card-stats">' +
          '<div class="school-stat"><span class="school-stat-value">' + formatCost(s.tuition_in) + '</span><span class="school-stat-label">in-state</span></div>' +
          '<div class="school-stat"><span class="school-stat-value">' + s.acceptance_rate + '%</span><span class="school-stat-label">acceptance</span></div>' +
          '<div class="school-stat"><span class="school-stat-value">' + s.size + '</span><span class="school-stat-label">campus</span></div>' +
        '</div>' +
        '<div class="school-card-majors">' + majorPills(s.strong_majors) + '</div>' +
        '<a href="' + s.url + '" target="_blank" rel="noopener" class="school-card-link">Visit website <span class="btn-arrow" aria-hidden="true">→</span></a>' +
        '</div>' +
      '</div>';
    }

    function render() {
      var major = filterMajor.value;
      var state = filterState.value;
      var costOpt = filterCost.options[filterCost.selectedIndex];
      var costLow = costOpt && costOpt.dataset.low ? parseInt(costOpt.dataset.low) : 0;
      var costHigh = costOpt && costOpt.dataset.high ? parseInt(costOpt.dataset.high) : 999999;
      var type = filterType.value;

      var filtered = SCHOOLS.filter(function(s) {
        if (major && s.strong_majors.indexOf(major) === -1) return false;
        if (state && s.state !== state) return false;
        if (filterCost.value && (s.tuition_in < costLow || s.tuition_in > costHigh)) return false;
        if (type && s.type !== type) return false;
        return true;
      });

      filtered.sort(function(a, b) {
        if (major) {
          var aMajorIdx = a.strong_majors.indexOf(major);
          var bMajorIdx = b.strong_majors.indexOf(major);
          if (aMajorIdx !== bMajorIdx) return aMajorIdx - bMajorIdx;
        }
        return a.tuition_in - b.tuition_in;
      });

      grid.innerHTML = filtered.map(function(s, i) { return schoolCard(s, i); }).join('');
      countEl.textContent = filtered.length + ' school' + (filtered.length !== 1 ? 's' : '');
      noResults.style.display = filtered.length === 0 ? 'block' : 'none';

      if (quizBadge) {
        quizBadge.style.display = major ? 'flex' : 'none';
        if (quizMajorLabel && MAJOR_LABELS[major]) quizMajorLabel.textContent = MAJOR_LABELS[major];
      }

      if (typeof initReveal === 'function') requestAnimationFrame(function() { initReveal(); });
    }

    filterMajor.addEventListener('change', render);
    filterState.addEventListener('change', render);
    filterCost.addEventListener('change', render);
    filterType.addEventListener('change', render);

    clearAllBtn.addEventListener('click', function() {
      filterMajor.value = '';
      filterState.value = '';
      filterCost.value = '';
      filterType.value = '';
      render();
    });

    if (clearQuiz) {
      clearQuiz.addEventListener('click', function() {
        filterMajor.value = '';
        render();
      });
    }

    render();

    requestAnimationFrame(function() {
      if (typeof initReveal === 'function') initReveal();
    });
  };
})();
