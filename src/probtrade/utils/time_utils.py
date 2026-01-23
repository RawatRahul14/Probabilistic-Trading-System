# === Python Modules ===
from typing import Tuple, Literal
from datetime import datetime, time
import pytz

# === Function to get the Indian current time ===
class GetTime:
    def __init__(
            self,
            timezone: str | None = None
    ):
        self.zone = timezone or "Asia/Kolkata"
        self.timezone = pytz.timezone(self.zone)

    def current_time(
            self
    ) -> Tuple[str, datetime.time]:
        """
        Gets the current time based on the timezone

        returns:
            - current_time_str (str): Current time for the timezone
            - current_time (datetime.time()): Time to compare
        """
        ## === getting the current time ===
        current_time = datetime.now(self.timezone).time()

        return current_time.strftime("%H:%M"), current_time

    def market_aware(
            self
    ) -> Literal[
        "pre_market",
        "open_market",
        "close_market",
        "close"
    ]:
        """
        Returns the current status of the market.
        """
        ## === Extracting the current_time ===
        _, current_time = self.current_time()

        ## === Getting the market status ===
        if time(9, 0) <= current_time <= time(9, 14):
            return "pre_market"
        
        elif time(9, 15) <= current_time <= time(15, 30):
            return "open_market"
        
        elif time(15, 31) <= current_time <= time(15, 45):
            return "close_market"

        else:
            return "close"