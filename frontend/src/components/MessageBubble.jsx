import { Bot, CheckCircle } from "lucide-react";

export default function MessageBubble({ role, content }) {
  if (role === "system_ui") {
    return (
      <div className="flex justify-center w-full">
        <div className="bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 px-4 py-1.5 rounded-full text-xs border border-yellow-200 dark:border-yellow-800/50 flex items-center gap-2 my-2">
          <CheckCircle size={12} />
          {content}
        </div>
      </div>
    );
  }

  const isUser = role === "user";
  return (
    <div
      className={`flex gap-3 max-w-[85%] ${isUser ? "justify-end ml-auto" : "justify-start"}`}
    >
      {role === "assistant" && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
          <Bot className="w-4 h-4 text-indigo-600 dark:text-indigo-300" />
        </div>
      )}
      <div
        className={`rounded-2xl px-5 py-3 shadow-sm ${
          isUser
            ? "bg-indigo-600 text-white rounded-tr-none"
            : "bg-white dark:bg-slate-800 border dark:border-slate-700 text-gray-800 dark:text-slate-100 rounded-tl-none"
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {content}
        </p>
      </div>
    </div>
  );
}
