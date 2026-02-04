"""
Google Gemini chat service.
Maps frontend model names to API model IDs and runs chat completion.
"""

import logging
from typing import Any

import google.generativeai as genai

from config import get_gemini_api_key

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Gemini API configuration
# ---------------------------------------------------------------------

_API_KEY = get_gemini_api_key()

if _API_KEY:
    genai.configure(api_key=_API_KEY)
    logger.info("Gemini API configured.")
else:
    logger.warning("GEMINI_API_KEY is missing or empty in .env")

# ---------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------

SUPPORTED_MODELS = {
    "gemini-1.5-flash",
    "gemini-1.5-pro",
}

MODEL_ID_MAP = {
    "gemini-1.5-flash": "gemini-2.5-flash",
    "gemini-1.5-pro": "gemini-2.5-pro",
}

# ---------------------------------------------------------------------
# Default system prompt (Hebrew, delivery service agent)
# ---------------------------------------------------------------------

DEFAULT_SYSTEM_PROMPT = """זהות ותפקיד
אתה מייצג את חברת המשלוחים
כנציג שירות ומכירות וירטואלי.

עליך לפעול במקצועיות, ביטחון ואדיבות
בכל אינטראקציה עם הלקוח.
יש להשתמש בעברית רהוטה וטבעית
ולספק מענה מדויק על מצב משלוחים.

בנוסף, יש לעודד שימוש חוזר
בשירותי החברה בצורה נעימה ולא לוחצת.

עקרונות שיח
שפה וסגנון:
פנייה בגוף שני (זכר או נקבה לפי ההקשר),
בשפה ברורה וקלילה.

תמציתיות:
תשובות באורך של 2–4 משפטים לכל היותר.

איסוף נתונים:
אם חסרים פרטים מזהים
(שם, טלפון או מספר הזמנה),
בקש אותם בנימוס לפני המשך הטיפול.

אמינות:
אין למסור מידע משוער או מומצא.
אם פרטי ההזמנה אינם זמינים,
יש לציין זאת במפורש.

תהליכי שירות
בירור סטטוס משלוח:
לאחר קבלת פרטי ההזמנה,
אשר את קליטתם והצג את הסטטוס העדכני
וזמן ההגעה המשוער, אם קיים.

טיפול בעיכובים:
במקרה של עיכוב,
התנצל בקצרה,
הסבר את הסיבה ברוגע,
והתחייב לעדכן בהמשך במידת הצורך.

הצעת ערך (מכירה):
בסיום הטיפול השירותי,
שאל בעדינות אם הלקוח מעוניין
לתאם משלוח נוסף
או להזמין מראש לחיסכון בזמן.

אם הלקוח מסרב,
יש לכבד זאת ולעבור הלאה ללא לחץ.

מגבלות קריטיות (חובה)
אין להשתמש באימוג'ים
או סמלים גרפיים.

כל התקשורת תתבצע בעברית בלבד,
ללא שימוש באנגלית.

חל איסור על גישה אגרסיבית
או לוחצת במכירה.

אין להבטיח זמני הגעה
או פתרונות שאינם ודאיים
או בשליטתך.

סיום אינטראקציה
יש לסיים כל פנייה בשאלה הקבועה:
"יש עוד משהו שאוכל לעזור בו?"
"""


# ---------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------

class UnsupportedModelError(ValueError):
    """Raised when model_name is not in SUPPORTED_MODELS."""


# ---------------------------------------------------------------------
# Chat function
# ---------------------------------------------------------------------

def chat(
    messages: list[dict[str, Any]],
    model_name: str = "gemini-1.5-flash",
    system_prompt: str | None = None,
) -> str:
    """
    Run a chat completion with Gemini.

    messages:
        list of {"role": "user" | "assistant" | "system", "content": str}

    Returns:
        Assistant reply text or a user-facing error message in Hebrew.
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

    # Build Gemini-compatible history
    for message in messages:
        role = message.get("role")
        content = (message.get("content") or "").strip()

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
        return "אירעה שגיאה: ההודעה האחרונה חייבת להיות מהמשתמש."

    last_user_text = gemini_history[-1]["parts"][0]["text"]

    try:
        model = genai.GenerativeModel(
            model_name=api_model_id,
            system_instruction=system_instruction,
        )

        chat_session = model.start_chat(history=gemini_history[:-1])
        response = chat_session.send_message(last_user_text)

        return (response.text or "").strip() or "אין תשובה."
    except Exception:
        logger.exception("Gemini runtime error")
        return "אירעה שגיאה זמנית בחיבור למערכת. אנא נסה שוב."
