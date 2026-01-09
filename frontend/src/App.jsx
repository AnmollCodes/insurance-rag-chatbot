import { useState, useEffect } from "react";
import ChatWidget from "./ChatWidget";
import Experience from "./Experience";
import "./App.css"; // We'll update this too

export default function App() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <>
      <Experience />
      <main className="main-content">
        <div className="hero-section">
          <h1 className="title">
            <span className="gradient-text">Future</span> of Insurance
          </h1>
          <p className="subtitle">
            Intelligent. Responsive. <span className="highlight">Always there.</span>
          </p>
          <div className="status-badge">
            <span className="dot"></span> Systems Operational
          </div>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <h3>Fast Claims</h3>
            <p>AI-driven speed for instant results.</p>
          </div>
          <div className="feature-card">
            <h3>Secure Data</h3>
            <p>Your information is our top priority.</p>
          </div>
          <div className="feature-card">
            <h3>24/7 Support</h3>
            <p>We never sleep, so you can.</p>
          </div>
        </div>

        <ChatWidget />
      </main>
    </>
  );
}
