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
- **Intelligence Layer (AI)**: An agentic workflow that processes news sentiment through a multi-stage pipeline (Query → Dedup → Sentiment → Save).

### 🎯 Probabilistic Target Objective

The system estimates the conditional probability of a market regime given the current technical, sentiment, and volatility state:

$$
P(Regime_t \mid Technical_t,\ NewsPressure_t,\ Volatility_t)
$$

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
- **Production-Oriented Engineering** - Logging, benchmarking, and modular compute kernels are first-class citizens.