import { useState } from "react";
import { Bot, User, Phone } from "lucide-react";
import { APP_NAME } from "../constants";

export default function WelcomeForm({ onSubmit }) {
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const name = fullName.trim();
    const tel = phone.trim();
    setError("");
    if (!name) {
      setError("נא להזין שם מלא");
      return;
    }
    if (!tel) {
      setError("נא להזין מספר טלפון");
      return;
    }
    onSubmit({ fullName: name, phone: tel });
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md rounded-3xl bg-white dark:bg-slate-800 shadow-xl border border-gray-200 dark:border-slate-700 p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-300 mb-4">
            <Bot className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold">{APP_NAME}</h2>
          <p className="text-sm text-gray-500 dark:text-slate-400 mt-2">
            הזן פרטים כדי להתחיל בצ'אט
          </p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-2">שם מלא</label>
            <div className="relative">
              <User className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full rounded-xl border border-gray-300 dark:border-slate-600 bg-gray-50 dark:bg-slate-900 pr-10 pl-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                placeholder="ישראל ישראלי"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">טלפון נייד</label>
            <div className="relative">
              <Phone className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full rounded-xl border border-gray-300 dark:border-slate-600 bg-gray-50 dark:bg-slate-900 pr-10 pl-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                placeholder="050-0000000"
              />
            </div>
          </div>
          {error && (
            <p className="text-sm text-red-500 text-center">{error}</p>
          )}
          <button
            type="submit"
            className="w-full rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 transition-all shadow-lg"
          >
            התחל שיחה
          </button>
        </form>
      </div>
    </div>
  );
}
