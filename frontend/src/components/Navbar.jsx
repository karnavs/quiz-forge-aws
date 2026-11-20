import React from "react";

export default function Navbar({ onReset }) {
  return (
    <header className="navbar">
      <div className="container nav-container">
        <div className="nav-brand" onClick={onReset} role="button" tabIndex={0}>
          <div className="logo-badge">⚡</div>
          <span className="brand-name">QuizForge</span>
        </div>
        <span className="serverless-pill">☁️ AWS Serverless</span>
      </div>
    </header>
  );
}
