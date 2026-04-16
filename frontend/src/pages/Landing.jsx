import { useNavigate } from "react-router-dom";
import useMediaQuery from "../hooks/useMediaQuery";
import Logo from "../components/brand/Logo";
import InsightCarousel from "../components/ui/InsightCarousel";

export default function Landing({ user }) {
  const navigate = useNavigate();
  const isDesktop = useMediaQuery("(min-width: 900px)");

  if (isDesktop) {
    return (
      <div className="landing-desktop-layout">
        {!user && (
          <button
            type="button"
            className="landing-return-link"
            onClick={() => navigate("/login")}
          >
            Return to my profile
          </button>
        )}
        <div className="ld-split">
          <div className="ld-split-left">
            <div className="ld-split-content">
              <Logo layout="horizontal" wordmarkSize="md" />
              <h1 className="ld-split-title">
                Before you choose a path, understand how you think
              </h1>
              <p className="ld-split-sub">
                A structured 5-minute assessment that maps your thinking patterns
                to real academic majors and career paths.
              </p>
              <button
                type="button"
                className="btn btn-primary btn-lg ld-split-cta"
                onClick={() => navigate("/quiz")}
              >
                Start Assessment
              </button>
              <div className="landing-meta">
                <span className="landing-meta-item">5 minutes</span>
                <span className="landing-meta-item">Evidence-based</span>
                <span className="landing-meta-item">No signup required</span>
              </div>
            </div>
          </div>
          <div className="ld-split-right">
            <div className="ld-visual">
              <img
                src="/hero-owl.png"
                alt="Calm white owl portrait"
                className="ld-owl-image"
              />
            </div>
          </div>
        </div>
        <InsightCarousel />
      </div>
    );
  }

  return (
    <div className="landing-mobile-layout">
      <div className="landing-screen">
        {!user && (
          <button
            type="button"
            className="landing-return-link"
            onClick={() => navigate("/login")}
          >
            Return to my profile
          </button>
        )}
        <div className="landing-content">
          <Logo layout="stacked" wordmarkSize="lg" />
          <h1 className="landing-title">
            Before you choose a path, understand how you think
          </h1>
          <p className="landing-subtitle">
            A structured 5-minute assessment that maps your thinking patterns to
            real academic majors and career paths.
          </p>
          <div className="landing-cta">
            <button
              type="button"
              className="btn btn-primary btn-xl"
              onClick={() => navigate("/quiz")}
            >
              Start Assessment
            </button>
          </div>
          <div className="landing-meta">
            <span className="landing-meta-item">5 minutes</span>
            <span className="landing-meta-item">Evidence-based</span>
            <span className="landing-meta-item">No signup required</span>
          </div>
        </div>
      </div>
      <InsightCarousel />
    </div>
  );
}
