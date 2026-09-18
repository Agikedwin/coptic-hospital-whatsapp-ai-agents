import os
import httpx
from dotenv import load_dotenv


load_dotenv()


WHATSAPP_API_TOKEN = os.getenv(
    "WHATSAPP_API_TOKEN"
)

WHATSAPP_PHONE_NUMBER_ID = os.getenv(
    "WHATSAPP_PHONE_NUMBER_ID"
)

WHATSAPP_API_VERSION = os.getenv(
    "WHATSAPP_API_VERSION"
)


URL = (
    f"https://graph.facebook.com/v25.0/1301803526349316/messages"
    #f"{WHATSAPP_API_VERSION}/"
    #f"{WHATSAPP_PHONE_NUMBER_ID}/messages"
)


HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
    "Content-Type": "application/json"
}
