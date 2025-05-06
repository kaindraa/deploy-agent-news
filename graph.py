from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Optional, List, Callable

class GState(TypedDict):
    topic: str
    outline: Optional[str]
    context: str
    iteration_count: int
    queries: Optional[List[str]]
    is_continue: Optional[str]
    searched_query: Optional[List[str]]
    result: Optional[str]

def build_graph(planner, web_planner, web_retriever, grader, writer, branch):

    g = StateGraph(GState)
    g.add_node("planner", planner)
    g.add_node("web_planner", web_planner)
    g.add_node("web_retriever", web_retriever)
    g.add_node("grader", grader)
    g.add_node("writer", writer)
    g.add_edge(START, "planner")
    g.add_edge("planner", "web_planner")
    g.add_edge("web_planner", "web_retriever")
    g.add_edge("web_retriever", "grader")
    g.add_conditional_edges("grader", branch, {
        "web_planner": "web_planner",
        "writer": "writer"
    })
    g.add_edge("writer", END)
    return g.compile()
