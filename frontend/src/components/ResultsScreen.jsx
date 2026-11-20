import React from "react";

export default function ResultsScreen({ result, onPlayAgain }) {
  const { score = 0, totalQuestions = 0, percentage = 0, review = [] } = result || {};

  const incorrectCount = totalQuestions - score;

  const getHeadline = () => {
    if (percentage === 100) return "Flawless Victory! 🏆";
    if (percentage >= 80) return "Mastermind! 🌟";
    if (percentage >= 60) return "Well Played! 👏";
    if (percentage >= 40) return "Good Effort! 👍";
    return "Keep Learning! 📚";
  };

  return (
    <div className="card">
      <div className="results-summary">
        <div className="score-circle">
          <div className="score-fraction">
            {score}/{totalQuestions}
          </div>
          <div className="score-percent">{percentage}% Score</div>
        </div>

        <h1 className="results-headline">{getHeadline()}</h1>
        <p className="results-feedback">
          Server-validated results computed by AWS Lambda backend.
        </p>

        <div className="stats-row">
          <span className="stat-pill correct">✓ {score} Correct</span>
          <span className="stat-pill incorrect">✗ {incorrectCount} Incorrect</span>
        </div>
      </div>

      <div className="review-section">
        <h2 className="review-header">Detailed Question Breakdown</h2>

        <div className="review-list">
          {review.map((item, idx) => (
            <div
              key={idx}
              className={`review-item ${item.isCorrect ? "correct" : "incorrect"}`}
            >
              <div className="review-question">
                <strong>Q{idx + 1}:</strong> {item.question}
              </div>

              <div className="review-answers">
                <div className="review-ans">
                  <span className="ans-label">Your Answer:</span>
                  <span className={item.isCorrect ? "ans-val-correct" : "ans-val-wrong"}>
                    {item.userAnswer || "(No answer selected)"}
                  </span>
                </div>

                {!item.isCorrect && (
                  <div className="review-ans">
                    <span className="ans-label">Correct:</span>
                    <span className="ans-val-correct">✓ {item.correctAnswer}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <button type="button" className="btn-primary" onClick={onPlayAgain}>
        ⚡ Play Another Quiz
      </button>
    </div>
  );
}
