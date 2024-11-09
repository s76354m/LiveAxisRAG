import pytest
from pathlib import Path
import shutil
import logging
import os
from src.core.config.app_config import AppConfig
from src.core.config.schemas import AppConfigSchema
from pydantic import ValidationError

# Setup logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def cleanup_config():
    """Clean up configuration files before and after tests"""
    # Clean up before test
    if Path('config').exists():
        shutil.rmtree('config')
    
    # Reset AppConfig singleton state
    AppConfig._instance = None
    AppConfig._initialized = False
    
    # Store original environment
    original_env = os.environ.get('ENVIRONMENT')
    
    yield
    
    # Restore original environment
    if original_env:
        os.environ['ENVIRONMENT'] = original_env
    elif 'ENVIRONMENT' in os.environ:
        del os.environ['ENVIRONMENT']
    
    # Clean up after test
    if Path('config').exists():
        shutil.rmtree('config')

def test_config_loading(cleanup_config):
    """Test basic configuration loading"""
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    base_config = """
database:
  pool_size: 5
  max_overflow: 10
logging:
  level: INFO
api:
  version: '1.0'
"""
    config_file = config_dir / 'base.yaml'
    config_file.write_text(base_config)
    
    config = AppConfig()
    
    assert config.get('database.pool_size') == 5
    assert config.get('logging.level') == 'INFO'
    assert config.get('api.version') == '1.0'
    assert config.get('nonexistent.key', 'default') == 'default'
    assert config.get('nonexistent.key') is None

def test_environment_override(cleanup_config):
    """Test environment-specific configuration override"""
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    # Create base config
    base_config = """
database:
  host: localhost
  port: 5432
logging:
  level: INFO
"""
    (config_dir / 'base.yaml').write_text(base_config)
    
    # Create development config
    dev_config = """
database:
  host: dev-host
logging:
  level: DEBUG
"""
    (config_dir / 'development.yaml').write_text(dev_config)
    
    os.environ['ENVIRONMENT'] = 'development'
    config = AppConfig()
    
    assert config.get('database.host') == 'dev-host'
    assert config.get('database.port') == 5432
    assert config.get('logging.level') == 'DEBUG'

def test_deep_merge(cleanup_config):
    """Test deep merging of configurations"""
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    base_config = """
database:
  connections:
    primary:
      host: localhost
      port: 5432
    secondary:
      host: localhost
      port: 5433
"""
    (config_dir / 'base.yaml').write_text(base_config)
    
    env_config = """
database:
  connections:
    primary:
      host: prod-host
"""
    (config_dir / 'production.yaml').write_text(env_config)
    
    os.environ['ENVIRONMENT'] = 'production'
    config = AppConfig()
    
    assert config.get('database.connections.primary.host') == 'prod-host'
    assert config.get('database.connections.primary.port') == 5432
    assert config.get('database.connections.secondary.host') == 'localhost'

def test_env_interpolation(cleanup_config):
    """Test environment variable interpolation"""
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    # Set environment variables
    os.environ['DB_HOST'] = 'test-db-host'
    os.environ['DB_PORT'] = '5432'
    
    base_config = """
database:
    host: ${DB_HOST}
    port: $DB_PORT
    name: testdb
    user: testuser
    password: testpass
logging:
    level: INFO
api:
    version: '1.0'
"""
    (config_dir / 'base.yaml').write_text(base_config)
    
    config = AppConfig()
    assert config.get('database.host') == 'test-db-host'
    assert config.get('database.port') == '5432'

def test_config_validation(cleanup_config):
    """Test configuration validation"""
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    valid_config = """
database:
    host: localhost
    port: 5432
    name: testdb
    user: testuser
    password: testpass
logging:
    level: INFO
api:
    version: '1.0'
"""
    (config_dir / 'base.yaml').write_text(valid_config)
    
    config = AppConfig()
    config.validate_config()  # Should not raise
    
    # Test invalid config
    invalid_config = """
database:
    host: localhost
    # Missing required fields
logging:
    level: INVALID_LEVEL
api:
    version: '1.0'
"""
    (config_dir / 'base.yaml').write_text(invalid_config)
    
    with pytest.raises(ValidationError):
        config = AppConfig()
        config.validate_config()