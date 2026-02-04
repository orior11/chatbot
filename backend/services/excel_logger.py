"""
Append chat interactions to an Excel log file.
"""
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from config import get_chat_log_path

logger = logging.getLogger(__name__)


def log_conversation(
    user_name: str,
    user_phone: str,
    interaction_log: str,
    log_path: Path | None = None,
) -> None:
    """
    Append one chat interaction to the Excel log.
    Creates the file if it does not exist.
    """
    path = log_path or get_chat_log_path()
    new_data = {
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "User Name": [user_name],
        "Phone": [user_phone],
        "Interaction": [interaction_log],
    }
    df_new = pd.DataFrame(new_data)

    try:
        if path.exists():
            df_existing = pd.read_excel(path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(path, index=False)
        else:
            df_new.to_excel(path, index=False)
        logger.info("Saved to Excel for: %s", user_name)
    except Exception as e:
        logger.warning("Error saving to Excel: %s", e)
