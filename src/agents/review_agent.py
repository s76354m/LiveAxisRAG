from typing import Dict
from .base_agent import BaseAgent
from ..config import Config
import logging

logger = logging.getLogger(__name__)

class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("Review Agent")
        self.system_prompt = """
        You are an expert technical reviewer with deep knowledge across multiple domains. 
        Your role is to thoroughly analyze technical reports for:

        1. Technical Accuracy
           - Verify all technical claims and statements
           - Identify any technical inconsistencies
           - Validate architectural decisions
           - Check implementation recommendations

        2. Completeness
           - Ensure all required sections are adequately covered
           - Verify depth of technical detail
           - Check for missing critical information

        3. Practical Implementation
           - Assess feasibility of proposed solutions
           - Verify resource estimates and timelines
           - Validate technical dependencies
           - Check for potential implementation challenges

        4. Security and Best Practices
           - Verify security recommendations
           - Check compliance with industry standards
           - Validate best practices recommendations

        If you find any issues, clearly explain:
        - The specific problem or inaccuracy
        - Why it's incorrect or problematic
        - The recommended correction
        - Impact if not addressed

        Format your response as:
        {
            "needs_revision": true/false,
            "critical_issues": [list of critical issues],
            "recommendations": [specific corrections needed],
            "additional_notes": "Any other important observations"
        }

        Be thorough and precise in your analysis. Your role is to ensure 
        the final report is accurate, implementable, and valuable.
        """

    async def process(self, context: dict) -> Dict[str, Dict]:
        report_content = context.get('final_report', {})
        reader_output = context.get('reader_output', {})
        analyzer_output = context.get('analyzer_output', {})

        review_prompt = f"""
        Review this technical implementation report for accuracy, completeness, 
        and practical implementation. Consider the original analysis data when 
        evaluating the report's conclusions.

        Original Reader Analysis:
        {reader_output}

        Original Technical Analysis:
        {analyzer_output}

        Report to Review:
        {report_content}

        Provide a detailed review focusing on:
        1. Technical accuracy of all claims and recommendations
        2. Completeness of required sections
        3. Practical implementation feasibility
        4. Security and best practices compliance
        5. Consistency with original analysis

        If you find any issues that require revision, clearly explain:
        - The specific problem
        - Why it's incorrect
        - The recommended correction
        - Impact if not addressed

        Format your response as a JSON structure with:
        - needs_revision (boolean)
        - critical_issues (array)
        - recommendations (array)
        - additional_notes (string)
        """

        responses = await self.generate_responses(self.system_prompt, review_prompt)
        
        return {
            'type': 'review_report',
                 'claude': {
                'content': responses['claude'],
                'sources': {
                    'report': report_content.get('claude', {}).get('content', '')
                }
            }
        } 