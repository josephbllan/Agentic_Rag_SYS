"""
FastAPI Application with MVC Architecture
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.routes import api_router
from api.middleware import (
    setup_logging_middleware,
    setup_error_handlers,
    setup_rate_limiter,
    setup_request_id_middleware,
)
from config.settings import API_CONFIG, APP_VERSION

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("RAG Image Search API Starting...")
    logger.info("Version: %s", APP_VERSION)
    logger.info("=" * 60)
    yield
    logger.info("RAG Image Search API shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="RAG Image Search API",
        description="Multi-modal image search system",
        version=APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=API_CONFIG.get("cors_origins", ["*"]),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_request_id_middleware(app)
    setup_logging_middleware(app)
    setup_error_handlers(app)
    setup_rate_limiter(app)

    app.include_router(api_router, prefix="/api")

    logger.info("FastAPI application created successfully")
    return app


app = create_app()
