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
def save_node(
        state: AgentState
) -> AgentState:
    """
    Saves the sentiment data in a json file 
    """
    ## === Node intiating ===
    logger.info("Initiated the `save_node_node`.")

    ## === Saving the data ===
    append_sentiments_with_timestamp(
        sentiments = state.get("sentiments"),
        file_path = "news/sentiment_data.json"
    )

    logger.info("Finished the `save_node_node`.")

    return state