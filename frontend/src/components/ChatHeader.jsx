import { Bot, Sun, Moon } from "lucide-react";
import { APP_NAME, MODEL_LABELS } from "../constants";

export default function ChatHeader({
  userName,
  model,
  onModelChange,
  isDark,
  onToggleDark,
}) {
  return (
    <header className="sticky top-0 z-10 flex items-center justify-between px-4 py-3 bg-white dark:bg-slate-800 border-b dark:border-slate-700 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="bg-indigo-600 p-2 rounded-full text-white">
          <Bot size={20} />
        </div>
        <div>
          <h1 className="font-bold">{APP_NAME}</h1>
          <p className="text-xs text-green-500">מחובר כ-{userName}</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <select
          value={model}
          onChange={onModelChange}
          className="bg-gray-100 dark:bg-slate-700 text-sm rounded-lg p-2 pr-8 pl-3 border-none outline-none cursor-pointer min-w-[10rem]"
          dir="rtl"
          aria-label="בחירת מודל"
        >
          {Object.entries(MODEL_LABELS).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={onToggleDark}
          className="p-2 rounded-lg bg-gray-100 dark:bg-slate-700"
          aria-label={isDark ? "מעבר למצב בהיר" : "מעבר למצב כהה"}
        >
          {isDark ? (
            <Sun className="w-5 h-5 text-yellow-500" />
          ) : (
            <Moon className="w-5 h-5 text-gray-600" />
          )}
        </button>
      </div>
    </header>
  );
}
