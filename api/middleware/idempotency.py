from typing import Set
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class IdempotencyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.seen: Set[str] = set()

    async def dispatch(self, request: Request, call_next):
        key = request.headers.get("Idempotency-Key")
        if key and key in self.seen:
            return Response(status_code=409, content="Duplicate request")
        if key:
            self.seen.add(key)
        response = await call_next(request)
        return response
