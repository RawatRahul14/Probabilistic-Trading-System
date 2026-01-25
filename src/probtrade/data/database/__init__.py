from .save_sentiment import (
    AggDuckDB
)

from .save_news import (
    NewsDuckDB
)

from .news_daily import (
    DailyNewsDuckDB
)

__all__ = [
    "AggDuckDB",
    "NewsDuckDB",
    "DailyNewsDuckDB"
]