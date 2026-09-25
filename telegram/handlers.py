# telegram/handlers.py

import logging

from telebot.async_telebot import AsyncTeleBot

from telegram.telegram_ai_service import process_ai_message

logger = logging.getLogger(__name__)
import asyncio



def register_telegram_handlers(bot: AsyncTeleBot):


    # --------------------------------------------------
    # START COMMAND
    # --------------------------------------------------

    @bot.message_handler(commands=["start"])
    async def send_welcome(message):

        first_name = (
            message.from_user.first_name
            if message.from_user
            else "there"
        )

        welcome_text = (
            f"Hello {first_name} 👋\n\n"
            "Welcome to Coptic AI Agent.\n\n"
            "I can assist you with information about "
            "Coptic services and answer your questions.\n\n"
            "How can I assist you today?"
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=welcome_text,
        )


    # --------------------------------------------------
    # HELP
    # --------------------------------------------------

    @bot.message_handler(commands=["help"])
    async def send_help(message):

        help_text = (
            "Coptic AI Agent can help answer your questions.\n\n"
            "Simply type your question and send it to me."
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=help_text,
        )


    # --------------------------------------------------
    # TEXT MESSAGE -> AI
    # --------------------------------------------------

    @bot.message_handler(content_types=["text"])
    async def handle_text_message(message):

        chat_id = message.chat.id

        user_id = (
            message.from_user.id
            if message.from_user
            else chat_id
        )

        user_message = message.text

        if not user_message:
            return
            # Used to stop the typing loop
        stop_typing = asyncio.Event()

        # Start typing immediately
        typing_task = asyncio.create_task(
            keep_typing(
                bot=bot,
                chat_id=chat_id,
                stop_event=stop_typing,
            )
        )

        try:

            logger.info(
                "Telegram message user=%s chat=%s",
                user_id,
                chat_id,
            )

            # Show "typing..."
            await bot.send_chat_action(
                chat_id=chat_id,
                action="typing",
            )

            # --------------------------------------------
            # CALL YOUR LANGGRAPH/LANGCHAIN AGENT
            # --------------------------------------------

            ai_response = await process_ai_message(
                user_message=user_message,
                user_id=user_id,
                chat_id=chat_id,
            )

            # --------------------------------------------
            # SEND RESPONSE BACK TO TELEGRAM
            # --------------------------------------------

            for chunk in split_telegram_message(ai_response):

                await bot.send_message(
                    chat_id=chat_id,
                    text=chunk,
                    parse_mode="HTML",
                )

        except Exception:

            logger.exception(
                "Error processing Telegram AI message"
            )

            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "Sorry, I encountered an error while "
                    "processing your request. Please try again."
                ),
            )

        finally:

            #==============================================
            # STOP TYPING
            # ==============================================

            stop_typing.set()

            try:
                await typing_task
            except asyncio.CancelledError:
                pass


    # --------------------------------------------------
    # PHOTO
    # --------------------------------------------------

    @bot.message_handler(content_types=["photo"])
    async def handle_photo(message):

        await bot.reply_to(
            message,
            (
                "I have received your photo. "
                "Image analysis will be available shortly."
            ),
        )


    # --------------------------------------------------
    # DOCUMENT
    # --------------------------------------------------

    @bot.message_handler(content_types=["document"])
    async def handle_document(message):

        filename = (
            message.document.file_name
            if message.document
            else "document"
        )

        await bot.reply_to(
            message,
            f"I have received your document: {filename}",
        )


    # --------------------------------------------------
    # AUDIO / VOICE
    # --------------------------------------------------

    @bot.message_handler(
        content_types=["audio", "voice"]
    )
    async def handle_audio(message):

        await bot.reply_to(
            message,
            "I have received your audio message.",
        )


    # --------------------------------------------------
    # VIDEO
    # --------------------------------------------------

    @bot.message_handler(content_types=["video"])
    async def handle_video(message):

        await bot.reply_to(
            message,
            "I have received your video.",
        )


    # --------------------------------------------------
    # STICKERS
    # --------------------------------------------------

    @bot.message_handler(content_types=["sticker"])
    async def handle_sticker(message):

        await bot.reply_to(
            message,
            "Nice sticker 😊",
        )


def split_telegram_message(
    text: str,
    max_length: int = 4000,
) -> list[str]:
    """
    Split long AI responses into Telegram-safe chunks.
    """

    if not text:
        return [""]

    if len(text) <= max_length:
        return [text]

    chunks = []

    while text:

        if len(text) <= max_length:

            chunks.append(text)

            break

        split_position = text.rfind(
            "\n",
            0,
            max_length,
        )

        if split_position == -1:

            split_position = text.rfind(
                " ",
                0,
                max_length,
            )

        if split_position == -1:
            split_position = max_length

        chunk = text[:split_position].strip()

        if chunk:
            chunks.append(chunk)

        text = text[split_position:].strip()

    return chunks




async def keep_typing(bot, chat_id: int, stop_event: asyncio.Event):
    """
    Keep showing 'typing...' in Telegram until stop_event is set.
    """

    while not stop_event.is_set():

        try:
            await bot.send_chat_action(
                chat_id=chat_id,
                action="typing",
            )

        except Exception:
            logger.exception(
                "Failed to send Telegram typing action"
            )

        try:
            # Telegram typing lasts about 5 seconds.
            # Refresh it every 4 seconds.
            await asyncio.wait_for(
                stop_event.wait(),
                timeout=2,
            )

        except asyncio.TimeoutError:
            pass