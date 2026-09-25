import asyncio
import httpx

from whatsapp.constants import HEADERS, URL


# ============================================================
# SEND NORMAL WHATSAPP TEXT MESSAGE
# ============================================================

async def send_whatsapp_message(
    to: str,
    body: str
):
    """
    Send a text message through the WhatsApp Cloud API.
    """

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": body
        }
    }

    try:

        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                URL,
                headers=HEADERS,
                json=payload
            )

        print(
            "WHATSAPP RESPONSE =====================",
            response.status_code,
            response.text
        )

        if response.status_code not in (200, 201):

            print(
                "❌ Error sending WhatsApp message:",
                response.text
            )

            response.raise_for_status()

        print(
            f"✓ WhatsApp message sent successfully to {to}"
        )

        return response.json()

    except httpx.RequestError as e:

        print(
            "❌ WhatsApp network error:",
            str(e)
        )

        raise

    except httpx.HTTPStatusError as e:

        print(
            "❌ WhatsApp HTTP error:",
            str(e)
        )

        raise

    except Exception as e:

        print(
            "❌ Unexpected WhatsApp error:",
            str(e)
        )

        raise


# ============================================================
# SEND WHATSAPP TYPING INDICATOR
# ============================================================

async def send_typing_indicator(
    message_id: str
):
    """
    Mark an incoming WhatsApp message as read
    and display the native WhatsApp typing indicator.

    message_id must be the ID of the INCOMING message,
    for example:

    wamid.HBgL2547...
    """

    if not message_id:

        print(
            "⚠ Cannot send typing indicator: "
            "message_id is missing"
        )

        return False

    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
        "typing_indicator": {
            "type": "text"
        }
    }

    try:

        async with httpx.AsyncClient(timeout=15.0) as client:

            response = await client.post(
                URL,
                headers=HEADERS,
                json=payload
            )

        print(
            "WHATSAPP TYPING RESPONSE ===============",
            response.status_code,
            response.text
        )

        if response.status_code == 200:

            print(
                f"✓ Typing indicator started "
                f"for message {message_id}"
            )

            return True

        print(
            "❌ Error starting typing indicator:",
            response.text
        )

        return False

    except httpx.RequestError as e:

        print(
            "❌ Typing indicator network error:",
            str(e)
        )

        return False

    except Exception as e:

        print(
            "❌ Typing indicator error:",
            str(e)
        )

        return False


# ============================================================
# KEEP WHATSAPP TYPING INDICATOR ACTIVE
# ============================================================

async def keep_typing(
    message_id: str,
    interval: int = 20
):
    """
    Keep refreshing the WhatsApp typing indicator
    while the AI agent is generating its response.

    The task should be cancelled once the AI response
    is ready.
    """

    try:

        while True:

            await send_typing_indicator(
                message_id=message_id
            )

            await asyncio.sleep(interval)

    except asyncio.CancelledError:

        print(
            f"✓ Typing refresh stopped "
            f"for message {message_id}"
        )

        raise

    except Exception as e:

        print(
            "❌ keep_typing error:",
            str(e)
        )