# === Python Modules ===
from typing import Literal
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# === Logger Directory ===
LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    exist_ok = True
)

# === Logger Function ===
def get_logger(
        name: Literal[
            "NEWS_DATA",
            "SENTIMENT_AGGREGATION",
            "SAVING_SENTIMENT",
            "Main",
            "DAILY_NEWS_AGG"
        ],
        log_file: Literal[
            "news_data.log",
            "main.log",
            "sentiment.log",
            "save_sentiment.log",
            "daily_news_agg.py"
        ],
        level: int = logging.INFO
) -> logging.Logger:
    """
    Returns a configured logger.
    """
    logger = logging.getLogger(name = name)

    ## === Returns if the logger already exists ===
    if logger.handlers:
        return logger
    
    ## === Configuring the logger ===
    logger.setLevel(level = level)

    formatter = logging.Formatter(
        fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    ## === File Handler ===
    file_handler = RotatingFileHandler(
        filename = LOG_DIR / log_file,
        maxBytes = 150_000_000,
        backupCount = 5
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    ## === Console Handler ===
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger