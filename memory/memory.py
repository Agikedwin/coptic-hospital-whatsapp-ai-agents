from langgraph.graph import MessagesState
from pydantic import Field, BaseModel


class AgentState(MessagesState):

    client_id: str

    session_id: str

    memory_context: str


    # Supervisor decision
    next_agent: str



    # RAG state
    question: str
    documents: list[str] = []
    rag_answer: str = ""


    # Tool state
    tool_results: dict = {}


    # Final response
    final_answer: str = ""


class MemoryExtraction(BaseModel):

    summary: str = Field(
        description="One concise summary of the current session"
    )

    memory_facts: list[str] = Field(
        default_factory=list,
        description=
        "Durable user preferences, facts, or context worthy of carrying into future sessions."
    )