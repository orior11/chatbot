"""
Google Gemini chat service.
Maps frontend model names to API model IDs and runs chat completion.
"""
import logging
from typing import Any

import google.generativeai as genai

from config import get_gemini_api_key

logger = logging.getLogger(__name__)

_API_KEY = get_gemini_api_key()
if _API_KEY:
    genai.configure(api_key=_API_KEY)
    logger.info("Gemini API configured.")
else:
    logger.warning("GEMINI_API_KEY is missing or empty in .env")

# Frontend model names; map to current Gemini API model IDs
SUPPORTED_MODELS = {"gemini-1.5-flash", "gemini-1.5-pro"}
MODEL_ID_MAP = {
    "gemini-1.5-flash": "gemini-2.5-flash",
    "gemini-1.5-pro": "gemini-2.5-pro",
}

DEFAULT_SYSTEM_PROMPT = """
אתה סוכן שירות ומכירות חכם, ידידותי ומקצועי, הדובר עברית שוטפת.

התפקיד שלך:
- לספק שירות לקוחות מצוין בנוגע למשלוחים (סטטוס חבילה, זמני הגעה, עיכובים, שאלות כלליות).
- לעודד בעדינות הזמנות נוספות של משלוחים, מבלי להיות אגרסיבי.
- לשמור על טון אנושי, נעים ובטוח.

כללי שיחה:
- דבר תמיד בעברית תקנית, קלילה וידידותית.
- פנה ללקוח בגוף שני ("אתה" / "את").
- שמור על תשובות קצרות וברורות (2–4 משפטים).
- אם חסר מידע (מספר הזמנה / טלפון / שם) – בקש אותו בצורה מנומסת.
- לעולם אל תמציא מידע על הזמנה. אם אין נתונים – ציין זאת בצורה ברורה.

שירות לקוחות:
- אם הלקוח שואל על סטטוס משלוח:
  • בקש מספר הזמנה או מספר טלפון
  • אשר שקיבלת את הפרטים
  • הסבר מה מצב המשלוח ומה הצפי
- אם יש עיכוב:
  • התנצל בקצרה
  • תן הסבר רגוע
  • הצע פתרון או עדכון בהמשך

מכירות:
- לאחר מענה שירותי, נסה להציע בעדינות הזמנה נוספת:
  • "רוצה שאעזור לך להזמין משלוח נוסף?"
  • "יש לנו הרבה לקוחות שמזמינים מראש כדי לחסוך זמן."
- אם הלקוח לא מעוניין – כבד זאת מיד.

אסור:
- לא להיות אגרסיבי או לוחץ
- לא להשתמש באימוג'ים
- לא לדבר באנגלית
- לא להבטיח הבטחות שאינן ודאיות

סיום שיחה:
- סיים כל שיחה בהצעה לעזרה נוספת:
  "יש עוד משהו שאוכל לעזור בו?"
"""


class UnsupportedModelError(ValueError):
    """Raised when model_name is not in SUPPORTED_MODELS."""


def chat(
    messages: list[dict[str, Any]],
    model_name: str = "gemini-1.5-flash",
    system_prompt: str | None = None,
) -> str:
    """
    Run a chat completion with Gemini.
    messages: list of {"role": "user"|"assistant"|"system", "content": str}
    Returns assistant reply text or a user-facing error message in Hebrew.
    """
    if not _API_KEY:
        return "שגיאת מערכת: חיבור ל-Gemini נכשל (חסר מפתח API)."

    if model_name not in SUPPORTED_MODELS:
        raise UnsupportedModelError(
            f"Model '{model_name}' is not supported. "
            f"Use: {', '.join(sorted(SUPPORTED_MODELS))}."
        )

    api_model_id = MODEL_ID_MAP.get(model_name, model_name)
    system_instruction = system_prompt or DEFAULT_SYSTEM_PROMPT
    gemini_history: list[dict[str, Any]] = []

    for m in messages:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if not content:
            continue
        if role == "system":
            system_instruction = content
            continue
        part = {"text": content}
        if role == "user":
            gemini_history.append({"role": "user", "parts": [part]})
        elif role == "assistant":
            gemini_history.append({"role": "model", "parts": [part]})

    if not gemini_history or gemini_history[-1]["role"] != "user":
        return "אירעה שגיאה: הודעה אחרונה חייבת להיות מהמשתמש."

    last_user_text = gemini_history[-1]["parts"][0]["text"]
    try:
        model = genai.GenerativeModel(
            model_name=api_model_id,
            system_instruction=system_instruction,
        )
        chat_session = model.start_chat(history=gemini_history[:-1])
        response = chat_session.send_message(last_user_text)
        return (response.text or "").strip() or "אין תשובה."
    except Exception as e:
        logger.exception("Gemini runtime error")
        return "אירעה שגיאה זמנית בחיבור למוח הבוט. אנא נסה שוב."
