from typing import Dict
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class ReaderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reader Agent")
        self.system_prompt = """
        You are an expert technical document analyzer focusing on PowerApps to Python conversion requirements.
        
        Analysis Categories:
        
        1. Control Identification
        - Identify all PowerApps controls and their properties
        - Note special control behaviors and events
        - Map controls to equivalent HTML/Flask components
        
        2. Data Structure Analysis
        - Identify collections and their schemas
        - Map data sources to SQLAlchemy models
        - Note relationships and constraints
        
        3. Business Logic Extraction
        - Identify formulas and calculations
        - Map workflows to Python functions
        - Note conditional logic and validation rules
        
        4. Integration Requirements
        - Identify external service connections
        - Map authentication methods
        - Note data sync requirements
        
        5. UI/UX Patterns
        - Identify screen layouts and navigation
        - Map visual components to Bootstrap/HTML
        - Note responsive design requirements
        
        Provide detailed analysis focusing on Python implementation requirements.
        Note any PowerApps features requiring special handling.
        Identify potential conversion challenges.
        """

    async def process(self, context: dict) -> Dict[str, Dict]:
        vector_store = context.get('vector_store')
        
        # Define specific queries for each aspect
        queries = [
            "What are the core application features, workflows, and user interactions?",
            "What are the data models, schemas, and relationships?",
            "What are the UI/UX specifications, layouts, and components?",
            "What are the business rules, validations, and process flows?",
            "What are the integration requirements and external system interfaces?"
        ]
        
        all_relevant_text = []
        for query in queries:
            docs = vector_store.similarity_search(query)
            relevant_text = "\n\n".join(doc.page_content for doc in docs)
            all_relevant_text.append(f"Query: {query}\n\nFindings:\n{relevant_text}")
        
        analysis_prompt = f"""
        Analyze the following technical documentation for application development requirements:

        {'\n\n'.join(all_relevant_text)}

        Provide a detailed analysis focusing on:
        1. Application Requirements
           - Core functionality
           - User workflows
           - Feature specifications
           - System constraints
           - Performance requirements

        2. Data Architecture
           - Data models
           - Relationships
           - Data flows
           - Storage requirements
           - Validation rules

        3. UI/UX Specifications
           - Screen layouts
           - Navigation flows
           - Component details
           - Interaction patterns
           - Visual requirements

        4. Business Logic
           - Business rules
           - Validation logic
           - Calculation methods
           - Process flows
           - State management

        5. Integration Requirements
           - External systems
           - APIs
           - Authentication
           - Data sync
           - Error handling

        6. PowerApps to Python Conversion Requirements
           - Specific UI component mapping requirements
           - State management patterns
           - Data flow specifications

        For each section:
        - Provide specific details found in the documentation
        - Explicitly note any missing critical information
        - Include technical specifications where available
        - Note any ambiguities or areas needing clarification

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
