"""
Speed/Strength (RSI, MACD, Stochastic)
"""
# === Python Modules ===
import numpy as np
import pandas as pd

# === Class for Speed/Strength Indicators ===
class MomentumIndicators:
    def __init__(
            self,
            data: pd.DataFrame,
            close_col: str = "close",
            high_col: str = "high",
            low_col: str = "low"
    ):
        """
        Calculates momentum, speed, and strength indicators for financial data.
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

    ## === Relative Strength Index (RSI) ===
    def calculate_rsi(
            self,
            period: int = 14
    ) -> pd.DataFrame:
        """
        Calculates the Relative Strength Index (RSI).
        
        Args:
            - period (int): The lookback period for calculating RSI
        """
        ## === Calculate Price Changes ===
        delta = self.close.diff()

        ## === Separate Gains and Losses ===
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        ## === Calculate Exponential Moving Averages (Wilder's Smoothing) ===
        avg_gain = gain.ewm(com = period - 1, min_periods = period).mean()
        avg_loss = loss.ewm(com = period - 1, min_periods = period).mean()

        ## === Calculate RS and RSI ===
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        ## === Handle Division by Zero (RSI is 100 when avg_loss is 0) ===
        rsi = rsi.where(avg_loss != 0, 100.0)

        return rsi.rename("rsi").to_frame()

    ## === Moving Average Convergence Divergence (MACD) ===
    def calculate_macd(
            self,
            fast_period: int = 12,
            slow_period: int = 26,
            signal_period: int = 9
    ) -> pd.DataFrame:
        """
        Calculates the MACD Line, Signal Line, and MACD Histogram.

        Args:
            - fast_period (int): Lookback period for the fast EMA
            - slow_period (int): Lookback period for the slow EMA
            - signal_period (int): Lookback period for the signal line EMA
        """
        ## === Calculate Fast and Slow EMAs ===
        ema_fast = self.close.ewm(span = fast_period, adjust = False).mean()
        ema_slow = self.close.ewm(span = slow_period, adjust = False).mean()

        ## === MACD and Signal Lines ===
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span = signal_period, adjust = False).mean()

        ## === MACD Histogram ===
        macd_histogram = macd_line - signal_line

        ## === Combine into DataFrame ===
        macd_df = pd.concat([macd_line, signal_line, macd_histogram], axis = 1)
        macd_df.columns = ["macd_line", "macd_signal", "macd_histogram"]

        return macd_df

    ## === Stochastic Oscillator ===
    def calculate_stochastic(
            self,
            k_period: int = 14,
            d_period: int = 3
    ) -> pd.DataFrame:
        """
        Calculates the Stochastic Oscillator (%K and %D lines).

        Args:
            - k_period (int): Lookback period for finding the highest high and lowest low
            - d_period (int): Period for the moving average of %K (creates %D)
        """
        ## === Find Highest High and Lowest Low over the Window ===
        lowest_low = self.low.rolling(window = k_period).min()
        highest_high = self.high.rolling(window = k_period).max()

        ## === Calculate %K and %D ===
        percent_k = 100 * ((self.close - lowest_low) / (highest_high - lowest_low))
        percent_d = percent_k.rolling(window = d_period).mean()

        ## === Combine into DataFrame ===
        stoch_df = pd.concat([percent_k, percent_d], axis = 1)
        stoch_df.columns = ["stoch_k", "stoch_d"]

        return stoch_df

    ## === Calculate All Indicators ===
    def calculate_all(
            self,
            rsi_period: int = 14,
            macd_fast: int = 12,
            macd_slow: int = 26,
            macd_signal: int = 9,
            stoch_k: int = 14,
            stoch_d: int = 3
    ) -> pd.DataFrame:
        """
        Calculates all speed and strength indicators in one go.
        """
        ## === Calculating RSI ===
        rsi_df: pd.DataFrame = self.calculate_rsi(
            period = rsi_period
        )

        ## === Calculating MACD ===
        macd_df: pd.DataFrame = self.calculate_macd(
            fast_period = macd_fast,
            slow_period = macd_slow,
            signal_period = macd_signal
        )

        ## === Calculating Stochastic ===
        stoch_df: pd.DataFrame = self.calculate_stochastic(
            k_period = stoch_k,
            d_period = stoch_d
        )

        ## === Merging all the DataFrames ===
        merged_df = pd.concat(
            [rsi_df, macd_df, stoch_df],
            axis = 1
        )

        return merged_df