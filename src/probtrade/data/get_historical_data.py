"""
Production-only historical data loader.

NOTE:
- During development/backtesting, data is fetched using `yfinance`
- In production, `yfinance` will be fully replaced by the Zerodha API
- Function signature and output format MUST remain unchanged to avoid breaking downstream components (features, indicators, risk, execution)

Outputs:
- Dict[str, pandas.DataFrame]
    {
        "NIFTY50": OHLCV dataframe,
        "RELIANCE": OHLCV dataframe,
        ...
    }

Each DataFrame:
- Indexed by datetime
- Columns: ["Open", "High", "Low", "Close", "Volume"]

And each dataframe will be downloaded as a csv file.
"""

# === Python Modules ===
import yfinance as yf

# === Utils ===
from probtrade.utils import (
    load_yaml
)

class HistoricalData:
    def __init__(
            self
    ):
        """
        Downloads the historical data for index and stocks
        """
        pass

    def download_data(self):
        