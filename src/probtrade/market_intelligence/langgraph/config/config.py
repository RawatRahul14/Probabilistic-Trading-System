# === Python Modules ===
from typing import TypedDict, Literal

# === Configuration for the Sentiment Dictionary ===
class SentimentConfig(TypedDict):
    content: str
    sentiment_score: int
    market_bias: Literal["BULLISH", "NEUTRAL", "BEARISH"]
    news_impact: Literal["very_low", "low", "medium", "high", "very_high"]
    confidence: float