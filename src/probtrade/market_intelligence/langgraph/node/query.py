# === Python modules ===
from typing import List

# === Utils ===
from probtrade.utils import load_yaml

# === Agentstate ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Query Generation Node ===
def get_queries(
    state: AgentState
) -> AgentState:
    """
    Loads the queries from the yaml file
    """
    ## === Getting the date ===
    # state["date"] = get_date()

    ## === Loading queries from the yaml file ===
    data = load_yaml(
        file_path = "config",
        file_name = "query.yaml"
    )

    ## === Initialising an empty list ===
    queries: List[str] = []

    ## === Looping through the data ===
    for q in data.get("queries"):
        queries.append(data["queries"][q]["query"])

    state["queries"] = queries

    return state