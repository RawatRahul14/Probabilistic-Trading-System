# === Python modules ===
from typing import List

# === Tavily Search Agent ===
from probtrade.market_intelligence import fetch_data_tavily

# === Agentstate ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Logger ===
from probtrade import get_logger

## === Setting up the logger ===
logger = get_logger(
    name = "NEWS_DATA",
    log_file = "news_data.log"
)

# === Fetch Data ===
def fetch_data(
        state: AgentState
) -> AgentState:
    """
    Fetches data using the Tavily search client.
    """
    ## === Node intiating ===
    logger.info("Initiated the `fetch_data_node`.")

    ## === All responses ===
    all_response: List[str] = []

    ## === Looping through the queries ===
    for query in state["queries"]:
        all_response.extend(fetch_data_tavily(query = query))

    state["contents"] = all_response
    logger.info("Finished the `fetch_data_node`.")

    return state