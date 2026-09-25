# services/telegram_ai_service.py

from typing import Any

from agent.agent import run_chat
from app import schemas
from app.schemas import ChatMessages


async def process_ai_message(
    user_message: str,
    user_id: int,
    chat_id: int,
) -> str:
    """
    Pass a Telegram message to the existing AI agent.

    Each Telegram user gets a unique session.
    """

    session_id = f"telegram:{chat_id}:{user_id}"

    user_text = [
        ChatMessages(
            role="user",
            content=user_message
        )
    ]

    chat_messages = [

        ChatMessages(
            role="user",
            content=user_text
        )

    ]

    # ====================================================
    # RUN AI AGENT
    # ====================================================

    response = await run_chat(
        messages=chat_messages,
        session_id=session_id,
        client_id=session_id
    )

    result = schemas.ChatResponse(
        message=response,
        session_id=session_id
    )

    return extract_ai_response(result)


def extract_ai_response(result) -> str:
    """
    Extract only the human-readable AI response.
    """

    if result is None:
        return "I could not generate a response."

    # Plain text
    if isinstance(result, str):
        return result

    # Object such as:
    # ChatResponse(message="...", session_id="...")
    if hasattr(result, "message"):
        return str(result.message)

    # LangChain AIMessage
    if hasattr(result, "content"):
        return str(result.content)

    # Dictionary response
    if isinstance(result, dict):

        if result.get("message"):
            return str(result["message"])

        if result.get("response"):
            return str(result["response"])

        if result.get("answer"):
            return str(result["answer"])

        if result.get("output"):
            return str(result["output"])

        messages = result.get("messages")

        if messages:
            last_message = messages[-1]

            if hasattr(last_message, "content"):
                return str(last_message.content)

            return str(last_message)

    return str(result)