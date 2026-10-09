import os
import secrets
import hashlib
import hmac
from telebot import types

from dotenv import load_dotenv
from redis.asyncio import  Redis

load_dotenv()

redis_client = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)

OTP_EXPIRY = int(os.getenv("OTP_EXPIRY", 300))
SESSION_EXPIRY = int(os.getenv("SESSION_EXPIRY", 86400))

OTP_SECRET = os.environ["OTP_HASH_SECRET"]


def hash_opt(telegram_id, opt):
    message = f"{telegram_id}:{opt}".encode("utf-8")
    return hmac.new(OTP_SECRET.encode("utf-8"), message, hashlib.sha256).hexdigest()


async def generate_otp(telegram_id):

    otp = f"{secrets.randbelow(1000000):06d}"

    # Hash OTP synchronously
    hashed_otp =  hash_opt(telegram_id, otp)


    # Save OTP hash in Redis
    await redis_client.set(
        f"otp:{telegram_id}",
        hashed_otp,
        ex=OTP_EXPIRY
    )

    # Initialize OTP attempts
    await redis_client.set(
        f"otp_attempts:{telegram_id}",
        0,
        ex=OTP_EXPIRY
    )

    print(f"OTP stored successfully in Redis {otp}")

    return otp

async def verify_otp(telegram_id, otp):

    key = f"otp:{telegram_id}"
    attempts_key = f"otp_attempts:{telegram_id}"
    attempts = int(await redis_client.get(attempts_key) or 0 )

    if attempts >= 5:
        return False

    stored_hash = await redis_client.get(key)

    if not stored_hash:
        return False

    entered_hash = hash_opt(telegram_id, otp)

    if not hmac.compare_digest(stored_hash, entered_hash):
        redis_client.incr(attempts_key)
        return False

    await redis_client.delete(key, attempts_key)

    return True

async  def create_session(telegram_id, user_id):

    await redis_client.set(
        f"auth:telegram:{telegram_id}",
        str(user_id),
        ex=OTP_EXPIRY
    )

async def get_authenticated_user(telegram_id):

    user_id = await redis_client.get(
        f"auth:telegram:{telegram_id}"
    )

    if user_id:
        print(
            f"User authenticated successfully | "
            f"Telegram ID: {telegram_id} | "
            f"User ID: {user_id}"
        )

        return True

    else:
        print(
            f"User not authenticated | "
            f"Telegram ID: {telegram_id}"
        )

        return False

async def verify_phone_number(phone_number):
    #retrieve phone numbers from the db
    db_numbers = ['+254717450644', '+254780698944']

    for number in db_numbers:
        if number == phone_number:
            return True
        else:
            return False

    return False



async def logout(telegram_id):
    await redis_client.delete(
        f"auth:telegram:{telegram_id}"
    )




