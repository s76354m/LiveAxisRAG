from typing import Optional, Dict, Any
from pathlib import Path
import os
import base64
from cryptography.fernet import Fernet
from src.utils.exceptions import ConfigurationError
import logging

logger = logging.getLogger(__name__)

class SecretsManager:
    _instance = None
    
    def __new__(cls) -> 'SecretsManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self) -> None:
        """Initialize secrets manager"""
        self._load_encryption_key()
        self._secrets: Dict[str, str] = {}
        self._load_secrets()
        
    def _load_encryption_key(self) -> None:
        """Load or generate encryption key"""
        key_file = Path('.secret.key')
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self._key = f.read()
        else:
            self._key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self._key)
                
        self._cipher = Fernet(self._key)
        
    def _load_secrets(self) -> None:
        """Load encrypted secrets"""
        secrets_file = Path('config/secrets.enc')
        if secrets_file.exists():
            try:
                with open(secrets_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self._cipher.decrypt(encrypted_data)
                self._secrets = eval(decrypted_data.decode())
            except Exception as e:
                logger.error(f"Failed to load secrets: {str(e)}")
                raise ConfigurationError(f"Failed to load secrets: {str(e)}")
                
    def get_secret(self, key: str) -> Optional[str]:
        """Safely retrieve a secret"""
        return self._secrets.get(key)
        
    def set_secret(self, key: str, value: str) -> None:
        """Safely store a secret"""
        self._secrets[key] = value
        self._save_secrets()
        
    def _save_secrets(self) -> None:
        """Save encrypted secrets"""
        try:
            encrypted_data = self._cipher.encrypt(str(self._secrets).encode())
            with open('config/secrets.enc', 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            logger.error(f"Failed to save secrets: {str(e)}")
            raise ConfigurationError(f"Failed to save secrets: {str(e)}") 