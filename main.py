# === Python Modules ===
from datetime import date

# === Pipelines ===
from probtrade.pipelines import (
    AgenticAiPipeline,
    SentimentAggPipeline,
    SentimentSavePipeline
)

# === Logger ===
from probtrade import get_logger

# === Utils ===
from probtrade.utils import get_run_id

# === Logger Defining ===
logger = get_logger(
    name = "Main",
    log_file = "main.log"
)

# === Getting the run_id ===
run_id = get_run_id()

# === Main Run ===
async def main():
    logger.info("="*70)
    logger.info(
        f">>>>>>>> {date.today()}, run_id: {run_id} <<<<<<<<"
    )

    try:
        ## === 1st Pipeline ===
        logger.info("Started the 1st pipeline: `AgenticAiPipeline`.")
        state = await AgenticAiPipeline(run_id = run_id).main()
        logger.info("Completed the 1st pipeline: `AgenticAiPipeline`.")

        ## === 2nd Pipeline ===
        logger.info("Started the 2nd pipeline: `SentimentAggPipeline`.")
        agg_sentiment = SentimentAggPipeline(run_id = run_id).main(state = state)
        logger.info("Completed the 2nd pipeline: `SentimentAggPipeline`.")

        ## === 3rd Pipeline ===
        logger.info("Started the 3rd pipeline: `SentimentSavePipeline`.")
        agg_sentiment_db = SentimentSavePipeline(run_id = run_id)
        agg_sentiment_db.main(sentiment = agg_sentiment)
        logger.info("Completed the 3rd pipeline: `SentimentSavePipeline`.")

        logger.info("=" * 70 + "\n")

        return agg_sentiment
    
    except Exception as e:
        logger.exception(
            "Fatal error in running the main.py file."
        )