# === Python Modules ===
from typing import List
import time
import asyncio
from langchain_openai import ChatOpenAI

# === Utils ===
from probtrade.utils import read_md

# === Schema ===
from probtrade.market_intelligence.schemas import SentimentSchema
from probtrade.market_intelligence.langgraph.config.config import SentimentConfig

# === AgentState ===
from probtrade.market_intelligence.langgraph.state import AgentState

# === Logger ===
from probtrade import get_logger

## === Setting up the logger ===
logger = get_logger(
    name = "NEWS_DATA",
    log_file = "news_data.log"
)

# === Function to get the sentiment scores of the fetched news data ===
async def get_sentiment(
        state: AgentState
) -> AgentState:
    """
    Using OpenAI's ChatOpenAI, finding the sentiment of the fetched news articles.
    """
    ## === Start Time ===
    start_time = time.perf_counter()

    ## === Node intiating ===
    logger.info("Initiated the `get_sentiment_node`.")

    ## === LLM model ===
    llm = ChatOpenAI(
        model = "gpt-4o-mini",
        temperature = 0.0
    ).with_structured_output(SentimentSchema)

    ## === Prompts ===
    system_prompt = read_md(
        file_path = "prompts/sentiment.md"
    )

    ## === Placeholder to hold sentiment scores ===
    sentiments: List[SentimentConfig] = []

    ## === Concurrency limiter ===
    semaphore = asyncio.Semaphore(5)

    async def analyze_news(news: str):
        async with semaphore:
            try:
                ## === Setting up the user prompt ===
                user_prompt = (
                    "Analyze the following financial news item:\n\n"
                    f"{news}"
                )

                ## === Invoking the llm model asynchronously ===
                response = await llm.ainvoke(
                    [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )

                return {
                    "content": news,
                    "sentiment_score": response.sentiment_score,
                    "market_bias": response.market_bias,
                    "news_impact": response.news_impact,
                    "confidence": response.confidence
                }

            except Exception:
                logger.exception("Error occurred while processing a news item.")
                return None

    try:
        ## === Creating async tasks ===
        tasks = [
            analyze_news(news)
            for news in state.get("norm_content", [])
        ]

        ## === Running tasks concurrently ===
        results = await asyncio.gather(*tasks)

        ## === Filtering valid results ===
        sentiments = [
            result for result in results
            if result is not None
        ]

        state["sentiments"] = sentiments

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(
            f"Finished the `get_sentiment_node`, "
            f"Duration = {duration:.2f}s, "
            f"Items = {len(sentiments)}."
        )

    except Exception:
        logger.exception("Error occurred in `get_sentiment_node`")

    return state