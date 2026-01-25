# === Python Modules ===
from datetime import date
import time
import pandas as pd

# === Logger ===
from probtrade import get_logger

# === DataBase Logic ===
from probtrade.data import DailyNewsDuckDB

# === Cpp Logic for daily aggregation ===
from probtrade.cpp import aggregate_daily_news

class DailyNewsPipeline:
    def __init__(self):
        self.logger = get_logger(
            name = "DAILY_NEWS_AGG",
            log_file = "daily_news_agg.log"
        )

    def main(self, given_date: str | None = None):

        run_date = given_date or date.today().isoformat()

        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {run_date} <<<<<<<<")
        self.logger.info(">>>>>>> Starting Sentiment Aggregation Pipeline <<<<<<<")

        ## === Start Time ===
        start_time = time.perf_counter()

        try:
            ## === Loading the required data from the database ===
            self.logger.info("Loading the Data from the Database")

            ## === Getting the data from the table ===
            daily_news = DailyNewsDuckDB()
            data: pd.DataFrame = daily_news.load_data(date = run_date)

            self.logger.info("Successfully loaded the Data from the Database.")
            self.logger.info("Exctracting required columns and applying the aggregation.")

            ## === Selecting the required columns ===
            cols = [
                "news_count",
                "sentiment_mean",
                "sentiment_std",
                "BULLISH_count",
                "BEARISH_count",
                "NEUTRAL_count",
            ]

            ## === Converting data into a Dictionary ===
            runs = data[cols].to_dict(orient = "records")

            ## === Calculating daily aggregations using cpp ===
            data_dict = aggregate_daily_news(runs)

            ## === Adding the date column ===
            data_dict["date"] = str(run_date)

            self.logger.info("Successfully applied the aggregation.")
            self.logger.info("Saving the data into the table.")

            ## === Saving the data into the table in database ===
            daily_news.insert_data(data = data_dict)

            self.logger.info("Successfully saved the data into the table.")

            ## === Stop Time ===
            end_time = time.perf_counter()
            duration = end_time - start_time

            self.logger.info(f"Finished Aggregating daily news, Duration: {duration}.")
            self.logger.info("=" * 70 + "\n")

        except Exception as e:
            self.logger.exception(
                "Fatal error while running Daily Aggregated Pipeline"
            )