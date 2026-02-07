# === Python Modules ===
import os
import yfinance as yf
from pathlib import Path
from typing import List

# === Yfinance download data logic ===
from .downloader import AsyncDownloader
from .worker_yfinance import download_worker

# === Utils ===
from probtrade.utils import (
    load_yaml,
    normalise_ticker
)

# === DuckDB Saving Data Logic ===
from ..database import HistoricalDuckDB

# === Date Utils ===
from probtrade.utils import UpdateDateManager

# === Logger ===
from probtrade import get_logger

# === Function to save historical data of tickers ===
class HistoricalData():
    def __init__(
            self,
            update_date_flag: bool = False,
            dir_name: str = "data",
            sub_folder_1: List[str] = ["raw", "processed"],
            sub_folder_2: List[str] = ["index", "stocks"],
            time_frame: List[str] = ["5m", "15m", "30m", "1h", "1d"]
    ):
        """
        Downloads the historical data for index and stocks
        """

        ## === Update Date Flag ===
        self.update_date_flag = update_date_flag

        ## === Logger ===
        self.logger = get_logger(
            name = "HISTORICAL_DATA",
            log_file = "historical_data.log"
        )

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

        ## === Getting the date, will return the date in the config/last_update.yaml otherwise a N days fallback date ===
        self.get_intial_date = UpdateDateManager().read_start_date()

        ## === If folders don't exists ===
        if not os.path.exists(path = Path("data/raw")):
            self._init_folders()

        ## === Getting the paths for raw folders ===
        self._get_raw_path()

        ## === Initiating the downloader logic ===
        self.downloader = AsyncDownloader()

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

    async def download_data(
            self,
            tickers: List[str] | None = None,
            index: List[str] | None = None,
            raw_stocks_folder: Path | None = None,
            raw_index_folder: Path | None = None
    ):
        """
        Downloads the historical data by different timeframes and saves them in a database.

        Args:
            tickers: List of stock tickers to download
            index: List of index tickers to download
            raw_stocks_folder: Path to save stock data
            raw_index_folder: Path to save index data
            
        Raises:
            ValueError: If invalid parameter combinations are provided or download fails
        """
        ## === Making sure only 1 parameter is passed at a time ===
        if (tickers is not None) == (index is not None):
            self.logger.exception("Only pass either `tickers` or `index` at a time.")
            raise

        if (raw_stocks_folder is not None) == (raw_index_folder is not None):
            self.logger.exception("Only pass either `raw_stocks_folder` or `raw_index_folder` at a time.")
            raise

        ## === Determine the target folder ===
        target_folder = raw_stocks_folder or raw_index_folder

        ## === Track overall success ===
        all_successful = True
        failed_timeframes = {}

        try:

            ## === Looping through each timeframe ===
            for tf in self.time_frame:

                self.logger.info(f"Starting the timeframe: {tf}.")
                try:

                    ## === Database path name using time frame ===
                    db_path_name = target_folder / f"{tf}"

                    ## === Runnning the async function for downloading the data ===
                    self.logger.info("Starting the historical data download.")
                    data = await self.downloader.run(
                        tickers = sorted(index or tickers),
                        worker = download_worker,
                        timeframe = tf,
                        start_date = self.get_intial_date
                    )

                    self.logger.info(f"Download complete! Total number of indexes/tickers: {len(index or tickers)}, download completed: {len(self.downloader.done)}, download failed: {len(self.downloader.failed)}")

                    ## === Retry failed downloads ===
                    retry_count = 0
                    max_retry_attempts = 3

                    ## === If there's failed tickers and the retry_count is less than max_retry_attempts ===
                    while self.downloader.failed and retry_count < max_retry_attempts:

                        ## === Incrementing the retry_count by 1 ===
                        retry_count += 1

                        self.logger.info(f"Running the pending failed tickers, failed: {self.downloader.failed}, retry_count: {retry_count}")

                        ## === Fetching the failed tickers ===
                        retry_data = await self.downloader.run(
                            tickers = list(self.downloader.failed),
                            worker = download_worker,
                            timeframe = tf,
                            start_date = self.get_intial_date
                        )

                        ## === Merge successful retries ===
                        data = data | retry_data

                    ## === If still has failures after retries, mark as not fully successful ===
                    if self.downloader.failed:
                        all_successful = False
                        failed_timeframes[tf] = list(self.downloader.failed)
                        self.logger.exception(f"Warning: Failed to download {len(self.downloader.failed)} tickers for {tf}: {self.downloader.failed}")

                        ## === Stopping the run before saving the data ===
                        raise

                    ## === Save each ticker's data to database ===
                    for key, value in data.items():
                        try:
                            ## === Historical Data Logic ===
                            hist_db = HistoricalDuckDB(
                                ticker_index_raw_path = db_path_name,
                                ticker_index = normalise_ticker(key)
                            )

                            ## === Inserting data into the tables ===
                            hist_db.insert(
                                key = normalise_ticker(key),
                                values = value
                            )

                        except Exception as e:
                            all_successful = False
                            self.logger.exception(f"Error saving {key} data for {tf}: {e}")

                except Exception as e:
                    all_successful = False
                    self.logger.exception(f"Error processing timeframe {tf}: {e}")
                    failed_timeframes[tf] = str(e)

            ## === Only commit the update date if all downloads succeeded ===
            if all_successful:
                if self.update_date_flag:
                    update_manager = UpdateDateManager()

                    ## === Updating the date in the `last_update.yaml` ===
                    update_manager.commit_update()
                    self.logger.info("All downloads completed successfully. Last update date has been updated.")

                else:
                    self.logger.info("All downloads completed successfully.")
            else:
                self.logger.exception(f"Some downloads failed. Last update date NOT updated. Failed timeframes: {failed_timeframes}")
                raise

        except Exception as e:
            raise ValueError(f"Download process failed: {e}")