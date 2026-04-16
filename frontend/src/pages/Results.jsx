import { useLocation, useNavigate } from "react-router-dom";

const ARCHETYPE_META = [
  { key: "systems_thinker", label: "Systems", tone: "sage" },
  { key: "analytical_solver", label: "Analytical", tone: "blue" },
  { key: "creative_builder", label: "Creative", tone: "teal" },
  { key: "people_strategist", label: "People", tone: "sage" },
  { key: "explorer", label: "Explorer", tone: "blue" },
  { key: "impact_visionary", label: "Visionary", tone: "teal" },
];

function firstSentence(text = "") {
  const cleaned = text.replace(/\s+/g, " ").trim();
  if (!cleaned) return "";
  const idx = cleaned.search(/[.!?]/);
  if (idx === -1) return cleaned;
  return cleaned.slice(0, idx + 1);
}

function compactLine(text = "", max = 110) {
  const line = firstSentence(text);
  if (line.length <= max) return line;
  return `${line.slice(0, max).trimEnd()}...`;
}

function pickInsightLines(behaviorBreakdown = [], thinkingProfile = "") {
  const lower = (s) => s.toLowerCase();
  const finding = (needle) =>
    behaviorBreakdown.find((line) => lower(line).includes(needle)) || "";

  const thinkingStyle =
    finding("approach") ||
    finding("engaged") ||
    firstSentence(thinkingProfile) ||
    "You tend to work best with clear cognitive patterns.";

  const learningStyle =
    finding("learn") ||
    finding("understanding") ||
    "You absorb information best when ideas are structured and practical.";

  const decisionStyle =
    finding("uncertain") ||
    finding("decision") ||
    finding("focus") ||
    "You make decisions by balancing clarity, context, and momentum.";

  return [
    compactLine(thinkingStyle, 100),
    compactLine(learningStyle, 100),
    compactLine(decisionStyle, 100),
  ];
}

function normalizeScores(scores = []) {
  const map = new Map(scores.map((s) => [s.archetype, s.score]));
  const values = ARCHETYPE_META.map((a) => map.get(a.key) ?? 0);
  const maxScore = Math.max(...values, 1);
  return ARCHETYPE_META.map((a) => ({
    ...a,
    score: map.get(a.key) ?? 0,
    percent: ((map.get(a.key) ?? 0) / maxScore) * 100,
  }));
}

