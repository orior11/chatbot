/**
 * Chat API service. Matches backend POST /api/chat contract.
 * Request: { messages: [{role, content}], model_name?, user_name?, user_phone? }
 * Response: { message: { role: "assistant", content: string } }
 */

import { API_BASE_URL, CHAT_TIMEOUT_MS } from "../config";

export async function sendChatRequest(body, { signal } = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), CHAT_TIMEOUT_MS);
  const effectiveSignal = signal || controller.signal;

  try {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: effectiveSignal,
    });

    clearTimeout(timeoutId);

    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error("BACKEND_INVALID_JSON");
    }

    if (!res.ok) {
      const detail = typeof data?.detail === "string" ? data.detail : JSON.stringify(data?.detail ?? "שגיאה בשרת");
      throw new Error(detail);
    }

    if (!data?.message || data.message.content == null) {
      throw new Error("BACKEND_EMPTY_RESPONSE");
    }

    return data.message;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") {
      throw new Error("TIMEOUT");
    }
    throw err;
  }
}
