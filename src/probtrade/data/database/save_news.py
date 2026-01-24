# === Python Modules ===
import duckdb
import json
from pathlib import Path
import pandas as pd

# === Schema ===
from probtrade.schemas import NewsStat

# ===  ===
class NewsDuckDB:
    def __init__(
        self,
        file_name: str | None = None,
        folder_name: str = "news",
        json_name: str = "sentiment_data.json"
    ):
        ## === Paths ===
        self.folder_path = Path(folder_name)
        self.folder_path.mkdir(
            parents = True,
            exist_ok = True
        )

        self.db_path = self.folder_path / (file_name or "news.db")
        self.json_path = self.folder_path / json_name

        ## === IMPORTANT: check existence BEFORE any DB connection ===
        self.db_exists = self.db_path.exists()

        ## === Initialize DB ===
        self._init_db()

        ## === One-time migration ===
        if not self.db_exists and self.json_path.exists():
            self._migrate_json_to_db()

    def _init_db(self):
        """
        Create DB and table if not exists.
        """
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    content JSON,
                    sentiment_score INTEGER,
                    market_bias TEXT,
                    news_impact TEXT,
                    confidence DOUBLE,
                    timestamp TIMESTAMPTZ
                )
            """)

    def _migrate_json_to_db(self):
        """
        One-time migration from existing sentiment_data.json -> DuckDB.
        """
        ## === Loading the json data ===
        with open(self.json_path, "r", encoding = "utf-8") as f:
            data = json.load(f)

        ## === If the data is not a List ===
        if not isinstance(data, list):
            raise ValueError("sentiment_data.json must contain a list of news entries")

        ## === Migrating the News data into the duckdb database ===
        with duckdb.connect(str(self.db_path)) as conn:
            for entry in data:
                raw_content = entry.get("content")

                if isinstance(raw_content, list):
                    content = raw_content
                elif isinstance(raw_content, str):
                    content = [raw_content]
                else:
                    content = []

                conn.execute(
                    """
                    INSERT INTO news (
                        content,
                        sentiment_score,
                        market_bias,
                        news_impact,
                        confidence,
                        timestamp
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        content,
                        entry.get("sentiment_score"),
                        entry.get("market_bias"),
                        entry.get("news_impact"),
                        entry.get("confidence"),
                        entry.get("timestamp")
                    ]
                )

    def insert_news(
            self,
            news_entry: NewsStat
    ):
        """
        Insert a single new news entry.
        """
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO news (
                    content,
                    sentiment_score,
                    market_bias,
                    news_impact,
                    confidence,
                    timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    news_entry.get("content"),
                    news_entry.get("sentiment_score"),
                    news_entry.get("market_bias"),
                    news_entry.get("news_impact"),
                    news_entry.get("confidence"),
                    news_entry.get("timestamp")
                ]
            )

    def load_news(
            self,
            n: int = 5
    ) -> pd.DataFrame:
        """
        Load latest `n` news entries from DuckDB.
        """
        ## === Query for the data loading ===
        query = f"""
            SELECT *
            FROM news
            ORDER BY timestamp DESC
        """

        ## === Loading the whole table ===
        if n != -1:
            query += f" LIMIT {n}"

        ## === making connection and loading the dataset ===
        with duckdb.connect(str(self.db_path)) as conn:
            return conn.execute(query).fetchdf()