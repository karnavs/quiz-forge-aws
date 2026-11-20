// API Client for QuizForge
const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/categories`);
  if (!res.ok) {
    throw new Error(`Failed to load categories: status ${res.status}`);
  }
  return res.json();
}

export async function createQuiz({ category, difficulty, amount }) {
  const res = await fetch(`${API_BASE}/quizzes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category, difficulty, amount }),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "Failed to start quiz.");
  }
  return data;
}

export async function submitQuiz(quizId, answers) {
  const res = await fetch(`${API_BASE}/quizzes/${quizId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "Failed to submit quiz.");
  }
  return data;
}

export async function fetchHistory() {
  try {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) return { attempts: [] };
    return res.json();
  } catch {
    return { attempts: [] };
  }
}
