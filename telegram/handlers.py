# telegram/handlers.py

import logging

from telebot.async_telebot import AsyncTeleBot

from authentication.telegram_auth import get_authenticated_user, generate_otp, verify_otp, redis_client, create_session, \
    verify_phone_number
from memory.memory import AgentState
from telegram.telegram_ai_service import process_ai_message

logger = logging.getLogger(__name__)
import asyncio
from telebot import types


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
        telegram_id = message.from_user.id
        user_message = (message.text or "").strip()

        if not user_message:
            return

        user_id = (
            message.from_user.id
            if message.from_user
            else chat_id
        )

        # is user authenticated
        auth_user = await get_authenticated_user(telegram_id)
        if not auth_user:
            print("AUTHENTICATED USER:", auth_user)



            # ==========================================
            # CHECK IF USER IS SUBMITTING AN OTP
            # ==========================================

            otp_attempts = await redis_client.exists(
                f"otp_attempts:{telegram_id}"
            )

            #verify OPTP and authenticate
            if otp_attempts:

                if user_message.isascii() and user_message.isdigit() and len(user_message) == 6:

                    otp_valid = await verify_otp(telegram_id,user_message)

                    if otp_valid:
                        #Authenticate user
                        await create_session(telegram_id, create_session)
                        # Remove Secure Login button
                        remove_keyboard = types.ReplyKeyboardRemove()

                        await bot.send_message(
                            chat_id,
                            "✅ OTP verified. Type your question and send it to me.",
                            reply_markup=remove_keyboard
                        )
                        return

                    else:
                        await bot.send_message(
                            chat_id,
                            "❌ Invalid or expired OTP. Please try again."
                        )
                        return

            # Show login button only when no authentication
            # and no OTP verification is pending
            await share_phone_number(message)
            return
        else:
            #stop typing

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
                    chat_id=chat_id
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

                # ==============================================
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

    async def share_phone_number(message):

        telegram_id = message.from_user.id
        chat_id = message.chat.id

        # Check authentication status
        auth_user = await get_authenticated_user(telegram_id)

        # If authenticated, do not display login button
        if auth_user:
            print(f"User {telegram_id} already authenticated")
            return

        # If OTP is pending, do not display login button again
        otp_pending = await redis_client.exists(
            f"otp_attempts:{telegram_id}"
        )

        if otp_pending:
            print(f"OTP verification pending for {telegram_id}")
            return

        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            row_width=1
        )

        button = types.KeyboardButton(
            text="🔐 Secure Login",
            request_contact=True
        )

        keyboard.add(button)

        await bot.send_message(
            chat_id=chat_id,
            text="Please click login button",
            reply_markup=keyboard
        )

    @bot.message_handler(content_types=["contact"])
    async def receive_contact(message):

        contact = message.contact

        telegram_id = message.from_user.id
        contact_user_id = contact.user_id

        # Ensure the contact belongs to the sender
        if contact_user_id != telegram_id:
            await bot.send_message(
                message.chat.id,
                "Please click the button bellow to login."
            )
            return

        phone_number = contact.phone_number

        # Normalize Kenyan phone numbers
        cleaned = phone_number.replace(" ", "").replace("-", "")

        if cleaned.startswith("0") and len(cleaned) == 10:
            phone_number = "+254" + cleaned[1:]
        elif cleaned.startswith("254"):
            phone_number = "+" + cleaned
        else:
            phone_number = cleaned

        print(f"phone_number: {phone_number}")
        print("Phone number received successfully")

        # validate the phone number if registered in our system
        number_valid = await  verify_phone_number(phone_number)

        if not number_valid:

            await bot.send_message(
               message.chat.id,
               "Phone number not registered. Please contact our facility through 07******13.",
               #reply_markup=types.ReplyKeyboardRemove()
            )
            return

        # Store phone temporarily in Redis


        # Generate OTP using your existing function
        otp = await generate_otp(telegram_id)

        # Send OTP via your SMS provider
        #await send_sms(phone_number, otp)


        await bot.send_message(
            message.chat.id,
            "A verification code has been sent to your phone. "
            f"Please enter the 6-digit OTP :{otp}."
        )



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