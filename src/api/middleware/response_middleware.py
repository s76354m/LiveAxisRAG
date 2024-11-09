from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional, Union, List
import time
import logging
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class APIResponse(BaseModel):
    """Standard API Response Model"""
    success: bool = Field(default=True, description="Indicates if the request was successful")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[Dict[str, Any]] = Field(default=None, description="Error details if any")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Response metadata including timing, version, etc."
    )

class ResponseFormattingMiddleware:
    def __init__(
        self,
        app_version: str = "1.0.0",
        include_timing: bool = True,
        include_request_id: bool = True,
        pretty_json: bool = False,
        exclude_paths: set = {"/health", "/metrics"},
        error_handlers: Optional[Dict] = None,
        track_stats: bool = True
    ):
        self.app_version = app_version
        self.include_timing = include_timing
        self.include_request_id = include_request_id
        self.pretty_json = pretty_json
        self.exclude_paths = exclude_paths
        self.error_handlers = error_handlers or {}
        self.track_stats = track_stats
        
        # Initialize statistics
        self.stats = {
            "total_responses": 0,
            "success_responses": 0,
            "error_responses": 0,
            "response_times": [],
            "status_codes": {},
            "error_types": {}
        }

    def _update_stats(
        self,
        success: bool,
        status_code: int,
        duration: float,
        error_type: Optional[str] = None
    ):
        """Update response statistics"""
        if not self.track_stats:
            return
            
        self.stats["total_responses"] += 1
        if success:
            self.stats["success_responses"] += 1
        else:
            self.stats["error_responses"] += 1
            
        self.stats["status_codes"][status_code] = (
            self.stats["status_codes"].get(status_code, 0) + 1
        )
        
        if error_type:
            self.stats["error_types"][error_type] = (
                self.stats["error_types"].get(error_type, 0) + 1
            )
            
        self.stats["response_times"].append(duration)
        if len(self.stats["response_times"]) > 1000:
            self.stats["response_times"] = self.stats["response_times"][-1000:]

    def _format_error(
        self,
        status_code: int,
        error_detail: Union[str, Dict, List],
        error_type: Optional[str] = None
    ) -> Dict:
        """Format error response"""
        if isinstance(error_detail, str):
            error = {"message": error_detail}
        elif isinstance(error_detail, dict):
            error = error_detail
        else:
            error = {"details": error_detail}
            
        if error_type:
            error["type"] = error_type
            
        error["status_code"] = status_code
        return error

    def _get_metadata(
        self,
        request: Request,
        start_time: float,
        response: Response
    ) -> Dict:
        """Generate response metadata"""
        metadata = {
            "version": self.app_version,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.include_timing:
            metadata["duration_ms"] = round((time.time() - start_time) * 1000, 2)
            
        if self.include_request_id and hasattr(request.state, "request_id"):
            metadata["request_id"] = request.state.request_id
            
        # Add rate limit info if available
        if "X-RateLimit-Remaining" in response.headers:
            metadata["rate_limit"] = {
                "remaining": response.headers["X-RateLimit-Remaining"],
                "limit": response.headers["X-RateLimit-Limit"],
                "reset": response.headers["X-RateLimit-Reset"]
            }
            
        return metadata

    async def __call__(self, request: Request, call_next: Callable):
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Skip formatting for non-JSON responses
            if not response.headers.get("content-type", "").startswith("application/json"):
                return response
                
            status_code = response.status_code
            success = 200 <= status_code < 400
            
            # Get response content
            body = await response.body()
            content = body.decode()
            
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                data = content
                
            # Format response
            formatted_response = APIResponse(
                success=success,
                data=data if success else None,
                error=self._format_error(status_code, data) if not success else None,
                metadata=self._get_metadata(request, start_time, response)
            )
            
            # Update statistics
            if self.track_stats:
                self._update_stats(
                    success=success,
                    status_code=status_code,
                    duration=time.time() - start_time
                )
                
            return JSONResponse(
                status_code=status_code,
                content=formatted_response.dict(),
                headers=dict(response.headers),
                media_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            error_type = type(e).__name__
            
            # Get custom error handler if available
            error_handler = self.error_handlers.get(error_type)
            if error_handler:
                error_response = error_handler(e)
            else:
                error_response = self._format_error(
                    500,
                    str(e),
                    error_type=error_type
                )
                
            # Update statistics
            if self.track_stats:
                self._update_stats(
                    success=False,
                    status_code=500,
                    duration=time.time() - start_time,
                    error_type=error_type
                )
                
            return JSONResponse(
                status_code=500,
                content=APIResponse(
                    success=False,
                    error=error_response,
                    metadata=self._get_metadata(request, start_time, Response())
                ).dict()
            )

    def get_stats(self) -> Dict:
        """Get response formatting statistics"""
        if not self.track_stats:
            return {"stats_enabled": False}
            
        response_times = self.stats["response_times"]
        avg_response_time = (
            sum(response_times) / len(response_times)
            if response_times else 0
        )
        
        return {
            "total_responses": self.stats["total_responses"],
            "success_rate": (
                self.stats["success_responses"] / self.stats["total_responses"] * 100
                if self.stats["total_responses"] > 0 else 0
            ),
            "average_response_time": round(avg_response_time * 1000, 2),  # in ms
            "status_codes": self.stats["status_codes"],
            "error_types": self.stats["error_types"]
        }

    def reset_stats(self):
        """Reset response statistics"""
        self.stats = {
            "total_responses": 0,
            "success_responses": 0,
            "error_responses": 0,
            "response_times": [],
            "status_codes": {},
            "error_types": {}
        }
