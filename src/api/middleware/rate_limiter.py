from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Tuple
import time
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_limit: int = 100,
        expire_time: int = 60
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.expire_time = expire_time
        self.requests: Dict[str, list] = {}
        self._cleanup_task = None

    async def init(self):
        """Initialize the cleanup task"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_old_requests())

    async def _cleanup_old_requests(self):
        """Periodically clean up old request records"""
        while True:
            current_time = time.time()
            for ip in list(self.requests.keys()):
                self.requests[ip] = [
                    req_time for req_time in self.requests[ip]
                    if current_time - req_time < self.expire_time
                ]
                if not self.requests[ip]:
                    del self.requests[ip]
            await asyncio.sleep(10)  # Cleanup every 10 seconds

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request headers or direct IP"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host

    async def __call__(self, request: Request, call_next):
        await self.init()
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        current_time = time.time()

        # Initialize request list for new IPs
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Clean old requests for this IP
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.expire_time
        ]

        # Check burst limit
        if len(self.requests[client_ip]) >= self.burst_limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": "Rate limit exceeded. Please try again later.",
                    "retry_after": self.expire_time
                }
            )

        # Check rate limit
        request_count = len(self.requests[client_ip])
        if request_count >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": "Rate limit exceeded. Please try again later.",
                    "retry_after": self.expire_time
                }
            )

        # Add current request timestamp
        self.requests[client_ip].append(current_time)

        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.requests[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(current_time + self.expire_time)
        )

        return response
