# 📈 Probabilistic Trading System
![Python](https://img.shields.io/badge/Python-3.x-blue)
![C++](https://img.shields.io/badge/C++-17%2F20-darkblue)
![DuckDB](https://img.shields.io/badge/DB-DuckDB-orange)
![Architecture](https://img.shields.io/badge/Architecture-Medallion-green)
![Modeling](https://img.shields.io/badge/Modeling-Probabilistic-red)
![Status](https://img.shields.io/badge/Status-Production%20Oriented-success)

### Overview
A high-performance, hybrid **Probabilistic Market Regime Detection System** designed for the Indian equity markets. This system combines the agentic reasoning of LLMs with the raw speed of C++ to quantify market sentiment and price action into probabilistic decision-support signals.

### 🚀 System Architecture

The system follows a **Medallion Architecture** to transform raw market noise into refined signals:

- **Ingestion Layer (Python)**: Orchestrates data fetching for 82+ tickers across multiple timeframes ($5m, 15m, 30m, 1h, 1d$) using `yfinance` and news data using `Tavily`.
- **Storage Layer (DuckDB)**: An OLAP-optimized database for high-speed time-series queries and vectorized data management.
- **Computational Kernel (C++/pybind11)**: High-speed technical indicator calculations and "NewsPressure" algorithms implemented in pure C++ for sub-millisecond execution.
- **Intelligence Layer (AI / LangGraph)**: An agentic workflow orchestrated by LangGraph that runs multiple specialized agents in parallel:
    - **Sentiment Agent** – Processes market news through a multi-stage pipeline (Query -> Dedup -> Sentiment -> Save).
    - **VIX Ingestion Agent** – Continuously ingests and normalizes volatility data (India VIX) to provide real-time market fear/uncertainty signals.

These agents execute concurrently using LangGraph's parallel node execution to minimize latency while enriching the probabilistic state used by the regime detection model.

### 📊 Feature Engineering & Indicators
The system implements a robust feature engineering pipeline focused on **Trend, Momentum, Volatility, and Volume**. Recent updates have introduced a **Stateful Indicator Engine** to handle live market feeds efficiently.

1. Incremental Calculation Logic
To avoid the computational overhead of recalculating full historical windows on every new tick, the system utilizes incremental math for core indicators:
    - **Stateful SMA/EMA**: Updates averages using only the previous state and the incoming price point.
    - **Wilder’s Smoothing (ADX)**: Implements incremental True Range (TR) and Directional Movement (+DM/-DM) smoothing to maintain accuracy across streaming data.
    - **Multi-Timeframe Support**: Native handling of windows ($5, 10, 20$) across all standard timeframes ($5m$ to $1d$).

2. Metadata & Persistence
The `RecordIndicators` utility ensures system resilience and cold-start efficiency:
    - **Metadata Tracking**: Persists the last known state of all indicators in `metadata.json`.
    - **Seamless Transitions**: On system restart, the kernel bootstraps using historical state, allowing for immediate, accurate signal generation without "warming up" windows.

### 🎯 Probabilistic Target Objective

The system calculates the conditional probability of the current market state by fusing technical signals, sentiment intensity, and volatility metrics:

$$
\underbrace{P(Regime_t \mid Technical_t, \dots, NewsPressure_t, Volatility_t)}_{\text{Market State}}
$$

Where the system quantifies the environment through:
- $\text{Regime}_t \in \{ \text{Trending, Mean-Reverting, High-Volatility Noise} \}$: The latent market state the system seeks to classify.
- $\text{Technical Indicators}_t$: A stateful vector of price-action features (SMA, EMA, ADX) calculated with $O(1)$ complexity.
- $\dots$: Expansion slots for upcoming Momentum, Volume, and Liquidity features currently in the `feature/indicators/`.
- $\text{News Pressure}_t$: A proprietary intensity metric derived from the Async Multi-Agent Sentiment Pipeline, quantifying the impact of external narrative shifts.
- $\text{Volatility}_t$: Real-time fear gauge signals ingested from India VIX, used to adjust the confidence intervals of the probabilistic output.

### 🔒 Proprietary Notice & Core Logic
Please note that while this repository demonstrates the system's **architecture, data engineering pipelines, and high-performance C++ kernels**, certain core proprietary components have been intentionally omitted to protect intellectual property. These include:
- **Signal Generation Heuristics**: The specific mathematical thresholds for entry/exit.
- **Probability Weighting Models**: The final layer of the Intelligence module.
- **Risk Management Algorithms**: Live execution safety parameters and drawdown protection logic.

### 🛠 Tech Stack
- **Language**: Python 3.x, C++17/20
- **Database**: DuckDB
- **Bindings**: pybind11
- **Tools**: LangChain, LangGraph, Pydantic
- **Data Sourcing**: yfinance, Tavily

### 🚀 Key Features
1. **Agentic Sentiment Analysis**  
Unlike static sentiment tools, this system uses a **LangGraph-driven pipeline** to:
- Search for event-specific news via `Tavily`.
- Deduplicate information to avoid "echo chamber" bias.
- Score sentiment using structured LLM prompts.

2. C++ NewsPressure Engine  
The system calculates NewsPressure, a quantitative metric of how news volume and sentiment intensity are likely to impact price volatility.

3. Market Regime Detection  
The probability/ module (in development) uses the combined data from technical indicators and sentiment to classify the market into regimes:
- Trending High-Confidence
- Mean Reverting
- High-Volatility Noise

4. Parallel Agent Execution (LangGraph)
The system runs two specialized agents in parallel using LangGraph:

- **Sentiment Agent**
    - Fetches market news using Tavily
    - Deduplicates articles to avoid narrative amplification
    - Generates structured sentiment scores using LLM prompts

- **VIX Ingestion Agent**
    - Ingests and tracks India VIX data
    - Quantifies market fear and volatility expectations
    - Feeds volatility state directly into the probabilistic regime model

Running these agents concurrently ensures that **news sentiment and volatility signals are ingested with minimal latency**, allowing the probabilistic model to react to evolving market conditions faster.

### ⚡ Performance & Optimization: The Async Leap
The news sentiment pipeline was recently overhauled from a **sequential execution** model to an **Asynchronous Multi-Agent** architecture. By parallelizing I/O-bound tasks and implementing a C++ aggregation layer, the system now processes larger volumes of data in a fraction of the time.

News Pipeline Benchmarks:
| Phase | Sequential (Old) | Async + C++ (Current) | Improvement |
|---|---|---|---|
| News Fetching | 23.05s (15 articles) | 5.08s (24 articles) | **78% Faster** |
| Sentiment Analysis | 22.32s | 4.99s | **77% Faster** |
| C++ Aggregation | N/A | 0.001s | **Instant** |
| **Total Pipeline** | **46.00s** | **11.00s** | **~76% Reduction** |

> Benchmark results are derived from timed pipeline runs using structured logging. Detailed run logs are available in `logs/`.  
Full benchmark logs: [View Logs](logs/)

### 🧠 Design Philosophy

- **Probabilistic > Deterministic Signals** - Markets are noisy systems; outputs are expressed as probability distributions, not binary signals.
- **Latency-Aware Architecture** - IO-bound and compute-bound tasks are separated (Async Python vs C++ kernels).
- **Agentic Over Monolithic AI** - Multi-stage reasoning pipelines provide auditability and explainability.
- **Production-Oriented Engineering** - Logging, metadata persistence, benchmarking, and modular compute kernels are first-class citizens.