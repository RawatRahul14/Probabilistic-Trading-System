# === Python Modules ===
import numpy as np
from typing import List, Tuple
from collections import Counter

# === Schema ===
from probtrade.schemas import SentimentPipelineData, SentimentStats

# === Function to extract key details from the fetched data ===
def extract_details(
        data: List[SentimentPipelineData]
) -> SentimentStats:
    """
    Extracts keys features from the dataset

    Args:
    - data (List[SentimentPipelineData]): List containing the fetched data details.

    returns:
    - news_count (int): Count of the number of news
    - sentiment_mean (float): Average of the sentiments
    - sentiment_std (float): Standard Deviation of the sentiments
    - BULLISH_count (int): BULLISH news count
    - BEARISH_count (int): BEARISH news count
    - NEUTRAL_count (int): NEUTRAL news count
    - BULLISH_prob (float): BULLISH news prob
    - BEARISH_prob (float): BEARISH news prob
    - NEUTRAL_prob (float): NEUTRAL news prob
    """
    ## === If news data is empty ===
    if not data:
        return {
            "news_count": 0,
            "sentiment_mean": 0.0,
            "sentiment_std": 0.0,
            "BULLISH_count": 0,
            "BEARISH_count": 0,
            "NEUTRAL_count": 0,
            "BULLISH_prob": 0.0,
            "BEARISH_prob": 0.0,
            "NEUTRAL_prob": 0.0,
        }

    ## === Initialising an empty dict ===
    data_dict: SentimentStats = {}
    
    ## === Number of news articles ===
    data_dict["news_count"] = len(data)

    ## === Mean and std calculations ===
    sentiment_scores = [d["sentiment_score"] for d in data]

    data_dict["sentiment_mean"] = np.mean(sentiment_scores)
    data_dict["sentiment_std"] = np.std(sentiment_scores, ddof = 0)

    ## === Counter ===
    bias_counts = Counter(d["market_bias"] for d in data)

    data_dict["BULLISH_count"] = bias_counts.get("BULLISH", 0)
    data_dict["BEARISH_count"] = bias_counts.get("BEARISH", 0)
    data_dict["NEUTRAL_count"] = bias_counts.get("NEUTRAL", 0)

    ## === Probabilities ===
    data_dict["BULLISH_prob"] = data_dict["BULLISH_count"] / data_dict["news_count"]
    data_dict["BEARISH_prob"] = data_dict["BEARISH_count"] / data_dict["news_count"]
    data_dict["NEUTRAL_prob"] = data_dict["NEUTRAL_count"] / data_dict["news_count"]

    return data_dict