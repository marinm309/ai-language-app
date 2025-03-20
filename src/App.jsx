import { useState, useRef } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [context, setContext] = useState([]);
  const [loading, setLoading] = useState(false);

  const textareaRef = useRef(null);

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "100px";
      textarea.style.height = Math.min(textarea.scrollHeight, 300) + "px";
    }
  };

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

      <div className="chat-box-wrapper">
          {messages.map((msg, index) => (
            <div className={msg.role === 'user' ? 'user-msg-wrapper' : 'ai-msg-wrapper'}>
              <p key={index} className={msg.role === 'user' ? 'user-msg' : 'ai-msg'}>{msg.text}</p>
            </div>
          ))}
      </div>

      <div className="input-box-wrapper">
        <textarea
          ref={textareaRef}
          className="input-box"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type a message..."
          disabled={loading}
          onInput={adjustHeight}
        />
        <button onClick={generateText} disabled={loading} className="input-box-btn">
          {loading ? <i class="fa-solid fa-spinner"></i> : <i class="fa-solid fa-share"></i>}
        </button>
      </div>

    </div>
  );
}

export default App;
