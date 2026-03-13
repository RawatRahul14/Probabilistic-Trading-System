# === Python Modules ===
import re

# === VixState ===
from ...state import VixState

# === Logger ===
from probtrade import get_logger

# === Initiating the Logger ===
logger = get_logger(
    name = "VIX",
    log_file = "vix.log"
)

# === Function to extract the indian vix from the the string ===
async def extract_india_vix(
        state: VixState
) -> VixState:
    """
    Extracts the indian vix from the string fetched from the web using tavily.
    """

    logger.info("Starting the VIX Exttracting from the fetched data.")

    ## === Pattern to search in query ===
    pattern = r"India VIX\s*\|\s*([\d\.]+)"

    try:
        ## === Finding the match ===
        match = re.search(
            pattern,
            state.get("vix_fetched")[0][0]
        )

        ## === If match is found ===
        if match:
            state["india_vix"] = float(match.group(1))

        else:
            state["india_vix"] = 0.0

        logger.info(f"Completed the VIX Exttracting from the fetched data. VIX = {state.get('india_vix')}")

        return state

    except re.error as e:
        raise e