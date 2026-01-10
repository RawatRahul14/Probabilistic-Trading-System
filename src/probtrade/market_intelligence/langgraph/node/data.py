# === Python modules ===
import time
from typing import List

# === Tavily Search Agent ===
from probtrade.market_intelligence import fetch_data_tavily, fetch_multiple_queries

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
async def fetch_data(
        state: AgentState
) -> AgentState:
    """
    Fetches data using the Tavily search client.
    """
    ## === Start Time ===
    start_time = time.perf_counter()

    ## === Node intiating ===
    logger.info("Initiated the `fetch_data_node`.")

    ## === All responses ===
    all_response: List[str] = []

    try:
        ## === Looping through the queries ===
        all_response = await fetch_multiple_queries(queries = state["queries"])

        state["contents"] = all_response

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f"Finished the `fetch_data_node`, Duration = {duration:.2f}s, Articles = {len(all_response)}.")

    except Exception as e:
        logger.exception("Error occurred in `fetch_data_node`")
        raise

    return state