import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [context, setContext] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateText = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    setMessages(prevMessages => [...prevMessages, { role: "user", text: prompt }]);

    const formattedContext = context.map(msg => ({
      role: msg.role,
      text: msg.text
    }));

    const res = await fetch("http://127.0.0.1:8000/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, context: formattedContext }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let botResponse = "";
    let wordsBuffer = [];

    setMessages(prevMessages => [...prevMessages, { role: "ai", text: "" }]);

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      const lines = text.split("\n").filter(line => line.trim() !== "");

      for (let line of lines) {
        try {
          const json = JSON.parse(line);
          if (json.response) {
            wordsBuffer.push(...json.response.split(" "));
          }
        } catch (error) {
          console.error(error);
        }
      }

      for (let i = 0; i < wordsBuffer.length; i++) {
        botResponse += wordsBuffer[i] + " ";
        setMessages(prevMessages => {
          const newMessages = [...prevMessages];
          newMessages[newMessages.length - 1] = { role: "ai", text: botResponse };
          return newMessages;
        });
        await new Promise(resolve => setTimeout(resolve, 50));
      }
      wordsBuffer = [];
    }

    setContext(prevContext => [
      ...prevContext,
      { role: "user", text: prompt },
      { role: "ai", text: botResponse.trim() }
    ]);

    setPrompt("");
    setLoading(false);
  };

  return (
    <div>
      <h1>AI Chat</h1>
      <div style={{ maxHeight: "300px", overflowY: "auto", border: "1px solid #ddd", padding: "10px" }}>
        {messages.map((msg, index) => (
          <p key={index} className={msg.role === 'user' ? 'user-msg' : 'ai-msg'}>
            <strong>{msg.role === "user" ? "You" : "AI"}:</strong> {msg.text}
          </p>
        ))}
      </div>
      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type a message..."
        disabled={loading}
      />
      <button onClick={generateText} disabled={loading}>
        {loading ? "Loading..." : "Send"}
      </button>
    </div>
  );
}

export default App;
