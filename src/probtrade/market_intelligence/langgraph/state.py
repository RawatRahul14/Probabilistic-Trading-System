# === Python Modules ===
from typing import TypedDict, List

# === Schema ===
from probtrade.market_intelligence.langgraph.config.config import SentimentConfig

# === AgentState ===
class AgentState(TypedDict):

    ## === Date ===
    # date: str

    ## === Queries ===
    queries: List[str]

    ## === Contents ===
    contents: List[str]

    ## === Sentiments ===
    sentiments: List[SentimentConfig]