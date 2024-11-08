from .settings import Settings

class Config:
    """Application configuration"""
    # Model settings
    CLAUDE_MODEL = "claude-3-sonnet-20240229"
    
    def __init__(self):
        self.settings = Settings()
        self.ANTHROPIC_API_KEY = self.settings.anthropic_api_key
        self.MAX_REPORT_SECTIONS = self.settings.max_report_sections
        self.MAX_PAGES = self.settings.max_pages

    @property
    def database_url(self) -> str:
        return self.settings.database_url

    @property
    def api_key(self) -> str:
        return self.settings.api_key

    @property
    def environment(self) -> str:
        return self.settings.environment 