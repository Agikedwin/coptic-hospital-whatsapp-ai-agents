import os
import telebot
import logging
from dotenv import load_dotenv

from telebot.async_telebot import  AsyncTeleBot


load_dotenv()

TELEGRAM_API=os.getenv("TELEGRAM_API")


logger = logging.getLogger(__name__)

bot = AsyncTeleBot(
    TELEGRAM_API
)

