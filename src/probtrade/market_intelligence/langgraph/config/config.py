# === Python Modules ===
from typing import TypedDict, Literal

# === Configuration for the Sentiment Dictionary ===
class SentimentConfig(TypedDict):
    content: str
    sentiment_score: int
    news_impact: Literal["low", "medium", "high"]