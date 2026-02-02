import os
from datetime import datetime
import pandas as pd

# שם הקובץ שבו נשמור את הנתונים
LOG_FILE = "chat_logs.xlsx"

def log_conversation(user_name, user_phone, interaction_log):
    """
    Saves the chat interaction to an Excel file.
    If the file doesn't exist, it creates it.
    """
    
    # הנתונים שאנחנו רוצים לשמור בשורה החדשה
    new_data = {
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "User Name": [user_name],
        "Phone": [user_phone],
        "Interaction": [interaction_log]
    }
    
    # יצירת DataFrame (טבלה) מהנתונים החדשים
    df_new = pd.DataFrame(new_data)
    
    try:
        if os.path.exists(LOG_FILE):
            # אם הקובץ קיים, טוענים אותו ומוסיפים את השורה החדשה
            # שימוש ב-mode='a' (append) מחייב מנוע מסוים, לכן לעתים קל יותר לקרוא ולכתוב מחדש:
            df_existing = pd.read_excel(LOG_FILE)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(LOG_FILE, index=False)
        else:
            # אם הקובץ לא קיים, יוצרים חדש
            df_new.to_excel(LOG_FILE, index=False)
            
    except Exception as e:
        print(f"Error saving to Excel: {e}")