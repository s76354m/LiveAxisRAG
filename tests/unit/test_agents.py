import pytest
from src.agents.base_agent import BaseAgent
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_base_agent():
    """Test base agent functionality"""
    # Create mock config with required attributes
    mock_config = Mock()
    mock_config.CLAUDE_MODEL = "claude-3-sonnet-20240229"
    mock_config.ANTHROPIC_API_KEY = "test_key"
    mock_config.MAX_REPORT_SECTIONS = 10
    mock_config.MAX_PAGES = 100
    
    # Patch ChatAnthropic
    with patch('src.agents.base_agent.ChatAnthropic') as mock_chat:
        class TestAgent(BaseAgent):
            """Test implementation of base agent"""
            async def process(self, input_data: str) -> dict:
                return {"result": input_data}
        
        agent = TestAgent(mock_config)
        result = await agent.process("test input")
        assert result is not None
        assert result["result"] == "test input"