export default function Results({ user }) {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results;
  const pendingQuiz = location.state?.pendingQuiz || null;

  if (!results) {
    return (
      <div className="page-center">
        <p>No results to display.</p>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => navigate("/")}
        >
          Take the Assessment
        </button>
      </div>
    );
  }

  const {
    personality,
    scores,
    identity_summary,
    behavior_breakdown,
    thinking_profile = "",
    careers,
    suggested_majors,
  } = results;

  const primaryKey = personality?.primary?.key;
  const secondaryKey = personality?.secondary?.key;
  const scoreRows = normalizeScores(scores);
  const insightLines = pickInsightLines(behavior_breakdown, thinking_profile);
  const notes = (behavior_breakdown || []).slice(0, 5);
  const majors = (suggested_majors || []).slice(0, 5);
  const careerItems = (careers || []).slice(0, 6);
  const isAuthed = Boolean(user);
  const lockSummary = compactLine(identity_summary, 140);

  return (
    <div className="report-page">
      <section className="report-header">
        <span className="report-kicker">Personal Thinking Report</span>
        <div className="report-header-row">
          <h1 className="report-primary">
            {personality?.primary?.name || "Thinking Profile"}
          </h1>
          {personality?.secondary?.name && (
            <span className="report-secondary">
              + {personality.secondary.name}
            </span>
          )}
        </div>
        <p className="report-summary">{compactLine(identity_summary, 180)}</p>
      </section>

      <section className="report-insight-strip">
        {insightLines.map((line, i) => (
          <p key={i} className="report-insight-line">
            {line}
          </p>
        ))}
      </section>

      <section className="report-scores">
        <h2 className="report-section-title">Archetype Distribution</h2>
        <div className="report-score-list">
          {scoreRows.map((row) => {
            const emphasis =
              row.key === primaryKey ? "primary" : row.key === secondaryKey ? "secondary" : "base";
            return (
              <div key={row.key} className="report-score-row">
                <span className="report-score-label">{row.label}</span>
                <div className="report-score-track">
                  <span
                    className={`report-score-fill ${emphasis} tone-${row.tone}`}
                    style={{ width: `${Math.max(row.percent, 3)}%` }}
                  />
                </div>
                <span className="report-score-value">{row.score.toFixed(1)}</span>
              </div>
            );
          })}
        </div>
      </section>

      <section className="report-pathways">
        <div className="report-pathway-card">
          <h3 className="report-subtitle">Majors</h3>
          <ul className="report-list">
            {majors.map((major) => (
              <li key={major.name} className="report-list-item">
                <span className="report-item-title">{major.name}</span>
                <span className="report-item-reason">{compactLine(major.reason, 96)}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="report-pathway-card">
          <h3 className="report-subtitle">Career Directions</h3>
          <ul className="report-list">
            {careerItems.map((career) => (
              <li key={career.title} className="report-list-item">
                <span className="report-item-title">{career.title}</span>
                <span className="report-item-reason">{compactLine(career.reason, 96)}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="report-notes">
        <h2 className="report-section-title">Insight Notes</h2>
        <ul className="report-note-list">
          {notes.map((note, idx) => (
            <li key={idx} className="report-note-item">
              {compactLine(note, 130)}
            </li>
          ))}
        </ul>
      </section>

      <section className="report-advanced">
        <h2 className="report-section-title">Advanced Insights</h2>
        <div className="report-advanced-grid">
          <article className={`report-advanced-card ${isAuthed ? "" : "locked"}`}>
            <h3>Compare Me Insights</h3>
            <p>Compare your cognitive profile against similar thinking patterns.</p>
            {!isAuthed && <div className="report-lock-overlay">Unlock full analysis</div>}
          </article>
          <article className={`report-advanced-card ${isAuthed ? "" : "locked"}`}>
            <h3>Career Deep Analysis</h3>
            <p>See deeper role fit signals and environment compatibility notes.</p>
            {!isAuthed && <div className="report-lock-overlay">Unlock full analysis</div>}
          </article>
          <article className={`report-advanced-card ${isAuthed ? "" : "locked"}`}>
            <h3>Thinking Evolution Tracking</h3>
            <p>Track how your profile changes across future assessments.</p>
            {!isAuthed && <div className="report-lock-overlay">Unlock full analysis</div>}
          </article>
          <article className={`report-advanced-card ${isAuthed ? "" : "locked"}`}>
            <h3>Extended Explanations</h3>
            <p>Access expanded interpretation notes by context and task style.</p>
            {!isAuthed && <div className="report-lock-overlay">Unlock full analysis</div>}
          </article>
        </div>
        {!isAuthed && (
          <div className="report-gate-cta">
            <p>Save your results to unlock your full thinking report and comparison tools.</p>
            <div className="report-gate-actions">
              <button
                type="button"
                className="btn btn-primary"
                onClick={() =>
                  navigate("/login", {
                    state: { pendingQuiz, summary: lockSummary },
                  })
                }
              >
                Save your results
              </button>
              <button
                type="button"
                className="btn"
                onClick={() =>
                  navigate("/register", {
                    state: { pendingQuiz, summary: lockSummary },
                  })
                }
              >
                Unlock full analysis
              </button>
            </div>
          </div>
        )}
      </section>

      <div className="report-footer">
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => navigate("/")}
        >
          Retake Assessment
        </button>
      </div>
    </div>
  );
}
