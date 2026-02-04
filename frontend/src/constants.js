/**
 * App-wide constants and error message mapping.
 */

export const APP_NAME = "א.ב שליחויות";

export const GEMINI_MODEL_KEY = "gemini_model";
export const VALID_MODELS = ["gemini-1.5-flash", "gemini-1.5-pro"];
export const DEFAULT_MODEL = "gemini-1.5-flash";

export const MODEL_LABELS = {
  "gemini-1.5-flash": "Gemini 1.5 Flash (מהיר)",
  "gemini-1.5-pro": "Gemini 1.5 Pro (חכם)",
};

export const MODEL_LABEL_LONG = {
  "gemini-1.5-pro": "Gemini 1.5 Pro (חכם ומתקדם)",
  "gemini-1.5-flash": "Gemini 1.5 Flash (מהיר)",
};

const BACKEND_HINT =
  "וודא שהבקאנד רץ: בתיקיית backend הרץ .\\run.ps1 או python -m uvicorn main:app --port 3002";

/**
 * Map API/network error codes to user-facing Hebrew messages.
 */
export function getChatErrorMessage(message) {
  const msg = message || "שגיאת תקשורת";
  if (msg === "TIMEOUT") return "הבקשה ארכה יותר מדי. נסה שוב.";
  if (msg === "BACKEND_INVALID_JSON" || msg === "BACKEND_EMPTY_RESPONSE")
    return "תשובה לא תקינה מהשרת. וודא שהבקאנד רץ על פורט 3002.";
  if (
    msg.includes("Failed") ||
    msg.includes("fetch") ||
    msg.includes("NetworkError")
  )
    return "לא ניתן להתחבר לשרת. " + BACKEND_HINT;
  return msg;
}
