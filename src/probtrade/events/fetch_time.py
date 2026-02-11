# === Python Modules ===
from datetime import datetime
from typing import Dict, List, Optional

## === TimeFrame dictionary ===
timeframes: Dict[str, int] = {
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60
}

# === Function to get the timeframe at the moment ===
def fetch_condition(
        current_time: datetime
) -> List[Optional[str]]:
    """
    Returns a list containing the timeframes required to fetch at the moment.

    Args:
        - current_time (datetime): Current time
    """
    ## === Current time ===
    now = current_time.replace(
        second = 2,
        microsecond = 0
    )

    ## === Market Open timings ===
    market_open = current_time.replace(
        hour = 9,
        minute = 15,
        second = 0,
        microsecond = 0
    )

    ## === Elapsed Time ===
    elapsed_time = now - market_open
    elapsed_min = int(elapsed_time.total_seconds() / 60)

    ## === Needed Timeframes ===
    needed_timeframes = [
        tf for tf, mins in timeframes.items() if elapsed_min % mins == 0
    ]

    return needed_timeframes