# === Python Module ===
import duckdb
from pathlib import Path
from typing import List
import pandas as pd

# === Saves the historical data in the database ===
class HistoricalDuckDB:
    def __init__(
            self,
            ticker_index_raw_path: Path | None = None,
            ticker_index: str | None = None
    ):
        self.ticker_index_raw_path = ticker_index_raw_path
        self.ticker_index = ticker_index

        ## === Initialising the duckdb connection ===
        self._init_db()

    def _init_db(self):
        """
        Create DB and table if not exists.
        """
        TABLE_SCHEMA = """
            CREATE TABLE IF NOT EXISTS {ticker_index_name} (
                datetime TIMESTAMP,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume DOUBLE
            )
        """

        ## === Connecting to the DuckDb ===
        with duckdb.connect(str(self.ticker_index_raw_path ) + ".db") as conn:
            conn.execute(
                TABLE_SCHEMA.format(
                    ticker_index_name = self.ticker_index
                )
            )

    def insert(
            self,
            key: str,
            values: pd.DataFrame
    ):
        """
        Inserts the data into their respective tables

        Args:
            - key (str): Table name
            - values (pd.DataFrame): Data of that ticker/index
        """
        if values is None or values.empty:
            raise ValueError(f"Cannot insert empty data for {key}")

        try:
            ## === Create a copy to avoid modifying original ===
            dataset = values.copy()
            
            ## === Reset index if it's a DatetimeIndex ===
            if isinstance(dataset.index, pd.DatetimeIndex):
                dataset = dataset.reset_index()
                datetime_col = dataset.columns[0]
            else:
                datetime_col = None
            
            ## === Handle timezone-aware datetime if present ===
            if datetime_col and hasattr(dataset[datetime_col].dtype, "tz"):
                if dataset[datetime_col].dtype.tz is not None:
                    dataset[datetime_col] = dataset[datetime_col].dt.tz_localize(None)
            
            ## === Normalize column names to lowercase ===
            dataset.columns = [col.lower() for col in dataset.columns]
            
            ## === Get the datetime column name (could be 'date', 'datetime', etc.) ===
            datetime_col_lower = datetime_col.lower() if datetime_col else None
            
            with duckdb.connect(str(self.ticker_index_raw_path) + ".db") as conn:

                ## === Create temporary table from DataFrame ===
                conn.execute("CREATE TEMP TABLE temp_data AS SELECT * FROM dataset")

                # Insert from temporary table
                conn.execute(f"""
                    INSERT INTO {key} (
                        datetime,
                        open,
                        high,
                        low,
                        close,
                        volume
                    )
                    SELECT 
                        {datetime_col_lower},
                        open,
                        high,
                        low,
                        close,
                        volume
                    FROM temp_data
                """)

                conn.commit()

        except Exception as e:
            raise Exception(f"Failed to insert data for {key}: {str(e)}")