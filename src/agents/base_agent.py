from abc import ABC, abstractmethod
from langchain_anthropic import ChatAnthropic
from ..config import Config
import logging
import time
from typing import Dict, List

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.name = agent_name
        logger.info(f"Initializing {agent_name}...")
        
        # Initialize Claude
        self.claude = ChatAnthropic(
            model_name=Config.CLAUDE_MODEL,
            temperature=0.3,
            max_tokens=4096,
            anthropic_api_key=Config.ANTHROPIC_API_KEY
        )
        
        self.token_limit = 100000  # Claude's context window
        self.chunk_overlap_tokens = 500
        
        logger.info(f"{agent_name} initialization complete")
    
    async def generate_responses(self, system_prompt: str, user_prompt: str) -> Dict[str, str]:
        """Generate responses from Claude model"""
        responses = {}
        
        # Generate Claude response
        start_time = time.time()
        logger.info(f"{self.name}: Generating Claude response...")
        
        claude_messages = [
            {"role": "assistant", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            # Split the user prompt into chunks if necessary
            user_prompt_chunks = self._split_into_chunks(user_prompt, 3000)  # Adjust chunk size as needed
            claude_response_parts = []
            
            for chunk in user_prompt_chunks:
                claude_messages[1]["content"] = chunk
                claude_response = await self.claude.agenerate([claude_messages])
                claude_response_parts.append(claude_response.generations[0][0].text)
            
            responses['claude'] = "\n".join(claude_response_parts)
            elapsed_time = time.time() - start_time
            logger.info(f"{self.name}: Claude response generated in {elapsed_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Claude generation error: {str(e)}")
            responses['claude'] = f"Error generating Claude response: {str(e)}"
        
        return responses
    
    def _split_into_chunks(self, text: str, chunk_size: int) -> list:
        """Split text into chunks of specified size"""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count - rough approximation"""
        return len(text.split()) * 1.3
        
    def _chunk_text_by_tokens(self, text: str) -> List[str]:
        """Chunk text based on token estimates"""
        chunks = []
        words = text.split()
        current_chunk = []
        current_tokens = 0
        
        for word in words:
            word_tokens = self._estimate_tokens(word)
            if current_tokens + word_tokens > self.token_limit:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_tokens = 0
            current_chunk.append(word)
            current_tokens += word_tokens
            
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks
    
    @abstractmethod
    async def process(self, context: dict) -> Dict[str, Dict]:
        """Process the input and generate response"""
        pass
