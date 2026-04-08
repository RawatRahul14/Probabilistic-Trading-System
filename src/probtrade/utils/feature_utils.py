# === Python Modules ===
from pathlib import Path
import json

# === Data to save ===
data = {
    "time_frame_5m": {
        "last_candle": {
            "last_close": None,
            "last_high": None,
            "last_low": None
        },
        "indicators": {
            "old_window_start_price": {
                "close": None,
                "high": None,
                "low": None
            },
            "window_5": {
                "sma": {
                    "previous_sma": None
                },
                "ema": {
                    "previous_ema": None
                },
                "adx": {
                    "previous_adx": None,
                    "previous_smoothed_tr": None,
                    "previous_smoothed_plus_dm": None,
                    "previous_smoothed_minus_dm": None
                }
            }
        }
    },
    "time_frame_15m": {
        "last_candle": {
            "last_close": None,
            "last_high": None,
            "last_low": None
        },
        "indicators": {
            "old_window_start_price": {
                "close": None,
                "high": None,
                "low": None
            },
            "window_5": {
                "sma": {
                    "previous_sma": None
                },
                "ema": {
                    "previous_ema": None
                },
                "adx": {
                    "previous_adx": None,
                    "previous_smoothed_tr": None,
                    "previous_smoothed_plus_dm": None,
                    "previous_smoothed_minus_dm": None
                }
            }
        }
    },
    "time_frame_30m": {
        "last_candle": {
            "last_close": None,
            "last_high": None,
            "last_low": None
        },
        "indicators": {
            "old_window_start_price": {
                "close": None,
                "high": None,
                "low": None
            },
            "window_5": {
                "sma": {
                    "previous_sma": None
                },
                "ema": {
                    "previous_ema": None
                },
                "adx": {
                    "previous_adx": None,
                    "previous_smoothed_tr": None,
                    "previous_smoothed_plus_dm": None,
                    "previous_smoothed_minus_dm": None
                }
            }
        }
    },
    "time_frame_1h": {
        "last_candle": {
            "last_close": None,
            "last_high": None,
            "last_low": None
        },
        "indicators": {
            "old_window_start_price": {
                "close": None,
                "high": None,
                "low": None
            },
            "window_5": {
                "sma": {
                    "previous_sma": None
                },
                "ema": {
                    "previous_ema": None
                },
                "adx": {
                    "previous_adx": None,
                    "previous_smoothed_tr": None,
                    "previous_smoothed_plus_dm": None,
                    "previous_smoothed_minus_dm": None
                }
            }
        }
    },
    "time_frame_1d": {
        "last_candle": {
            "last_close": None,
            "last_high": None,
            "last_low": None
        },
        "indicators": {
            "old_window_start_price": {
                "close": None,
                "high": None,
                "low": None
            },
            "window_5": {
                "sma": {
                    "previous_sma": None
                },
                "ema": {
                    "previous_ema": None
                },
                "adx": {
                    "previous_adx": None,
                    "previous_smoothed_tr": None,
                    "previous_smoothed_plus_dm": None,
                    "previous_smoothed_minus_dm": None
                }
            }
        }
    }
}

# === Function to keep record of the last updates of indicators ===
class RecordIndicators:
    def __init__(
            self,
            folder_name: Path = Path("config"),
            file_name: str = "metadata.json"
    ):
        ## === Defining the file path ===
        self.file_path = folder_name / file_name

        ## === Initiating the file only if it doesn't exists ===
        if not self.file_path.exists():
            self._init_file()

    def _init_file(self):
        """
        Creating the metadata file if not exists.
        """
        with open(f"{str(self.file_path)}", "w") as f:
            json.dump(
                data,
                f,
                indent = 4
            )