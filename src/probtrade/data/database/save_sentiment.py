# === Python Modules ===
import duckdb
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# === Schema ===
from probtrade.schemas import SentimentStats

# === Setting the time zone ===
IST = ZoneInfo("Asia/Kolkata")

# === DuckDB class for saving and loading Agg sentiment data ===
class AggDuckDB:
    def __init__(self, db_path: str, run_id: str | None = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(
            parents = True,
            exist_ok = True
        )
        self.run_id = run_id
        self._init_db()

    def _init_db(self) -> None:
        """
        Initializes the DuckDB database and sentiment table. The database file is created automatically if it does not exist.
        """
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS news_agg_sentiment (
                    timestamp TIMESTAMP,
                    run_id VARCHAR,
                    agg_sentiment DOUBLE,
                    news_count INT,
                    sentiment_mean DOUBLE,
                    sentiment_std DOUBLE,
                    BULLISH_count INT,
                    BEARISH_count INT,
                    NEUTRAL_count INT,
                    BULLISH_prob DOUBLE,
                    BEARISH_prob DOUBLE,
                    NEUTRAL_prob DOUBLE
                )
            """)

    def save_agg_sentiment(
        self,
        agg_sentiment: float,
        feature_data: SentimentStats,
        timestamp: datetime | None = None
    ) -> None:
        """
        Saves aggregated news sentiment with a timestamp.
        """
        timestamp = timestamp or datetime.now(IST)

        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT INTO news_agg_sentiment (
                    timestamp,
                    run_id,
                    agg_sentiment,
                    news_count,
                    sentiment_mean,
                    sentiment_std,
                    BULLISH_count,
                    BEARISH_count,
                    NEUTRAL_count,
                    BULLISH_prob,
                    BEARISH_prob,
                    NEUTRAL_prob
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    timestamp,
                    self.run_id,
                    agg_sentiment,
                    feature_data["news_count"],
                    feature_data["sentiment_mean"],
                    feature_data["sentiment_std"], 
                    feature_data["BULLISH_count"], 
                    feature_data["BEARISH_count"],
                    feature_data["NEUTRAL_count"],
                    feature_data["BULLISH_prob"],
                    feature_data["BEARISH_prob"],
                    feature_data["NEUTRAL_prob"]
                )
            )

    def load_agg_sentiment(
            self,
            limit: int | None = None
    ):
        """
        Loads aggregated sentiment score from the database.
        """
        ## === Hardcoding limit if not given ===
        limit = limit or 5

        ## === Query for the Data loading ===
        query = f"""
            SELECT *
            FROM news_agg_sentiment
            ORDER BY timestamp DESC
            LIMIT {limit}
        """

        ## === Making connection to the file path ===
        with duckdb.connect(str(self.db_path)) as conn:
            return conn.execute(query).fetchdf()
        
    def load_agg_sentiment_date(
            self,
            date: str
    ):
        """
        Loads aggregated sentiment score from the database.
        """

        ## === Query for the Data loading ===
        query = f"""
            SELECT *
            FROM news_agg_sentiment
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp DESC
        """

        ## === Making connection to the file path ===
        with duckdb.connect(str(self.db_path)) as conn:
            return conn.execute(query, [date]).fetchdf()