from typing import Dict
import asyncio
from .agents.reader_agent import ReaderAgent
from .agents.analyzer_agent import AnalyzerAgent
from .agents.report_agent import ReportAgent
from .agents.review_agent import ReviewAgent
from .document_processor import DocumentProcessor
import logging
import json

logger = logging.getLogger(__name__)

class SwarmCoordinator:
    def __init__(self):
        logger.info("Initializing SwarmCoordinator...")
        self.document_processor = DocumentProcessor()
        self.agents = {
            'reader': ReaderAgent(),
            'analyzer': AnalyzerAgent(),
            'report': ReportAgent(),
            'review': ReviewAgent()
        }
        self.retry_config = {
            'max_retries': 3,
            'delay': 1,
            'backoff': 2
        }
        logger.info("SwarmCoordinator initialization complete")
    
    def _initialize_context(self, vector_store) -> Dict:
        """Initialize the context with vector store and default query"""
        return {
            'vector_store': vector_store,
            'query': 'Provide a comprehensive technical analysis of the system architecture and implementation details.'
        }
    
    def _prepare_final_output(self, reader_output, analyzer_output, final_report, review_output=None) -> Dict:
        """Prepare the final output dictionary"""
        return {
            'reader_output': reader_output,
            'analyzer_output': analyzer_output,
            'final_report': final_report,
            'review_output': review_output
        }
    
    async def _handle_review_process(self, context: Dict, initial_report: Dict) -> Dict:
        """Handle the review and revision process"""
        max_revision_attempts = 3
        revision_attempt = 0
        current_report = initial_report
        
        while revision_attempt < max_revision_attempts:
            context['final_report'] = current_report
            logger.info("Starting Review Agent analysis...")
            
            try:
                review_output = await self.execute_with_retry(
                    'review',
                    self.agents['review'].process,
                    context
                )
                
                review_content = review_output['claude']['content']
                review_data = json.loads(review_content)
                
                if review_data.get('needs_revision', False):
                    context['review_feedback'] = review_data
                    logger.info(f"Revision needed (attempt {revision_attempt + 1}/{max_revision_attempts})")
                    revision_attempt += 1
                    
                    current_report = await self.execute_with_retry(
                        'report',
                        self.agents['report'].process,
                        context
                    )
                else:
                    logger.info("No revisions needed. Report approved by Review Agent")
                    return current_report
                    
            except Exception as e:
                logger.error(f"Error in review process: {str(e)}")
                return current_report
        
        logger.warning(f"Max revision attempts ({max_revision_attempts}) reached")
        return current_report
    
    async def execute_with_retry(self, agent_name: str, method, *args, **kwargs):
        """Execute agent method with retry logic"""
        retries = 0
        delay = self.retry_config['delay']
        
        while retries < self.retry_config['max_retries']:
            try:
                return await method(*args, **kwargs)
            except Exception as e:
                retries += 1
                if retries == self.retry_config['max_retries']:
                    raise
                logger.warning(f"{agent_name} attempt {retries} failed: {str(e)}")
                await asyncio.sleep(delay)
                delay *= self.retry_config['backoff']
    
    async def process_document(self, pdf_path: str) -> Dict[str, Dict]:
        """Process document through the agent pipeline"""
        try:
            # Process document and create vector store
            vector_store = self.document_processor.process_document(pdf_path)
            context = self._initialize_context(vector_store)
            
            # Execute initial pipeline with retry logic
            logger.info("Starting Reader Agent analysis...")
            reader_output = await self.execute_with_retry(
                'reader',
                self.agents['reader'].process,
                context
            )
            
            context['reader_output'] = reader_output
            logger.info("Starting Analyzer Agent analysis...")
            analyzer_output = await self.execute_with_retry(
                'analyzer',
                self.agents['analyzer'].process,
                context
            )
            
            context['analyzer_output'] = analyzer_output
            logger.info("Starting Report Agent generation...")
            initial_report = await self.execute_with_retry(
                'report',
                self.agents['report'].process,
                context
            )
            
            # Handle review process
            final_report = await self._handle_review_process(context, initial_report)
            
            return self._prepare_final_output(
                reader_output,
                analyzer_output,
                final_report
            )
            
        except Exception as e:
            logger.error(f"Error in document processing pipeline: {str(e)}")
            raise
