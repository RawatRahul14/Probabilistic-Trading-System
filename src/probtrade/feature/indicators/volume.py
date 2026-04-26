"""
Liquidity (OBV, VWAP, Money Flow Index)
"""
# === Python Modules ===
import numpy as np
import pandas as pd

# === Class for Liquidity Indicators ===
class Liquidity:
    def __init__(
            self,
            data: pd.DataFrame,
            close_col: str = "close",
            high_col: str = "high",
            low_col: str = "low",
            volume_col: str = "volume"
    ):
        """
        Calculates volume and liquidity-based indicators for financial data.
        """
        ## === Price and Volume Data ===
        self.close = data[close_col]
        self.high = data[high_col]
        self.low = data[low_col]
        self.volume = data[volume_col]

        ## === Combined Data ===
        self.data_matrix: pd.DataFrame = pd.concat(
            [x for x in [self.close, self.high, self.low, self.volume] if x is not None],
            axis = 1
        )

    ## === On-Balance Volume (OBV) ===
    def calculate_obv(
            self
    ) -> pd.DataFrame:
        """
        Calculates On-Balance Volume (OBV).
        Adds volume on up days, subtracts volume on down days.
        """
        ## === Calculate Price Direction (1 for up, -1 for down, 0 for flat) ===
        price_change = np.sign(self.close.diff())
        
        ## === Calculate OBV ===
        # Fill the first NaN with 0 so the cumulative sum starts correctly
        obv = (price_change.fillna(0) * self.volume).cumsum()

        return obv.rename("obv").to_frame()

    ## === Volume Weighted Average Price (VWAP) ===
    def calculate_vwap(
            self,
            period: int | None = 14
    ) -> pd.DataFrame:
        """
        Calculates Volume Weighted Average Price (VWAP).
        
        Args:
            - period (int | None): Rolling window for Moving VWAP. If None, calculates cumulative VWAP.
        """
        ## === Calculate Typical Price ===
        typical_price = (self.high + self.low + self.close) / 3
        
        ## === Calculate Price * Volume ===
        pv = typical_price * self.volume

        ## === Calculate VWAP Logic ===
        if period is not None:
            # Moving VWAP (Better for sliding window ML models)
            vwap = pv.rolling(window = period).sum() / self.volume.rolling(window = period).sum()
        else:
            # Traditional Cumulative VWAP
            vwap = pv.cumsum() / self.volume.cumsum()

        return vwap.rename("vwap").to_frame()

    ## === Money Flow Index (MFI) ===
    def calculate_mfi(
            self,
            period: int = 14
    ) -> pd.DataFrame:
        """
        Calculates the Money Flow Index (MFI), a volume-weighted RSI.
        
        Args:
            - period (int): The lookback period for calculating MFI
        """
        ## === Calculate Typical Price and Raw Money Flow ===
        typical_price = (self.high + self.low + self.close) / 3
        raw_money_flow = typical_price * self.volume

        ## === Determine Positive and Negative Money Flows ===
        delta = typical_price.diff()
        
        positive_flow = raw_money_flow.where(delta > 0, 0.0)
        negative_flow = raw_money_flow.where(delta < 0, 0.0)

        ## === Calculate Rolling Sums ===
        pos_flow_sum = positive_flow.rolling(window = period).sum()
        neg_flow_sum = negative_flow.rolling(window = period).sum()

        ## === Calculate Money Flow Ratio and MFI ===
        money_flow_ratio = pos_flow_sum / neg_flow_sum
        mfi = 100 - (100 / (1 + money_flow_ratio))

        ## === Handle Division by Zero (MFI is 100 when neg_flow is 0) ===
        mfi = mfi.where(neg_flow_sum != 0, 100.0)

        return mfi.rename("mfi").to_frame()

    ## === Calculate All Indicators ===
    def calculate_all(
            self,
            vwap_period: int | None = 14,
            mfi_period: int = 14
    ) -> pd.DataFrame:
        """
        Calculates all liquidity indicators in one go.
        """
        ## === Calculating OBV ===
        obv_df: pd.DataFrame = self.calculate_obv()

        ## === Calculating VWAP ===
        vwap_df: pd.DataFrame = self.calculate_vwap(
            period = vwap_period
        )

        ## === Calculating MFI ===
        mfi_df: pd.DataFrame = self.calculate_mfi(
            period = mfi_period
        )

        ## === Merging all the DataFrames ===
        merged_df = pd.concat(
            [obv_df, vwap_df, mfi_df],
            axis = 1
        )

        return merged_df