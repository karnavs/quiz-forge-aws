# QuizForge ⚡

[![Live Demo](https://img.shields.io/badge/Live%20Demo-CloudFront%20HTTPS-brightgreen?style=for-the-badge&logo=amazon-aws)](https://d2ow1z0hk69nhf.cloudfront.net/)
[![AWS Architecture](https://img.shields.io/badge/AWS-Serverless-orange?style=for-the-badge&logo=amazonaws)](https://aws.amazon.com)
[![Trivia API](https://img.shields.io/badge/API-OpenTDB-blue?style=for-the-badge)](https://opentdb.com)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

**QuizForge** is an enterprise-grade serverless trivia quiz application built on **Amazon Web Services (AWS)**. It pulls dynamic questions from the free [Open Trivia Database (OpenTDB)](https://opentdb.com/) API, validates answers securely server-side to prevent client inspection/cheating, and serves users globally with low-latency edge caching and 100% serverless infrastructure.

---

## 🌐 Live Deployments

| Component | AWS Service | Live Endpoint |
| :--- | :--- | :--- |
| **Production Frontend** | Amazon CloudFront (Global CDN) | [https://d2owlz0hk69nhf.cloudfront.net](https://d2owlz0hk69nhf.cloudfront.net) |
| **S3 Origin Website** | Amazon S3 Static Hosting | [http://quizforge-frontend-415600258281.s3-website.eu-north-1.amazonaws.com](http://quizforge-frontend-415600258281.s3-website.eu-north-1.amazonaws.com) |
| **Microservice Backend** | AWS Lambda (Function URL) | [https://6u4dq632amszvbqxyrgxu37bky0vkjfe.lambda-url.eu-north-1.on.aws/categories](https://6u4dq632amszvbqxyrgxu37bky0vkjfe.lambda-url.eu-north-1.on.aws/categories) |
| **NoSQL Session Store** | Amazon DynamoDB | `QuizForge-Sessions` (`eu-north-1`) |

---

## 🌟 Key Capabilities

- **Dynamic Trivia Generation**: Questions retrieved in real-time across 24+ categories (General Knowledge, Science & Nature, Computers, History, Geography, Sports, Film, etc.) and 3 difficulty tiers.
- **Server-Side Scoring & Security**: The client **never** receives answer keys prior to submission. Quiz sessions are persisted in DynamoDB; user choices are scored and evaluated securely inside AWS Lambda.
- **Modern Minimalist UI**: High-contrast, monochromatic dark theme with zero unnecessary bloat, smooth progress bars, responsive category selection, and instant score breakdowns.
- **100% AWS Free-Tier & Zero Idle Cost**: Built entirely with serverless primitives ($0.00/month idle cost) requiring no continuous EC2 instances or NAT Gateways.
- **Global Edge Performance**: Cached and accelerated through AWS CloudFront's global edge network with automated SSL/TLS encryption.

---

## 🏗️ Architecture Blueprint

```text
                               ┌──────────────────────────────────────────────┐
                               │             AWS Global Edge                  │
                               │                                              │
[ Client Browser / Mobile ] ──►│   Amazon CloudFront (CDN + SSL Termination)  │
                               │        https://d2owlz0hk69nhf.cloudfront.net │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                                      ▼
                                       ┌─────────────────────────────┐
                                       │   Amazon S3 (Static Bucket) │
                                       │   index.html, style.css,    │
                                       │   app.js                    │
                                       └─────────────────────────────┘

                                                      │ (AJAX / Fetch)
                                                      ▼
                                       ┌─────────────────────────────┐
                                       │   AWS Lambda (Function URL) │
                                       │   - Route Handler           │
                                       │   - Base64 Payload Parser   │
                                       │   - CORS Formatter          │
                                       └──────┬───────────────┬──────┘
                                              │               │
                                              ▼               ▼
                                   ┌────────────────┐   ┌───────────────────────────┐
                                   │ Open Trivia DB │   │ Amazon DynamoDB           │
                                   │  (OpenTDB API) │   │ Table: QuizForge-Sessions │
                                   └────────────────┘   │ Key: quizID (String)      │
                                                        └───────────────────────────┘
```

---

## 📁 Repository Structure

```text
quiz-forge-aws/
├── backend/
│   ├── index.js                    # Consolidated Lambda handler (routes, OpenTDB proxy, grading)
│   ├── dynamodb.js                 # DynamoDB document client & in-memory fallback
│   ├── package.json                # Backend dependencies
│   └── local-server.js             # Local express development harness
├── public/                         # Production frontend (deployed to S3)
│   ├── index.html                  # Single-page application markup
│   ├── style.css                   # Responsive dark-theme styling
│   └── app.js                      # Quiz orchestration logic & API consumer
├── frontend/                       # Optional React + Vite frontend source
│   ├── src/                        # Componentized React screens (Setup, Quiz, Results)
│   ├── vite.config.js              # Vite bundler configuration
│   └── package.json                # React frontend manifest
├── docs/                           # Documentation & Presentation collateral
│   ├── QuizForge_Professor_Demo_Guide.pdf # Detailed step-by-step blueprint & viva defense guide
│   ├── QuizForge_Presentation.pptx # 5-slide academic presentation deck
│   ├── ARCHITECTURE.md             # In-depth architectural trade-off analysis
│   └── DEMO_CHEATSHEET.txt         # 5-minute rapid live demo cheatsheet
├── policies/
│   ├── s3_bucket_policy.json       # S3 public read bucket policy
│   └── dynamodb_table_schema.json  # DynamoDB table definition
├── template.yaml                   # AWS SAM / CloudFormation automation template
└── README.md                       # Comprehensive project documentation
```

---

## 🚀 Quick Setup & Deployment Runbook

### Step 1: Create DynamoDB Table
1. Name: `QuizForge-Sessions`
2. Partition Key: `quizID` (String)
3. Capacity: On-Demand (`PAY_PER_REQUEST`)

### Step 2: Deploy AWS Lambda Function
1. Name: `QuizForge-Backend`, Runtime: `Node.js 20.x` or `22.x`.
2. Role: Basic Lambda execution with DynamoDB read/write access.
3. Zip files from `backend/` and upload to Lambda.

### Step 3: Enable Lambda Function URL
1. Auth Type: `NONE` (Public invoke).
2. **⚠️ CORS Alert:** Ensure the AWS Console CORS checkbox is **UNCHECKED** (Lambda code handles CORS headers natively; enabling both creates duplicate `*, *` headers that browsers reject).

### Step 4: Configure Frontend
Update Line 2 in `public/app.js` with your generated Function URL:
```javascript
const API_BASE = window.QUIZFORGE_API_URL || "https://<YOUR-FUNCTION-URL>";
```

### Step 5: Host on Amazon S3
1. Create bucket: `quizforge-frontend-<unique-id>`.
2. Uncheck *Block all public access*.
3. Enable *Static website hosting* with index `index.html`.
4. Apply bucket policy from `policies/s3_bucket_policy.json`.
5. Upload `public/index.html`, `public/style.css`, and `public/app.js`.

### Step 6: Attach CloudFront CDN
1. Origin: S3 Website Endpoint.
2. Viewer Protocol: Redirect HTTP to HTTPS.
3. WAF: Do not enable security protections ($0 fee).
4. Default root object: `index.html`.

---

## 📜 Attribution & Licensing

- **Trivia Questions**: Powered by the [Open Trivia Database (OpenTDB)](https://opentdb.com/) under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
- **Application Code**: Licensed under the [MIT License](LICENSE).
