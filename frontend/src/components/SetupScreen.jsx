import React, { useState } from "react";

export default function SetupScreen({ categories, onStart, loading, error }) {
  const [selectedCategory, setSelectedCategory] = useState("any");
  const [selectedDifficulty, setSelectedDifficulty] = useState("any");
  const [questionCount, setQuestionCount] = useState(10);

  const difficulties = [
    { id: "any", label: "Any" },
    { id: "easy", label: "Easy" },
    { id: "medium", label: "Medium" },
    { id: "hard", label: "Hard" },
  ];

  const counts = [5, 10, 15];

  const handleSubmit = (e) => {
    e.preventDefault();
    onStart({
      category: selectedCategory === "any" ? null : selectedCategory,
      difficulty: selectedDifficulty === "any" ? null : selectedDifficulty,
      amount: questionCount,
    });
  };

  return (
    <div className="card">
      <div className="setup-header">
        <h1 className="setup-title">Test Your Knowledge</h1>
        <p className="setup-subtitle">
          Customize your trivia challenge with dynamically fetched questions.
        </p>
      </div>

      {error && <div className="alert-error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="category-select">
            Category
          </label>
          <select
            id="category-select"
            className="select-control"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            disabled={loading}
          >
            <option value="any">🎲 Any / Random Category</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Difficulty</label>
          <div className="pill-group">
            {difficulties.map((diff) => (
              <button
                key={diff.id}
                type="button"
                className={`pill-button ${selectedDifficulty === diff.id ? "active" : ""}`}
                onClick={() => setSelectedDifficulty(diff.id)}
                disabled={loading}
              >
                {diff.label}
              </button>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Number of Questions</label>
          <div className="pill-group">
            {counts.map((count) => (
              <button
                key={count}
                type="button"
                className={`pill-button ${questionCount === count ? "active" : ""}`}
                onClick={() => setQuestionCount(count)}
                disabled={loading}
              >
                {count} Questions
              </button>
            ))}
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? (
            <>
              <span className="spinner"></span>
              <span>Crafting Quiz...</span>
            </>
          ) : (
            <>
              <span>⚡ Start Quiz</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
