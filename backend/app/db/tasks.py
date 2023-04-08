import logging
from fastapi import FastAPI
from tenacity import (after_log, before_log, retry,
                      stop_after_attempt, wait_fixed)
from sqlalchemy.sql import text
from app.db.session import SessionLocal
from app.db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 1  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def connect_to_db(app: FastAPI) -> None:

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        app.state._db = db
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def prepopulate_db() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")


async def start_db(app: FastAPI) -> None:
    await connect_to_db(app)
    await prepopulate_db()


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
