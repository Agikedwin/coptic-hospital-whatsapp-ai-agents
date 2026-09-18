
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage, ChatMessage
from typing import  Literal, Any
from app.schemas import ChatMessages
import os
import httpx
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def _content_to_text(content: Any) -> str:
    print("AT  _content_to_text ", content)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces: list[str] = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                pieces.append(str(part.get("text", "")))
            elif isinstance(part, str):
                pieces.append(part)
        return "\n".join(piece for piece in pieces if piece)
    return str(content)

def _to_langchain_messages(messages: list[ChatMessages]) -> list[BaseMessage]:
    print("AT  _to_langchain_messages |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ", messages)
    converted: list[ChatMessage] = []

    for message in messages:
        text = _content_to_text(message)
        if not text:
            continue
        if message.role == "user":
            converted.append(HumanMessage(content=text))
        elif message.role == "assistant":
            converted.append(AIMessage(content=text))
        else:
            converted.append(SystemMessage(content=text))
    return converted

async def _get(path: str, params: dict[str, Any]) -> str:
    url = f"{API_BASE_URL}{path}"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            url,
            params=params
        )
        response.raise_for_status()
        return response.text

