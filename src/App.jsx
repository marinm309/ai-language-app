import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [context, setContext] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateText = async () => {
    setResponse("");
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, context }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      const lines = text.split("\n").filter(line => line.trim() !== "");

      for (let line of lines) {
        try {
          const json = JSON.parse(line);
          if (json.done) {
            setLoading(false);
            return;
          }
          setResponse(prev => prev + json.response);
        } catch (error) {
          console.error("Error parsing JSON", error);
        }
      }
    }
  };

  return (
    <div>
      <h1>AI Chat</h1>
      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={generateText} disabled={loading}>
        {loading ? "Loading..." : "Send"}
      </button>
      <p>{response}</p>
    </div>
  );
}

export default App;
