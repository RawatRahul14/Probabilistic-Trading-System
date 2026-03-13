# === Python Modules ===
import pandas as pd

# === VixState ===
from ...state import VixState

# === Saving Vix Logic ===
from probtrade.utils import append_vix

# === Logger ===
from probtrade import get_logger

logger = get_logger(
    name = "VIX",
    log_file = "vix.log"
)

async def save_vix_db_node(
        state: VixState
) -> VixState:
    """
    Saves the fetched VIX from the web to a database
    """
    logger.info("Saving the fetched VIX value in the Database.")
    try:
        ## === Saving the VIX in DB ====
        vix_value = state.get("india_vix")

        append_vix(
            vix_data = vix_value
        )

        logger.info("Completed saving the fetched VIX value in the Database.")
        logger.info("="*70)
        logger.info("\n")

    except Exception as e:
        logger.exception("Error Saving the VIX value in the database.")
        raise