# === Python Modules ===
# === Agent State ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Function to remove the duplicated news articles ===
async def apply_deduplicate(
        state: AgentState
) -> AgentState:
    """
    Removes the duplicated news article before proceeding for the sentiment.
    """
    