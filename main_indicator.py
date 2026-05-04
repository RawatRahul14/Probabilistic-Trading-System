# === Python Modules ===
from typing import List
from pathlib import Path
import duckdb

# === Pipeline ===
from probtrade.pipelines import IndicatorPipeline

# === Utils ===
from probtrade.utils import load_yaml, normalise_ticker

# === Function to Calculate the indicators for all the stocks/indexes ===
def main_indicator_fn(
        raw_data_filename: str = "data/raw",
        processed_data_filename: str = "data/processed",
        sub_folder_1: List[str] = ["index", "stocks"],
        time_frame: List[str] = ["5m", "15m", "30m", "1h", "1d"]
) -> None:
    """
    Loops through all the stocks/indices and calculate the indicators for all.
    """
    ## === Stocks List ===
    stocks = load_yaml(
        file_path = "config",
        file_name = "tickers.yaml"
    )["stocks"]

    ## === Index List ===
    indices = load_yaml(
        file_path = "config",
        file_name = "index.yaml"
    )["index"]

    ## === Paths ===
    raw_data_filename = Path(raw_data_filename)
    processed_data_filename = Path(processed_data_filename)

    try:
        ## === Initiating the Indicator pipeline ===
        indicator_pipeline = IndicatorPipeline()

        ## === Looping through the folders ===
        for folder in sub_folder_1:
            folder_path = raw_data_filename / f"{folder}"

            ## === Looping through different timeframes ===
            for timeframe in time_frame:
                db_path = str(folder_path / f"{timeframe}")