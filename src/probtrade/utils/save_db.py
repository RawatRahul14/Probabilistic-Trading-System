# === Python Modules ===
import pandas as pd
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Any

# === Database Logic ===
from probtrade.data import NewsDuckDB

# === Setting the time zone ===
IST = ZoneInfo("Asia/Kolkata")

# === Function to append the sentiment data to a table in the news database ===
def append_news(
        sentiments: List[Dict[str, Any]]
) -> None:
    """
    Appends news data to an existing table in the database and injects an ISO-8601 timestamp for each entry at write-time.
    """
    ## === Getting the current time ===
    now = datetime.now(IST).isoformat()

    ## === Converting the List into a Pandas DataFrame ===
    data = pd.DataFrame(sentiments)

    ## === Adding the Timestamp ===
    data["timestamp"] = now

    ## === Initiating the news db connection ===
    news_db = NewsDuckDB()

    ## === Appending data into the database ===
    news_db.insert_news_bulk_df(
        news_entries = data
    )