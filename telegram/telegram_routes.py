# api/routers/telegram.py

import json
import logging
import secrets
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Header,
    HTTPException,
    Request,
    status,
)

from telebot.types import Update

from app.settings import settings
from telegram.telegram_bot import bot

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
)
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    telegram_secret: Annotated[
        str | None,
        Header(
            alias="X-Telegram-Bot-Api-Secret-Token"
        ),
    ] = None,
):

    # --------------------------------------------------
    # Verify Telegram webhook secret
    # --------------------------------------------------

    expected_secret = (
        settings.telegram_webhook_secret
    )

    if (
        telegram_secret is None
        or not secrets.compare_digest(
            telegram_secret,
            expected_secret,
        )
    ):

        logger.warning(
            "Invalid Telegram webhook secret"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Telegram webhook secret",
        )

    # --------------------------------------------------
    # Read Telegram JSON
    # --------------------------------------------------

    try:

        payload = await request.json()

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload",
        )

    # --------------------------------------------------
    # Convert Telegram JSON -> Update
    # --------------------------------------------------

    try:

        update = Update.de_json(payload)

    except Exception as error:

        logger.exception(
            "Unable to parse Telegram update"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Telegram update",
        ) from error

    if update is None:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty Telegram update",
        )

    # --------------------------------------------------
    # Process AFTER returning response to Telegram
    # --------------------------------------------------

    background_tasks.add_task(
        bot.process_new_updates,
        [update],
    )

    return {
        "ok": True
    }