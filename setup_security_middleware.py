import os
import sys

def create_security_middleware():
    try:
        # Create the security middleware file
        security_content = '''from fastapi import Request, Response, HTTPException
from typing import Callable, Dict, List, Optional, Set
import secrets
import hashlib
import time
import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(
        self,
        secret_key: str,
        csrf_token_length: int = 32,
        csrf_cookie_name: str = "csrf_token",
        csrf_header_name: str = "X-CSRF-Token",
        csrf_safe_methods: Set[str] = {"GET", "HEAD", "OPTIONS"},
        csrf_exclude_paths: Set[str] = {"/api/v1/auth/login", "/api/v1/auth/logout"},
        xss_enable: bool = True,
        xss_content_types: Set[str] = {"text/html", "application/xml"},
        secure_headers: bool = True,
        rate_limit_tokens: int = 100,
        rate_limit_interval: int = 3600
    ):
        self.secret_key = secret_key
        self.csrf_token_length = csrf_token_length
        self.csrf_cookie_name = csrf_cookie_name
        self.csrf_header_name = csrf_header_name
        self.csrf_safe_methods = csrf_safe_methods
        self.csrf_exclude_paths = csrf_exclude_paths
        self.xss_enable = xss_enable
        self.xss_content_types = xss_content_types
        self.secure_headers = secure_headers
        self.rate_limit_tokens = rate_limit_tokens
        self.rate_limit_interval = rate_limit_interval
        
        # Rate limiting storage
        self.rate_limits: Dict[str, Dict] = {}
        
        # CSRF token storage
        self.csrf_tokens: Dict[str, Dict] = {}

    def _generate_csrf_token(self) -> str:
        """Generate a new CSRF token"""
        return secrets.token_urlsafe(self.csrf_token_length)

    def _validate_csrf_token(self, request: Request) -> bool:
        """Validate CSRF token from request"""
        if request.method in self.csrf_safe_methods:
            return True
            
        if request.url.path in self.csrf_exclude_paths:
            return True

        cookie_token = request.cookies.get(self.csrf_cookie_name)
        header_token = request.headers.get(self.csrf_header_name)

        if not cookie_token or not header_token:
            return False

        # Validate token existence and matching
        stored_token = self.csrf_tokens.get(cookie_token)
        if not stored_token:
            return False

        # Check if token has expired
        if stored_token["expires"] < datetime.utcnow():
            del self.csrf_tokens[cookie_token]
            return False

        return secrets.compare_digest(cookie_token, header_token)

    def _clean_html(self, content: str) -> str:
        """Clean potentially malicious HTML content"""
        # Basic XSS cleaning rules
        cleaners = [
            (r'<script[^>]*?>.*?</script>', ''),  # Remove script tags
            (r'on\w+="[^"]*"', ''),  # Remove on* event handlers
            (r'javascript:', ''),  # Remove javascript: protocols
            (r'data:', ''),  # Remove data: protocols
            (r'<iframe.*?</iframe>', ''),  # Remove iframes
            (r'<form.*?</form>', '')  # Remove forms
        ]
        
        cleaned = content
        for pattern, replacement in cleaners:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        return cleaned

    async def _check_rate_limit(self, request: Request) -> bool:
        """Check if request is within rate limits"""
        client_ip = request.client.host
        current_time = time.time()
        
        # Initialize or get client's rate limit info
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = {
                "tokens": self.rate_limit_tokens,
                "last_update": current_time
            }
        
        client = self.rate_limits[client_ip]
        
        # Replenish tokens based on time passed
        time_passed = current_time - client["last_update"]
        tokens_to_add = int(time_passed * (self.rate_limit_tokens / self.rate_limit_interval))
        client["tokens"] = min(self.rate_limit_tokens, client["tokens"] + tokens_to_add)
        client["last_update"] = current_time
        
        # Check if request can be processed
        if client["tokens"] > 0:
            client["tokens"] -= 1
            return True
            
        return False

    def _add_security_headers(self, response: Response):
        """Add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = self._get_csp_policy()
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = self._get_permissions_policy()

    def _get_csp_policy(self) -> str:
        """Get Content Security Policy"""
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
        """Get Permissions Policy"""
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

    async def __call__(self, request: Request, call_next: Callable):
        # Rate limiting check
        if not await self._check_rate_limit(request):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # CSRF validation
        if not self._validate_csrf_token(request):
            raise HTTPException(status_code=403, detail="Invalid CSRF token")

        # Process request
        response = await call_next(request)

        # Add security headers
        if self.secure_headers:
            self._add_security_headers(response)

        # XSS protection for HTML/XML content
        if self.xss_enable and response.headers.get("content-type") in self.xss_content_types:
            content = response.body.decode()
            cleaned_content = self._clean_html(content)
            response = Response(
                content=cleaned_content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        # Set new CSRF token
        if request.method in self.csrf_safe_methods:
            token = self._generate_csrf_token()
            self.csrf_tokens[token] = {
                "expires": datetime.utcnow() + timedelta(hours=24)
            }
            response.set_cookie(
                self.csrf_cookie_name,
                token,
                httponly=True,
                secure=True,
                samesite="strict"
            )

        return response

    def cleanup_expired_tokens(self):
        """Clean up expired CSRF tokens and rate limit data"""
        current_time = datetime.utcnow()
        
        # Clean CSRF tokens
        expired_tokens = [
            token for token, data in self.csrf_tokens.items()
            if data["expires"] < current_time
        ]
        for token in expired_tokens:
            del self.csrf_tokens[token]
        
        # Clean rate limit data
        expired_ips = [
            ip for ip, data in self.rate_limits.items()
            if time.time() - data["last_update"] > self.rate_limit_interval
        ]
        for ip in expired_ips:
            del self.rate_limits[ip]
'''
        
        with open("src/api/middleware/security_middleware.py", "w") as f:
            f.write(security_content)

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
    "SecurityMiddleware"
]
'''
        
        with open("src/api/middleware/__init__.py", "w") as f:
            f.write(init_content)
            
        print("✅ Security middleware has been created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating files: {str(e)}")
        return False

if __name__ == "__main__":
    response = input("Do you want to create the security middleware? (y/n): ")
    if response.lower() == 'y':
        create_security_middleware()
    else:
        print("Operation cancelled.") 