import logging
from pathlib import Path
from typing import Dict, Any, List
import fitz  # PyMuPDF
import re
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FocusedSwarmAnalysis:
    """Focused analysis of PDF document"""
    
    def __init__(self, pdf_path: str = None):
        if pdf_path is None:
            pdf_path = "C:/Users/xbows/OneDrive/Desktop/Dad/SwarmRAG/Axis Program Management_Unformatted detailed.pdf"
        self.pdf_path = Path(pdf_path)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("reports") / self.timestamp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _extract_service_area_rules(self) -> List[Dict[str, Any]]:
        """Extract service area specific rules"""
        logger.info("Extracting service area rules...")
        rules = []
        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                text = doc[page_num].get_text()
                
                # Search for service area patterns
                service_patterns = [
                    r"(?i)service\s+area.*?(?:requirement|rule|must|shall).*?(?:\.|$)",
                    r"(?i)mileage.*?(?:calculation|formula|method).*?(?:\.|$)",
                    r"(?i)(?:state|county).*?service.*?(?:requirement|rule).*?(?:\.|$)"
                ]
                
                for pattern in service_patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        rules.append({
                            "type": "service_area",
                            "text": match.group().strip(),
                            "page": page_num + 1
                        })
                        logger.info(f"Found service area rule on page {page_num + 1}")
            
            return rules
        except Exception as e:
            logger.error(f"Error extracting service area rules: {str(e)}")
            return []

    def _extract_project_id_rules(self) -> List[Dict[str, Any]]:
        """Extract project ID specific rules"""
        logger.info("Extracting project ID rules...")
        rules = []
        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                text = doc[page_num].get_text()
                
                # Search for project ID patterns
                id_patterns = [
                    r"(?i)project\s+id.*?(?:format|structure|rule).*?(?:\.|$)",
                    r"(?i)project.*?(?:validation|verify|check).*?(?:\.|$)",
                    r"(?i)state\s+code.*?(?:valid|allowed|required).*?(?:\.|$)"
                ]
                
                for pattern in id_patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        rules.append({
                            "type": "project_id",
                            "text": match.group().strip(),
                            "page": page_num + 1
                        })
                        logger.info(f"Found project ID rule on page {page_num + 1}")
            
            return rules
        except Exception as e:
            logger.error(f"Error extracting project ID rules: {str(e)}")
            return []

    def _extract_workflow_rules(self) -> List[Dict[str, Any]]:
        """Extract workflow specific rules"""
        logger.info("Extracting workflow rules...")
        rules = []
        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                text = doc[page_num].get_text()
                
                # Search for workflow patterns
                workflow_patterns = [
                    r"(?i)(?:workflow|process).*?(?:step|sequence|order).*?(?:\.|$)",
                    r"(?i)(?:before|after|then|must).*?(?:can|allowed|proceed).*?(?:\.|$)",
                    r"(?i)(?:validation|check).*?(?:required|needed).*?(?:\.|$)"
                ]
                
                for pattern in workflow_patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        rules.append({
                            "type": "workflow",
                            "text": match.group().strip(),
                            "page": page_num + 1
                        })
                        logger.info(f"Found workflow rule on page {page_num + 1}")
            
            return rules
        except Exception as e:
            logger.error(f"Error extracting workflow rules: {str(e)}")
            return []

    def _generate_combined_report(self, 
                                service_area_rules: List[Dict[str, Any]],
                                project_id_rules: List[Dict[str, Any]],
                                workflow_rules: List[Dict[str, Any]]):
        """Generate comprehensive analysis report"""
        logger.info("Generating comprehensive report...")
        
        report_path = self.output_dir / f"focused_analysis_report_{self.timestamp}.md"
        
        try:
            with open(report_path, 'w') as f:
                # Write report header
                f.write("# Focused SwarmRAG Analysis Report\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Write service area rules
                f.write("## Service Area Rules\n")
                for rule in service_area_rules:
                    f.write(f"- Page {rule['page']}: {rule['text']}\n")
                
                # Write project ID rules
                f.write("\n## Project ID Rules\n")
                for rule in project_id_rules:
                    f.write(f"- Page {rule['page']}: {rule['text']}\n")
                
                # Write workflow rules
                f.write("\n## Workflow Rules\n")
                for rule in workflow_rules:
                    f.write(f"- Page {rule['page']}: {rule['text']}\n")
                
                # Write implementation recommendations
                f.write("\n## Implementation Recommendations\n")
                f.write("### Service Area Implementation\n")
                f.write("- Implement validation for mileage calculations\n")
                f.write("- Add state-specific rule checking\n")
                f.write("- Include county validation\n")
                
                f.write("\n### Project ID Implementation\n")
                f.write("- Implement format validation\n")
                f.write("- Add state code verification\n")
                f.write("- Include existence checking\n")
                
                f.write("\n### Workflow Implementation\n")
                f.write("- Implement step sequencing\n")
                f.write("- Add dependency checking\n")
                f.write("- Include validation gates\n")
            
            logger.info(f"Report generated: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise

    def run_analysis(self):
        """Execute complete focused analysis"""
        try:
            logger.info(f"Starting analysis of: {self.pdf_path}")
            
            # Extract rules
            service_area_rules = self._extract_service_area_rules()
            project_id_rules = self._extract_project_id_rules()
            workflow_rules = self._extract_workflow_rules()
            
            # Generate report
            self._generate_combined_report(
                service_area_rules,
                project_id_rules,
                workflow_rules
            )
            
            logger.info("Analysis complete!")
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise

if __name__ == "__main__":
    analyzer = FocusedSwarmAnalysis()
    analyzer.run_analysis()