from typing import  Literal, Any


from helpers.helper import _content_to_text
from memory.memory import  AgentState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage, ChatMessage

from memory.sessions import get_sessions_memory, save_session
from tool_calls.tool_call import TOOLS
from utilty.utilities import SYSTEM_PROMPT, summary_model, model


def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:

    """
    memory_context = state["memory_context"]

    system_message = SystemMessage(
        content=SYSTEM_PROMPT.format(
            memory_context=memory_context
            if memory_context
            else "No saved memory yet."
        )
    )
    """

    response = model.bind_tools(TOOLS).invoke(
        [
            #system_message,
            *state["messages"]
        ]
    )

    return {
        "messages": [response]
    }

#Agent decides if toll call is need or not
def route_after_agent(state: AgentState) -> Literal["tools", "finalize"]:
    last_message = state["messages"][-1]
    print("LAST MESSAGE =========================================||||||||||||||||||||||||||||||||||||||||||||||\\")
    print(last_message)
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return  "tools"

    return "finalize"
import json
from sqlalchemy import select



async  def finalize_node(state: AgentState) -> dict[str, Any]:
    visible_messages = state["messages"]
    transcript = "\n".join(
        f"{message.type}: {_content_to_text(message.content)}" for message in visible_messages
    )

    previous_memory = get_sessions_memory(state["client_id"], 2)
    memory_context = "\n".join(f"- {item}" for item in previous_memory) or "None"

    extraction = await  summary_model.ainvoke(
        [
            SystemMessage(
                content=(
                    "Summarize the current chat and extract only durable facts that are useful across future sessions. "
                    "Extremely minimum database results, always store client  unique identifiers and phone numbers only. Only store Identifiers not yet stored before\n\n"
                    f"Existing long-term memory:\n{memory_context}"
                )
            ),
            HumanMessage(content=transcript),
        ]
    )

    merged_memory = list(
        dict.fromkeys(
            previous_memory + extraction.memory_facts
        )
    )

    save_session(
        client_id=int(state["client_id"]),
        session_id=state["session_id"],
        summary=extraction.summary,
        memory=merged_memory[-2:],
    )


