import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from src.swarm.agents import (
    DocumentProcessor,
    BusinessAnalyzer,
    ImplementationPlanner,
    ReportGenerator
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SwarmAnalysis:
    """Main SwarmRAG analysis controller"""
    
    def __init__(self, doc_path: str):
        self.doc_path = Path(doc_path)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("reports") / self.timestamp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def run_full_analysis(self) -> Dict[str, Any]:
        """Execute complete analysis workflow"""
        logger.info("Starting full SwarmRAG analysis...")
        
        try:
            # 1. Process Document
            logger.info("Processing document...")
            processor = DocumentProcessor(self.doc_path)
            doc_content = processor.process()
            
            # 2. Analyze Business Rules
            logger.info("Analyzing business rules...")
            analyzer = BusinessAnalyzer(doc_content)
            business_rules = analyzer.analyze()
            
            # 3. Create Implementation Plan
            logger.info("Creating implementation plan...")
            planner = ImplementationPlanner(business_rules)
            implementation_plan = planner.create_plan()
            
            # 4. Generate Report
            logger.info("Generating comprehensive report...")
            generator = ReportGenerator(
                doc_content=doc_content,
                business_rules=business_rules,
                implementation_plan=implementation_plan
            )
            report = generator.generate_report()
            
            # Save report
            report_path = self.output_dir / f"swarm_analysis_report_{self.timestamp}.md"
            report_path.write_text(report)
            
            logger.info(f"Analysis complete! Report saved to: {report_path}")
            return {
                "status": "success",
                "report_path": str(report_path),
                "timestamp": self.timestamp
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": self.timestamp
            }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run SwarmRAG Analysis")
    parser.add_argument("--doc-path", type=str, 
                       default="C:/Users/xbows/OneDrive/Desktop/Dad/SwarmRAG/Axis Program Management_Unformatted detailed.pdf",
                       help="Path to the document to analyze")
    
    args = parser.parse_args()
    
    analyzer = SwarmAnalysis(args.doc_path)
    result = analyzer.run_full_analysis()
    
    if result["status"] == "success":
        logger.info(f"Analysis completed successfully!")
        logger.info(f"Report available at: {result['report_path']}")
    else:
        logger.error(f"Analysis failed: {result['error']}")