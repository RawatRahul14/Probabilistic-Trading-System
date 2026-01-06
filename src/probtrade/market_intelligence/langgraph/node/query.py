# === Python modules ===
from typing import List

# === Utils ===
from probtrade.utils import load_yaml

# === Agentstate ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Logger ===
from probtrade import get_logger

## === Setting up the logger ===
logger = get_logger(
    name = "NEWS_DATA",
    log_file = "news_data.log"
)

# === Query Generation Node ===
def get_queries(
    state: AgentState
) -> AgentState:
    """
    Loads the queries from the yaml file
    """
    ## === Node intiating ===
    logger.info("Initiated the `get_queries_node`.")

    ## === Loading queries from the yaml file ===
    data = load_yaml(
        file_path = "config",
        file_name = "query.yaml"
    )
    logger.info("Loaded the queries successfully.")

    ## === Initialising an empty list ===
    queries: List[str] = []

    ## === Looping through the data ===
    for q in data.get("queries"):
        queries.append(data["queries"][q]["query"])

    state["queries"] = queries
    logger.info("Finished the `get_queries_node`.")

    return state