# === Python Modules ===
from datetime import date
import pandas as pd

# === Logger ===
from probtrade import get_logger

# === Indicators ===
from probtrade.feature.indicators import (
    MomentumIndicators,
    Transformation,
    TrendIndicators,
    RangeIndicators,
    Liquidity
)

class IndicatorPipeline:
    def __init__(
            self
    ):
        ## === Initiating the logger ===
        self.logger = get_logger(
            name = "INDICATOR",
            log_file = "indicator.log"
        )

    def main(
            self,
            data: pd.DataFrame
    ):
        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {date.today()} <<<<<<<<")
        self.logger.info(">>>>>>> Starting Indicator Pipeline <<<<<<<")

        try:
            ## === Initiating all the indicators ===
            momentum = MomentumIndicators(data = data)
            transformation = Transformation(data = data)
            range = RangeIndicators(data = data)

            ## === Only applying the  ===
            if type == "stocks":
                liquidity = Liquidity(data = data)