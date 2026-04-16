const BASE_URL = import.meta.env.VITE_API_URL || "";

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const headers = { "Content-Type": "application/json", ...options.headers };

  const token = localStorage.getItem("token");
  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  const data = await res.json();

  if (!res.ok) {
    const message = data.error || data.detail || JSON.stringify(data);
    throw new Error(message);
  }

  return data;
}

/** Single fetch — backend always returns exactly 10 questions. */
export function getQuestions() {
  return request("/api/quiz/questions/");
}

/** Submit exactly 10 choice keys in question order (no short/long flag). */
export function submitQuiz(answers) {
  return request("/api/quiz/submit/", {
    method: "POST",
    body: JSON.stringify({ answers }),
  });
}

export function register(username, password, pendingQuiz = null) {
  return request("/api/users/register/", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
      ...(pendingQuiz ? { pending_quiz: pendingQuiz } : {}),
    }),
  });
}

export function login(username, password, pendingQuiz = null) {
  return request("/api/users/login/", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
      ...(pendingQuiz ? { pending_quiz: pendingQuiz } : {}),
    }),
  });
}

export function getMe() {
  return request("/api/users/me/");
}

export function getDashboard() {
  return request("/api/users/dashboard/");
}
