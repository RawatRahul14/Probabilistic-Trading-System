# === Python modules ===
from typing import List
import time

# === Utils ===
from probtrade.utils import GetQueries

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
async def get_queries(
    state: AgentState
) -> AgentState:
    """
    Loads the queries from the yaml file
    """
    ## === Start Time ===
    start_time = time.perf_counter()

    ## === Node intiating ===
    logger.info("Initiated the `get_queries_node`.")

    ## === Loading queries from the yaml file ===
    queries_fn = GetQueries()
    queries_data = queries_fn.get_queries()

    logger.info("Loaded the queries successfully.")

    ## === Initialising an empty list ===
    queries: List[str] = []

    try:
        ## === Getting the Queries ===
        queries = queries_fn.list_queries(
            data = queries_data
        )

        state["queries"] = queries

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f"Finished the `get_queries_node`, Duration = {duration:.2f}s.")

    except Exception as e:
        logger.exception("Error occurred in `get_queries_node`")

    return state