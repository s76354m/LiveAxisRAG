import os
import sys

def create_cache_middleware():
    try:
        # Create the cache middleware file
        cache_content = '''from fastapi import Request, Response
from typing import Optional, Dict, Any, Callable
import hashlib
import json
import time
import asyncio
from datetime import datetime
import logging
from cachetools import TTLCache, LRUCache

logger = logging.getLogger(__name__)

class CacheMiddleware:
    def __init__(
        self,
        ttl: int = 300,  # 5 minutes default TTL
        max_size: int = 1000,  # Maximum number of cached items
        ignore_paths: set = {"/health", "/metrics"},
        cache_by_auth: bool = True,
        cache_by_query: bool = True
    ):
        self.cache = TTLCache(maxsize=max_size, ttl=ttl)
        self.metadata_cache = LRUCache(maxsize=max_size)
        self.ignore_paths = ignore_paths
        self.cache_by_auth = cache_by_auth
        self.cache_by_query = cache_by_query
        self._cleanup_task = None

    async def init(self):
        """Initialize the cleanup task"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_expired())

    async def _cleanup_expired(self):
        """Periodically clean up expired cache entries"""
        while True:
            try:
                current_time = time.time()
                # Clean up TTLCache (it's done automatically, but we'll log it)
                expired_count = len([k for k, v in self.cache.items() 
                                  if v.get("expire_time", 0) < current_time])
                if expired_count > 0:
                    logger.info(f"Cleaned up {expired_count} expired cache entries")
                
                # Clean up metadata
                expired_metadata = [k for k, v in self.metadata_cache.items() 
                                 if v.get("last_accessed", 0) < current_time - 3600]
                for key in expired_metadata:
                    self.metadata_cache.pop(key, None)
                
            except Exception as e:
                logger.error(f"Error during cache cleanup: {str(e)}")
            
            await asyncio.sleep(60)  # Run cleanup every minute

    def _generate_cache_key(self, request: Request) -> str:
        """Generate a unique cache key based on request attributes"""
        key_parts = [request.method, request.url.path]
        
        if self.cache_by_query:
            key_parts.append(str(request.query_params))
        
        if self.cache_by_auth and hasattr(request.state, "user"):
            key_parts.append(str(request.state.user.get("id")))
        
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _should_cache(self, request: Request, response: Response) -> bool:
        """Determine if the response should be cached"""
        return (
            request.method in ["GET", "HEAD"] and
            response.status_code == 200 and
            request.url.path not in self.ignore_paths
        )

    def _update_metadata(self, cache_key: str, response: Response):
        """Update cache metadata"""
        self.metadata_cache[cache_key] = {
            "last_accessed": time.time(),
            "hit_count": self.metadata_cache.get(cache_key, {}).get("hit_count", 0) + 1,
            "size": len(response.body) if hasattr(response, "body") else 0
        }

    async def __call__(self, request: Request, call_next: Callable):
        await self.init()
        
        # Skip caching for non-GET methods or ignored paths
        if request.method not in ["GET", "HEAD"] or request.url.path in self.ignore_paths:
            return await call_next(request)

        cache_key = self._generate_cache_key(request)

        # Try to get from cache
        cached_response = self.cache.get(cache_key)
        if cached_response:
            self._update_metadata(cache_key, cached_response)
            response = Response(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers=cached_response["headers"],
                media_type=cached_response["media_type"]
            )
            response.headers["X-Cache"] = "HIT"
            return response

        # Get fresh response
        response = await call_next(request)

        # Cache if appropriate
        if self._should_cache(request, response):
            try:
                response_body = await response.body()
                self.cache[cache_key] = {
                    "content": response_body,
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "media_type": response.media_type,
                    "expire_time": time.time() + self.cache.ttl
                }
                self._update_metadata(cache_key, response)
                response.headers["X-Cache"] = "MISS"
            except Exception as e:
                logger.error(f"Error caching response: {str(e)}")

        return response

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_size = sum(meta.get("size", 0) for meta in self.metadata_cache.values())
        total_hits = sum(meta.get("hit_count", 0) for meta in self.metadata_cache.values())
        
        return {
            "cache_size": len(self.cache),
            "total_memory": total_size,
            "total_hits": total_hits,
            "cache_keys": list(self.cache.keys()),
            "metadata": self.metadata_cache
        }

    def clear_cache(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.metadata_cache.clear()
        logger.info("Cache cleared")
'''
        
        with open("src/api/middleware/cache_middleware.py", "w") as f:
            f.write(cache_content)

        # Update __init__.py to export all middleware
        init_content = '''from .error_handler import error_handler
from .request_validator import RequestValidationMiddleware
from .rate_limiter import RateLimiter
from .auth_middleware import AuthMiddleware
from .logging_middleware import LoggingMiddleware
from .cors_middleware import CustomCORSMiddleware, CORSConfig
from .cache_middleware import CacheMiddleware

__all__ = [
    "error_handler",
    "RequestValidationMiddleware",
    "RateLimiter",
    "AuthMiddleware",
    "LoggingMiddleware",
    "CustomCORSMiddleware",
    "CORSConfig",
    "CacheMiddleware"
]
'''
        
        with open("src/api/middleware/__init__.py", "w") as f:
            f.write(init_content)
            
        # Create requirements update
        requirements_content = '''
cachetools>=5.3.0
'''
        with open("requirements.txt", "a") as f:
            f.write(requirements_content)
            
        print("✅ Cache middleware has been created successfully!")
        print("✅ Requirements.txt has been updated with cachetools dependency")
        return True
    except Exception as e:
        print(f"❌ Error creating files: {str(e)}")
        return False

if __name__ == "__main__":
    response = input("Do you want to create the cache middleware? (y/n): ")
    if response.lower() == 'y':
        create_cache_middleware()
    else:
        print("Operation cancelled.") 