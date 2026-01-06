# === Python modules ===
from typing import List

# === Tavily Search Agent ===
from probtrade.market_intelligence import fetch_data_tavily

# === Agentstate ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Fetch Data ===
def fetch_data(
        state: AgentState
) -> AgentState:
    """
    Fetches data using the Tavily search client.
    """
    ## === All responses ===
    all_response: List[str] = []

    ## === Looping through the queries ===
    for query in state["queries"]:
        all_response.extend(fetch_data_tavily(query = query))

    state["contents"] = all_response

    return state