# === Python modules ===
from typing import List
import time

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
    data = load_yaml(
        file_path = "config",
        file_name = "query.yaml"
    )
    logger.info("Loaded the queries successfully.")

    ## === Initialising an empty list ===
    queries: List[str] = []

    try:
        ## === Looping through the data ===
        for q in data.get("queries"):
            queries.append(data["queries"][q]["query"])

        state["queries"] = queries

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f"Finished the `get_queries_node`, Duration = {duration:.2f}s.")

    except Exception as e:
        logger.exception("Error occurred in `get_queries_node`")

    return state