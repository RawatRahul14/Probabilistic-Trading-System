# Probabilistic-Trading-System

### Overview
This project implements a probabilistic market regime detection system designed for intraday and short-term trading strategies in Indian equity markets.

Instead of relying on opaque machine learning models, the system estimates conditional probabilities of future market regimes (Advance / Neutral / Decline) based on the current market state. The goal is to build a `transparent`, `auditable`, and `statistically` grounded regime layer that can be used upstream of trading signals, position sizing, and risk management.

#### Why Probabilistic (Not ML)
- Market regimes are low-signal, high-impact events
- Interpretability and stability are prioritised over raw prediction accuracy
- Frequency-based conditional probability avoids overfitting and regime flickering
- Every regime decision can be explained, reproduced, and audited