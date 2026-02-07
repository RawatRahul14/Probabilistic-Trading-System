# === Python Modules ===
import yfinance as yf
import asyncio
from typing import Literal
import pandas as pd

# === Yfinance function to download the historical data ===
async def download_worker(
        ticker: str,
        start_date: str,
        timeframe: Literal["5m", "15m", "30m", "1h", "1d"]
) -> pd.DataFrame:
    """
    Using Yfinance API downloads the historical data for different time frames.
    
    Args:
        ticker: Stock ticker symbol (will be appended with .NS for Indian stocks)
        start_date: Start date for historical data in ISO format (YYYY-MM-DD)
        timeframe: Time interval for candles. Valid options: 5m, 15m, 30m, 1h, 1d
        
    Returns:
        pd.DataFrame: Historical OHLCV data for the ticker
        
    Raises:
        ValueError: If the download fails or returns no data
    """
    try:
        ## === Handling Ticker and index differently ===
        full_symbol = ticker if ticker.startswith("^") else f"{ticker}.NS"

        ## === The download logic ===
        result = await asyncio.to_thread(
            yf.download,
            full_symbol,
            start = start_date,
            interval = timeframe,
            progress = False,
            rounding = True,
            multi_level_index = False
        )
        
        if result is None or result.empty:
            raise ValueError(f"No data returned for {ticker} on interval {timeframe}")
            
        return result
        
    except Exception as e:
        raise ValueError(f"Failed to download {ticker} data: {str(e)}")