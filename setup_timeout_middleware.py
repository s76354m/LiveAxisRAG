import os
import sys

def create_timeout_middleware():
    try:
        # Create the timeout middleware file
        timeout_content = '''from fastapi import Request, Response, HTTPException
from typing import Callable, Dict, Optional, Union
import asyncio
import logging
import time
from datetime import datetime
from functools import partial

logger = logging.getLogger(__name__)

class TimeoutMiddleware:
    def __init__(
        self,
        timeout: Union[int, Dict[str, int]] = 30,  # Default 30 seconds
        default_timeout: int = 30,
        grace_period: int = 1,  # Grace period for cleanup
        exclude_paths: set = {"/health", "/metrics"},
        error_response: Optional[Dict] = None,
        track_stats: bool = True
    ):
        self.timeout = timeout if isinstance(timeout, dict) else {"default": timeout}
        self.default_timeout = default_timeout
        self.grace_period = grace_period
        self.exclude_paths = exclude_paths
        self.error_response = error_response or {
            "error": "Request timeout",
            "detail": "The request exceeded the allowed time limit"
        }
        self.track_stats = track_stats
        
        # Initialize statistics
        self.stats = {
            "total_requests": 0,
            "timeouts": 0,
            "close_calls": 0,  # Requests that used >80% of their time
            "average_time": 0,
            "max_time": 0,
            "request_times": []
        }

    def _get_timeout(self, path: str) -> int:
        """Get timeout value for specific path"""
        for route_prefix, timeout_value in self.timeout.items():
            if path.startswith(route_prefix):
                return timeout_value
        return self.timeout.get("default", self.default_timeout)

    def _update_stats(self, duration: float, timed_out: bool):
        """Update request statistics"""
        if not self.track_stats:
            return
            
        self.stats["total_requests"] += 1
        if timed_out:
            self.stats["timeouts"] += 1
        
        self.stats["request_times"].append(duration)
        self.stats["max_time"] = max(self.stats["max_time"], duration)
        
        # Keep only last 1000 request times
        if len(self.stats["request_times"]) > 1000:
            self.stats["request_times"] = self.stats["request_times"][-1000:]
            
        self.stats["average_time"] = sum(self.stats["request_times"]) / len(self.stats["request_times"])
        
        # Check if this was a close call (>80% of timeout used)
        timeout_threshold = self._get_timeout("default") * 0.8
        if duration > timeout_threshold:
            self.stats["close_calls"] += 1

    async def _handle_timeout(
        self,
        request: Request,
        call_next: Callable,
        timeout_seconds: int
    ) -> Response:
        """Handle request with timeout"""
        start_time = time.time()
        timed_out = False
        
        try:
            # Create task for the request
            request_task = asyncio.create_task(call_next(request))
            
            # Wait for either the request to complete or timeout
            try:
                response = await asyncio.wait_for(
                    request_task,
                    timeout=timeout_seconds
                )
                return response
                
            except asyncio.TimeoutError:
                timed_out = True
                logger.warning(
                    f"Request timeout: {request.method} {request.url.path} "
                    f"after {timeout_seconds} seconds"
                )
                
                # Try to cancel the task
                request_task.cancel()
                
                # Give it a grace period to cleanup
                try:
                    await asyncio.wait_for(request_task, timeout=self.grace_period)
                except (asyncio.TimeoutError, asyncio.CancelledError):
                    pass
                
                return Response(
                    status_code=504,
                    content=self.error_response,
                    media_type="application/json"
                )
                
        finally:
            duration = time.time() - start_time
            if self.track_stats:
                self._update_stats(duration, timed_out)

    async def __call__(self, request: Request, call_next: Callable):
        # Skip timeout for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Get timeout for this request
        timeout_seconds = self._get_timeout(request.url.path)
        
        # Add timeout information to request state
        request.state.timeout = timeout_seconds
        request.state.timeout_start = time.time()
        
        # Handle request with timeout
        return await self._handle_timeout(request, call_next, timeout_seconds)

    def get_stats(self) -> Dict:
        """Get timeout statistics"""
        if not self.track_stats:
            return {"stats_enabled": False}
            
        return {
            "total_requests": self.stats["total_requests"],
            "timeouts": self.stats["timeouts"],
            "close_calls": self.stats["close_calls"],
            "average_time": round(self.stats["average_time"], 3),
            "max_time": round(self.stats["max_time"], 3),
            "timeout_rate": round(
                (self.stats["timeouts"] / self.stats["total_requests"] * 100)
                if self.stats["total_requests"] > 0 else 0,
                2
            )
        }

    def reset_stats(self):
        """Reset timeout statistics"""
        self.stats = {
            "total_requests": 0,
            "timeouts": 0,
            "close_calls": 0,
            "average_time": 0,
            "max_time": 0,
            "request_times": []
        }

class RequestTimeout:
    """Context manager to check remaining timeout in route handlers"""
    
    def __init__(self, request: Request):
        self.request = request
        self.start_time = time.time()
        self.timeout = getattr(request.state, "timeout", 30)
        self.timeout_start = getattr(request.state, "timeout_start", self.start_time)

    @property
    def remaining(self) -> float:
        """Get remaining timeout in seconds"""
        elapsed = time.time() - self.timeout_start
        return max(0, self.timeout - elapsed)

    def check(self):
        """Check if request has timed out"""
        if self.remaining <= 0:
            raise HTTPException(
                status_code=504,
                detail="Request timeout during processing"
            )

# Helper function to get timeout context in routes
def get_timeout(request: Request) -> RequestTimeout:
    return RequestTimeout(request)
'''
        
        with open("src/api/middleware/timeout_middleware.py", "w") as f:
            f.write(timeout_content)

        # Update __init__.py to export all middleware
        init_content = '''from .error_handler import error_handler
from .request_validator import RequestValidationMiddleware
from .rate_limiter import RateLimiter
from .auth_middleware import AuthMiddleware
from .logging_middleware import LoggingMiddleware
from .cors_middleware import CustomCORSMiddleware, CORSConfig
from .cache_middleware import CacheMiddleware
from .compression_middleware import CompressionMiddleware
from .metrics_middleware import MetricsMiddleware
from .security_middleware import SecurityMiddleware
from .db_middleware import DatabaseMiddleware, get_db
from .timeout_middleware import TimeoutMiddleware, get_timeout

__all__ = [
    "error_handler",
    "RequestValidationMiddleware",
    "RateLimiter",
    "AuthMiddleware",
    "LoggingMiddleware",
    "CustomCORSMiddleware",
    "CORSConfig",
    "CacheMiddleware",
    "CompressionMiddleware",
    "MetricsMiddleware",
    "SecurityMiddleware",
    "DatabaseMiddleware",
    "get_db",
    "TimeoutMiddleware",
    "get_timeout"
]
'''
        
        with open("src/api/middleware/__init__.py", "w") as f:
            f.write(init_content)
            
        print("✅ Timeout middleware has been created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating files: {str(e)}")
        return False

if __name__ == "__main__":
    response = input("Do you want to create the timeout middleware? (y/n): ")
    if response.lower() == 'y':
        create_timeout_middleware()
    else:
        print("Operation cancelled.")