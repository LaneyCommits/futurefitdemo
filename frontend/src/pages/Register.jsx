import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { register } from "../api/client";

export default function Register({ onAuth, user }) {
  const location = useLocation();
  const navigate = useNavigate();
  const pendingQuiz = location.state?.pendingQuiz || null;
  const summary =
    location.state?.summary || "Save your thinking profile so you can revisit it anytime.";
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) navigate("/dashboard");
  }, [user, navigate]);

  if (user) return null;

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await register(username, password, pendingQuiz);
      onAuth(data.token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-gate-page">
      <section className="auth-gate-context">
        <h1 className="auth-gate-title">Unlock your full thinking report</h1>
        <p className="auth-gate-copy">{summary}</p>
        <ul className="auth-gate-points">
          <li>Save your results</li>
          <li>Unlock your full thinking report</li>
          <li>See how your path compares</li>
          <li>Continue your profile</li>
        </ul>
      </section>

      <section className="auth-gate-form-wrap">
        <h2 className="auth-title">Continue your profile</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-banner">{error}</div>}
          <div className="form-group">
            <label className="form-label" htmlFor="reg-user">
              Username
            </label>
            <input
              id="reg-user"
              className="form-input"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="reg-pass">
              Password (min 8 characters)
            </label>
            <input
              id="reg-pass"
              className="form-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>
          <button
            className="btn btn-primary"
            type="submit"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save your results"}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account?{" "}
          <Link to="/login" state={{ pendingQuiz, summary }}>
            Continue your profile
          </Link>
        </p>
      </section>
    </div>
  );
}
