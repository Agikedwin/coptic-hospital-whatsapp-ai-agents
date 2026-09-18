
from fastapi import APIRouter, Request, HTTPException, Query, BackgroundTasks


from agent.agent import run_chat
from whatsapp.whatsapp_service import send_whatsapp_message
from app import schemas
from app.schemas import ChatMessages

import os
from dotenv import load_dotenv
load_dotenv()
MAX_MESSAGE_LENGTH = 100


router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])


@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    print("WhatsApp webhook message received")

    try:
        data = await request.json()


    except Exception as e:
        body = await request.body()

        print("Invalid JSON body:")
        print(body.decode("utf-8"))

        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload"
        )

    print("Webhook payload:")
    print(data)

    # Immediately queue the processing tasks and return 200
    # Process the messages asynchronously after responding
    background_tasks.add_task(
        process_whatsapp_message,
        data
    )
    # Return 200 Ok immediately to acknowledge receipt
    return {
        "status": "received"
    }



async def process_whatsapp_message(data: dict):
    # Extract messages update
    print("STARTED Processing WhatsApp messages")

    entry = data.get("entry", [])

    if not entry:
        return

    changes = entry[0].get("changes", [])

    if not changes:
        return

    value = changes[0].get("value", {})
    print("WhatsApp message process_whatsapp_message ::2:")


    # Ignore delivery/read receipts
    if "messages" not in value:
        print("No incoming message")
        return

    messages = value["messages"]

    message = messages[0]

    from_number = message["from"]

    user_text = message.get("text", {}).get("body")

    if not user_text:
        return

    print(
        f"Message from {from_number}: {user_text}"
    )

    # Check message length
    if len(user_text) > MAX_MESSAGE_LENGTH:

        await send_whatsapp_message(
            to=from_number,
            body=f"Some random message body needed here"
        )
        return {"status": "message_too_long"}
    # Process chat pipeline
    user_text = [
        ChatMessages(
            role="user",
            content=user_text
        )
    ]
    response = await  run_chat(messages=user_text, session_id=from_number, client_id=from_number)


    result = schemas.ChatResponse(message=response, session_id=from_number)

    # send response
    return await send_whatsapp_message(to=from_number, body = result.message)


@router.get("/webhook")
async def verify_webhook(
        hub_mode: str = Query(None, alias="hub_mode"),
        hub_verify_token: str = Query(None, alias="hub_verify_token"),
        hub_challenge: str = Query(None, alias="hub_challenge")

):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    print(hub_verify_token)
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return int(hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Token Verification failed")