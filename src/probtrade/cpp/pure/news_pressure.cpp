#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cmath>
#include <string>
#include <vector>

namespace py = pybind11;

// ====================
// Internal enums
// ====================
enum class MarketBias {
    BULLISH,
    NEUTRAL,
    BEARISH
};

enum class ImpactLevel {
    VERY_HIGH,
    HIGH,
    MEDIUM,
    LOW,
    VERY_LOW
};

// ====================
// Compile-time helpers
// ====================
constexpr double impact_weight(ImpactLevel impact) {
    switch (impact) {
        case ImpactLevel::VERY_HIGH: return 1.5;
        case ImpactLevel::HIGH: return 1.2;
        case ImpactLevel::MEDIUM: return 1.0;
        case ImpactLevel::LOW: return 0.6;
        case ImpactLevel::VERY_LOW: return 0.3;
    }

    return 0.0;
}

constexpr int bias_direction(MarketBias bias) {
    switch (bias) {
        case MarketBias::BULLISH: return 1;
        case MarketBias::NEUTRAL: return 0;
        case MarketBias::BEARISH: return -1;
    }

    return 0;
}

// ====================
// Parsing Helpers
// ====================
MarketBias parse_bias(const std::string& s) {
    if (s == "BULLISH") return MarketBias::BULLISH;
    if (s == "BEARISH") return MarketBias::BEARISH;
    return MarketBias::NEUTRAL;
}

ImpactLevel parse_impact(const std::string& s) {
    if (s == "very_high") return ImpactLevel::VERY_HIGH;
    if (s == "high") return ImpactLevel::HIGH;
    if (s == "low") return ImpactLevel::LOW;
    if (s == "very_low") return ImpactLevel::VERY_LOW;

    return ImpactLevel::MEDIUM;
}

// ====================
// Core Computation
// ====================
inline double compute_single_score(
    int sentiment_score,
    MarketBias bias,
    ImpactLevel impact,
    double confidence
) {
    // Returning 0, if the direction is Neutral
    const int direction = bias_direction(bias);
    if (direction == 0) return 0;

    // Standardising the sentiment score
    const double tone_mod = std::abs(sentiment_score - 5) / 5.0;

    // Calculating the aggregated news score for a single article.
    return direction * impact_weight(impact) * confidence * (1.0 + tone_mod);
}

// ====================
// Python Facing Function
// ====================
double compute_news_pressure(py::list news_items) {

    // Initiating a placeholder to store final outcome.
    double total_score = 0.0;

    // Looping through Each article
    for (const auto& item: news_items) {

        // Defining the item as a python dict
        py::dict d = py::cast<py::dict>(item);

        // Extracting all values
        int sentiment_score = py::cast<int>(d["sentiment_score"]);
        std::string bias_str = py::cast<std::string>(d["market_bias"]);
        std::string impact_str = py::cast<std::string>(d["news_impact"]);
        double confidence = py::cast<double>(d["confidence"]);

        // Adding each article's aggregated outcome
        total_score += compute_single_score(
            sentiment_score,
            parse_bias(bias_str),
            parse_impact(impact_str),
            confidence
        );
    }

    return total_score;
}

// ====================
// Pybind Module
// ====================
PYBIND11_MODULE(news_pressure, m) {
    m.def(
        "compute_news_pressure",
        &compute_news_pressure,
        "Compute aggregated news pressure score"
    );
}