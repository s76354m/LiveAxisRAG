import logging
import logging.handlers
import json
from datetime import datetime
from pathlib import Path

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logger()
        
    def _setup_logger(self):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Rotate logs daily, keep 30 days of history
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_dir / "application.log",
            when="midnight",
            interval=1,
            backupCount=30
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler) 