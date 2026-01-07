# === Python Modules ===
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class SentimentSchema(BaseModel):
    sentiment_score: int = Field(
        description = "Sentiment given to a news fetched from web using tavily. 0 means negative news whereas 10 means positive news.",
        ge = 0,
        le = 10
    )

    market_bias: Literal["BULLISH", "NEUTRAL", "BEARISH"] = Field(
        description = "Expected short-term directional pressure on Indian equity indices"
    )

    news_impact: Literal["very_low", "low", "medium", "high", "very_high"] = Field(
        description = "Suggested impact of the news on market."
    )

    confidence: float = Field(
        description = "Confidence in the assigned market_bias",
        ge = 0.0,
        le = 1.0
    )

    @field_validator("sentiment_score")
    @classmethod
    def validate_sentiment_score(cls, v: int) -> int:

        ## === If the score datatype is not integer ===
        if not isinstance(v, int):
            raise TypeError("sentiment_score must be an integer.")

        ## === If the value is not between 0 and 10 ===
        if not 0 <= v <= 10:
            raise ValueError("sentiment_score must be between 0 and 10.")

        return v
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: int) -> int:

        ## === If the score datatype is not integer ===
        if not isinstance(v, float):
            raise TypeError("confidence must be a float value.")

        ## === If the value is not between 0 and 1 ===
        if not 0.0 <= v <= 1.0:
            raise ValueError("confidence must be between 0 and 1.")

        return v