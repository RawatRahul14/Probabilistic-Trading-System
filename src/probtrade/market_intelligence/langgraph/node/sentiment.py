# === Python Modules ===
from typing import List
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
def get_sentiment(
        state: AgentState
) -> AgentState:
    """
    Usnig OpenAI's ChatOpenAI, finding the sentiment of the fetched news articles.
    """
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
                "news_impact": response.news_impact
            }
        )

    state["sentiments"] = sentiments
    logger.info("Finished the `get_sentiment_node`.")

    return state