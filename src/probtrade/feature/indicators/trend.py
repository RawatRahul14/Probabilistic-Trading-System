"""
Directional (SMA, EMA, ADX, SuperTrend)
"""
# === Python Modules ===
import numpy as np
import pandas as pd
from typing import Literal, List

# === Class for Trend Based Indicators ===
class TrendIndicators:
    def __init__(
            self,
            data: pd.DataFrame,
            last_close: float | None = None,
            last_high: float | None = None,
            last_low: float | None = None,
            close_col: str = "close",
            high_col: str = "high",
            low_col: str = "low"
    ):
        """
        Calculates multiple trend based indicators.
        """
        ## === Close Prices ===
        self.close = data[close_col]

        ## === High and Low Prices (Optional for ADX, SuperTrend) ===
        self.high = data[high_col] if high_col else None
        self.low  = data[low_col] if low_col  else None

        ## === Combined Prices Dataframe ===
        self.prices = pd.concat(
            [x for x in [self.close, self.high, self.low] if x is not None],
            axis = 1
        )

        ## === Last Prices (For Incremental Transitions) ===
        self.last_close = last_close
        self.last_high = last_high
        self.last_low = last_low

    ## === SMA: Simple Moving Average ===
    def calculate_sma(
            self,
            sma_window: int | None = None,
            previous_sma: float | None = None,
    ) -> pd.DataFrame:
        """
        Calculates the Simple Moving Average of the specified column.

        Args:
            - sma_window (int): Window Size
            - previous_sma (float): The previous SMA value from JSON
        """
        ## === If the run is for first time ===
        if previous_sma is None:
            sma_values = self.close.rolling(
                            window = sma_window
                        ).mean()

            return sma_values.rename(f"sma_{sma_window}").to_frame()

        ## === When the previous SMA value is given ===
        else:

            ## === Required Variables ===
            sma_values = np.full(
                len(self.close),
                np.nan
            )

            ## === Running SMA ===
            running_sma = float(previous_sma)

            ## === Looping through all new prices ===
            for i in range(len(self.close)):

                ## === Fetching the current price ===
                current_price = float(self.close.iloc[i])

                ## === Fetching the dropped price (Requires History) ===
                # If we have N prior prices in this chunk, drop the Nth price.
                # Otherwise, fallback to last_close (an approximation for tight chunks).
                if i >= sma_window:
                    dropped_price = float(self.close.iloc[i - sma_window])
                else:
                    dropped_price = float(self.last_close) if self.last_close else current_price

                ## === Calculating the new SMA ===
                new_sma = running_sma - (dropped_price / sma_window) + (current_price / sma_window)
                sma_values[i] = new_sma

                ## === Sliding the window forward ===
                running_sma = new_sma

            return pd.DataFrame(
                data = sma_values,
                index = self.close.index,
                columns = [f"sma_{sma_window}"]
            )

    ## === EMA: Exponential Moving Average ===
    def calculate_ema(
            self,
            ema_window: int | None = None,
            previous_ema: float | None = None,
    ) -> pd.DataFrame:
        """
        Calculates the Exponential Moving Average of the specified column.

        Args:
            - ema_window (int): Window Size
            - previous_ema (float): The previous EMA value from JSON
        """
        ## === Smoothing Factor ===
        multiplier = 2 / (ema_window + 1)

        ## === If the run is for first time ===
        if previous_ema is None:
            ema_values = self.close.ewm(
                            span = ema_window,
                            adjust = False
                        ).mean()

            return ema_values.rename(f"ema_{ema_window}").to_frame()

        ## === When the previous EMA value is given ===
        else:

            ## === Required Variables ===
            ema_values = np.full(
                len(self.close),
                np.nan
            )

            ## === Running EMA ===
            running_ema = float(previous_ema)

            ## === Looping through all new prices ===
            for i in range(len(self.close)):

                ## === Fetching the current price ===
                current_price = float(self.close.iloc[i])

                ## === Calculating the new EMA ===
                new_ema = (current_price * multiplier) + (running_ema * (1 - multiplier))
                ema_values[i] = round(new_ema, 2)

                ## === Sliding the window forward ===
                running_ema = new_ema

            return pd.DataFrame(
                data = ema_values,
                index = self.close.index,
                columns = [f"ema_{ema_window}"]
            )

    ## === ADX: Average Directional Index ===
    def calculate_adx(
            self,
            adx_window: int | None = None,
            previous_adx: float | None = None,
            previous_smoothed_tr: float | None = None,
            previous_smoothed_plus_dm: float | None = None,
            previous_smoothed_minus_dm: float | None = None,
    ) -> pd.DataFrame:
        """
        Calculates the Average Directional Index of the specified column.

        Args:
            - adx_window (int): Window Size
            - previous_adx (float): The previous ADX value from JSON
            - previous_smoothed_tr (float): The previous smoothed TR value from JSON
            - previous_smoothed_plus_dm (float): The previous smoothed +DM value from JSON
            - previous_smoothed_minus_dm (float): The previous smoothed -DM value from JSON
        """
        ## === Smoothing Factor (Wilder's RMA) ===
        alpha = 1 / adx_window

        ## === If the run is for first time ===
        if previous_adx is None:

            ## === High, Low, Close Prices ===
            high = self.prices["high"]
            low = self.prices["low"]
            close = self.prices["close"]

            ## === True Range ===
            tr = pd.concat([
                high - low,
                (high - close.shift(1)).abs(),
                (low  - close.shift(1)).abs()
            ], axis = 1).max(axis = 1)

            ## === Directional Movement ===
            plus_dm = high.diff()
            minus_dm = -low.diff()

            plus_dm = plus_dm.where((plus_dm > minus_dm)  & (plus_dm > 0),  0)
            minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)

            ## === Smoothed TR, +DM, -DM (Wilder's Smoothing) ===
            smoothed_tr = tr.ewm(alpha=alpha, adjust=False).mean()
            smoothed_plus_dm = plus_dm.ewm(alpha=alpha, adjust=False).mean()
            smoothed_minus_dm = minus_dm.ewm(alpha=alpha, adjust=False).mean()

            ## === +DI and -DI ===
            plus_di = 100 * (smoothed_plus_dm  / smoothed_tr)
            minus_di = 100 * (smoothed_minus_dm / smoothed_tr)

            ## === DX and ADX ===
            dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
            adx = dx.rolling(window = adx_window).mean()

            return pd.DataFrame({
                f"adx_{adx_window}"               : adx.values,
                f"plus_di_{adx_window}"           : plus_di.values,
                f"minus_di_{adx_window}"          : minus_di.values,
                f"smoothed_tr_{adx_window}"       : smoothed_tr.values,
                f"smoothed_plus_dm_{adx_window}"  : smoothed_plus_dm.values,
                f"smoothed_minus_dm_{adx_window}" : smoothed_minus_dm.values,
            }, index = self.prices.index)

        ## === When the previous ADX value is given ===
        else:

            ## === Required Variables ===
            adx_values = np.full(len(self.prices), np.nan)
            plus_di_values = np.full(len(self.prices), np.nan)
            minus_di_values = np.full(len(self.prices), np.nan)
            smoothed_tr_values = np.full(len(self.prices), np.nan)
            smoothed_plus_dm_values = np.full(len(self.prices), np.nan)
            smoothed_minus_dm_values = np.full(len(self.prices), np.nan)

            ## === Running Values ===
            running_adx = float(previous_adx)
            running_smoothed_tr = float(previous_smoothed_tr)
            running_smoothed_plus_dm = float(previous_smoothed_plus_dm)
            running_smoothed_minus_dm = float(previous_smoothed_minus_dm)

            ## === Looping through all new prices ===
            for i in range(len(self.prices)):

                ## === Fetching Current and Previous Prices ===
                current_high = float(self.prices["high"].iloc[i])
                current_low = float(self.prices["low"].iloc[i])
                current_close = float(self.prices["close"].iloc[i])

                prev_high = float(self.prices["high"].iloc[i - 1])  if i > 0 else float(self.last_high)
                prev_low = float(self.prices["low"].iloc[i - 1])   if i > 0 else float(self.last_low)
                prev_close = float(self.prices["close"].iloc[i - 1]) if i > 0 else float(self.last_close)

                ## === True Range ===
                tr = max(
                    current_high - current_low,
                    abs(current_high - prev_close),
                    abs(current_low  - prev_close)
                )

                ## === Directional Movement ===
                plus_dm = current_high - prev_high
                minus_dm = prev_low - current_low

                plus_dm = plus_dm  if (plus_dm  > minus_dm) and (plus_dm  > 0) else 0
                minus_dm = minus_dm if (minus_dm > plus_dm)  and (minus_dm > 0) else 0

                ## === Smoothed TR, +DM, -DM ===
                new_smoothed_tr = (running_smoothed_tr * (1 - alpha)) + (tr * alpha)
                new_smoothed_plus_dm = (running_smoothed_plus_dm * (1 - alpha)) + (plus_dm * alpha)
                new_smoothed_minus_dm = (running_smoothed_minus_dm * (1 - alpha)) + (minus_dm * alpha)

                ## === +DI and -DI ===
                new_plus_di = 100 * (new_smoothed_plus_dm / new_smoothed_tr) if new_smoothed_tr != 0 else 0
                new_minus_di = 100 * (new_smoothed_minus_dm / new_smoothed_tr) if new_smoothed_tr != 0 else 0

                ## === DX and ADX ===
                dx = 100 * abs(new_plus_di - new_minus_di) / (new_plus_di + new_minus_di) if (new_plus_di + new_minus_di) != 0 else 0
                new_adx = (running_adx * (1 - alpha)) + (dx * alpha)

                ## === Storing Values ===
                adx_values[i] = new_adx
                plus_di_values[i] = new_plus_di
                minus_di_values[i] = new_minus_di
                smoothed_tr_values[i] = new_smoothed_tr
                smoothed_plus_dm_values[i] = new_smoothed_plus_dm
                smoothed_minus_dm_values[i] = new_smoothed_minus_dm

                ## === Sliding the Window Forward ===
                running_adx = new_adx
                running_smoothed_tr = new_smoothed_tr
                running_smoothed_plus_dm = new_smoothed_plus_dm
                running_smoothed_minus_dm = new_smoothed_minus_dm

            return pd.DataFrame({
                f"adx_{adx_window}"               : adx_values,
                f"plus_di_{adx_window}"           : plus_di_values,
                f"minus_di_{adx_window}"          : minus_di_values,
                f"smoothed_tr_{adx_window}"       : smoothed_tr_values,
                f"smoothed_plus_dm_{adx_window}"  : smoothed_plus_dm_values,
                f"smoothed_minus_dm_{adx_window}" : smoothed_minus_dm_values,
            }, index = self.prices.index)
        
    def calculate_all(
            self,
            sma_window: int | None = None,
            previous_sma: float | None = None,
            ema_window: int | None = None,
            previous_ema: float | None = None,
            adx_window: int | None = None,
            previous_adx: float | None = None,
            previous_smoothed_tr: float | None = None,
            previous_smoothed_plus_dm: float | None = None,
            previous_smoothed_minus_dm: float | None = None,
    ) -> pd.DataFrame:
        """
        Calculates all the trend based indicators in one go.
        Use Dropna after calling this function to keep all the non-Nan values.
        """
        ## === Calculating SMA ===
        sma_df: pd.DataFrame = self.calculate_sma(
            sma_window = sma_window,
            previous_sma = previous_sma
        )

        ## === Calculating EMA ===
        ema_df: pd.DataFrame = self.calculate_ema(
            ema_window = ema_window,
            previous_ema = previous_ema
        )

        ## === Calculating ADX ===
        adx_df: pd.DataFrame = self.calculate_adx(
            adx_window = adx_window,
            previous_adx = previous_adx,
            previous_smoothed_tr = previous_smoothed_tr,
            previous_smoothed_plus_dm = previous_smoothed_plus_dm,
            previous_smoothed_minus_dm = previous_smoothed_minus_dm
        )

        ## === Merging all the DataFrames ===
        merged_df = pd.concat(
            [sma_df, ema_df, adx_df],
            axis = 1
        )

        return merged_df