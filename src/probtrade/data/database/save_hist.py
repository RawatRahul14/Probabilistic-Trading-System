# === Python Module ===
import duckdb
from pathlib import Path
from typing import List

# === Saves the historical data in the database ===
class HistoricalDuckDB:
    def __init__(
            self,
            tickers_raw_path: Path,
            index_raw_path: Path,
            tickers_list: List[str],
            index_list: List[str]
    ):
        pass

    def _init_db(self):
        """
        Create DB and table if not exists.
        """
        TABLE_SCHEMA = """
            CREATE TABLE IF NOT EXISTS {table_name} (
                datetime TIMESTAMP,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volumne DOUBLE
            )
        """