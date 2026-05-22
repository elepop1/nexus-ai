import { useState, useRef, useEffect } from "react";
import Head from "next/head";

interface Message {
  role: "user" | "assistant";
  content: string;
  reasoning?: string[];
  timestamp: Date;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          session_id: sessionId,
          reasoning: true,
        }),
      });

      const data = await response.json();

      if (data.session_id) {
        setSessionId(data.session_id);
      }

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
        reasoning: data.reasoning_steps,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please check if the backend is running.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>NexusAI - Smart Reasoning Assistant</title>
        <meta name="description" content="Powered by Xiaomi MiMo V2.5" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="flex flex-col h-screen bg-gray-950 text-white">
        {/* Header */}
        <header className="border-b border-gray-800 p-4">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                🧠 NexusAI
              </h1>
              <p className="text-sm text-gray-400">Powered by MiMo V2.5</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-green-900/30 border border-green-700 rounded-full text-green-400 text-xs">
                ● Online
              </span>
              {sessionId && (
                <span className="px-3 py-1 bg-gray-800 rounded-full text-gray-400 text-xs">
                  Session: {sessionId.slice(0, 8)}...
                </span>
              )}
            </div>
          </div>
        </header>

        {/* Messages */}
        <main className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.length === 0 && (
              <div className="text-center py-20">
                <div className="text-6xl mb-4">🧠</div>
                <h2 className="text-2xl font-bold mb-2">Welcome to NexusAI</h2>
                <p className="text-gray-400 mb-8">
                  Ask me anything. I can reason, analyze images, and read documents.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                  {[
                    { icon: "💡", text: "Explain quantum computing step by step" },
                    { icon: "📊", text: "Analyze this chart for me" },
                    { icon: "📄", text: "Summarize this document" },
                  ].map((suggestion, i) => (
                    <button
                      key={i}
                      onClick={() => setInput(suggestion.text)}
                      className="p-4 bg-gray-900 border border-gray-800 rounded-xl hover:border-blue-500 transition text-left"
                    >
                      <span className="text-2xl">{suggestion.icon}</span>
                      <p className="text-sm text-gray-300 mt-2">{suggestion.text}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl p-4 ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-900 border border-gray-800"
                  }`}
                >
                  {msg.role === "assistant" && msg.reasoning && msg.reasoning.length > 0 && (
                    <div className="mb-3 p-3 bg-gray-800/50 rounded-lg border border-gray-700">
                      <p className="text-xs text-blue-400 font-semibold mb-2">🧠 REASONING STEPS</p>
                      <ul className="space-y-1">
                        {msg.reasoning.map((step, j) => (
                          <li key={j} className="text-xs text-gray-300">{step}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                  <div className="mt-2 text-xs opacity-50">
                    {msg.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-4">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                    <span className="text-sm text-gray-400 ml-2">Thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </main>

        {/* Input */}
        <footer className="border-t border-gray-800 p-4">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask NexusAI anything..."
                className="flex-1 p-3 bg-gray-900 border border-gray-700 rounded-xl focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-xl font-semibold transition"
              >
                Send
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Powered by Xiaomi MiMo V2.5 • Reasoning • Multimodal • TTS
            </p>
          </form>
        </footer>
      </div>
    </>
  );
}
