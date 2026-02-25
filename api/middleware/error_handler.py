"""
Error Handler Middleware
Global error handling. Hides internal details in production.
"""
import logging
from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.settings import DEBUG

logger = logging.getLogger(__name__)


def _request_id(request: Request) -> str:
    """Extracts the request ID from the request state, falling back
    to 'unknown' if no ID has been assigned.
    """
    return getattr(request.state, "request_id", "unknown")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles request validation errors by returning a 422 JSON response
    with error details in debug mode or a generic message in production.
    """
    rid = _request_id(request)
    logger.warning(f"[{rid}] Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors() if DEBUG else "Check request payload",
                "request_id": rid,
            },
        },
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles HTTP exceptions by returning a standardized JSON error
    response containing the status code and detail message.
    """
    rid = _request_id(request)
    logger.warning(f"[{rid}] HTTP exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "status_code": exc.status_code,
                "request_id": rid,
            },
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Catches all unhandled exceptions and returns a 500 JSON response,
    exposing the error message only when debug mode is enabled.
    """
    rid = _request_id(request)
    logger.error(f"[{rid}] Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc) if DEBUG else "An internal error occurred",
                "request_id": rid,
            },
        },
    )


def setup_error_handlers(app: FastAPI):
    """Registers all global exception handlers on the FastAPI application
    for validation errors, HTTP exceptions, and unhandled exceptions.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    logger.info("Error handlers configured (debug=%s)", DEBUG)
