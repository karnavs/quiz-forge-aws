import React from "react";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <p>
          Trivia questions provided by{" "}
          <a href="https://opentdb.com/" target="_blank" rel="noopener noreferrer">
            Open Trivia Database (OpenTDB)
          </a>
          . Question content is licensed under{" "}
          <a
            href="https://creativecommons.org/licenses/by-sa/4.0/"
            target="_blank"
            rel="noopener noreferrer"
          >
            CC BY-SA 4.0
          </a>
          .
        </p>
        <p style={{ marginTop: "6px" }}>
          Built with AWS Lambda, API Gateway, DynamoDB, S3, and CloudFront.
        </p>
      </div>
    </footer>
  );
}
