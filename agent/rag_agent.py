from langchain_core.messages import AIMessage

from memory.memory import AgentState as sharedAgentState

from rag.llm_rag import rag_graph



def rag_node(
    state:sharedAgentState
):


    question = (
        state["messages"][-1]
    )


    result = rag_graph.invoke(

        {

        "messages":
            state["messages"],


        "question":
            question,


        "retry_count":
            0,


        "client_id":
            state["client_id"],


        "session_id":
            state["session_id"],


        "memory_context":
            state["memory_context"]

        }

    )

    return {


        "documents":
            result.get(
                "documents",
                []
            ),


        "rag_answer":
            result.get(
                "generation",
                ""
            ),


        "messages":
        [
            AIMessage(

                content=
                result["generation"]

            )
        ]

    }