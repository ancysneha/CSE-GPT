import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  function getCurrentTime() {
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  const [messages, setMessages] = useState([
    {
      text: "Hello! I’m your CSE Department Assistant. Ask me anything about the department.",
      sender: "bot",
      source: "",
      category: "assistant",
      time: getCurrentTime(),
    },
  ]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const clearChat = () => {
    setMessages([
      {
        text: "Chat cleared. Ask me anything about the CSE Department.",
        sender: "bot",
        source: "",
        category: "assistant",
        time: getCurrentTime(),
      },
    ]);
  };

  const copyText = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      alert("Answer copied!");
    } catch (err) {
      console.error("Copy failed", err);
    }
  };

  const exportChat = () => {
    const content = messages
      .map(
        (msg) =>
          `[${msg.time}] ${msg.sender.toUpperCase()} (${msg.category || "general"}): ${msg.text}${
            msg.source ? `\nSource: ${msg.source}` : ""
          }`
      )
      .join("\n\n");

    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "cse_chat_history.txt";
    link.click();
  };

  const startVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice input not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };
  };

  const sendMessage = async (questionText = input) => {
    const question = questionText.trim();
    if (!question) return;

    setMessages((prev) => [
      ...prev,
      {
        text: question,
        sender: "user",
        source: "",
        category: "user",
        time: getCurrentTime(),
      },
    ]);
    setInput("");

    setMessages((prev) => [
      ...prev,
      {
        text: "Typing",
        sender: "bot",
        typing: true,
        source: "",
        category: "thinking",
        time: getCurrentTime(),
      },
    ]);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      setMessages((prev) => {
        const filtered = prev.filter((msg) => !msg.typing);
        return [
          ...filtered,
          {
            text: data.answer,
            sender: "bot",
            source: data.sources?.join(", ") || "",
            category: data.category || "general",
            time: getCurrentTime(),
          },
        ];
      });
    } catch (error) {
      setMessages((prev) => {
        const filtered = prev.filter((msg) => !msg.typing);
        return [
          ...filtered,
          {
            text: "Error connecting to backend. Make sure your FastAPI server is running.",
            sender: "bot",
            source: "",
            category: "error",
            time: getCurrentTime(),
          },
        ];
      });
      console.error(error);
    }
  };

  return (
    <div className={darkMode ? "app-bg dark" : "app-bg"}>
      <div className="app-shell">
        <header className="topbar">
          <div className="branding">
            <div className="logo-circle">🏫</div>
            <div>
              <h1>CSE-GPT</h1>
              <p>Your smart assistant for department queries</p>
            </div>
          </div>

          <div className="topbar-actions">
            <button className="toggle-btn" onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? "☀ Light" : "🌙 Dark"}
            </button>
            <button className="ghost-btn" onClick={exportChat}>
              Export Chat
            </button>
            <button className="ghost-btn" onClick={clearChat}>
              Clear Chat
            </button>
          </div>
        </header>

        <main className="chat-area">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={msg.sender === "user" ? "message-row user" : "message-row bot"}
            >
              <div className="avatar">{msg.sender === "user" ? "🧑" : "🤖"}</div>

              <div className="message-block">
                <div className={msg.sender === "user" ? "message user-msg" : "message bot-msg"}>
                  {msg.typing ? (
                    <div className="typing">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  ) : (
                    msg.text
                  )}
                </div>

                <div className="meta-row">
                  <span className="time-tag">🕒 {msg.time}</span>
                  {msg.category && <span className="category-tag">{msg.category}</span>}
                  {msg.source && msg.sender === "bot" && (
                    <span className="source-tag">📄 {msg.source}</span>
                  )}
                  {msg.sender === "bot" && !msg.typing && (
                    <button className="copy-btn" onClick={() => copyText(msg.text)}>
                      📋 Copy
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </main>

        <footer className="input-bar">
          <input
            type="text"
            placeholder="Type your question here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button className="voice-btn" onClick={startVoiceInput}>
            🎙️
          </button>
          <button className="send-btn" onClick={() => sendMessage()}>
            Send
          </button>
        </footer>
      </div>
    </div>
  );
}

export default App;