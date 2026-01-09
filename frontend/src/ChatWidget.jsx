import { useState } from "react";
import "./ChatWidget.css";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [msgs, setMsgs] = useState([
    { role: "bot", text: "Hi! Ask me anything about your policy or claims." },
  ]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    const msg = text.trim();
    if (!msg) return;

    // Optimistic update
    const newMsgs = [...msgs, { role: "user", text: msg }];
    setMsgs(newMsgs);
    setText("");
    setLoading(true);

    try {
      // Prepare history: map frontend msgs to {role, content}
      const history = newMsgs.map(m => ({
        role: m.role === "bot" ? "assistant" : "user",
        content: m.text
      }));

      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg, history: history }),
      });

      const data = await res.json();
      setMsgs((m) => [...m, { role: "bot", text: data.answer, sources: data.sources }]);
    } catch (e) {
      setMsgs((m) => [...m, { role: "bot", text: "Error connecting to server." }]);
    } finally {
      setLoading(false);
    }
  }

  const handleHandoff = () => {
    setMsgs((m) => [...m, { role: "bot", text: "Connecting you to a human agent... (Demo: Handoff Triggered)" }]);
  };

  return (
    <>
      <button className="chat-fab" onClick={() => setOpen(!open)}>
        {open ? "×" : "Chat"}
      </button>

      {open && (
        <div className="chat-modal">
          <div className="chat-header">
            <span>Insurance Help</span>
            <button className="handoff-btn" onClick={handleHandoff} title="Talk to a Human">
              🎧
            </button>
          </div>

          <div className="chat-body">
            {msgs.map((m, i) => (
              <div key={i} className={`bubble ${m.role}`}>
                <div>{m.text}</div>
                {m.sources && m.sources.length > 0 && (
                  <div className="citation-box">
                    <div className="citation-title">Sources:</div>
                    {m.sources.map((src, idx) => (
                      <div key={idx} className="citation-item">
                        • "{src.substring(0, 50)}..."
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && <div className="bubble bot">Thinking...</div>}
          </div>

          <div className="chat-input">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type your question..."
              onKeyDown={(e) => e.key === "Enter" && send()}
            />
            <button onClick={send} disabled={loading}>Send</button>
          </div>
        </div>
      )}
    </>
  );
}
