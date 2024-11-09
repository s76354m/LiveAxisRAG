import os
import sys

def create_metrics_middleware():
    try:
        # Create the metrics middleware file
        metrics_content = '''from fastapi import Request, Response
from typing import Callable, Dict, List, Optional
import time
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest

logger = logging.getLogger(__name__)

class MetricsMiddleware:
    def __init__(
        self,
        app_name: str = "swarmrag",
        exclude_paths: set = {"/metrics", "/health"},
        bucket_size: int = 10,  # Number of time buckets for latency tracking
    ):
        self.app_name = app_name
        self.exclude_paths = exclude_paths
        self.bucket_size = bucket_size
        
        # Initialize Prometheus metrics
        self.request_count = Counter(
            f'{app_name}_http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status']
        )
        
        self.request_latency = Histogram(
            f'{app_name}_http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            buckets=self._generate_buckets()
        )
        
        self.requests_in_progress = Gauge(
            f'{app_name}_http_requests_in_progress',
            'Number of HTTP requests in progress',
            ['method']
        )
        
        self.response_size = Histogram(
            f'{app_name}_http_response_size_bytes',
            'HTTP response size in bytes',
            ['method', 'endpoint'],
            buckets=[100, 1000, 10000, 100000, 1000000]
        )
        
        # Additional internal metrics
        self.errors = defaultdict(int)
        self.status_codes = defaultdict(int)
        self.endpoint_usage = defaultdict(int)
        self.recent_requests: List[Dict] = []
        self.max_recent_requests = 1000

    def _generate_buckets(self) -> List[float]:
        """Generate histogram buckets for latency tracking"""
        return [0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]

    async def __call__(self, request: Request, call_next: Callable):
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Special handling for metrics endpoint
        if request.url.path == "/metrics":
            return Response(
                content=generate_latest(),
                media_type="text/plain"
            )

        # Track request start
        start_time = time.time()
        method = request.method
        endpoint = request.url.path
        
        # Increment in-progress requests
        self.requests_in_progress.labels(method=method).inc()

        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Update metrics
            status = str(response.status_code)
            self.request_count.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()
            
            self.request_latency.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            # Track response size
            response_body = await response.body()
            self.response_size.labels(
                method=method,
                endpoint=endpoint
            ).observe(len(response_body))
            
            # Update internal metrics
            self.status_codes[status] += 1
            self.endpoint_usage[endpoint] += 1
            
            # Store recent request data
            self.recent_requests.append({
                "timestamp": datetime.utcnow().isoformat(),
                "method": method,
                "endpoint": endpoint,
                "status": status,
                "duration": duration,
                "size": len(response_body)
            })
            
            # Maintain recent requests limit
            if len(self.recent_requests) > self.max_recent_requests:
                self.recent_requests.pop(0)
            
            return response

        except Exception as e:
            # Track errors
            error_type = type(e).__name__
            self.errors[error_type] += 1
            logger.error(f"Request error: {str(e)}")
            raise

        finally:
            # Decrement in-progress requests
            self.requests_in_progress.labels(method=method).dec()

    def get_metrics_summary(self) -> Dict:
        """Get a summary of current metrics"""
        return {
            "total_requests": sum(self.status_codes.values()),
            "status_codes": dict(self.status_codes),
            "errors": dict(self.errors),
            "endpoint_usage": dict(self.endpoint_usage),
            "requests_in_progress": {
                method: self.requests_in_progress.labels(method=method)._value
                for method in ["GET", "POST", "PUT", "DELETE"]
            },
            "recent_requests": self.recent_requests[-10:]  # Last 10 requests
        }

    def reset_metrics(self):
        """Reset internal metrics (not Prometheus metrics)"""
        self.errors.clear()
        self.status_codes.clear()
        self.endpoint_usage.clear()
        self.recent_requests.clear()
'''
        
        with open("src/api/middleware/metrics_middleware.py", "w") as f:
            f.write(metrics_content)

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
    "MetricsMiddleware"
]
'''
        
        with open("src/api/middleware/__init__.py", "w") as f:
            f.write(init_content)
            
        # Create requirements update
        requirements_content = '''
prometheus-client>=0.16.0
'''
        with open("requirements.txt", "a") as f:
            f.write(requirements_content)
            
        print("✅ Metrics middleware has been created successfully!")
        print("✅ Requirements.txt has been updated with prometheus-client dependency")
        return True
    except Exception as e:
        print(f"❌ Error creating files: {str(e)}")
        return False

if __name__ == "__main__":
    response = input("Do you want to create the metrics middleware? (y/n): ")
    if response.lower() == 'y':
        create_metrics_middleware()
    else:
        print("Operation cancelled.") 