from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine
from app.routers import all_routers
from app.settings import settings

from telegram.telegram_bot import bot
from telegram.handlers import register_telegram_handlers


# ======================================================
# LOGGING
# ======================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


# ======================================================
# REGISTER TELEGRAM MESSAGE HANDLERS
# ======================================================

register_telegram_handlers(bot)


# ======================================================
# FASTAPI LIFESPAN
# ======================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # --------------------------------------------------
    # APPLICATION STARTUP
    # --------------------------------------------------

    logger.info(
        "Starting %s version %s",
        settings.app_name,
        settings.app_version,
    )

    try:

        logger.info(
            "Registering Telegram webhook: %s",
            settings.telegram_webhook_url,
        )

        # --------------------------------------------------
        # Register webhook with Telegram
        # --------------------------------------------------

        webhook_result = await bot.set_webhook(
            url=settings.telegram_webhook_url,
            secret_token=settings.telegram_webhook_secret,
            allowed_updates=[
                "message"
            ],
            drop_pending_updates=False,
        )

        logger.info(
            "Telegram webhook registration result: %s",
            webhook_result,
        )

        # --------------------------------------------------
        # Verify webhook
        # --------------------------------------------------

        webhook_info = await bot.get_webhook_info()

        logger.info(
            "Telegram webhook URL: %s",
            webhook_info.url,
        )

        logger.info(
            "Telegram pending updates: %s",
            webhook_info.pending_update_count,
        )

        if webhook_info.last_error_message:

            logger.warning(
                "Telegram webhook last error: %s",
                webhook_info.last_error_message,
            )

        else:

            logger.info(
                "Telegram webhook registered successfully"
            )

    except Exception:

        logger.exception(
            "Failed to register Telegram webhook"
        )

    # --------------------------------------------------
    # APPLICATION RUNNING
    # --------------------------------------------------

    yield

    # --------------------------------------------------
    # APPLICATION SHUTDOWN
    # --------------------------------------------------

    logger.info(
        "Shutting down %s",
        settings.app_name,
    )

    await bot.close_session()


# ======================================================
# FASTAPI APPLICATION
# ======================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description=(
        "REST API for the Family Planning MySQL database."
    ),

    # VERY IMPORTANT
    lifespan=lifespan,
)


# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=(
        settings.cors_origin_list != ["*"]
    ),
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================================
# ROUTERS
# ======================================================

for router in all_routers:

    app.include_router(
        router,
        prefix=settings.api_prefix,
    )


# ======================================================
# ROOT
# ======================================================

@app.get(
    "/",
    tags=["system"],
)
async def root():

    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "api_prefix": settings.api_prefix,
    }


# ======================================================
# HEALTH CHECK
# ======================================================

@app.get(
    "/health",
    tags=["system"],
)
def health():

    with engine.connect() as conn:

        conn.execute(
            text("SELECT 1")
        )

    return {
        "status": "ok",
        "database": settings.mysql_database,
    }