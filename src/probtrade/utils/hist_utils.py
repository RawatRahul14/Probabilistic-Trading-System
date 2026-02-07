# === Removes special characters from the ticker's name ===
def normalise_ticker(
        ticker: str
) -> str:
    """
    Removes special Characters from tickers
    """
    ## === Handling Index ===
    if ticker == "^NSEI":
        return "NIFTY50"

    ticker =  ticker.replace("-", "")

    return ticker