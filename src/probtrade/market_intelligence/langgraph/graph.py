# === Python Modules ===
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langchain_core.runnables import RunnableLambda

# === AgentState ===
from .state import AgentState

# === Nodes ===
from .agents import (
    get_queries,
    fetch_data,
    get_sentiment,
    save_node,
    apply_deduplicate
)

# === Graph Workflow ===
def run_graph():
    """
    Runs the state graph
    """
    ## === Initialising the StateGraph ===
    workflow = StateGraph(AgentState)

    ## === Nodes ===
    workflow.add_node(
        "Node_1_Get_Queries",
        RunnableLambda(get_queries).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.add_node(
        "Node_2_fetch_data",
        RunnableLambda(fetch_data).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.add_node(
        "Node_3_Apply_deduplicate",
        RunnableLambda(apply_deduplicate).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.add_node(
        "Node_4_get_sentiment",
        RunnableLambda(get_sentiment).with_config(
            {
                "run_async": True
            }
        )
    )

    workflow.add_node(
        "Node_5_save_node",
        RunnableLambda(save_node).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === Edges ===
    workflow.add_edge(
        START, "Node_1_Get_Queries"
    )

    workflow.add_edge(
        "Node_1_Get_Queries", "Node_2_fetch_data"
    )

    workflow.add_edge(
        "Node_2_fetch_data", "Node_3_Apply_deduplicate"
    )

    workflow.add_edge(
        "Node_3_Apply_deduplicate", "Node_4_get_sentiment"
    )

    workflow.add_edge(
        "Node_4_get_sentiment", "Node_5_save_node"
    )

    workflow.add_edge(
        "Node_5_save_node", END
    )

    return workflow.compile()