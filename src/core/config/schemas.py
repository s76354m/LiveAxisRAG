from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DatabaseConfig(BaseModel):
    host: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    name: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Maximum connection overflow")

class LoggingConfig(BaseModel):
    level: str = Field(default="INFO", description="Logging level")
    format: Optional[str] = Field(default=None, description="Log format")
    file: Optional[str] = Field(default=None, description="Log file path")

class ApiConfig(BaseModel):
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, description="API port")
    debug: bool = Field(default=False, description="Debug mode")
    version: str = Field(..., description="API version")

class AppConfigSchema(BaseModel):
    database: DatabaseConfig
    logging: LoggingConfig
    api: ApiConfig
    custom: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom configuration") 