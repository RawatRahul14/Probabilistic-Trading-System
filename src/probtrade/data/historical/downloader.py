# === Python Modules ===
import asyncio
import random
from typing import Iterable, Dict
import pandas as pd

# === Downloader class for the Historical Data ===
class AsyncDownloader():
    def __init__(
            self,
            max_concurrency: int = 5,
            max_retries: int = 3,
            base_delay: float = 1.0
    ):
        """
        Initializes async downloader state.
        """
        ## === Initialising sets to keep track of failed and done tickers ===
        self.done = set()
        self.failed = set()

        ## === Variable to hold data ===
        data: Dict[str, pd.DataFrame] = {}
        self.data = data

        ## === Retries and delays ===
        self.max_retries = max_retries
        self.base_delay = base_delay

        ## === Semaphore to control concurrency ===
        self.sem = asyncio.Semaphore(
            value = max_concurrency
        )

    async def _run_one(
            self,
            ticker: str,
            worker,
            *args,
            **kwargs
    ):
        """
        Runs a single async worker with retry

        returns:
            - ticker (str): Name of the ticker
            - result (pd.DataFrame): Historical Data of that ticker
            - err (str | None): e
        """
        ## === Placeholder for number of attempts ===
        attempt = 0

        while True:
            try:

                ## === Running a single async worker ===
                async with self.sem:
                    result = await worker(
                        ticker,
                        *args,
                        **kwargs
                    )

                ## === If the output is empty ===
                if result is None or result.empty:
                    raise RuntimeError(f"Empty data returned for ticker: {ticker}")

                return ticker, result, None
            
            except Exception as e:

                ## === Incrementing the number of attempts by 1 ===
                attempt += 1

                ## === If Number of attempts is equal to number of max_retries ===
                if attempt >= self.max_retries:
                    return ticker, None, e
                
                ## === Exponential backoff with jitter ===
                delay = self.base_delay * (2 ** (attempt - 1))
                delay += random.uniform(0, 0.3)

                await asyncio.sleep(delay)

    async def run(
            self,
            tickers: Iterable[str],
            worker,
            *args,
            **kwargs
    ):
        """
        Runs async downloads for all tickers.
        """
        tasks = [
            self._run_one(
                ticker = ticker,
                worker = worker,
                *args,
                **kwargs
            )
            for ticker in tickers
        ]

        results = await asyncio.gather(*tasks)

        ## === Looping through all the results ===
        for ticker, df, error in results:

            ## === If there's no error add the ticker in the self.done ===
            if error is None:
                self.done.add(ticker)
                self.data[ticker] = df

            ## === If there's error add the ticker in the self.failed ===
            else:
                self.failed.add(ticker)

        return self.data