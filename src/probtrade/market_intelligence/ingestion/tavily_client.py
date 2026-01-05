# === Python Modules ===
import os
from typing import List
from tavily import TavilyClient
from dotenv import load_dotenv

# === Loading API Keys ===
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# === Tavily Client ===
tavily = TavilyClient(
    api_key = TAVILY_API_KEY,
)

# === Tavily function ===
def fetch_data_tavily(
        query: str
):
    """
    Fetches the data from the web using Tavily client.

    Args:
        - query (str): Query that need to be searched.
    """
    ## === Getting response ===
    response = tavily.search(
        query = query,
        max_results = 3,
        include_raw_content = False,
        search_depth = "advanced"
    )

    ## === Extracting useful data ===
    data_dic: List[str] = []

    for data in response["results"]:
        data_dic.append(data["content"])

    return data_dic