from typing import Dict
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Analyzer Agent")
        self.system_prompt = """
        You are an expert technical analyst specializing in software architecture 
        and implementation. Your role is to:
        
        1. Analyze technical requirements and specifications
        2. Evaluate architectural decisions and patterns
        3. Identify potential implementation challenges
        4. Assess technical feasibility and risks
        5. Recommend best practices and solutions
        
        Provide detailed technical analysis with:
        - Clear architectural recommendations
        - Implementation strategies
        - Technical considerations and trade-offs
        - Risk mitigation approaches
        - Best practices and standards
        
        Format your response with clear sections and specific technical details.
        """

    async def process(self, context: dict) -> Dict[str, Dict]:
        reader_output = context.get('reader_output', {})
        
        analysis_prompt = f"""
        Review the following technical analysis and provide detailed implementation 
        recommendations:

        {reader_output.get('claude', {}).get('content', '')}

        Provide a comprehensive technical analysis covering:
        1. Architecture and Design Patterns
        2. Implementation Strategy
        3. Technical Requirements
        4. Integration Approaches
        5. Security Considerations
        6. Performance Optimization
        7. Risk Mitigation

        Format your response with clear sections and specific technical details.
        Include code examples or pseudo-code where appropriate.
        """
        
        responses = await self.generate_responses(self.system_prompt, analysis_prompt)
        
        return {
            'type': 'implementation_analysis',
            'claude': {
                'content': responses['claude'],
                'sources': {
                    'reader': reader_output.get('claude', {}).get('content', '')
                }
            }
        }
