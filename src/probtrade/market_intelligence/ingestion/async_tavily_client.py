# === Python Modules ===
import os
from typing import List
import asyncio
from tavily import AsyncTavilyClient
from dotenv import load_dotenv

# === Loading API Keys ===
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# === Async Tavily Client ===
tavily = AsyncTavilyClient(
    api_key = TAVILY_API_KEY
)

# === Async Tavily function ===
async def fetch_data_tavily(
    query: str
) -> List[str]:
    """
    Fetches data from Tavily asynchronously for a single query.
    """
    response = await tavily.search(
        query = query,
        topic = "news",
        time_range = "day",
        max_results = 3,
        include_raw_content = False,
        search_depth = "advanced",
        timeout = 10
    )

    ## === Extracting useful data ===
    data_dic: List[str] = []

    for data in response["results"]:
        data_dic.append(data["content"])

    return data_dic

# === Fetching Multiple queries at a time ===
async def fetch_multiple_queries(
    queries: List[str],
    concurrency: int = 5
) -> List[List[str]]:
    """
    Fetches Tavily data for multiple queries concurrently.
    """
    ## === Limiting the number of searches, to avoid rate limit ===
    semaphore = asyncio.Semaphore(concurrency)

    ## === Calling Async ===
    async def safe_fetch(q):
        async with semaphore:
            try:
                return await fetch_data_tavily(q)
            except Exception as e:
                return []

    ## === Running the async function ===
    tasks = [safe_fetch(q) for q in queries]
    return await asyncio.gather(*tasks)