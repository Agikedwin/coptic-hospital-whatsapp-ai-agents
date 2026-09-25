# scripts/set_telegram_webhook.py

import asyncio

from app.settings import settings
from telegram.telegram_bot import bot


async def set_webhook():

    print(
        "Setting Telegram webhook:"
    )

    print(
        settings.telegram_webhook_url
    )

    # Remove existing webhook
    await bot.delete_webhook(
        drop_pending_updates=False
    )

    # Register FastAPI webhook
    result = await bot.set_webhook(
        url=settings.telegram_webhook_url,
        secret_token=(
            settings.telegram_webhook_secret
        ),
        allowed_updates=[
            "message"
        ],
    )

    print(
        "Webhook result:",
        result,
    )

    # Check configuration
    info = await bot.get_webhook_info()

    print(
        "Webhook URL:",
        info.url,
    )

    print(
        "Pending updates:",
        info.pending_update_count,
    )

    if info.last_error_message:

        print(
            "Last error:",
            info.last_error_message,
        )

    await bot.close_session()


if __name__ == "__main__":

    asyncio.run(
        set_webhook()
    )