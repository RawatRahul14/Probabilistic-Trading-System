# === Python Modules ===
import duckdb
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# === Setting the time zone ===
IST = ZoneInfo("Asia/Kolkata")

# === DuckDB class for saving and loading Agg sentiment data ===
class AggDuckDB:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(
            parents = True,
            exist_ok = True
        )
        self._init_db()

    def _init_db(self) -> None:
        """
        Initializes the DuckDB database and sentiment table. The database file is created automatically if it does not exist.
        """
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS news_agg_sentiment (
                    timestamp TIMESTAMP,
                    agg_sentiment DOUBLE
                )
            """)

    def save_agg_sentiment(
        self,
        agg_sentiment: float,
        timestamp: datetime | None = None
    ) -> None:
        """
        Saves aggregated news sentiment with a timestamp.
        """
        timestamp = timestamp or datetime.now(IST)

        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute(
                "INSERT INTO news_agg_sentiment VALUES (?, ?)",
                (timestamp, agg_sentiment)
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
            SELECT timestamp, agg_sentiment
            FROM news_agg_sentiment
            ORDER BY timestamp DESC
            LIMIT {limit}
        """

        ## === Making connection to the file path ===
        with duckdb.connect(str(self.db_path)) as conn:
            return conn.execute(query).fetchdf()