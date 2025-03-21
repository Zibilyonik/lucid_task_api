"""
Custom middleware components.

This module defines middleware classes for request processing,
including request size limitation for security.
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class RequestSizeLimiter(BaseHTTPMiddleware):
    """
    Middleware to limit request size

    Attributes:
        max_size: Maximum request size in bytes
    """

    def __init__(self, app, max_size: int = 1_048_576):  # 1MB
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        """
        Check and limit request size

        Args:
            request: HTTP request
            call_next: Next middleware or endpoint

        Returns:
            Response: HTTP response

        Raises:
            HTTPException: If request exceeds size limit
        """
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            raise HTTPException(status_code=413, detail="Request too large")
        return await call_next(request)
