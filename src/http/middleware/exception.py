import logging
import traceback

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except (Exception,):
            self._log_exception()
            return Response("Internal server error", status_code=500)

    @staticmethod
    def _log_exception():
        logger.error(traceback.format_exc())
