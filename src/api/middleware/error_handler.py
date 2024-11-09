from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ErrorDetail:
    def __init__(self, message: str, code: str = None, params: Dict[str, Any] = None):
        self.message = message
        self.code = code
        self.params = params or {}

async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global error handler for the API
    
    Args:
        request (Request): The incoming request
        exc (Exception): The raised exception
    
    Returns:
        JSONResponse: Formatted error response
    """
    error_response = {
        "success": False,
        "error": {
            "type": exc.__class__.__name__,
            "message": str(exc)
        }
    }

    if isinstance(exc, HTTPException):
        error_response["error"]["status_code"] = exc.status_code
        error_response["error"]["detail"] = exc.detail
        status_code = exc.status_code
    else:
        logger.exception("Unhandled exception occurred")
        error_response["error"]["status_code"] = 500
        error_response["error"]["detail"] = "Internal server error"
        status_code = 500

    return JSONResponse(
        status_code=status_code,
        content=error_response
    )
