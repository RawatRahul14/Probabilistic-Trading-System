#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>
#include <stdexcept>

namespace py = pybind11;

// ====================
// Result Structure (Python visible as dict)
// ====================
py::dict aggregate_daily_news(py::list runs) {
    if (runs.empty()) {
        throw std::runtime_error("No run provided for daily aggregation.");
    }

    // ====================
    // Initiating the variables
    // ====================
    int unique_runs = static_cast<int>(runs.size());

    int total_news_count = 0;
    int bullish_count = 0;
    int bearish_count = 0;
    int neutral_count = 0;

    double weighted_sentiment_sum = 0.0;
    double sentiment_std_sum = 0.0;

    // ====================
    // Looping over the runs
    // ====================
    for (const auto& item: runs) {
        py::dict d = py::cast<py::dict>(item);

        int news_count = py::cast<int>(d["news_count"]);
        double sentiment_mean = py::cast<double>(d["sentiment_mean"]);
        double sentiment_std = py::cast<double>(d["sentiment_std"]);

        int bull = py::cast<int>(d["BULLISH_count"]);
        int bear = py::cast<int>(d["BEARISH_count"]);
        int neutral = py::cast<int>(d["NEUTRAL_count"]);

        total_news_count += news_count;

        bullish_count += bull;
        bearish_count += bear;
        neutral_count += neutral;

        weighted_sentiment_sum += sentiment_mean * news_count;
        sentiment_std_sum += sentiment_std;
    }

    if (total_news_count == 0) {
        throw std::runtime_error("Total news count is zero");
    }

    // ====================
    // Final Calculations
    // ====================
    double daily_sentiment_mean  = weighted_sentiment_sum / total_news_count;
    double daily_sentiment_std   = sentiment_std_sum / unique_runs;
    double bullish_prob = static_cast<double>(bullish_count) / total_news_count;
    double bearish_prob = static_cast<double>(bearish_count) / total_news_count;
    double neutral_prob = static_cast<double>(neutral_count) / total_news_count;
    double daily_bias_score = static_cast<double>(bullish_count - bearish_count) / total_news_count;
    double sentiment_disagreement = daily_sentiment_std  ;

    // ====================
    // Return as Python dict
    // ====================
    py::dict result;
    result["unique_runs"] = unique_runs;
    result["news_count"] = total_news_count;

    result["sentiment_mean"] = daily_sentiment_mean ;
    result["sentiment_std"] = daily_sentiment_std  ;
    result["daily_bias_score"] = daily_bias_score;

    result["bullish_count"] = bullish_count;
    result["bearish_count"] = bearish_count;
    result["neutral_count"] = neutral_count;

    result["bullish_prob"] = bullish_prob;
    result["bearish_prob"] = bearish_prob;
    result["neutral_prob"] = neutral_prob;

    result["sentiment_disagreement"] = sentiment_disagreement;

    return result;
}

// ====================
// Pybind module
// ====================
PYBIND11_MODULE(daily_news_agg, m) {
    m.def(
        "aggregate_daily_news",
        &aggregate_daily_news,
        "Aggregate per-run news data into a daily signal"
    );
}