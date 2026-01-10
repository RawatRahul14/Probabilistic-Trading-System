# === Python Modules ===
from typing import List
from langchain_openai import ChatOpenAI
import time

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
    Usnig OpenAI's ChatOpenAI, finding the sentiment of the fetched news articles.
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

    try:
        ## === Looping through the news ===
        for news in state.get("contents"):

            ## === Setting up the user prompt ===
            user_prompt = (
                "Analyze the following financial news item:\n\n"
                f"{news}"
            )

            ## === Invoking the llm model ===
            response = llm.invoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            ## === Saving the data ===
            sentiments.append(
                {
                    "content": news,
                    "sentiment_score": response.sentiment_score,
                    "market_bias": response.market_bias,
                    "news_impact": response.news_impact,
                    "confidence": response.confidence
                }
            )

        state["sentiments"] = sentiments

        ## === Stop Time ===
        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f"Finished the `get_sentiment_node`, Duration = {duration:.2f}s, Items = {len(sentiments)}.")

    except Exception as e:
        logger.exception("Error occurred in `get_sentiment_node`")

    return state