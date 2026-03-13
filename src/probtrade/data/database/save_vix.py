# === Python Modules ===
import duckdb 
import pandas as pd
from pathlib import Path

# === Class method for saving vix in duckdb database (news/vix.db) ===
class VixDuckDB:
    def __init__(
            self,
            file_name: str | None = None,
            folder_name: str = "news"
    ):
        ## === Paths ===
        self.folder_path = Path(folder_name)
        self.folder_path.mkdir(
            parents = True,
            exist_ok = True
        )

        self.db_path = self.folder_path / (file_name or "vix.db")

        ## === Initialising the database if not exists ===
        self._init_db()

    def _init_db(self):
        """
        Create DB and table if not exists.
        """
        with duckdb.connect(str(self.db_path)) as conn:
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS vix (
                        timestamp TIMESTAMPTZ,
                        vix_value DOUBLE
                    )
                """)

    def save_all(
            self,
            data: pd.DataFrame
    ):
        """
        Saves the nifty vix which is in Pandas DataFrame
        Expects columns: ['timestamp', 'vix_value']
        """
        try:
            with duckdb.connect(str(self.db_path)) as conn:

                ## === Registering the python object ===
                conn.register("vix_data", data)

                ## === Saving the Data in the table ===
                conn.execute("""
                    INSERT INTO vix
                    SELECT * FROM vix_data
                """)

                ## === Unregistering the view ===
                conn.unregister("vix_data")

        except Exception as e:
            raise

    def load_vix(
            self,
            k: int | None = None
    ) -> pd.DataFrame:
        """
        Loads the latest vix data from the database.
        """
        query = """
            SELECT * FROM vix
            ORDER BY timestamp DESC
        """

        if k is not None:
            query += f"LIMIT {k}"

        with duckdb.connect(str(self.db_path)) as conn:
            return conn.execute(query = query).fetchdf()
