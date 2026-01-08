# === Python Modules ===
from datetime import date

# === Pipelines ===
from probtrade.pipelines import (
    AgenticAiPipeline,
    SentimentAggPipeline
)

# === Logger ===
from probtrade import get_logger

# === Logger Defininf ===
logger = get_logger(
    name = "Main",
    log_file = "main.log"
)

# === Main Run ===
def main():
    logger.info("="*70)
    logger.info(
        f">>>>>>>> {date.today()} <<<<<<<<"
    )

    try:
        ## === 1st Pipeline ===
        logger.info("Started the 1st pipeline: `AgenticAiPipeline`.")
        state = AgenticAiPipeline().main()
        logger.info("Completed the 1st pipeline: `AgenticAiPipeline`.")

        ## === 2nd Pipeline ===
        logger.info("Started the 2nd pipeline: `SentimentAggPipeline`.")
        agg_sentiment = SentimentAggPipeline().main(state = state)
        logger.info("Completed the 2nd pipeline: `SentimentAggPipeline`.")

        logger.info("=" * 70, "\n")

        return agg_sentiment
    
    except Exception as e:
        logger.exception(
            "Fatal error in running the main.py file."
        )