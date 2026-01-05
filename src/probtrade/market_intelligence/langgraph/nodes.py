# === Python modules ===
from typing import List
from dotenv import load_dotenv

# === Utils ===
from probtrade.utils import load_yaml, get_date

# === Tavily Search Agent ===
from probtrade.market_intelligence import fetch_data_tavily

# === Agentstate ===
from .state import AgentState

# === Loading env keys ===
load_dotenv()

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