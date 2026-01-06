# === Python Modules ===
from datetime import date

# === Logger ===
from probtrade import get_logger

# === Agentic AI Graph Function ===
from probtrade.market_intelligence import run_graph

class AgenticAiPipeline:
    def __init__(self):
        self.logger = get_logger(
            name = "NEWS_DATA",
            log_file = "news_data.log"
        )

    def main(self):
        self.logger.info("=" * 70)
        self.logger.info(f">>>>>>>> DATE: {date.today()} <<<<<<<<")
        self.logger.info(">>>>>>> Starting Agentic AI Graph Pipeline <<<<<<<")

        try:
            ## === Initialize graph ===
            self.logger.info("Initializing agentic graph")
            graph = run_graph()

            ## === Run graph ===
            self.logger.info("Invoking agentic graph")
            state = graph.invoke(
                input = {}
            )

            ## === Log completion ===
            self.logger.info("Agentic AI Graph completed successfully")

            ## === log state keys only ===
            if isinstance(state, dict):
                self.logger.info(
                    f"Graph output keys: {list(state.keys())}"
                )

            self.logger.info("=" * 70 + "\n")

            return state

        except Exception as e:
            self.logger.exception(
                "Fatal error while running Agentic AI Graph"
            )
            raise


if __name__ == "__main__":
    pipeline = AgenticAiPipeline()
    pipeline.main()