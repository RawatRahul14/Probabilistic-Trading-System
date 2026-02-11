# === Python Modules ===
import os
from pathlib import Path
from datetime import date
import time
import asyncio
from typing import List
from datetime import datetime

# === Downloading Historical Data Logic ===
from probtrade.data.historical import HistoricalData

# === Logger ===
from probtrade import get_logger

# === Events ===
from probtrade.events import fetch_condition

# === Pipeline class for downloading the historical data ===
class HistPipeline:
    def __init__(
            self,
            current_time: datetime = datetime.now()
    ):
        ## === calling logger ===
        self.logger = get_logger(
            name = "HISTORICAL_DATA",
            log_file = "historical_data.log"
        )

        ## === Required Timeframes ===
        self.current_time = current_time

        self.timeframes: List[str] = fetch_condition(
            current_time = self.current_time
        )

        ## === Checking if the 1st run ===
        self.first_run_flag: bool = os.path.exists(
            path = Path("data/raw")
        )

    async def main(self):
        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {date.today()} <<<<<<<<")
        self.logger.info(f">>>>>>> Starting Historical Data Ingestion Pipeline, timeframes downloading: {self.timeframes} <<<<<<<")

        ## === Start Time ===
        start_time = time.perf_counter()

        try:
            ## === Downloading tickers ===
            if self.first_run_flag:
                ## === If the folder already exists, then required timeframes ===
                hist_data_tickers = HistoricalData(
                    time_frame = self.timeframes
                )

            else:
                ## === If the folder not exists, then fetch all the historical data for all timeframes ===
                hist_data_tickers = HistoricalData()

            self.logger.info("Starting downloading the tickers.")

            await hist_data_tickers.download_data(
                tickers = hist_data_tickers.tickers,
                raw_stocks_folder = hist_data_tickers.raw_stocks_folder
            )

            self.logger.info("Completed downloading the tickers.")

            ## === Downloading Indexes ===
            hist_data_index = HistoricalData(
                update_date_flag = True
            )
            self.logger.info("Starting downloading the indexes.")

            await hist_data_index.download_data(
                tickers = hist_data_index.index,
                raw_stocks_folder = hist_data_index.raw_index_folder
            )

            self.logger.info("Completed downloading the indexes.")

            ## === Stop Time ===
            end_time = time.perf_counter()
            duration = end_time - start_time

            self.logger.info(f"Historical Data Ingestion Pipeline completed successfully, Duration: {duration}.")
            self.logger.info("=" * 70 + "\n")

        except Exception as e:
            self.logger.exception("Historical Data Ingestion Pipeline")

if __name__ == "__main__":

    ## === Initialize pipeline class ===
    pipeline = HistPipeline()

    try:
        ## === Start the event loop and run the main method ===
        asyncio.run(pipeline.main())

    except KeyboardInterrupt:
        pipeline.logger.exception("\nPipeline interrupted by user.")

    except Exception as e:
        pipeline.logger.exception(f"Critical Failure: {e}")