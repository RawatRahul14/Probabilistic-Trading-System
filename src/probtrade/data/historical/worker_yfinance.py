# === Python Modules ===
import yfinance as yf
import asyncio
from typing import Literal

# === Yfinance function to download the historical data ===
async def download_worker(
        ticker: str,
        start_date: str,
        timeframe: Literal["5m"]
):
    """
    Using Yfinance API downloads the historical data for different time frames.
    """
    return await asyncio.to_thread(
        yf.download,
        f"{ticker}.NS",
        start = start_date,
        interval = timeframe,
        progress = False,
        rounding = True,
        multi_level_index = False
    )