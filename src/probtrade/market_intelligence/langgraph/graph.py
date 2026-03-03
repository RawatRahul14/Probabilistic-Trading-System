# === Python Modules ===
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langchain_core.runnables import RunnableLambda

# === AgentState ===
from .state import (
    NewsState,
    VixState,
    AgentState
)

# === Nodes ===
from .agents import (
    get_queries,
    fetch_data,
    get_sentiment,
    save_node,
    apply_deduplicate
)

from .agents import (
    extract_vix_query,
    get_vix,
    extract_india_vix
)

# === Graph Workflow ===
def run_news_subgraph():
    """
    Runs the News subgraph
    """
    ## === News graph ===
    news_workflow = StateGraph(NewsState)

    news_workflow.add_node(
        "Node_1_Get_Queries",
        RunnableLambda(get_queries).with_config(
            {
                "run_async": True
            }
        )
    )
    news_workflow.add_node(
        "Node_2_Fetch_Data",
        RunnableLambda(fetch_data).with_config(
            {
                "run_async": True
            }
        )
    )
    news_workflow.add_node(
        "Node_3_Apply_Deduplicate",
        RunnableLambda(apply_deduplicate).with_config(
            {
                "run_async": True
            }
        )
    )
    news_workflow.add_node(
        "Node_4_Get_Sentiment",
        RunnableLambda(get_sentiment).with_config(
            {
                "run_async": True
            }
        )
    )
    news_workflow.add_node(
        "Node_5_Save_Node",
        RunnableLambda(save_node).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === Vix Graph edges ===
    news_workflow.add_edge(
        START, "Node_1_Get_Queries"
    )
    news_workflow.add_edge(
        "Node_1_Get_Queries", "Node_2_Fetch_Data"
    )
    news_workflow.add_edge(
        "Node_2_Fetch_Data", "Node_3_Apply_Deduplicate"
    )
    news_workflow.add_edge(
        "Node_3_Apply_Deduplicate", "Node_4_Get_Sentiment"
    )
    news_workflow.add_edge(
        "Node_4_Get_Sentiment", "Node_5_Save_Node"
    )
    news_workflow.add_edge(
        "Node_5_Save_Node", END
    )

    return news_workflow.compile()

def run_vix_subgraph():
    """
    Runs the Vix subgraph
    """
    ## === News graph ===
    vix_workflow = StateGraph(VixState)

    vix_workflow.add_node(
        "Node_1_Extract_Vix_Query",
        RunnableLambda(extract_vix_query).with_config(
            {
                "run_async": True
            }
        )
    )
    vix_workflow.add_node(
        "Node_2_Get_Vix",
        RunnableLambda(get_vix).with_config(
            {
                "run_async": True
            }
        )
    )
    vix_workflow.add_node(
        "Node_3_Extract_India_Vix",
        RunnableLambda(extract_india_vix).with_config(
            {
                "run_async": True
            }
        )
    )

    ## === Edges ===
    vix_workflow.add_edge(
        START, "Node_1_Extract_Vix_Query"
    )
    vix_workflow.add_edge(
        "Node_1_Extract_Vix_Query", "Node_2_Get_Vix"
    )
    vix_workflow.add_edge(
        "Node_2_Get_Vix", "Node_3_Extract_India_Vix"
    )
    vix_workflow.add_edge(
        "Node_3_Extract_India_Vix", END
    )

    return vix_workflow.compile()

def run_graph():
    """
    Runs the parent graph with subgraphs in parallel
    """
    workflow = StateGraph(AgentState)

    ## === Compiled Sub-Graphs ===
    news_subgraph = run_news_subgraph()
    vix_subgraph = run_vix_subgraph()

    ## === Parent Nodes ===
    # We add the compiled graphs just like regular nodes
    workflow.add_node(
        "News_Branch", news_subgraph
    )
    workflow.add_node(
        "VIX_Branch", vix_subgraph
    )

    ## === Parallel Edges ===
    # Start both branches at the same time
    workflow.add_edge(START, "News_Branch")
    workflow.add_edge(START, "VIX_Branch")

    # The graph will wait for both to finish before reaching END
    workflow.add_edge("News_Branch", END)
    workflow.add_edge("VIX_Branch", END)

    return workflow.compile()