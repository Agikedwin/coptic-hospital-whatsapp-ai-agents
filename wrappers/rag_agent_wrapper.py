from memory.sharedState import AgentSharedState
from rag.llm_rag import rag_graph


def rag_node(state:AgentSharedState):

    question = state["messages"][-1].content


    result = rag_graph.invoke(
        {
            "question":question,
            "memory":state["memory"],
            "retry_count": 0
        }
    )


    return {

        "rag_context": result["documents"],

        "messages":[
            {
             "role":"assistant",
             "content":result["answer"]
            }
        ]

    }