// QuizForge — Minimalist, Clean Frontend Logic
const API_BASE = window.QUIZFORGE_API_URL || "https://6u4dq632amszvbqxyrgxu37bky0vkjfe.lambda-url.eu-north-1.on.aws";

let state = {
  categories: [],
  selectedCategory: "any",
  selectedDifficulty: "any",
  questionCount: 10,
  activeQuiz: null,
  currentIndex: 0,
  answers: {}, // questionId -> selectedOption
  quizResult: null,
  loading: false,
};

// Elements
const setupView = document.getElementById("setup-view");
const quizView = document.getElementById("quiz-view");
const resultsView = document.getElementById("results-view");
const categorySelect = document.getElementById("category-select");
const setupError = document.getElementById("setup-error");
const startBtn = document.getElementById("start-btn");

document.addEventListener("DOMContentLoaded", () => {
  loadCategories();
  bindEvents();
});

async function loadCategories() {
  try {
    const res = await fetch(`${API_BASE}/categories`);
    if (res.ok) {
      const data = await res.json();
      state.categories = data.categories || [];
      renderCategoryOptions();
    } else {
      renderDefaultCategories();
    }
  } catch {
    renderDefaultCategories();
  }
}

function renderCategoryOptions() {
  categorySelect.innerHTML = `<option value="any">Any Category</option>`;
  state.categories.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = cat.id;
    opt.textContent = cat.name;
    categorySelect.appendChild(opt);
  });
}

function renderDefaultCategories() {
  state.categories = [
    { id: 9, name: "General Knowledge" },
    { id: 18, name: "Science: Computers" },
    { id: 23, name: "History" },
    { id: 21, name: "Sports" },
    { id: 11, name: "Entertainment: Film" },
    { id: 12, name: "Entertainment: Music" },
    { id: 15, name: "Entertainment: Video Games" },
  ];
  renderCategoryOptions();
}

function bindEvents() {
  document.getElementById("nav-brand-btn").addEventListener("click", resetToSetup);

  document.querySelectorAll(".diff-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".diff-pill").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.selectedDifficulty = btn.dataset.diff;
    });
  });

  document.querySelectorAll(".count-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".count-pill").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.questionCount = parseInt(btn.dataset.count, 10);
    });
  });

  categorySelect.addEventListener("change", (e) => {
    state.selectedCategory = e.target.value;
  });

  document.getElementById("setup-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    await handleStartQuiz();
  });

  document.getElementById("play-again-btn").addEventListener("click", resetToSetup);
}

