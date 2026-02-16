/**
 * Quiz results: calculating animation, then animated pie chart (analytics circle).
 */
(function () {
  var DATA_EL = document.getElementById('quiz-scores-json');
  var CALC_EL = document.getElementById('quiz-calculating');
  var CHART_EL = document.getElementById('quiz-chart-container');
  var CHART_CANVAS = document.getElementById('quiz-pie-chart');

  if (!DATA_EL || !CALC_EL || !CHART_EL) return;

  var data = [];
  try {
    data = JSON.parse(DATA_EL.textContent || '[]');
  } catch (e) {
    showChart();
    return;
  }

  if (!data.length) {
    CALC_EL.style.display = 'none';
    CHART_EL.style.display = 'none';
    return;
  }

  var total = data.reduce(function (sum, d) { return sum + d.score; }, 0);
  var segments = data.map(function (d) {
    return {
      name: d.name,
      score: d.score,
      percentage: total > 0 ? Math.round((d.score / total) * 100) : 0,
      rawRatio: total > 0 ? d.score / total : 0
    };
  });

  // Top 5 categories only
  segments = segments.slice(0, 5);
  var top5Total = segments.reduce(function (sum, s) { return sum + s.score; }, 0);
  segments.forEach(function (s) {
    s.percentage = top5Total > 0 ? Math.round((s.score / top5Total) * 100) : 0;
    s.rawRatio = top5Total > 0 ? s.score / top5Total : 0;
  });

  // FutureFit palette: 5 distinct colors matching site vibe
  var COLORS = [
    '#584053',  /* plum */
    '#8dc6bf',  /* teal */
    '#fcbc66',  /* peach */
    '#f97b4f',  /* coral */
    '#9a8a95'   /* dusty mauve */
  ];

  // --- Calculating animation: count up then hide ---
  var calcDuration = 1800;
  var startTime = null;

  function easeOutQuart(t) {
    return 1 - (1 - t) * (1 - t) * (1 - t) * (1 - t);
  }

  function animateCalculating(timestamp) {
    if (!startTime) startTime = timestamp;
    var elapsed = timestamp - startTime;
    var progress = Math.min(elapsed / calcDuration, 1);
    var eased = easeOutQuart(progress);

    var pctEl = document.getElementById('quiz-calc-percent');
    if (pctEl) pctEl.textContent = Math.round(eased * 100) + '%';

    if (progress < 1) {
      requestAnimationFrame(animateCalculating);
    } else {
      CALC_EL.classList.add('quiz-calc-done');
      setTimeout(function () {
        CALC_EL.style.display = 'none';
        showChart();
      }, 400);
    }
  }

  function showChart() {
    CHART_EL.style.display = 'block';
    CHART_EL.classList.add('quiz-chart-visible');
    drawPieChart(segments, COLORS);
  }

  function drawPieChart(segments, colors) {
    if (!CHART_CANVAS) return;
    var ctx = CHART_CANVAS.getContext('2d');
    var dpr = window.devicePixelRatio || 1;
    var size = 280;
    CHART_CANVAS.width = size * dpr;
    CHART_CANVAS.height = size * dpr;
    CHART_CANVAS.style.width = size + 'px';
    CHART_CANVAS.style.height = size + 'px';
    ctx.scale(dpr, dpr);

    var cx = size / 2;
    var cy = size / 2;
    var radius = size / 2 - 8;
    var innerRadius = radius * 0.55; // donut hole

    // Draw segments with animation (each slice grows from 0 to full)
    var duration = 900;
    var start = null;
    var PI2 = Math.PI * 2;
    var currentAngle = -Math.PI / 2; // start from top

    function drawSegment(sliceIndex, startAngle, endAngle, color, progress) {
      var from = startAngle + (endAngle - startAngle) * (1 - progress);
      var to = endAngle;
      ctx.beginPath();
      ctx.moveTo(cx + innerRadius * Math.cos(from), cy + innerRadius * Math.sin(from));
      ctx.lineTo(cx + radius * Math.cos(from), cy + radius * Math.sin(from));
      ctx.arc(cx, cy, radius, from, to, false);
      ctx.lineTo(cx + innerRadius * Math.cos(to), cy + innerRadius * Math.sin(to));
      ctx.arc(cx, cy, innerRadius, to, from, true);
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,0.15)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    function frame(timestamp) {
      if (!start) start = timestamp;
      var elapsed = timestamp - start;
      var progress = Math.min(elapsed / duration, 1);
      progress = 1 - Math.pow(1 - progress, 2); // ease out quad

      ctx.clearRect(0, 0, size, size);
      var angle = -Math.PI / 2;
      for (var i = 0; i < segments.length; i++) {
        var sweep = segments[i].rawRatio * PI2;
        drawSegment(i, angle, angle + sweep, colors[i % colors.length], progress);
        angle += sweep;
      }

      if (progress < 1) requestAnimationFrame(frame);
      else drawLabels();
    }

    function drawLabels() {
      var angle = -Math.PI / 2;
      for (var i = 0; i < segments.length; i++) {
        var sweep = segments[i].rawRatio * PI2;
        if (sweep > 0.12) {
          var midAngle = angle + sweep / 2;
          var midRadius = (innerRadius + radius) / 2;
          var x = cx + midRadius * Math.cos(midAngle);
          var y = cy + midRadius * Math.sin(midAngle);
          var pct = segments[i].percentage;
          var label = pct + '%';
          ctx.save();
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 13px DM Sans, system-ui, sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.shadowColor = 'rgba(0,0,0,0.35)';
          ctx.shadowBlur = 2;
          ctx.fillText(label, x, y);
          ctx.restore();
        }
        angle += sweep;
      }
      fillLegend();
    }

    function fillLegend() {
      var legend = document.getElementById('quiz-chart-legend');
      if (!legend) return;
      legend.innerHTML = '';
      segments.forEach(function (seg, i) {
        var li = document.createElement('li');
        li.className = 'quiz-legend-item';
        var span = document.createElement('span');
        span.className = 'quiz-legend-dot';
        span.style.backgroundColor = colors[i % colors.length];
        var text = document.createElement('span');
        text.textContent = seg.name + ' ' + seg.percentage + '%';
        li.appendChild(span);
        li.appendChild(text);
        legend.appendChild(li);
      });
    }

    requestAnimationFrame(frame);
  }

  // Start calculating animation
  requestAnimationFrame(animateCalculating);
})();
