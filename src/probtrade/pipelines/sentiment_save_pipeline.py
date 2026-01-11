# === Python Modules ===
from datetime import date
import time

# === DuckDB Logic ===
from probtrade.data import AggDuckDB

# === Logger ===
from probtrade import get_logger

# === Saving the data logic ===
class SentimentSavePipeline:
    def __init__(self, run_id):
        self.db_path: str = "db/sentiment.db"

        self.run_id = run_id

        # === Defining the Logger ===
        self.logger = get_logger(
            name = "SAVING_SENTIMENT",
            log_file = "save_sentiment.log"
        )

    def main(self, sentiment):
        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {date.today()}, run_id: {self.run_id} <<<<<<<<")
        self.logger.info(">>>>>>> Starting Saving Sentiment Aggregation Pipeline <<<<<<<")

        ## === Start Time ===
        start_time = time.perf_counter()

        try:
            # === Initiating the database ===
            agg_database = AggDuckDB(db_path = self.db_path)

            # === Saving the agg sentiment ===
            agg_database.save_agg_sentiment(agg_sentiment = sentiment, run_id = self.run_id)

            ## === Stop Time ===
            end_time = time.perf_counter()
            duration = end_time - start_time

            ## === Savin the logs ===
            self.logger.info(f"Finished saving the aggregated sentiment in database, Duration: {duration}.")
            self.logger.info("=" * 70 + "\n")

        except Exception as e:
            self.logger.exception(
                "Fatal error while running Saving Sentiment Aggregation Pipeline."
            )
            raise