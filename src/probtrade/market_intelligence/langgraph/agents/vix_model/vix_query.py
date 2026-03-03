# === Python Modules ===
import time
from typing import List, Dict

# === Utils ===
from probtrade.utils import load_yaml

# === VixState ===
from ...state import VixState

# === Logger ===
from probtrade import get_logger

# === Initialising the logger ===
logger = get_logger(
    name = "VIX",
    log_file = "vix.log"
)

# === Extracts queries for the vix ===
async def extract_vix_query(
        state: VixState
) -> VixState:
    """
    Retrieves VIX query from the `config/vix_query.yaml`
    """
    ## === Starting the Counter ===
    start_time = time.perf_counter()
    logger.info("Starting the VIX query ingestion.")

    try:
        vix_query: Dict[str, List[str]] = load_yaml(
            file_path = "config",
            file_name = "vix_query.yaml"
        )

        ## === Raising exception if there's more than 1 query ===
        if len(vix_query) != 1:
            logger.exception(f"Invalid VIX query config: Expected exactly 1 root key in vix_query.yaml, found: {len(vix_query)}.")
            raise

        ## === Saving the query in the state ===
        state["vix_query"] = vix_query["query"]

        ## === Stooping the counter ===
        end_time = time.perf_counter()

        ## === Duration ===
        duration = end_time - start_time

        logger.info(f"Completed the VIX query ingestion, Duration = {duration}.")

        return state

    except Exception as e:
        logger.exception("Error fetching the query from the `config/vix_query.yaml`.")
        raise