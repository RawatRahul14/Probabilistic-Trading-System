# === Python Modules ===
from typing import List
from datetime import date
import time

# === Schema ===
from probtrade.schemas import SentimentPipelineData

# === Utils ===
from probtrade.utils import extract_details

# === Cpp Function ===
from probtrade.cpp import compute_news_pressure

# === Logger ===
from probtrade import get_logger

# === Cpp Aggregated Sentiment Function ===
class SentimentAggPipeline:
    def __init__(self, run_id):
        self.logger = get_logger(
            name = "SENTMENT_AGGREGATION",
            log_file = "sentiment.log"
        )

        self.run_id = run_id

    def main(self, state):
        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {date.today()}, run_id: {self.run_id} <<<<<<<<")
        self.logger.info(">>>>>>> Starting Sentiment Aggregation Pipeline <<<<<<<")

        ## === Start Time ===
        start_time = time.perf_counter()

        try:
            ## === Extracting the required data ===
            self.logger.info("Extracting Data from Agentic Graph State.")

            ## === Initiating a new List to hold data ===
            data: List[SentimentPipelineData] = []

            ## === Looping through each article ===
            for article in state["sentiments"]:
                data.append(
                    {
                        "sentiment_score": article["sentiment_score"],
                        "market_bias": article["market_bias"],
                        "news_impact": article["news_impact"],
                        "confidence": article["confidence"]
                    }
                )

            self.logger.info("Successfully Extracted Data from Agentic Graph State.")

            ## === Calculating the Aggregated sentiment ===
            self.logger.info("Computing the aggregated sentiment using cpp.")
            agg_sentiment: float = compute_news_pressure(data)

            ## === Extravting Features ===
            details = extract_details(data = data)

            ## === Stop Time ===
            end_time = time.perf_counter()
            duration = end_time - start_time

            self.logger.info(f"Finished computing the aggregated sentiment using cpp, Duration: {duration}.")
            self.logger.info("=" * 70 + "\n")

            return round(agg_sentiment, 3), details

        except Exception as e:
            self.logger.exception(
                "Fatal error while running Aggregated Sentiment Pipeline."
            )