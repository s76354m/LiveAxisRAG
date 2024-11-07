from typing import Dict
from .base_agent import BaseAgent
from ..config import Config
import logging

logger = logging.getLogger(__name__)

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("Report Agent")
        # Get only the configured number of sections
        sections = Config.get_report_sections()
        logger.info(f"Initializing Report Agent with {len(sections)} sections: {sections}")
        
        sections_list = "\n".join(f"{i+1}. {section}" for i, section in enumerate(sections))
        
        self.system_prompt = f"""
        You are a technical documentation specialist that creates detailed 
        implementation reports. Your report must be strictly limited to ONLY 
        these {len(sections)} sections, in this exact order:

        {sections_list}
        
        Important: Do not include any additional sections beyond these {len(sections)} sections.
        
        For each section:
        - Provide detailed, actionable information
        - Include specific examples where applicable
        - Maintain clear structure with subsections
        - Use bullet points and numbered lists for clarity
        
        Format each section with a clear heading using markdown (e.g., ## Section Name).
        Start each section on a new line for better readability.
        """
    
    async def process(self, context: dict) -> Dict[str, Dict]:
        reader_output = context.get('reader_output', {})
        analyzer_output = context.get('analyzer_output', {})
        
        sections = Config.get_report_sections()
        sections_str = ", ".join(sections)
        
        report_prompt = f"""
        Create a technical implementation report based on the following analysis.
        You must strictly limit your response to ONLY these {len(sections)} sections:
        {sections_str}

        Reader Analysis:
        {reader_output.get('claude', {}).get('content', '')}

        Technical Analysis:
        {analyzer_output.get('claude', {}).get('content', '')}

        Important Instructions:
        1. Include ONLY the {len(sections)} sections listed above
        2. Use markdown headings (##) for each section
        3. Provide detailed, implementation-focused content
        4. Include specific examples and code snippets where relevant
        5. DO NOT add any additional sections
        
        Start each section with its heading on a new line.
        """
        
        logger.info(f"Generating report with {len(sections)} sections: {sections}")
        responses = await self.generate_responses(self.system_prompt, report_prompt)
        
        # Validate and clean responses to ensure only requested sections are included
        content = responses['claude']
        if isinstance(content, str):
            # Split content into sections and filter to keep only requested sections
            sections_content = []
            current_section = ""
            for line in content.split('\n'):
                if line.startswith('## '):
                    if current_section:
                        sections_content.append(current_section.strip())
                    current_section = line + '\n'
                else:
                    current_section += line + '\n'
            if current_section:
                sections_content.append(current_section.strip())
            
            # Keep only the configured number of sections
            max_sections = Config.MAX_REPORT_SECTIONS
            sections_content = sections_content[:max_sections]
            responses['claude'] = '\n\n'.join(sections_content)
            
            logger.info(f"Processed claude response: kept {len(sections_content)} sections")
        
        return {
            'type': 'implementation_report',
            'claude': {
                'content': responses['claude'],
                'sources': {
                    'reader': reader_output.get('claude', {}).get('content', ''),
                    'analyzer': analyzer_output.get('claude', {}).get('content', '')
                }
            }
        }
