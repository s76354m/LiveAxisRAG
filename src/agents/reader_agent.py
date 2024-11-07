from typing import Dict
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class ReaderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reader Agent")
        self.system_prompt = """
        You are an expert technical document analyzer. Your role is to:
        1. Extract key technical information from documents
        2. Identify core system components and architecture
        3. Recognize technical requirements and specifications
        4. Highlight implementation details and patterns
        
        Provide a detailed analysis that covers:
        - System architecture and components
        - Technical requirements and constraints
        - Implementation patterns and approaches
        - Integration points and interfaces
        - Security considerations
        - Performance requirements
        
        Format your response with clear sections and bullet points.
        Be specific and technical in your analysis.
        """

    async def process(self, context: dict) -> Dict[str, Dict]:
        vector_store = context.get('vector_store')
        query = context.get('query', '')
        
        # Get relevant documents from vector store
        docs = vector_store.similarity_search(query)
        relevant_text = "\n\n".join(doc.page_content for doc in docs)
        
        analysis_prompt = f"""
        Analyze the following technical documentation and extract key implementation details:

        {relevant_text}

        Provide a detailed technical analysis focusing on:
        1. System architecture and components
        2. Technical requirements and specifications
        3. Implementation patterns and approaches
        4. Integration points and interfaces
        5. Security considerations
        6. Performance requirements

        Format your response with clear sections and bullet points.
        """
        
        responses = await self.generate_responses(self.system_prompt, analysis_prompt)
        
        return {
            'type': 'technical_analysis',
            'claude': {
                'content': responses['claude'],
                'sources': [doc.metadata for doc in docs]
            }
        }
