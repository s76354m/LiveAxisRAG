import os
import sys

def create_request_validator():
    try:
        # Create directories if they don't exist
        os.makedirs("src/api/middleware", exist_ok=True)
        
        # Create the validator file
        validator_content = '''from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Callable
import uuid
import json

class RequestValidationMiddleware:
    def __init__(
        self,
        max_content_length: int = 1024 * 1024,  # 1MB default
        allowed_content_types: set = {"application/json"}
    ):
        self.max_content_length = max_content_length
        self.allowed_content_types = allowed_content_types

    async def __call__(self, request: Request, call_next: Callable):
        # Add request ID
        request.state.request_id = str(uuid.uuid4())

        # Validate content type
        content_type = request.headers.get("content-type", "").lower()
        if request.method in ["POST", "PUT", "PATCH"]:
            if not any(allowed in content_type for allowed in self.allowed_content_types):
                return JSONResponse(
                    status_code=415,
                    content={
                        "error": "Unsupported Media Type",
                        "detail": f"Content-Type must be one of: {self.allowed_content_types}"
                    }
                )

        # Validate content length
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_content_length:
            return JSONResponse(
                status_code=413,
                content={
                    "error": "Payload Too Large",
                    "detail": f"Request body must not exceed {self.max_content_length} bytes"
                }
            )

        # Process the request
        response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request.state.request_id
        
        return response
'''
        
        with open("src/api/middleware/request_validator.py", "w") as f:
            f.write(validator_content)

        # Update __init__.py to export the middleware
        init_content = '''from .error_handler import error_handler
from .request_validator import RequestValidationMiddleware

__all__ = ["error_handler", "RequestValidationMiddleware"]
'''
        
        with open("src/api/middleware/__init__.py", "w") as f:
            f.write(init_content)
            
        print("✅ Request validation middleware has been created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating files: {str(e)}")
        return False

if __name__ == "__main__":
    response = input("Do you want to create the request validation middleware? (y/n): ")
    if response.lower() == 'y':
        create_request_validator()
    else:
        print("Operation cancelled.")