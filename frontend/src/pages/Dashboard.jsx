import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getDashboard } from "../api/client";

function fmtDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        const res = await getDashboard();
        if (mounted) setData(res);
      } catch (err) {
        if (mounted) setError(err.message);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="page-center">
        <div className="loading-spinner" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-center">
        <p className="error-text">{error}</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Your Thinking Dashboard</h1>
        <p className="dashboard-sub">
          Saved profiles, comparison insights, and report history.
        </p>
      </header>

      {data?.latest && (
        <section className="dashboard-card">
          <h2 className="dashboard-card-title">Latest Saved Profile</h2>
          <p className="dashboard-primary">{data.latest.primary_name}</p>
          {data.latest.secondary_name && (
            <p className="dashboard-secondary">+ {data.latest.secondary_name}</p>
          )}
          <p className="dashboard-meta">Saved {fmtDate(data.latest.created_at)}</p>
        </section>
      )}

      <section className="dashboard-card">
        <h2 className="dashboard-card-title">Report History</h2>
        {!data?.history?.length ? (
          <p className="dashboard-empty">
            No saved reports yet. <Link to="/quiz">Take the assessment</Link>.
          </p>
        ) : (
          <ul className="dashboard-history">
            {data.history.map((item) => (
              <li key={item.id} className="dashboard-history-item">
                <div>
                  <strong>{item.primary_name || "Profile"}</strong>
                  {item.secondary_name ? ` + ${item.secondary_name}` : ""}
                </div>
                <span>{fmtDate(item.created_at)}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

