import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import SetupScreen from "./components/SetupScreen";
import QuizScreen from "./components/QuizScreen";
import ResultsScreen from "./components/ResultsScreen";
import { fetchCategories, createQuiz, submitQuiz } from "./api";

export default function App() {
  const [screen, setScreen] = useState("SETUP"); // "SETUP" | "QUIZ" | "RESULTS"
  const [categories, setCategories] = useState([]);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCategories() {
      try {
        const data = await fetchCategories();
        setCategories(data.categories || []);
      } catch (err) {
        console.warn("Could not load categories initially:", err);
      }
    }
    loadCategories();
  }, []);

  const handleStartQuiz = async (params) => {
    setLoading(true);
    setError(null);
    try {
      const data = await createQuiz(params);
      setActiveQuiz(data);
      setScreen("QUIZ");
    } catch (err) {
      setError(err.message || "Failed to start quiz. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitQuiz = async (answers) => {
    if (!activeQuiz?.quizId) return;
    setLoading(true);
    setError(null);
    try {
      const result = await submitQuiz(activeQuiz.quizId, answers);
      setQuizResult(result);
      setScreen("RESULTS");
    } catch (err) {
      setError(err.message || "Failed to submit answers.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setActiveQuiz(null);
    setQuizResult(null);
    setError(null);
    setScreen("SETUP");
  };

  return (
    <>
      <Navbar onReset={handleReset} />
      <main className="main-content">
        <div className="container">
          {screen === "SETUP" && (
            <SetupScreen
              categories={categories}
              onStart={handleStartQuiz}
              loading={loading}
              error={error}
            />
          )}

          {screen === "QUIZ" && activeQuiz && (
            <QuizScreen
              quiz={activeQuiz}
              onSubmit={handleSubmitQuiz}
              submitting={loading}
              error={error}
            />
          )}

          {screen === "RESULTS" && quizResult && (
            <ResultsScreen result={quizResult} onPlayAgain={handleReset} />
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
