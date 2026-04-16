import { useState, useCallback, useMemo } from "react";
import { getQuestions, submitQuiz } from "../api/client";

/** Must match backend apps.quiz.constants.QUIZ_QUESTION_COUNT */
export const QUIZ_TOTAL = 10;

export default function useQuiz() {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  /** { [questionId]: choiceKey } — never mutate `questions` after load */
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadQuestions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getQuestions();
      if (!Array.isArray(data) || data.length !== QUIZ_TOTAL) {
        throw new Error(
          `Quiz must load exactly ${QUIZ_TOTAL} questions. Try re-running seed_quiz.`,
        );
      }
      setQuestions(data);
      setCurrentIndex(0);
      setAnswers({});
      setResults(null);
    } catch (err) {
      setError(err.message);
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const selectAnswer = useCallback((questionId, choiceKey) => {
    setAnswers((prev) => ({ ...prev, [questionId]: choiceKey }));
  }, []);

  const next = useCallback(() => {
    setCurrentIndex((i) => Math.min(i + 1, QUIZ_TOTAL - 1));
  }, []);

  const back = useCallback(() => {
    setCurrentIndex((i) => Math.max(i - 1, 0));
  }, []);

  const submit = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const orderedKeys = questions.map((q) => answers[q.id]);
      if (orderedKeys.length !== QUIZ_TOTAL || orderedKeys.some((k) => !k)) {
        throw new Error(`Please answer all ${QUIZ_TOTAL} questions before submitting.`);
      }
      const data = await submitQuiz(orderedKeys);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [questions, answers]);

  const reset = useCallback(() => {
    setQuestions([]);
    setCurrentIndex(0);
    setAnswers({});
    setResults(null);
    setError(null);
  }, []);

  /** Step indicator: 1..QUIZ_TOTAL from currentIndex only */
  const stepNumber = currentIndex + 1;
  const progressPercent = useMemo(
    () => Math.round((stepNumber / QUIZ_TOTAL) * 100),
    [stepNumber],
  );

  const isComplete =
    questions.length === QUIZ_TOTAL &&
    questions.every((q) => Boolean(answers[q.id]));

  return {
    questions,
    currentIndex,
    answers,
    results,
    loading,
    error,
    stepNumber,
    progressPercent,
    isComplete,
    loadQuestions,
    selectAnswer,
    next,
    back,
    submit,
    reset,
  };
}
