# === Python Modules ===
from datetime import datetime, time

# === Function to check the market situation ===
def market_condition() -> str:
    """
    Returns the market's current condition.

    returns:
        - "pre_open"
        - "open"
        - "close"
    """

    ## === Current local time ===
    now = datetime.now().time()

    ## === NSE timings ===
    market_open = time(9, 15)
    market_close = time(15, 30)

    ## === Market conditions ===
    if now < market_open:
        return "pre_open"
    elif market_open <= now <= market_close:
        return "open"
    else:
        return "close"