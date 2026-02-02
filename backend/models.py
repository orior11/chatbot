from pydantic import BaseModel
from typing import List, Optional

# מודל של הודעה בודדת (כמו ש-OpenAI מצפה לקבל)
class ChatMessage(BaseModel):
    role: str       # "user", "assistant", או "system"
    content: str    # תוכן ההודעה

# מודל הבקשה שמגיעה מהצד-לקוח (Frontend)
class ChatRequest(BaseModel):
    messages: List[ChatMessage]  # רשימת כל ההודעות בשיחה
    model: str = "gpt-3.5-turbo" # המודל שנבחר (ברירת מחדל)
    
    # שדות אופציונליים (למקרה שנרצה לשמור לוגים לאקסל)
    user_name: Optional[str] = None
    user_phone: Optional[str] = None

# מודל התשובה שהשרת מחזיר
class ChatResponse(BaseModel):
    message: ChatMessage