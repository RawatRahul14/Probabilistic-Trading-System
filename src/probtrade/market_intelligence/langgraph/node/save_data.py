# === Python Modules ===
import time

# === Utils ===
from probtrade.utils import append_sentiments_with_timestamp

# === Config ===
from probtrade.market_intelligence.langgraph.config.config import SentimentConfig

# === AgentState ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Logger ===
from probtrade import get_logger

## === Setting up the logger ===
logger = get_logger(
    name = "NEWS_DATA",
    log_file = "news_data.log"
)

# === Node to save the data to a json file ===
async def save_node(
        state: AgentState
) -> AgentState:
    """
    Saves the sentiment data in a json file 
    """
    ## === Start Time ===
    start_time = time.perf_counter()

    ## === Node intiating ===
    logger.info("Initiated the `save_node_node`.")

    try:
        ## === Saving the data ===
        append_sentiments_with_timestamp(
            sentiments = state.get("sentiments"),
            file_path = "news/sentiment_data.json"
        )

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f"Finished the `save_node_node`, Duration = {duration:.2f}s.")

    except Exception as e:
        logger.exception("Error occurred in `save_node_node`")

    return state