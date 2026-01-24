# === Python Modules ===
from typing import TypedDict, Literal, List

# === Sentiment Pipeline Data ===
class SentimentPipelineData(TypedDict):
    sentiment_score: int
    market_bias: Literal["BULLISH", "NEUTRAL", "BEARISH"]
    news_impact: Literal["very_low", "low", "medium", "high", "very_high"]
    confidence: float

# === Sentiment Stats, used in (src/probtrade/utils/sentiment_utils.py)===
class SentimentStats(TypedDict):
    ## === News Count ===
    news_count: int

    ## === Mean and std ===
    sentiment_mean: float
    sentiment_std: float

    ## === Count for Market Bias ===
    BULLISH_count: int
    BEARISH_count: int
    NEUTRAL_count: int

    ## === Probabilities ===
    BULLISH_prob: float
    BEARISH_prob: float
    NEUTRAL_prob: float

# === News Stats, used in (src/probtrade/data/database/save_news.py) ===
class NewsStat(TypedDict):
    content: List[str]
    sentiment_score: int
    market_bias: Literal["BULLISH", "NEUTRAL", "BEARISH"]
    news_impact: Literal["very_low", "low", "medium", "high", "very_high"]
    confidence: float
    timestamp: str