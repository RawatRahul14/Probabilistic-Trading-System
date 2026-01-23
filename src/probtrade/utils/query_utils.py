# === Python Modules ===
from pathlib import Path
from typing import List, Dict, Any

# === Utils ===
from .common import load_yaml
from .time_utils import GetTime

# === Function to get the queries depending on the time ===
class GetQueries:
    def __init__(
            self,
            file_name: str | None = None
    ):
        name = file_name or "query.yaml"
        self.file_name = Path(name)

    def get_queries(self) -> Dict[str, Any]:
        """
        Extracts the queries from the yaml file
        """
        queries_yaml = load_yaml(
                file_path = "config",
                file_name = self.file_name
            )

        return queries_yaml

    def list_queries(
            self,
            data: Dict[str, Any]
    ) -> List[str]:
        """
        Lists the appropriate queries depending on the market status
        """
            ## === Current Time and Market Status ===
        get_time = GetTime()
        market_status = get_time.market_aware()

        ## === Initiating an empty List to hold all the queries ===
        queries: List[str] = []

        ## === Getting only the appropriate queries ===
        for query_name, query_data in data["queries"].items():

            ## === Extracting the time associated with the query ===
            when = query_data.get("when")

            ## === If `when` doesn't exist ===
            if not when:
                raise ValueError(f"`when` missing in the query: {query_name}")

            if market_status in when:
                queries.append(query_data["query"])

        return queries