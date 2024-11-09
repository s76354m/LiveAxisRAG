import pytest
from pathlib import Path
from src.core.config.app_config import AppConfig
from src.core.config.secrets_manager import SecretsManager

@pytest.fixture(scope="session")
def app_config():
    """Provide application configuration for tests"""
    return AppConfig()

@pytest.fixture(scope="session")
def secrets_manager():
    """Provide secrets manager for tests"""
    return SecretsManager()

@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path_factory):
    """Setup test environment"""
    # Create test config directory
    config_dir = tmp_path_factory.mktemp("config")
    
    # Create test configurations
    create_test_configs(config_dir)
    
    yield
    
    # Cleanup is handled automatically by pytest

def create_test_configs(config_dir: Path):
    """Create test configuration files"""
    # Create base config
    base_config = """
database:
    pool_size: 5
    max_overflow: 10
logging:
    level: INFO
api:
    version: '1.0'
"""
    (config_dir / "base.yaml").write_text(base_config)
    
    # Create test environment config
    test_config = """
database:
    host: test-host
    port: 5432
    name: test_db
logging:
    level: DEBUG
api:
    base_url: 'http://test-api'
"""
    (config_dir / "test.yaml").write_text(test_config)