async function handleStartQuiz() {
  setLoading(true);
  hideError();

  const payload = {
    category: state.selectedCategory === "any" ? null : state.selectedCategory,
    difficulty: state.selectedDifficulty === "any" ? null : state.selectedDifficulty,
    amount: state.questionCount,
  };

  try {
    const res = await fetch(`${API_BASE}/quizzes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Failed to start quiz.");
    }

    state.activeQuiz = data;
    state.currentIndex = 0;
    state.answers = {};
    showQuizScreen();
  } catch (err) {
    showError(err.message || "Failed to create quiz.");
  } finally {
    setLoading(false);
  }
}

function showQuizScreen() {
  setupView.style.display = "none";
  resultsView.style.display = "none";
  quizView.style.display = "block";
  renderCurrentQuestion();
}

function renderCurrentQuestion() {
  const quiz = state.activeQuiz;
  const questions = quiz.questions || [];
  const currentQ = questions[state.currentIndex];
  if (!currentQ) return;

  const total = questions.length;
  const percent = Math.round(((state.currentIndex + 1) / total) * 100);

  document.getElementById("quiz-category-badge").textContent = currentQ.category || "General";
  document.getElementById("quiz-counter").textContent = `Question ${state.currentIndex + 1} of ${total}`;
  document.getElementById("quiz-progress-bar").style.width = `${percent}%`;
  document.getElementById("quiz-question-text").textContent = currentQ.question;

  const container = document.getElementById("quiz-options-container");
  container.innerHTML = "";
  const letters = ["A", "B", "C", "D"];
  const currentSelection = state.answers[currentQ.id];

  (currentQ.options || []).forEach((opt, idx) => {
    const card = document.createElement("div");
    card.className = `option ${currentSelection === opt ? "selected" : ""}`;
    card.innerHTML = `
      <div class="option-key">${letters[idx] || idx + 1}</div>
      <div>${opt}</div>
    `;
    card.addEventListener("click", () => {
      state.answers[currentQ.id] = opt;
      renderCurrentQuestion();
    });
    container.appendChild(card);
  });

  const prevBtn = document.getElementById("btn-prev");
  prevBtn.disabled = state.currentIndex === 0;
  prevBtn.onclick = () => {
    if (state.currentIndex > 0) {
      state.currentIndex--;
      renderCurrentQuestion();
    }
  };

  const actionContainer = document.getElementById("quiz-action-container");
  const isLast = state.currentIndex === total - 1;
  const hasSelected = currentSelection !== undefined;

  actionContainer.innerHTML = isLast
    ? `<button type="button" class="btn-primary" id="btn-submit" style="width: auto; min-width: 140px; margin-top: 0;" ${!hasSelected ? "disabled" : ""}>Submit Quiz</button>`
    : `<button type="button" class="btn-primary" id="btn-next" style="width: auto; min-width: 110px; margin-top: 0;" ${!hasSelected ? "disabled" : ""}>Next</button>`;

  if (isLast) {
    document.getElementById("btn-submit").addEventListener("click", handleSubmitQuiz);
  } else {
    document.getElementById("btn-next").addEventListener("click", () => {
      if (state.currentIndex < total - 1) {
        state.currentIndex++;
        renderCurrentQuestion();
      }
    });
  }
}

async function handleSubmitQuiz() {
  const submitBtn = document.getElementById("btn-submit");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";
  }

  const formattedAnswers = Object.entries(state.answers).map(([qId, ans]) => ({
    questionId: Number(qId),
    answer: ans,
  }));

  try {
    const res = await fetch(`${API_BASE}/quizzes/${state.activeQuiz.quizId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers: formattedAnswers }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Failed to submit quiz.");
    }

    state.quizResult = data;
    showResultsScreen();
  } catch (err) {
    alert("Submission error: " + err.message);
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Quiz";
    }
  }
}

function showResultsScreen() {
  quizView.style.display = "none";
  setupView.style.display = "none";
  resultsView.style.display = "block";

  const { score = 0, totalQuestions = 0, percentage = 0, review = [] } = state.quizResult || {};

  document.getElementById("res-score-num").textContent = score;
  document.getElementById("res-score-total").textContent = `/ ${totalQuestions}`;
  document.getElementById("res-score-percent").textContent = `(${percentage}%)`;

  const listContainer = document.getElementById("res-review-list");
  listContainer.innerHTML = "";

  review.forEach((item, idx) => {
    const card = document.createElement("div");
    card.className = "review-item";
    card.innerHTML = `
      <div class="review-q">${idx + 1}. ${item.question}</div>
      <div class="review-answers">
        <div class="ans-row">
          <span class="ans-name">Your answer:</span>
          <span class="${item.isCorrect ? "ans-correct" : "ans-wrong"}">${item.userAnswer || "(None)"}</span>
        </div>
        ${
          !item.isCorrect
            ? `<div class="ans-row">
                 <span class="ans-name">Correct:</span>
                 <span class="ans-correct">${item.correctAnswer}</span>
               </div>`
            : ""
        }
      </div>
    `;
    listContainer.appendChild(card);
  });
}

function resetToSetup() {
  state.activeQuiz = null;
  state.quizResult = null;
  state.currentIndex = 0;
  state.answers = {};
  quizView.style.display = "none";
  resultsView.style.display = "none";
  setupView.style.display = "block";
}

function setLoading(isLoading) {
  state.loading = isLoading;
  startBtn.disabled = isLoading;
  startBtn.textContent = isLoading ? "Loading..." : "Start Quiz";
}

function showError(msg) {
  setupError.textContent = msg;
  setupError.style.display = "block";
}

function hideError() {
  setupError.style.display = "none";
}
