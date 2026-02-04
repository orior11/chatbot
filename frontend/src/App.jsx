import { useState, useRef, useEffect } from "react";
import { sendChatRequest } from "./api/chatService";
import WelcomeForm from "./components/WelcomeForm";
import ChatHeader from "./components/ChatHeader";
import MessageList from "./components/MessageList";
import ChatInput from "./components/ChatInput";
import {
  APP_NAME,
  GEMINI_MODEL_KEY,
  VALID_MODELS,
  DEFAULT_MODEL,
  MODEL_LABEL_LONG,
  getChatErrorMessage,
} from "./constants";
import { useLocalStorage } from "./hooks/useLocalStorage";

export default function App() {
  const [isDark, setIsDark] = useState(true);
  const [userDetails, setUserDetails] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [model, setModel] = useLocalStorage(
    GEMINI_MODEL_KEY,
    DEFAULT_MODEL,
    (v) => VALID_MODELS.includes(v)
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleWelcomeSubmit = ({ fullName, phone }) => {
    setUserDetails({ fullName, phone });
    setMessages([
      {
        role: "assistant",
        content: `שלום ${fullName}, אני הבוט של ${APP_NAME}. איך אוכל לעזור לך היום?`,
      },
    ]);
  };

  const handleModelChange = (e) => {
    const newModel = e.target.value;
    setModel(newModel);
    const label = MODEL_LABEL_LONG[newModel] || newModel;
    setMessages((prev) => [
      ...prev,
      { role: "system_ui", content: `המודל הוחלף בהצלחה ל-${label}` },
    ]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading || !userDetails) return;

    const userMessage = { role: "user", content: text };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setError(null);
    setLoading(true);

    try {
      const contextSystemMessage = {
        role: "system",
        content: `פרטי הלקוח הנוכחי: שם: ${userDetails.fullName}, טלפון: ${userDetails.phone}. פנה אליו בשמו.`,
      };
      const cleanHistory = updatedMessages.filter((m) => m.role !== "system_ui");
      const messagesToSend = [contextSystemMessage, ...cleanHistory];
      const body = {
        messages: messagesToSend,
        model_name: model,
        user_name: userDetails.fullName,
        user_phone: userDetails.phone,
      };
      const botMessage = await sendChatRequest(body);
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setError(getChatErrorMessage(err?.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={isDark ? "dark" : ""}>
      <div
        dir="rtl"
        className="min-h-screen bg-gray-100 dark:bg-slate-900 text-gray-900 dark:text-white transition-colors font-sans"
      >
        {userDetails === null ? (
          <WelcomeForm onSubmit={handleWelcomeSubmit} />
        ) : (
          <>
            <ChatHeader
              userName={userDetails.fullName}
              model={model}
              onModelChange={handleModelChange}
              isDark={isDark}
              onToggleDark={() => setIsDark(!isDark)}
            />
            <main className="flex flex-col max-w-3xl mx-auto px-4 py-6 min-h-[calc(100vh-80px)]">
              <MessageList
                messages={messages}
                loading={loading}
                error={error}
                messagesEndRef={messagesEndRef}
              />
              <ChatInput
                value={input}
                onChange={setInput}
                onSubmit={handleSubmit}
                disabled={loading}
              />
            </main>
          </>
        )}
      </div>
    </div>
  );
}
