# === Utils ===
from probtrade.utils import append_sentiments_with_timestamp

# === Config ===
from probtrade.market_intelligence.langgraph.config.config import SentimentConfig

# === AgentState ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Node to save the data to a json file ===
def save_node(
        state: AgentState
) -> AgentState:
    """
    Saves the sentiment data in a json file 
    """

    ## === Saving the data ===
    append_sentiments_with_timestamp(
        sentiments = state.get("sentiments"),
        file_path = "news/sentiment_data.json"
    )

    return state