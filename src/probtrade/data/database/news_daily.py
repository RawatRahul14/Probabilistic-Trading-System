# === Python Modules ===
from pathlib import Path
import duckdb
from datetime import datetime, date
import pandas as pd

# === Schema ===
from probtrade.schemas import DailyNewsRun

# === Class for the Aggregation of daily news and the Probability for each category ===
class DailyNewsDuckDB:
    def __init__(
            self,
            file_name: str | None = None,
            folder_name: str | Path = "db",
            news_table_name: str = "news_agg_sentiment",
            daily_news_table_name: str = "daily_news"
    ):
        ## === getting the Database Folder Path ===
        self.folder_path = Path(folder_name)
        self.db_path = self.folder_path / (file_name or "sentiment.db")

        self.news_table_name = news_table_name
        self.daily_news_table_name = daily_news_table_name

        ## === Initialising the table creation ===
        self._init_db()

    ## === Function to Initiate the table creation if not exists ===
    def _init_db(self):
        """
        Creates the Table if not exists
        """
        ## === Connecting to the Database ===
        with duckdb.connect(str(self.db_path)) as conn:

            ## === Query Execution ===
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.daily_news_table_name} (
                    date DATE,
                    unique_runs INTEGER,
                    news_count INTEGER,
                    sentiment_mean DOUBLE,
                    sentiment_std DOUBLE,
                    daily_bias_score DOUBLE,
                    bullish_count INTEGER,
                    bearish_count INTEGER,
                    neutral_count INTEGER,
                    bullish_prob DOUBLE,
                    bearish_prob DOUBLE,
                    neutral_prob DOUBLE,
                    sentiment_disagreement DOUBLE
                )
            """)

    ## === Validates the date Format ===
    def _validate_date(
            self,
            date_str: str
    ) -> str:
        """
        Validates date format (YYYY-MM-DD).
        Returns normalized date string.
        Raises ValueError if invalid.
        """
        try:
            return datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date().isoformat()

        except ValueError:
            raise ValueError(
                f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD."
            )

    ## === Function to load just the todays data ===
    def load_data(
            self,
            date: str | None = None
    ) -> pd.DataFrame:
        """
        Loads all rows from the parent news table for a given date. If date is None, loads today's data.
        """
        ## === Connecting to the database ===
        with duckdb.connect(str(self.db_path)) as conn:
            
            ## === If date is not mentioned ===
            if date is None:
                query = f"""
                    SELECT *
                    FROM {self.news_table_name}
                    WHERE DATE(timestamp) = CURRENT_DATE
                    ORDER BY timestamp DESC
                """

                ## === Execute the Query ===
                return conn.execute(query).fetchdf()
            
            else:
                ## === Validating the date format ===
                valid_date = self._validate_date(date_str = date)
                
                query = f"""
                    SELECT *
                    FROM {self.news_table_name}
                    WHERE DATE(timestamp) = ?
                    ORDER BY timestamp DESC
                """

                ## === Execute the Query ===
                return conn.execute(query, [valid_date]).fetchdf()

    ## === Function to insert the data into the table ===
    def insert_data(
            self,
            data: DailyNewsRun
    ):
        """
        Inserts the data into the daily_news table inside the sentiment db.
        """
        with duckdb.connect(str(self.db_path)) as conn:
            ## === Making sure that there's exists only 1 date ===
            conn.execute(
                f"""
                    DELETE FROM {self.daily_news_table_name}
                    WHERE DATE(date) = ?
                """,
                [data["date"]]
            )

            ## === Inserting the data in the table ===
            conn.execute(
                f"""
                    INSERT INTO {self.daily_news_table_name} (
                        date,
                        unique_runs,
                        news_count,
                        sentiment_mean,
                        sentiment_std,
                        daily_bias_score,
                        bullish_count,
                        bearish_count,
                        neutral_count,
                        bullish_prob,
                        bearish_prob,
                        neutral_prob,
                        sentiment_disagreement
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    data["date"],
                    data["unique_runs"],
                    data["news_count"],
                    data["sentiment_mean"],
                    data["sentiment_std"],
                    data["daily_bias_score"],
                    data["bullish_count"],
                    data["bearish_count"],
                    data["neutral_count"],
                    data["bullish_prob"],
                    data["bearish_prob"],
                    data["neutral_prob"],
                    data["sentiment_disagreement"]
                ]
            )