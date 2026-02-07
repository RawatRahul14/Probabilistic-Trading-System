# === Python Modules ===
import asyncio
import random
from typing import Iterable, Dict
import pandas as pd

# === Downloader class for the Historical Data ===
class AsyncDownloader():
    def __init__(
            self,
            max_concurrency: int = 1,
            max_retries: int = 3,
            base_delay: float = 1.0
    ):
        """
        Initializes async downloader state.
        
        Args:
            max_concurrency: Maximum number of concurrent downloads (Set it to 1, any other value is giving error)
            max_retries: Maximum number of retry attempts per ticker
            base_delay: Base delay in seconds for exponential backoff
        """
        ## === Retries and delays ===
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_concurrency = max_concurrency

        ## === Semaphore to control concurrency ===
        self.sem = asyncio.Semaphore(value=max_concurrency)
        
        ## === Initialize state containers ===
        self._reset_state()

    def _reset_state(self):
        """
        Resets internal state for a new download run.
        This prevents state leakage between multiple run() calls.
        """
        self.done = set()
        self.failed = set()
        self.data: Dict[str, pd.DataFrame] = {}

    async def _run_one(
            self,
            ticker: str,
            worker,
            *args,
            **kwargs
    ):
        """
        Runs a single async worker with retry logic.

        Args:
            ticker: Ticker symbol to download
            worker: Async worker function that performs the download
            *args: Positional arguments to pass to the worker
            **kwargs: Keyword arguments to pass to the worker

        Returns:
            - ticker (str): Name of the ticker
            - result (pd.DataFrame | None): Historical data of that ticker, None if failed
            - err (Exception | None): Exception if failed, None if successful
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
    ) -> Dict[str, pd.DataFrame]:
        """
        Runs async downloads for all tickers.
        
        Args:
            tickers: Iterable of ticker symbols to download
            worker: Async worker function that performs the download
            *args: Positional arguments to pass to the worker
            **kwargs: Keyword arguments to pass to the worker

        Returns:
            Dictionary mapping ticker symbols to their downloaded DataFrames
            (only includes successful downloads)

        Note:
            Failed tickers are available in self.failed set after run completes.
        """
        ## === Reset state to prevent leakage between runs ===
        self._reset_state()

        ## === Create task for all the tickers ===
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