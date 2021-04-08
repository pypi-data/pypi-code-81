from fastapi import Request
from loguru import logger
import uuid
from starlette.middleware.base import BaseHTTPMiddleware


class HttpMiddleware(BaseHTTPMiddleware):
    @logger.catch(reraise=True)
    async def dispatch(self, request: Request, call_next):
        """
        增加日志记录的trace_id
        """
        request_id = request.headers.get('X-Request-ID')
        if not request_id:
            request_id = uuid.uuid4()
        with logger.contextualize(ID=request_id):
            response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
