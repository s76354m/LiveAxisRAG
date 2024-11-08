from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    # API Keys
    anthropic_api_key: str = Field(default="")
    langchain_api_key: str = Field(default="")
    openai_api_key: str = Field(default="")
    
    # Database
    database_url: str = Field(default="sqlite:///./test.db")
    
    # API Configuration
    api_version: str = Field(default="v1")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # LangChain Settings
    langchain_tracing_v2: bool = Field(default=False)
    langchain_endpoint: str = Field(default="https://api.smith.langchain.com")
    langchain_project: str = Field(default="SwarmRAG")
    
    # Application Limits
    max_report_sections: int = Field(default=10)
    max_pages: int = Field(default=100)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )