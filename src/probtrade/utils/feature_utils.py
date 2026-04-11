# === Python Modules ===
import json
from pathlib import Path
from typing import Dict, Any, Literal

# === Data to save ===
data = {
    "first_update_done": False,
    "time_frame_5m": {
        "window_5": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        },
        "window_10": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        "window_5": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        },
        "window_10": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        "window_5": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        },
        "window_10": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        "window_5": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        },
        "window_10": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        "window_5": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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
        },
        "window_10": {
            "old_window": {
                "close": [],
                "high": [],
                "low": []
            },
            "indicators": {
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

        ## === Calling the MetaData file ===
        self._call_metadata()

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

    def _update_file(self):
        """
        Updates the metadata file if not exists.
        """
        with open(f"{str(self.file_path)}", "w") as f:
            json.dump(
                self.data,
                f,
                indent = 4
            )

    def _call_metadata(
            self
    ):
        """
        Calls and reads the metadata file made for storing the last values of each indicator used.
        """
        with open(f"{str(self.file_path)}", "r") as f:
            self.data = json.load(
                f
            )

    def _update_candle(
            self,
            new_candles: Dict[str, Any],
            window_size: Literal["5", "10", "20"],
            timeframe: Literal["5m", "15m", "30m", "1h", "1d"]
    ):
        """
        Updates the Candles in the metadata file based on the window_size

        Args:
            - new_candles (Dict[str, Any]): Dictionary containing `open`, `high` and `close` candle data.
            - window_size (int): Size of the window.
            - timeframe (Literal["5m", "15m", "30m", "1h", "1d"]): Timeframe
        """
        ## === Updating the Metadata ===
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["old_window"]["open"] = new_candles["open"]
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["old_window"]["high"] = new_candles["high"]
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["old_window"]["close"] = new_candles["close"]

    def _update_indicators(
            self,
            last_indicators: Dict[str, Dict[str, float]],
            window_size: Literal["5", "10", "20"],
            timeframe: Literal["5m", "15m", "30m", "1h", "1d"]
    ):
        """
        Updates the Indicator values in the metadata file based on the window_size

        Args:
            - last_indicators (Dict[str, float]): Dictionary containing `keys` as indicator's name and `values`.
            - window_size (int): Size of the window.
            - timeframe (Literal["5m", "15m", "30m", "1h", "1d"]): Timeframe
        """
        ## === Updating the Metadata ===
        ### ==== SMA ====
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["indicators"]["sma"]["previous_sma"] = last_indicators["sma"]["previous_sma"]

        ### ==== EMA ====
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["indicators"]["ema"]["previous_ema"] = last_indicators["ema"]["previous_ema"]

        ### ==== ADX ====
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["indicators"]["adx"]["previous_adx"] = last_indicators["adx"]["previous_adx"]
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["indicators"]["adx"]["previous_smoothed_tr"] = last_indicators["adx"]["previous_smoothed_tr"]
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["indicators"]["adx"]["previous_smoothed_plus_dm"] = last_indicators["adx"]["previous_smoothed_plus_dm"]
        self.data[f"time_frame_{timeframe}"][f"window_{window_size}"]["indicators"]["adx"]["previous_smoothed_minus_dm"] = last_indicators["adx"]["previous_smoothed_minus_dm"]

    def update(
            self,
            new_candles: Dict[str, Any],
            last_indicators: Dict[str, Dict[str, float]],
            window_size: Literal["5", "10", "20"],
            timeframe: Literal["5m", "15m", "30m", "1h", "1d"]
    ):
        """
        Updates both Last Candles and Indicators.
        """
        try:
            ## === Candles Update ===
            self._update_candle(
                new_candles = new_candles,
                window_size = window_size,
                timeframe = timeframe
            )

            ## === Indicators update ===
            self._update_indicators(
                last_indicators = last_indicators,
                window_size = window_size,
                timeframe = timeframe
            )

            ## === Updating the Metadata file ===
            self._update_file()

            return self.data

        except Exception as e:
            raise ValueError(e)