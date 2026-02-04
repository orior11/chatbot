import { Send } from "lucide-react";

export default function ChatInput({
  value,
  onChange,
  onSubmit,
  disabled,
  placeholder = "הקלד הודעה...",
}) {
  return (
    <form onSubmit={onSubmit} className="flex gap-2 sticky bottom-4">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className="flex-1 rounded-xl border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-4 py-3 focus:ring-2 focus:ring-indigo-500 outline-none shadow-lg"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="p-3 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50 transition-colors shadow-lg"
        aria-label="שלח"
      >
        <Send className="w-5 h-5" />
      </button>
    </form>
  );
}
