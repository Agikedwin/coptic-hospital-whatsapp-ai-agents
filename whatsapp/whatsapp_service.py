import httpx

from whatsapp.constants import HEADERS,WHATSAPP_PHONE_NUMBER_ID,WHATSAPP_API_TOKEN,URL,WHATSAPP_API_VERSION

import httpx

async def send_whatsapp_message(
    to: str,
    body: str
):
    """Call the WhatsApp Cloud API to send a text message"""

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": body
        }
    }

    async with httpx.AsyncClient() as client:
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

    if response.status_code != 200:
        print("Error sending WhatsApp message:", response.text)
        response.raise_for_status()

    return response.json()