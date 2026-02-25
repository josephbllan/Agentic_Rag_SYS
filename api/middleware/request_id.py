"""
Request-ID middleware.
Attaches a unique X-Request-ID to every request/response for traceability.
"""
import uuid
import logging
from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def setup_request_id_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestIDMiddleware)
    logger.info("Request-ID middleware configured")
