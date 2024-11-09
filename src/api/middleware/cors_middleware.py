from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class CustomCORSMiddleware:
    def __init__(
        self,
        allow_origins: List[str] = ["*"],
        allow_methods: List[str] = ["*"],
        allow_headers: List[str] = ["*"],
        allow_credentials: bool = True,
        max_age: int = 600,
        expose_headers: List[str] = ["X-Request-ID", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
        security_headers: bool = True
    ):
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.allow_credentials = allow_credentials
        self.max_age = max_age
        self.expose_headers = expose_headers
        self.security_headers = security_headers

    def setup_cors(self, app: FastAPI) -> None:
        """Configure CORS for the FastAPI application"""
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.allow_origins,
            allow_credentials=self.allow_credentials,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
            max_age=self.max_age,
            expose_headers=self.expose_headers
        )

        @app.middleware("http")
        async def add_security_headers(request: Request, call_next):
            response = await call_next(request)
            
            if self.security_headers:
                # Add security headers
                response.headers["X-Content-Type-Options"] = "nosniff"
                response.headers["X-Frame-Options"] = "DENY"
                response.headers["X-XSS-Protection"] = "1; mode=block"
                response.headers["Strict-Transport-Security"] = f"max-age={self.max_age}; includeSubDomains"
                response.headers["Content-Security-Policy"] = self._get_csp_policy()
                response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
                response.headers["Permissions-Policy"] = self._get_permissions_policy()

            return response

    def _get_csp_policy(self) -> str:
        """Generate Content Security Policy"""
        return "; ".join([
            "default-src 'self'",
            "img-src 'self' data: https:",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline'",
            "font-src 'self' data:",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ])

    def _get_permissions_policy(self) -> str:
        """Generate Permissions Policy"""
        return ", ".join([
            "accelerometer=()",
            "camera=()",
            "geolocation=()",
            "gyroscope=()",
            "magnetometer=()",
            "microphone=()",
            "payment=()",
            "usb=()"
        ])

class CORSConfig:
    """CORS Configuration Settings"""
    
    def __init__(
        self,
        environment: str = "development",
        allowed_origins: Optional[List[str]] = None
    ):
        self.environment = environment
        self._allowed_origins = allowed_origins or self._get_default_origins()

    def _get_default_origins(self) -> List[str]:
        """Get default origins based on environment"""
        if self.environment == "development":
            return [
                "http://localhost",
                "http://localhost:3000",
                "http://127.0.0.1",
                "http://127.0.0.1:3000"
            ]
        elif self.environment == "production":
            return [
                "https://swarmrag.com",
                "https://api.swarmrag.com",
                "https://admin.swarmrag.com"
            ]
        return ["*"]

    @property
    def settings(self) -> dict:
        """Get CORS settings"""
        return {
            "allow_origins": self._allowed_origins,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": [
                "Authorization",
                "Content-Type",
                "X-Request-ID",
                "X-API-Key"
            ],
            "allow_credentials": True,
            "max_age": 600,
            "expose_headers": [
                "X-Request-ID",
                "X-RateLimit-Limit",
                "X-RateLimit-Remaining"
            ],
            "security_headers": True
        }
