# === Python Modules ===
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Any

# === Setting the time zone ===
IST = ZoneInfo("Asia/Kolkata")

# === Function to append the sentiment data to a json file ===
def append_sentiments_with_timestamp(
    sentiments: List[Dict[str, Any]],
    file_path: str | Path
) -> None:
    """
    Appends sentiment data to an existing JSON file and injects
    an ISO-8601 timestamp for each entry at write-time.

    If the file does not exist, it will be created.
    """

    ## === Making sure folder exists ===
    path = Path(file_path)
    path.parent.mkdir(
        parents = True,
        exist_ok = True
    )

    ## === Getting the current time ===
    now = datetime.now(IST).isoformat()

    ## === Adding the timestamp column ===
    new_data = [
        {**item, "timestamp": now}
        for item in sentiments
    ]

    ## === Loading existing data if present ===
    if path.exists():
        with path.open(
            "r",
            encoding = "utf-8"
        ) as f:
            existing_data = json.load(f)

        if not isinstance(existing_data, list):
            raise ValueError("Existing JSON file must contain a list.")
    else:
        existing_data = []

    ## === Appending new data ===
    combined_data = existing_data + new_data

    ## === Saving the combined data ===
    with path.open(
        "w",
        encoding = "utf-8"
    ) as f:
        json.dump(
            combined_data,
            f,
            indent = 2,
            ensure_ascii = False
        )