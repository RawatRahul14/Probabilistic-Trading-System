# === Python Modules ===
from typing import TypedDict, List, Any, Annotated
import operator

# === Schema ===
from probtrade.market_intelligence.langgraph.config.config import SentimentConfig

# === AgentState ===
class AgentState(TypedDict):

    #### ==== Sentiment Model ====
    ## === Queries ===
    queries: List[str]

    ## === Contents ===
    contents: List[str]

    ## === Normalized Content ===
    norm_content: List[str]

    ## === Sentiments ===
    sentiments: List[SentimentConfig]

    #### ==== VIX Model ====
    ## === VIX query ===
    vix_query: List[str]

    ## === VIX fetched ===
    vix_fetched: Any

    ## === India VIX ===
    india_vix: float

class NewsState(TypedDict):
    #### ==== Sentiment Model ====
    ## === Queries ===
    queries: List[str]

    ## === Contents ===
    contents: List[str]

    ## === Normalized Content ===
    norm_content: List[str]

    ## === Sentiments ===
    sentiments: List[SentimentConfig]

class VixState(TypedDict):
    #### ==== VIX Model ====
    ## === VIX query ===
    vix_query: List[str]

    ## === VIX fetched ===
    vix_fetched: Any

    ## === India VIX ===
    india_vix: float