# === Python Modules ===
import re

# === VixState ===
from ...state import VixState

# === Function to extract the indian vix from the the string ===
async def extract_india_vix(
        state: VixState
) -> VixState:
    """
    Extracts the indian vix from the string fetched from the web using tavily.
    """
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

        return state

    except re.error as e:
        raise e