import React, { useState } from "react";

export default function QuizScreen({ quiz, onSubmit, submitting, error }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});

  const questions = quiz.questions || [];
  const currentQ = questions[currentIndex] || {};
  const total = questions.length;
  const progressPercent = Math.round(((currentIndex + 1) / total) * 100);

  const optionLetters = ["A", "B", "C", "D"];

  const handleSelectOption = (option) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [currentQ.id]: option,
    }));
  };

  const handleNext = () => {
    if (currentIndex < total - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleSubmit = () => {
    const formattedAnswers = Object.entries(selectedAnswers).map(([qId, ans]) => ({
      questionId: Number(qId),
      answer: ans,
    }));
    onSubmit(formattedAnswers);
  };

  const currentSelection = selectedAnswers[currentQ.id];
  const isLastQuestion = currentIndex === total - 1;
  const hasAnsweredCurrent = currentSelection !== undefined;

  return (
    <div className="card">
      <div className="quiz-meta">
        <span className="badge badge-category">{currentQ.category || "General"}</span>
        <span className="badge badge-difficulty">{currentQ.difficulty || "Trivia"}</span>
      </div>

      <div className="progress-container">
        <div className="progress-bar" style={{ width: `${progressPercent}%` }}></div>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "14px" }}>
        <span style={{ fontSize: "0.85rem", color: "var(--text-muted)", fontWeight: "600" }}>
          Question {currentIndex + 1} of {total}
        </span>
        <span style={{ fontSize: "0.85rem", color: "var(--accent)", fontWeight: "700" }}>
          {progressPercent}%
        </span>
      </div>

      {error && <div className="alert-error">{error}</div>}

      <h2 className="question-text">{currentQ.question}</h2>

      <div className="options-grid">
        {(currentQ.options || []).map((opt, idx) => {
          const isSelected = currentSelection === opt;
          return (
            <div
              key={idx}
              className={`option-card ${isSelected ? "selected" : ""}`}
              onClick={() => handleSelectOption(opt)}
              role="button"
              tabIndex={0}
            >
              <div className="option-indicator">{optionLetters[idx] || idx + 1}</div>
              <div className="option-label">{opt}</div>
            </div>
          );
        })}
      </div>

      <div className="quiz-actions">
        <button
          type="button"
          className="btn-secondary"
          onClick={handlePrev}
          disabled={currentIndex === 0 || submitting}
        >
          ← Previous
        </button>

        {isLastQuestion ? (
          <button
            type="button"
            className="btn-primary"
            style={{ width: "auto", minWidth: "150px" }}
            onClick={handleSubmit}
            disabled={submitting || !hasAnsweredCurrent}
          >
            {submitting ? (
              <>
                <span className="spinner"></span>
                <span>Scoring...</span>
              </>
            ) : (
              "Submit Quiz ✓"
            )}
          </button>
        ) : (
          <button
            type="button"
            className="btn-primary"
            style={{ width: "auto", minWidth: "130px" }}
            onClick={handleNext}
            disabled={!hasAnsweredCurrent}
          >
            Next →
          </button>
        )}
      </div>
    </div>
  );
}
