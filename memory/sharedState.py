from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from operator import add


class AgentSharedState(TypedDict):

    messages: Annotated[list[BaseMessage], add]

    client_id: str

    session_id: str

    route: str

    rag_context: list[str]

    tool_results: dict

    final_answer: str

    memory: dict