import logging
from contextlib import asynccontextmanager

from app.api.v1.core import router as core_router
from app.config import settings
from app.database import sessionmanager
from fastapi import FastAPI


def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(core_router, prefix="/api/v1")

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format=settings.log_format,
        datefmt=settings.log_date_format,
        filename=settings.log_path,
        filemode="a",
    )

    sessionmanager.init(settings.postgres_url)
    logging.info("Database session manager initialized")

    yield
    if sessionmanager.engine:
        await sessionmanager.close()
        logging.info("Database session manager closed")
