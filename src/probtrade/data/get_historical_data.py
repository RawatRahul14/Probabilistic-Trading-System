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
import os
import yfinance as yf
from pathlib import Path
from typing import List

# === Utils ===
from probtrade.utils import (
    load_yaml
)

# === Date Utils ===
from probtrade.utils import UpdateDateManager

class HistoricalData():
    def __init__(
            self,
            dir_name: str = "data",
            sub_folder_1: List[str] = ["raw", "processed"],
            sub_folder_2: List[str] = ["index", "stocks"],
            time_frame: List[str] = ["15m", "30m", "1h", "1d"]
    ):
        """
        Downloads the historical data for index and stocks
        """
        self.dir_name = Path(dir_name)

        self.sub_folder_1 = sub_folder_1
        self.sub_folder_2 = sub_folder_2
        self.time_frame = time_frame

        ## === Index Names ===
        self.index = load_yaml(
            file_path = "config",
            file_name = "index.yaml"
        ).get("index", [])

        ## === Tickers Names ===
        self.tickers = load_yaml(
            file_path = "config",
            file_name = "tickers.yaml"
        ).get("stocks", [])

        ## === Getting the date ===
        self.get_intial_date = UpdateDateManager().read_start_date()

        ## === If folders don't exists ===
        if not os.path.exists(path = Path("data/raw")):
            self._init_folders()

        ## === Getting the paths for raw folders ===
        self._get_raw_path()

    def _init_folders(self):
        """
        Initializes folder structure:
        data/{raw,processed}/{index,stocks}
        """
        ## === Looping through Subfolder_1 ===
        for level_1 in self.sub_folder_1:

            ## === Looping through Subfolder_2 ===
            for level_2 in self.sub_folder_2:
                    folder = self.dir_name / level_1 / level_2
                    folder.mkdir(
                        parents = True,
                        exist_ok = True
                    )

    def _get_raw_path(self):
        """
        Returns the raw data path, to save the data from yfinance data.
        """
        ## === Store explicit paths ===
        self.raw_index_folder = self.dir_name / "raw" / "index"
        self.raw_stocks_folder = self.dir_name / "raw" / "stocks"

    def _download_one(self, ticker_index):
        """
        Downloads a data for a sinle ticker/inedx.
        """

    def download_data(self):
        print(self.get_intial_date)