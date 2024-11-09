import os
import sys

def create_auth_middleware():
    try:
        # Create the auth middleware file
        auth_content = '''from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional, Dict
import jwt
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware:
    def __init__(
        self,
        secret_key: str,
        exclude_paths: set = {"/docs", "/redoc", "/openapi.json", "/health"},
        algorithm: str = "HS256"
    ):
        self.secret_key = secret_key
        self.exclude_paths = exclude_paths
        self.algorithm = algorithm
        self.security = HTTPBearer()
        self.token_cache: Dict[str, dict] = {}

    def _is_excluded_path(self, path: str) -> bool:
        """Check if the path is in excluded paths"""
        return any(path.startswith(excluded) for excluded in self.exclude_paths)

    async def decode_token(self, token: str) -> dict:
        """Decode and validate JWT token"""
        try:
            # Check cache first
            if token in self.token_cache:
                cached_payload = self.token_cache[token]
                if cached_payload.get("exp", 0) > time.time():
                    return cached_payload

            # Decode token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            # Validate expiration
            if payload.get("exp", 0) < time.time():
                raise HTTPException(
                    status_code=401,
                    detail="Token has expired"
                )

            # Cache valid token
            self.token_cache[token] = payload
            return payload

        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

    async def __call__(self, request: Request, call_next):
        # Skip authentication for excluded paths
        if self._is_excluded_path(request.url.path):
            return await call_next(request)

        try:
            # Extract token
            auth: HTTPAuthorizationCredentials = await self.security(request)
            if not auth:
                raise HTTPException(
                    status_code=401,
                    detail="Missing authentication token"
                )

            # Validate token
            payload = await self.decode_token(auth.credentials)

            # Add user info to request state
            request.state.user = payload
            request.state.token = auth.credentials

            # Process request
            response = await call_next(request)

            return response

        except HTTPException as he:
            return JSONResponse(
                status_code=he.status_code,
                content={"error": he.detail}
            )
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error during authentication"}
            )

    async def cleanup_cache(self):
        """Remove expired tokens from cache"""
        current_time = time.time()
        expired_tokens = [
            token for token, payload in self.token_cache.items()
            if payload.get("exp", 0) < current_time
        ]
        for token in expired_tokens:
            del self.token_cache[token]
'''
        
        with open("src/api/middleware/auth_middleware.py", "w") as f:
            f.write(auth_content)

        # Update __init__.py to export all middleware
        init_content = '''from .error_handler import error_handler
from .request_validator import RequestValidationMiddleware
from .rate_limiter import RateLimiter
from .auth_middleware import AuthMiddleware

__all__ = ["error_handler", "RequestValidationMiddleware", "RateLimiter", "AuthMiddleware"]
'''
        
        with open("src/api/middleware/__init__.py", "w") as f:
            f.write(init_content)

        print("✅ Authentication middleware has been created successfully!")
        return True
    except Exception as e:
        print(f"Failed to create authentication middleware: {str(e)}")
        return False 