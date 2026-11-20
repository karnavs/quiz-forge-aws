const crypto = require("crypto");
const {
  saveQuizSession,
  getQuizSession,
  markSessionCompleted,
  saveQuizAttempt,
  getRecentAttempts,
} = require("./dynamodb");

// Comprehensive HTML entity decoder
function decodeHtml(html) {
  if (typeof html !== "string") return html;
  return html
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&eacute;/g, "é")
    .replace(/&Eacute;/g, "É")
    .replace(/&aacute;/g, "á")
    .replace(/&iacute;/g, "í")
    .replace(/&oacute;/g, "ó")
    .replace(/&uacute;/g, "ú")
    .replace(/&ntilde;/g, "ñ")
    .replace(/&rsquo;/g, "’")
    .replace(/&lsquo;/g, "‘")
    .replace(/&rdquo;/g, "”")
    .replace(/&ldquo;/g, "“")
    .replace(/&#(\d+);/g, (match, dec) => String.fromCharCode(dec))
    .replace(/&#x([0-9a-fA-F]+);/g, (match, hex) => String.fromCharCode(parseInt(hex, 16)));
}

// Fisher-Yates array shuffle
function shuffleArray(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// Fallback categories if OpenTDB is temporarily down
const FALLBACK_CATEGORIES = [
  { id: 9, name: "General Knowledge" },
  { id: 17, name: "Science & Nature" },
  { id: 18, name: "Science: Computers" },
  { id: 19, name: "Science: Mathematics" },
  { id: 21, name: "Sports" },
  { id: 22, name: "Geography" },
  { id: 23, name: "History" },
  { id: 24, name: "Politics" },
  { id: 25, name: "Art" },
  { id: 27, name: "Animals" },
  { id: 11, name: "Entertainment: Film" },
  { id: 12, name: "Entertainment: Music" },
  { id: 14, name: "Entertainment: Television" },
  { id: 15, name: "Entertainment: Video Games" },
  { id: 31, name: "Entertainment: Japanese Anime & Manga" },
];

function buildCorsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
    "Content-Type": "application/json",
  };
}

function respond(statusCode, body) {
  return {
    statusCode,
    headers: buildCorsHeaders(),
    body: JSON.stringify(body),
  };
}

// Core Route Handlers
async function handleGetCategories() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    const res = await fetch("https://opentdb.com/api_category.php", {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      throw new Error(`OpenTDB error: status ${res.status}`);
    }

    const data = await res.json();
    return respond(200, { categories: data.trivia_categories || FALLBACK_CATEGORIES });
  } catch (err) {
    console.warn("Failed to fetch categories from OpenTDB, using fallback:", err.message);
    return respond(200, { categories: FALLBACK_CATEGORIES });
  }
}

async function handleCreateQuiz(body) {
  let { category, difficulty, amount } = body || {};

  amount = parseInt(amount, 10);
  if (![5, 10, 15].includes(amount)) {
    amount = 10;
  }

  const queryParams = new URLSearchParams({
    amount: amount.toString(),
    type: "multiple",
  });

  if (category && category !== "any" && category !== "random") {
    queryParams.set("category", category);
  }

  if (difficulty && ["easy", "medium", "hard"].includes(difficulty.toLowerCase())) {
    queryParams.set("difficulty", difficulty.toLowerCase());
  }

  const openTdbUrl = `https://opentdb.com/api.php?${queryParams.toString()}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    const res = await fetch(openTdbUrl, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (!res.ok) {
      return respond(502, {
        error: "OpenTDB service is temporarily unreachable. Please try again shortly.",
      });
    }

    const data = await res.json();
    const code = data.response_code;

    if (code === 1) {
      return respond(400, {
        error: "Not enough questions found for this combination. Try choosing 'Any Category' or lowering the question count.",
        code: "INSUFFICIENT_QUESTIONS",
      });
    }

    if (code === 2) {
      return respond(400, {
        error: "Invalid query parameters sent to OpenTDB.",
        code: "INVALID_PARAMETERS",
      });
    }

    if (code === 5) {
      return respond(429, {
        error: "Trivia database rate limit reached. Please wait 5 seconds before trying again.",
        code: "RATE_LIMITED",
      });
    }

    if (!data.results || data.results.length === 0) {
      return respond(400, {
        error: "No questions returned. Please try different filters.",
        code: "NO_QUESTIONS",
      });
    }

    // Process questions: decode and shuffle
    const quizId = crypto.randomUUID ? crypto.randomUUID() : `q_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;

    const serverQuestions = [];
    const clientQuestions = [];

    data.results.forEach((q, idx) => {
      const qId = idx + 1;
      const decodedQuestion = decodeHtml(q.question);
      const decodedCorrect = decodeHtml(q.correct_answer);
      const decodedIncorrect = (q.incorrect_answers || []).map(decodeHtml);

      const allOptions = shuffleArray([decodedCorrect, ...decodedIncorrect]);

      // Server keeps correct_answer
      serverQuestions.push({
        id: qId,
        question: decodedQuestion,
        category: decodeHtml(q.category),
        difficulty: q.difficulty,
        correct_answer: decodedCorrect,
        options: allOptions,
      });

      // Client only gets id, question, category, difficulty, and shuffled options
      clientQuestions.push({
        id: qId,
        question: decodedQuestion,
        category: decodeHtml(q.category),
        difficulty: q.difficulty,
        options: allOptions,
      });
    });

    const now = Date.now();
    const session = {
      quizId,
      questions: serverQuestions,
      category: category || "Any",
      difficulty: difficulty || "Any",
      totalQuestions: serverQuestions.length,
      status: "ACTIVE",
      createdAt: now,
      expiresAt: Math.floor(now / 1000) + 7200, // 2-hour TTL
    };

    await saveQuizSession(session);

    return respond(201, {
      quizId,
      totalQuestions: clientQuestions.length,
      category: category || "Any",
      difficulty: difficulty || "Any",
      questions: clientQuestions,
    });
  } catch (err) {
    console.error("Error creating quiz:", err);
    return respond(500, {
      error: "Failed to generate quiz: " + err.message,
    });
  }
}

