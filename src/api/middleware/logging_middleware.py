import logging
import time
import json
from typing import Callable, Dict, Any
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import uuid
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(
        self,
        app_name: str = "SwarmRAG",
        log_request_body: bool = True,
        log_response_body: bool = True,
        sensitive_fields: set = {"password", "token", "secret", "authorization"},
        max_body_length: int = 1000
    ):
        self.app_name = app_name
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.sensitive_fields = sensitive_fields
        self.max_body_length = max_body_length

    def _mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive information in logs"""
        if not isinstance(data, dict):
            return data

        masked_data = data.copy()
        for key in data:
            if any(sensitive in key.lower() for sensitive in self.sensitive_fields):
                masked_data[key] = "********"
            elif isinstance(data[key], dict):
                masked_data[key] = self._mask_sensitive_data(data[key])
        return masked_data

    async def _get_request_body(self, request: Request) -> str:
        """Safely get and format request body"""
        try:
            body = await request.body()
            if not body:
                return ""
            
            body_str = body.decode()
            if len(body_str) > self.max_body_length:
                return f"{body_str[:self.max_body_length]}... (truncated)"
            
            try:
                body_json = json.loads(body_str)
                return json.dumps(self._mask_sensitive_data(body_json))
            except json.JSONDecodeError:
                return body_str
        except Exception as e:
            logger.warning(f"Error reading request body: {str(e)}")
            return ""

    def _format_log_message(
        self,
        request: Request,
        response: Response,
        request_body: str,
        response_body: str,
        duration: float,
        request_id: str
    ) -> Dict[str, Any]:
        """Format log message with request and response details"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "app_name": self.app_name,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent", ""),
            "request_body": request_body if self.log_request_body else "***",
            "response_status": response.status_code,
            "response_body": response_body if self.log_response_body else "***",
            "duration_ms": round(duration * 1000, 2),
            "user_id": getattr(request.state, "user", {}).get("id", None)
        }

    async def __call__(self, request: Request, call_next: Callable):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        # Get request body
        request_body = await self._get_request_body(request) if self.log_request_body else ""

        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time

            # Get response body for logging
            response_body = ""
            if self.log_response_body and isinstance(response, JSONResponse):
                response_body = json.dumps(self._mask_sensitive_data(response.body.decode()))

            # Format and log the message
            log_data = self._format_log_message(
                request=request,
                response=response,
                request_body=request_body,
                response_body=response_body,
                duration=duration,
                request_id=request_id
            )

            # Log based on response status
            if response.status_code >= 500:
                logger.error(json.dumps(log_data))
            elif response.status_code >= 400:
                logger.warning(json.dumps(log_data))
            else:
                logger.info(json.dumps(log_data))

            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
                "app_name": self.app_name,
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "duration_ms": round(duration * 1000, 2)
            }))
            raise
