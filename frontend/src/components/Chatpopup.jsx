import React, { useEffect, useRef, useState } from "react";
import "./popup.css";

function ChatPopup() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);
  const [lastResponse, setLastResponse] = useState({});
  const bodyRef = useRef(null);

  const togglePopup = () => setIsOpen(!isOpen);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", content: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");

    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    const botMessage = {
      role: "bot",
      content: data.answer,
      confidence: data.confidence,
      sentiment: data.sentiment,
    };

    setMessages((prev) => [...prev, botMessage]);
    setLastResponse({ query, ...data });
    setShowFeedback(true);
  };

  const submitFeedback = async (feedbackType) => {
    await fetch("http://localhost:8000/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...lastResponse,
        feedback: feedbackType,
        email:
          feedbackType === "👎" && lastResponse.confidence < 60
            ? prompt("Please enter your email:")
            : "",
      }),
    });
    setShowFeedback(false);
  };

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <>
      <button className="chat-popup-button" onClick={togglePopup}>
        💬
      </button>
      {isOpen && (
        <div className="chat-popup">
          <div className="chat-popup-header">
            RAG-BOT
            <span
              style={{ float: "right", cursor: "pointer" }}
              onClick={togglePopup}
            >
              ❌
            </span>
          </div>
          <div className="chat-popup-body" ref={bodyRef}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-message ${msg.role}`}>
                <div>{msg.content}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="chat-popup-footer">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              placeholder="Ask something..."
            />
            <button onClick={handleSubmit}>Send</button>
          </div>
          {showFeedback && (
            <div style={{ textAlign: "center", padding: "10px" }}>
              Was this helpful?{" "}
              <button onClick={() => submitFeedback("👍")}>👍</button>{" "}
              <button onClick={() => submitFeedback("👎")}>👎</button>
            </div>
          )}
        </div>
      )}
    </>
  );
}

export default ChatPopup;
