import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="app">
      <section className="hero">
        <span className="badge">CAMPUS SERVICES</span>
        <h1>Campus Complaint Management</h1>
        <p>Report campus issues, track progress, and keep your campus connected.</p>
        <div className="actions">
          <button>Submit a Complaint</button>
          <button className="secondary">Track Complaint</button>
        </div>
      </section>

      <section className="cards">
        <article><strong>01</strong><h2>Submit</h2><p>Raise a complaint with category and details.</p></article>
        <article><strong>02</strong><h2>Track</h2><p>Follow the status from submission to resolution.</p></article>
        <article><strong>03</strong><h2>Resolve</h2><p>Administrators manage and close complaints.</p></article>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(
  <StrictMode><App /></StrictMode>
);
