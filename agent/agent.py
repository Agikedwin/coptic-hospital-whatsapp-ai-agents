# =====================================================
# IMPORTS
# =====================================================

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.schemas import ChatMessages

from memory.memory import AgentState
from memory.sessions import get_sessions_memory

from helpers.helper import (
    _content_to_text,
    _to_langchain_messages
)


# Nodes

from rag.agent_state import (
    supervisor_node,
)
from agent_route.agent_routes import (
    supervisor_router
)
from agent.node_route import (
    agent_node,
    route_after_agent,
    finalize_node
)

from agent.rag_agent import rag_node

from tool_calls.tool_call import TOOLS



# =====================================================
# BUILD GRAPH
# =====================================================


builder = StateGraph(
    AgentState
)



# -------------------------
# Nodes
# -------------------------

builder.add_node(
    "supervisor",
    supervisor_node
)


builder.add_node(
    "rag",
    rag_node
)


builder.add_node(
    "agent",
    agent_node
)


builder.add_node(
    "tools",
    ToolNode(TOOLS)
)


builder.add_node(
    "finalize",
    finalize_node
)



# -------------------------
# Entry
# -------------------------

builder.add_edge(
    START,
    "supervisor"
)



# =====================================================
# SUPERVISOR ROUTING
# =====================================================


builder.add_conditional_edges(

    "supervisor",

    supervisor_router,

    {

        "rag":
        "rag",

        "tool":
        "agent",

        "both":
        "rag"

    }

)



# =====================================================
# RAG ROUTING
# =====================================================


def after_rag(state: AgentState):

    """
    If supervisor selected both,
    send result to tool agent.
    Otherwise finalize.
    """

    if state["next_agent"] == "both":

        return "agent"


    return "finalize"



builder.add_conditional_edges(

    "rag",

    after_rag,

    {

        "agent":
        "agent",

        "finalize":
        "finalize"

    }

)



# =====================================================
# TOOL AGENT ROUTING
# =====================================================


builder.add_conditional_edges(

    "agent",

    route_after_agent,

    {

        "tools":
        "tools",

        "finalize":
        "finalize"

    }

)



# Tool returns back to agent
# so LLM can interpret tool result

builder.add_edge(
    "tools",
    "agent"
)



# =====================================================
# FINAL RESPONSE
# =====================================================


builder.add_edge(

    "finalize",

    END

)



# Compile

graph = builder.compile()



# =====================================================
# CHAT RUNNER
# =====================================================


async def run_chat(
    *,
    messages:list[ChatMessages],
    client_id:str,
    session_id:str,

)->str:


    # Load previous memory

    previous_memory = get_sessions_memory(
        client_id,
        2
    )


    memory_context = "\n".join(

        f"- {item}"

        for item in previous_memory

    )


    result = await graph.ainvoke(

        {

        "messages":
            _to_langchain_messages(messages),


        "client_id":
            str(client_id),


        "session_id":
            session_id,


        "memory_context":
            memory_context

        }

    )



    # Find final assistant response

    final_message = next(

        (

            message

            for message in reversed(
                result["messages"]
            )

            if isinstance(
                message,
                AIMessage
            )

            and not message.tool_calls

        ),

        None

    )

    if final_message is None:

        return (
            "I couldn't produce an answer. "
            "Please try again."
        )


    return _content_to_text(
        final_message.content
    )