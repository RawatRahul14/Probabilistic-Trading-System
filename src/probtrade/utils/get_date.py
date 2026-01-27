# === Python Module ===
from datetime import date, timedelta

# === Utils ===
from probtrade.utils import load_yaml, save_yaml


# === Handles reading & updating last historical data update date ===
class UpdateDateManager:
    def __init__(
            self,
            file_name: str = "last_update.yaml",
            fallback_days: int = 1000
    ):
        ## === Config file name ===
        self.file_name = file_name

        ## === Fallback window if no date exists ===
        self.fallback_days = fallback_days

        ## === Today's date ===
        self.today_date = date.today()

    def read_start_date(self):
        """
        Returns the start date for historical data fetching.
        """
        ## === Load the yaml config ===
        data = load_yaml(
            file_path = "config",
            file_name = self.file_name
        )

        ## === Extract date if exists ===
        raw_date = data.get("date")

        ## === If no date is present, fallback ===
        if "NA" in raw_date:
            return self._fallback_date()

        ## === Return stored last update date ===
        return raw_date

    def _fallback_date(self):
        """
        Returns fallback date (today - N days).
        Used for first-time bootstrapping.
        """
        ## === Calculate previous date ===
        prev_date = self.today_date - timedelta(self.fallback_days)

        ## === Return in ISO format ===
        return prev_date.isoformat()

    def commit_update(self):
        """
        Updates the yaml file with today's date.
        IMPORTANT:
        - Call this ONLY after ALL downloads succeed
        """
        save_yaml(
            file_path = "config",
            file_name = self.file_name,
            data = {
                "date": date.today().isoformat()
            }
        )