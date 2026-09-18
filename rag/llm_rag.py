from langgraph.graph import StateGraph, END

from rag.agent_state import (
    AgentState,
    retrieve,
    generate,
    retry_tracker,
    rewrite_query,
    grade_documents,
    decide
)


graph = StateGraph(AgentState)


graph.add_node(
    "rewrite",
    rewrite_query
)

graph.add_node(
    "retrieve",
    retrieve
)

graph.add_node(
    "grade",
    grade_documents
)

graph.add_node(
    "generate",
    generate
)

graph.add_node(
    "retry",
    retry_tracker
)


graph.set_entry_point(
    "rewrite"
)


graph.add_edge(
    "rewrite",
    "retrieve"
)


graph.add_edge(
    "retrieve",
    "grade"
)


graph.add_conditional_edges(

    "grade",

    decide,

    {
        "rewrite":"retry",

        "generate":"generate"
    }

)


graph.add_edge(
    "retry",
    "rewrite"
)


graph.add_edge(
    "generate",
    END
)


rag_graph = graph.compile()



print("RAG Graph compiled successfully")
