"""
Pre-processing (Log Returns, Scaling, Normalization)
"""
# === Python Modules ===
import numpy as np
import pandas as pd

# === Class for Data Transformation ===
class Transformation:
    def __init__(
            self,
            data: pd.DataFrame,
            last_close: float | None = None,
            close_col: str = "close",
            high_col: str = "high",
            low_col: str = "low"
    ):
        """
        Pre-processes data for machine learning or statistical analysis.
        """
        ## === Close/High/Low Prices ===
        self.close = data[close_col]
        self.high = data[high_col]
        self.low = data[low_col]

        ## === Combined Prices ===
        self.prices: pd.DataFrame = pd.concat(
            [x for x in [self.close, self.high, self.low] if x is not None],
            axis = 1
        )

        ## === Last Prices (For Incremental Returns) ===
        self.last_close = last_close

    ## === Log Returns ===
    def calculate_log_returns(
            self
    ) -> pd.DataFrame:
        """
        Calculates log returns of the close price.
        """
        ## === If last_close is provided, prepend it to calculate the first return ===
        if self.last_close is not None:
            combined_series = pd.concat(
                [pd.Series([self.last_close]), self.close]
            )
            log_returns = np.log(combined_series / combined_series.shift(1)).iloc[1:]
        else:
            log_returns = np.log(self.close / self.close.shift(1))

        return log_returns.rename("log_returns").to_frame()

    ## === Min-Max Scaling ===
    def calculate_scaling(
            self,
            min_val: float | None = None,
            max_val: float | None = None
    ) -> pd.DataFrame:
        """
        Scales data between 0 and 1.

        Args:
            - min_val (float): The global minimum for scaling
            - max_val (float): The global maximum for scaling
        """
        ## === If global bounds are not provided, use current batch bounds ===
        current_min = min_val if min_val is not None else float(self.close.min())
        current_max = max_val if max_val is not None else float(self.close.max())

        ## === Scaling Logic ===
        if current_max == current_min:
            scaled_values = pd.Series(0.0, index = self.close.index)
        else:
            scaled_values = (self.close - current_min) / (current_max - current_min)

        return scaled_values.rename("scaled_close").to_frame()

    ## === Normalization (Z-Score) ===
    def calculate_normalization(
            self,
            mean: float | None = None,
            std: float | None = None
    ) -> pd.DataFrame:
        """
        Normalizes data to have a mean of 0 and standard deviation of 1.

        Args:
            - mean (float): The previous/global mean
            - std (float): The previous/global standard deviation
        """
        ## === If global stats are not provided, use current batch stats ===
        current_mean = mean if mean is not None else float(self.close.mean())
        current_std = std if std is not None else float(self.close.std())

        ## === Normalization Logic ===
        if current_std == 0 or np.isnan(current_std):
            normalized_values = pd.Series(0.0, index = self.close.index)
        else:
            normalized_values = (self.close - current_mean) / current_std

        return normalized_values.rename("normalized_close").to_frame()

    def calculate_all(
            self,
            min_val: float | None = None,
            max_val: float | None = None,
            mean: float | None = None,
            std: float | None = None
    ) -> pd.DataFrame:
        """
        Calculates all transformations in one go.
        """
        ## === Calculating Log Returns ===
        log_df: pd.DataFrame = self.calculate_log_returns()

        ## === Calculating Scaling ===
        scaling_df: pd.DataFrame = self.calculate_scaling(
            min_val = min_val,
            max_val = max_val
        )

        ## === Calculating Normalization ===
        norm_df: pd.DataFrame = self.calculate_normalization(
            mean = mean,
            std = std
        )

        ## === Merging all the DataFrames ===
        merged_df = pd.concat(
            [log_df, scaling_df, norm_df],
            axis = 1
        )

        return merged_df