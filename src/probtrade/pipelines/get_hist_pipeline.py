# === Python Modules ===
from datetime import date
import time
import asyncio

# === Downloading Historical Data Logic ===
from probtrade.data.historical import HistoricalData

# === Logger ===
from probtrade import get_logger

# === Pipeline class for downloading the historical data ===
class HistPipeline:
    def __init__(
            self
    ):
        ## === calling logger ===
        self.logger = get_logger(
            name = "HISTORICAL_DATA",
            log_file = "historical_data.log"
        )

    async def main(self):
        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {date.today()} <<<<<<<<")
        self.logger.info(">>>>>>> Starting Historical Data Ingestion Pipeline <<<<<<<")

        ## === Start Time ===
        start_time = time.perf_counter()

        try:
            ## === Downloading tickers ===
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