# === Python Modules ===
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph

# === AgentState ===
from .state import AgentState

# === Nodes ===
from .nodes import (
    get_queries,
    fetch_data
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
        get_queries
    )

    workflow.add_node(
        "Node_2_fetch_data",
        fetch_data
    )

    ## === Edges ===
    workflow.add_edge(
        START, "Node_1_Get_Queries"
    )

    workflow.add_edge(
        "Node_1_Get_Queries", "Node_2_fetch_data"
    )

    workflow.add_edge(
        "Node_2_fetch_data", END
    )

    return workflow.compile()