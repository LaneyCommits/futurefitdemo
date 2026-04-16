import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import useQuiz, { QUIZ_TOTAL } from "../hooks/useQuiz";
import useMediaQuery from "../hooks/useMediaQuery";
import QuestionCard from "../components/quiz/QuestionCard";
import ProgressBar from "../components/ui/ProgressBar";
import Logo from "../components/brand/Logo";

function DesktopSidebar({ currentIndex, answers, questions }) {
  return (
    <div className="qd-sidebar">
      <div className="qd-sidebar-inner">
        <Logo layout="horizontal" wordmarkSize="sm" />
        <div className="qd-sidebar-steps">
          {questions.map((q, i) => {
            let cls = "qd-step";
            if (i === currentIndex) cls += " qd-step-active";
            else if (answers[q.id]) cls += " qd-step-done";
            return (
              <div key={q.id} className={cls}>
                <div className="qd-step-dot">
                  {answers[q.id] ? (
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path
                        d="M2.5 6L5 8.5L9.5 3.5"
                        stroke="currentColor"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  ) : (
                    <span>{i + 1}</span>
                  )}
                </div>
                <span className="qd-step-label">Question {i + 1}</span>
              </div>
            );
          })}
        </div>
        <div className="qd-sidebar-footer">
          {Object.keys(answers).length} of {QUIZ_TOTAL} answered
        </div>
      </div>
    </div>
  );
}

export default function Quiz() {
  const navigate = useNavigate();
  const isDesktop = useMediaQuery("(min-width: 900px)");
  const {
    questions,
    currentIndex,
    answers,
    results,
    loading,
    error,
    stepNumber,
    isComplete,
    loadQuestions,
    selectAnswer,
    next,
    back,
    submit,
  } = useQuiz();
  const [transitioning, setTransitioning] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  useEffect(() => {
    if (!results) return;
    const orderedAnswers = questions.map((q) => answers[q.id]).filter(Boolean);
    navigate("/results", {
      state: {
        results,
        pendingQuiz: { answers: orderedAnswers },
      },
    });
  }, [results, navigate, questions, answers]);

  const handleSelect = useCallback(
    (qId, key) => {
      selectAnswer(qId, key);
      if (currentIndex < QUIZ_TOTAL - 1) {
        setTransitioning(true);
        setTimeout(() => {
          next();
          setTransitioning(false);
        }, 280);
      }
    },
    [currentIndex, selectAnswer, next],
  );

  if (loading && questions.length === 0) {
    return (
      <div className="quiz-screen">
        <div className="page-center">
          <div className="loading-spinner" />
          <p>Preparing your assessment...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="quiz-screen">
        <div className="page-center">
          <p className="error-text">{error}</p>
        </div>
      </div>
    );
  }

  if (questions.length !== QUIZ_TOTAL) {
    return (
      <div className="quiz-screen">
        <div className="page-center">
          <p>Assessment unavailable. Please try again later.</p>
        </div>
      </div>
    );
  }

  const question = questions[currentIndex];
  const isLast = currentIndex === QUIZ_TOTAL - 1;

  if (isDesktop) {
    return (
      <div className="qd-layout">
        <DesktopSidebar
          currentIndex={currentIndex}
          answers={answers}
          questions={questions}
        />
        <div className="qd-main">
          <div className="qd-card">
            <div
              className={transitioning ? "quiz-slide-out" : "quiz-slide-in"}
              key={currentIndex}
            >
              <QuestionCard
                question={question}
                selectedKey={answers[question.id]}
                onSelect={handleSelect}
              />
            </div>
            <div className="qd-card-nav">
              {currentIndex > 0 ? (
                <button
                  type="button"
                  className="quiz-back-btn"
                  onClick={back}
                >
                  Back
                </button>
              ) : (
                <div />
              )}
              {isLast && isComplete ? (
                <button
                  type="button"
                  className="btn btn-primary btn-lg"
                  onClick={submit}
                  disabled={loading}
                >
                  {loading ? "Processing..." : "See Results"}
                </button>
              ) : (
                <div />
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="quiz-screen">
      <ProgressBar
        current={stepNumber}
        total={QUIZ_TOTAL}
        answers={answers}
        questions={questions}
      />
      <div className="quiz-body">
        <div
          className={transitioning ? "quiz-slide-out" : "quiz-slide-in"}
          key={currentIndex}
        >
          <QuestionCard
            question={question}
            selectedKey={answers[question.id]}
            onSelect={handleSelect}
          />
        </div>
      </div>
      <div className="quiz-bottom">
        {currentIndex > 0 ? (
          <button type="button" className="quiz-back-btn" onClick={back}>
            Back
          </button>
        ) : (
          <div />
        )}
        {isLast && isComplete ? (
          <button
            type="button"
            className="btn btn-primary btn-lg"
            onClick={submit}
            disabled={loading}
          >
            {loading ? "Processing..." : "See Results"}
          </button>
        ) : (
          <div />
        )}
      </div>
    </div>
  );
}
