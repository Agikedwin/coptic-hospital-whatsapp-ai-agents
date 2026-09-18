from typing import Literal
from memory.memory import AgentState

def supervisor_router(
    state:AgentState
)->Literal[
    "rag",
    "tool",
    "both"
]:

    return state["next_agent"]