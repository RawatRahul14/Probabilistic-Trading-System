# === Python Modules ===
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class SentimentSchema(BaseModel):
    sentiment_score: int = Field(
        description = "Sentiment given to a news fetched from web using tavily. 0 means negative news whereas 10 means positive news.",
        ge = 0,
        le = 10
    )

    news_impact: Literal["very_low", "low", "medium", "high", "very_high"] = Field(
        description = "Suggested impact of the news on market."
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