async function handleSubmitQuiz(quizId, body) {
  if (!quizId) {
    return respond(400, { error: "Missing quiz ID." });
  }

  const session = await getQuizSession(quizId);
  if (!session) {
    return respond(404, {
      error: "Quiz session not found or has expired. Please start a new quiz.",
      code: "QUIZ_NOT_FOUND",
    });
  }

  if (session.status === "COMPLETED") {
    return respond(400, {
      error: "This quiz has already been submitted.",
      code: "ALREADY_SUBMITTED",
    });
  }

  const userAnswers = Array.isArray(body?.answers) ? body.answers : [];
  const answerMap = new Map();
  userAnswers.forEach((a) => {
    if (a && a.questionId !== undefined) {
      answerMap.set(Number(a.questionId), a.answer);
    }
  });

  let correctCount = 0;
  const review = session.questions.map((q) => {
    const userAnswer = answerMap.get(q.id) || null;
    const isCorrect = userAnswer !== null && userAnswer.trim() === q.correct_answer.trim();
    if (isCorrect) correctCount++;

    return {
      id: q.id,
      question: q.question,
      category: q.category,
      difficulty: q.difficulty,
      userAnswer,
      correctAnswer: q.correct_answer,
      isCorrect,
      options: q.options,
    };
  });

  const total = session.questions.length;
  const percentage = Math.round((correctCount / total) * 100);

  // Update session status
  await markSessionCompleted(quizId);

  // Store attempt
  const attempt = {
    attemptId: `att_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
    quizId,
    score: correctCount,
    totalQuestions: total,
    percentage,
    category: session.category,
    difficulty: session.difficulty,
    completedAt: Date.now(),
  };
  await saveQuizAttempt(attempt);

  return respond(200, {
    quizId,
    score: correctCount,
    totalQuestions: total,
    percentage,
    category: session.category,
    difficulty: session.difficulty,
    review,
  });
}

async function handleGetHistory() {
  const attempts = await getRecentAttempts(10);
  return respond(200, { attempts });
}

// Main AWS Lambda Handler
exports.handler = async (event) => {
  // Normalize path & HTTP method for Function URLs, HTTP API v2 and REST API v1
  const httpMethod = event.requestContext?.http?.method || event.httpMethod || "GET";
  const rawPath = event.rawPath || event.requestContext?.http?.path || event.path || "/";
  // Strip stage or leading /api prefix if present
  const path = rawPath.replace(/^\/api/, "") || "/";

  // Handle CORS Preflight
  if (httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: buildCorsHeaders(),
      body: "",
    };
  }

  let body = {};
  if (event.body) {
    try {
      let raw = event.body;
      if (event.isBase64Encoded) {
        raw = Buffer.from(raw, "base64").toString("utf-8");
      }
      body = typeof raw === "string" ? JSON.parse(raw) : raw;
    } catch (e) {
      console.warn("Could not parse body:", e);
      body = {};
    }
  }

  // Routing
  if (httpMethod === "GET" && (path === "/categories" || path === "/")) {
    return handleGetCategories();
  }

  if (httpMethod === "POST" && (path === "/quizzes" || path === "/quizzes/")) {
    return handleCreateQuiz(body);
  }

  const submitMatch = path.match(/^\/quizzes\/([^/]+)\/submit$/);
  if (httpMethod === "POST" && submitMatch) {
    const quizId = submitMatch[1];
    return handleSubmitQuiz(quizId, body);
  }

  if (httpMethod === "GET" && path === "/history") {
    return handleGetHistory();
  }

  if (path === "/health") {
    return respond(200, { status: "ok", service: "QuizForge API" });
  }

  return respond(404, { error: `Endpoint not found: ${httpMethod} ${path}` });
};
