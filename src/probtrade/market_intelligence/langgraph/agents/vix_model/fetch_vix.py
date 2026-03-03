# === Python Modules ===
import time

# === VixState ===
from ...state import VixState

# === Async Tavily Ingestion ===
from probtrade.market_intelligence.ingestion import fetch_multiple_queries

# === Logger ===
from probtrade import get_logger

# === Initiating the Logger ===
logger = get_logger(
    name = "VIX",
    log_file = "vix.log"
)

# === AI Agent to fetch the nifty vix ===
async def get_vix(
        state: VixState
) -> VixState:
    """
    Fetches the nifty vix for 15 min intervals from the web using the Async Tavily
    """
    ## === Starting the timer ===
    start_time = time.perf_counter()

    try:
        logger.info("Starting the VIX fetching from the web.")

        ## === Using the Async to fetch the vix ===
        vix_fetched = await fetch_multiple_queries(
            queries = state.get("vix_query"),
            max_results = 1,
            topic = "news"
        )

        state["vix_fetched"] = vix_fetched

        ## === Ending the timer ===
        end_time = time.perf_counter()

        duration = end_time - start_time

        logger.info(f"Completed the VIX fetching from the web. Duration: {duration}")

        return state

    except Exception as e:
        logger.exception("Error fetching the vix from the web.")
        raise