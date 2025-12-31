# === Python Module ===
from pathlib import Path
from datetime import date, timedelta

# === Utils ===
from probtrade.utils import load_yaml, save_yaml

# === Gets the date for the last update and also updates the date ===
class GetDate:
    def __init__(
            self,
            file_name: str = "last_update.yaml",
            fallback_days: int = 1000
    ):
        self.file_name = file_name
        self.fallback_days = fallback_days
        self.today_date = date.today()

    def read_date(self):
        """
        Extracts the last update date
        """
        ## === Loading the yaml file ===
        data = load_yaml(
            file_path = "config",
            file_name = self.file_name
        )

        raw_date = data.get("date", ["None"])[0]

        ## === If date is None ===
        if raw_date == "None":
            result = self._adjust_date()

        else:
            result = data["date"][0]

        ## === Updates the date in the yaml to last updated date ===
        self._update_date(new_date = self.today_date)

        return result

    def _adjust_date(self):
        """
        If the date is not provided, it will adjust it to the last N days.
        """
        ## === Today's date ===
        prev_date = self.today_date - timedelta(self.fallback_days)
        return prev_date.isoformat()

    def _update_date(self, new_date):
        """
        Updates the date in the yaml file
        """
        save_yaml(
            file_path = "config",
            file_name = self.file_name,
            data = {"date": [new_date.isoformat()]}
        )