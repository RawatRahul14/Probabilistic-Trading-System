# === Python Modules ===
from typing import List
import time
from datetime import date

# === Utils ===
from probtrade.utils import (
    normalize_text,
    get_content
)

# === Agent State ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Data Logic ===
from probtrade.data.database.save_news import NewsDuckDB

# === Logger ===
from probtrade import get_logger

logger = get_logger(
    name = "NEWS_DATA",
    log_file = "news_data.log"
)

# === Function to remove the duplicated news articles ===
async def apply_deduplicate(
        state: AgentState
) -> AgentState:
    """
    Normalises the text and removes the duplicated news article before proceeding for the sentiment.
    """
    ## === Start Time ===
    start_time = time.perf_counter()

    ## === Getting the today's news ===
    db = NewsDuckDB()
    data = db.load_by_date(date = date.today().isoformat())

    ## === Initiating the norm_content key ===
    norm_content: List[str] = []

    ## === Node intiating ===
    logger.info("Initiated the `apply_deduplicate_node`.")

    try:
        ## === Normalising the content text ===
        for content in state.get("contents"):
            norm_content.append(
                normalize_text(text = content)
            )

        ## === Getting deduplication keys process ===
        limit = 300
        dedup_keys = set(get_content(
            data,
            character_limit = limit
        ))

        filtered_norm_content: List[str] = []
        ## === Looping through the normalised data ===
        for text in norm_content:
            key = text[:limit]

            if key not in dedup_keys:
                filtered_norm_content.append(text)

        ## === only passing the dedup data ===
        state["norm_content"] = filtered_norm_content

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f"Finished the `apply_deduplicate_node`, , Duration = {duration:.2f}s, Before = {len(norm_content)}, After = {len(filtered_norm_content)}.")

        return state

    except Exception as e:
        raise