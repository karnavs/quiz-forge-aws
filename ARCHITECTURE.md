# QuizForge — Architecture & Technical Explanation

This document explains the architecture of QuizForge in plain, professional language to help explain the project to a professor, examiner, or interviewer.

---

## 🎓 The 30-Second Elevator Pitch

> *"QuizForge is a serverless online quiz application built using AWS. When a user requests a quiz, AWS Lambda fetches questions dynamically from the Open Trivia Database, decodes special characters, shuffles the answer options, and saves the answer key securely in Amazon DynamoDB without exposing correct answers to the browser. The frontend is hosted statically in Amazon S3 and delivered globally through Amazon CloudFront. When the user finishes the quiz, Lambda validates the answers server-side, scores the quiz, and stores the completed attempt in DynamoDB. The entire project is 100% serverless, zero-maintenance, and completely free to run on AWS."*

---

## 🏛️ Service Breakdown & Responsibilities

| Service | Role in QuizForge | Why We Chose It |
| :--- | :--- | :--- |
| **Amazon S3** | Static Website Storage | Highly durable storage for the built React frontend (`index.html`, JavaScript bundles, CSS). Configured as a private bucket. |
| **Amazon CloudFront** | CDN & Single Entry Point | Delivers frontend assets globally over HTTPS via Edge locations. CloudFront also reverse-proxies `/api/*` routes to API Gateway, providing a single domain and eliminating CORS hurdles. Uses Origin Access Control (OAC) to read privately from S3. |
| **Amazon API Gateway** | HTTP API Router | Exposes lightweight HTTP endpoints to trigger the Lambda function. Automatically handles request throttling, routing, and HTTP methods. |
| **AWS Lambda** | Serverless Compute Engine | Runs our Node.js backend logic on demand. Fetches questions from OpenTDB, sanitizes HTML entities, manages session generation, and computes scores. |
| **Amazon DynamoDB** | NoSQL Persistence | Stores active quiz sessions in `QuizForge-Sessions` (with a 2-hour TTL to auto-expire stale sessions) and user scores in `QuizForge-Attempts`. |

---

## 🔄 End-to-End Request Flow

### 1. Loading the Application
1. The user visits `https://<id>.cloudfront.net`.
2. CloudFront checks its edge cache; if not cached, it securely retrieves `index.html` from the private S3 bucket using **Origin Access Control (OAC)**.
3. The React Single Page Application (SPA) loads in the browser and sends a `GET /api/categories` request.
4. CloudFront sees the `/api/*` path pattern and forwards the request to **Amazon API Gateway**, which invokes **AWS Lambda**.
5. Lambda queries OpenTDB's category endpoint and returns the available trivia categories.

### 2. Starting a Quiz
1. The user selects a category, difficulty (e.g., Medium), and question count (e.g., 10), then clicks **"Start Quiz"**.
2. Frontend sends `POST /api/quizzes`.
3. Lambda queries OpenTDB: `https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple`.
4. Lambda parses the response code (handling errors, rate limits, or empty sets).
5. For each question, Lambda decodes HTML entities (`&quot;` &rarr; `"`, `&#039;` &rarr; `'`), shuffles the answer options, generates a unique `quizId`, and writes the session to DynamoDB.
6. **Key Security Feature**: The response sent back to the browser contains only question text and shuffled options. **The correct answer is never sent to the browser during the quiz**, preventing inspection via DevTools.

### 3. Submitting the Quiz
1. When the user finishes all questions, the frontend sends `POST /api/quizzes/{quizId}/submit` with the chosen answers.
2. Lambda looks up the quiz session in DynamoDB using `quizId`.
3. Lambda iterates through each question, compares the user's choice to the stored `correct_answer`, increments the score, and generates an answer review.
4. Lambda marks the session status as `COMPLETED` (preventing repeat submissions) and records the attempt into the `QuizForge-Attempts` table.
5. Lambda returns the final score, percentage, and question-by-question review to the browser.

---

## 🛡️ Security Highlights

1. **Origin Access Control (OAC)**: The S3 bucket has public access blocked completely. Only the CloudFront distribution's service principal can read files.
2. **Server-Side Scoring**: Scores are strictly calculated on the backend. Client payloads only contain selected options; the user cannot manipulate their score.
3. **Least Privilege IAM**: The Lambda execution role has narrow permissions restricted solely to the DynamoDB tables and CloudWatch logging.
4. **No Secrets in Code**: No API keys or AWS credentials are baked into frontend JavaScript.
