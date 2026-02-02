import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ייבוא המודולים שלך
import ai
from models import ChatRequest, ChatResponse, ChatMessage
# מחזירים את הלוגר לאקסל
from excel_logger import log_conversation 

# --- 1. הגדרות אתחול ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 System startup...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: OPENAI_API_KEY is missing!")
    else:
        print("✅ OpenAI API Key loaded.")
    yield

app = FastAPI(lifespan=lifespan)

# --- 2. הגדרות CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. ה-Endpoint ---
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. שליחה ל-AI
        messages_dicts = [{"role": m.role, "content": m.content} for m in request.messages]
        
        try:
            ai_content = ai.chat(messages=messages_dicts, model=request.model)
        except Exception as e:
            print(f"❌ AI Error: {e}")
            raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")

        if not ai_content:
            ai_content = "⚠️ The AI returned an empty response."

        # 2. שמירה לאקסל (רק אם נשלחו שם וטלפון)
        # אנחנו בודקים אם יש שם וטלפון, כדי לא לשמור סתם שיחות ריקות
        if request.user_name and request.user_phone:
            try:
                last_user_msg = request.messages[-1].content if request.messages else "No Content"
                interaction_log = f"User: {last_user_msg} | AI: {ai_content}"
                
                # קריאה לפונקציה ששומרת לאקסל
                log_conversation(request.user_name, request.user_phone, interaction_log)
                print(f"📝 Saved to Excel for: {request.user_name}")
            except Exception as e:
                # מדפיסים שגיאה אבל לא עוצרים את התוכנה
                print(f"⚠️ Excel Error: {e}")

        return ChatResponse(
            message=ChatMessage(role="assistant", content=ai_content)
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"🔥 Critical Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)