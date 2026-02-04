import MessageBubble from "./MessageBubble";

export default function MessageList({
  messages,
  loading,
  error,
  messagesEndRef,
}) {
  return (
    <div className="flex-1 overflow-y-auto space-y-6 mb-4">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex w-full ${
            msg.role === "user"
              ? "justify-end"
              : msg.role === "system_ui"
                ? "justify-center"
                : "justify-start"
          }`}
        >
          <MessageBubble role={msg.role} content={msg.content} />
        </div>
      ))}
      {loading && (
        <div className="flex items-center gap-2 text-gray-500 dark:text-slate-400 text-sm mr-12">
          <span
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <span
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          />
          <span
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          />
          <span className="mr-1">הבוט כותב...</span>
        </div>
      )}
      {error && (
        <div className="text-center p-2 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-300 text-sm rounded-lg mx-auto w-fit">
          {error}
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}
