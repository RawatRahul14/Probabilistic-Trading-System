"""
Range/Risk (Bollinger Bands, ATR, Standard Deviation)
"""
# === Python Modules ===
import numpy as np
import pandas as pd

# === Class for Range/Risk Indicators ===
class RangeIndicators:
    def __init__(
            self,
            data: pd.DataFrame,
            close_col: str = "close",
            high_col: str = "high",
            low_col: str = "low"
    ):
        """
        Calculates volatility, range, and risk indicators for financial data.
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

    ## === Bollinger Bands ===
    def calculate_bollinger_bands(
            self,
            period: int = 20,
            std_dev: float = 2.0
    ) -> pd.DataFrame:
        """
        Calculates Bollinger Bands (Upper, Middle/SMA, and Lower bands).
        
        Args:
            - period (int): The lookback period for the Simple Moving Average
            - std_dev (float): The multiplier for the standard deviation
        """
        ## === Calculate Middle Band (Simple Moving Average) ===
        middle_band = self.close.rolling(window = period).mean()

        ## === Calculate Rolling Standard Deviation ===
        rolling_std = self.close.rolling(window = period).std()

        ## === Calculate Upper and Lower Bands ===
        upper_band = middle_band + (rolling_std * std_dev)
        lower_band = middle_band - (rolling_std * std_dev)

        ## === Combine into DataFrame ===
        bb_df = pd.concat([upper_band, middle_band, lower_band], axis = 1)
        bb_df.columns = ["bb_upper", "bb_middle", "bb_lower"]

        return bb_df

    ## === Average True Range (ATR) ===
    def calculate_atr(
            self,
            period: int = 14
    ) -> pd.DataFrame:
        """
        Calculates the Average True Range (ATR).
        
        Args:
            - period (int): The smoothing period for the True Range
        """
        ## === Calculate True Range Components ===
        high_low = self.high - self.low
        high_close_prev = (self.high - self.close.shift(1)).abs()
        low_close_prev = (self.low - self.close.shift(1)).abs()

        ## === Determine True Range (Maximum of the three components) ===
        tr = pd.concat([high_low, high_close_prev, low_close_prev], axis = 1).max(axis = 1)

        ## === Calculate ATR using Wilder's Smoothing ===
        # Wilder's smoothing is equivalent to an EMA with alpha = 1 / period
        atr = tr.ewm(alpha = 1 / period, adjust = False).mean()

        return atr.rename("atr").to_frame()

    ## === Standard Deviation ===
    def calculate_standard_deviation(
            self,
            period: int = 20
    ) -> pd.DataFrame:
        """
        Calculates the rolling Standard Deviation.
        
        Args:
            - period (int): The lookback window for the standard deviation
        """
        ## === Calculate Rolling Standard Deviation ===
        std_df = self.close.rolling(window = period).std()

        return std_df.rename("std_dev").to_frame()

    ## === Calculate All Indicators ===
    def calculate_all(
            self,
            bb_period: int = 20,
            bb_std: float = 2.0,
            atr_period: int = 14,
            std_period: int = 20
    ) -> pd.DataFrame:
        """
        Calculates all range and risk indicators in one go.
        """
        ## === Calculating Bollinger Bands ===
        bb_df: pd.DataFrame = self.calculate_bollinger_bands(
            period = bb_period,
            std_dev = bb_std
        )

        ## === Calculating ATR ===
        atr_df: pd.DataFrame = self.calculate_atr(
            period = atr_period
        )

        ## === Calculating Standard Deviation ===
        std_df: pd.DataFrame = self.calculate_standard_deviation(
            period = std_period
        )

        ## === Merging all the DataFrames ===
        merged_df = pd.concat(
            [bb_df, atr_df, std_df],
            axis = 1
        )

        return merged_df