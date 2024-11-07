import asyncio
import os
from .coordinator import SwarmCoordinator
import json
import logging
import time
from datetime import datetime
from typing import Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def save_reports(results: dict, base_dir: str) -> Dict[str, tuple]:
    """Save reports from both models"""
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = {}
    
    for model in ['claude']:
        if model in results and isinstance(results[model], dict) and 'content' in results[model]:
            # Save JSON report
            json_path = os.path.join(reports_dir, f"implementation_report_{model}_{timestamp}.json")
            with open(json_path, "w", encoding='utf-8') as f:
                json.dump(results[model], f, indent=2, ensure_ascii=False)
            
            # Save TXT report
            txt_path = os.path.join(reports_dir, f"implementation_report_{model}_{timestamp}.txt")
            with open(txt_path, "w", encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"TECHNICAL IMPLEMENTATION REPORT ({model.upper()})\n")
                f.write("=" * 80 + "\n\n")
                
                content = results[model]['content']
                f.write(content)
                
                f.write("\n\n" + "=" * 80 + "\n")
                f.write("METADATA AND SOURCES\n")
                f.write("=" * 80 + "\n\n")
                
                if 'sources' in results[model]:
                    f.write("## Sources and Dependencies\n\n")
                    f.write(json.dumps(results[model]['sources'], indent=2, ensure_ascii=False))
            
            paths[model] = (json_path, txt_path)
            logger.info(f"{model.upper()} reports saved to {json_path} and {txt_path}")
        else:
            logger.warning(f"No valid results available for {model.upper()}. Skipping report generation.")
    
    return paths

def save_logs(results: dict, base_dir: str) -> str:
    """Save logs of all agent responses and communications"""
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(logs_dir, f"run_log_{timestamp}.txt")
    
    with open(log_path, "w", encoding='utf-8') as f:
        f.write("RUN LOG\n")
        f.write("=" * 80 + "\n\n")
        
        for model in ['claude']:
            f.write(f"Model: {model.upper()}\n")
            f.write("-" * 80 + "\n")
            
            # Safely get responses from each agent
            try:
                if 'reader_output' in results and model in results['reader_output']:
                    f.write("Reader Agent Response:\n")
                    f.write(results['reader_output'][model]['content'] + "\n\n")
                
                if 'analyzer_output' in results and model in results['analyzer_output']:
                    f.write("Analyzer Agent Response:\n")
                    f.write(results['analyzer_output'][model]['content'] + "\n\n")
                
                if 'final_report' in results and model in results['final_report']:
                    f.write("Report Agent Response:\n")
                    f.write(results['final_report'][model]['content'] + "\n\n")
            except Exception as e:
                logger.error(f"Error writing log for {model}: {str(e)}")
                f.write(f"Error capturing response: {str(e)}\n\n")
            
            f.write("=" * 80 + "\n\n")
    
    logger.info(f"Run log saved to {log_path}")
    return log_path

async def main():
    start_time = time.time()
    logger.info("Starting RAG Agent Swarm application...")
    
    coordinator = SwarmCoordinator()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(base_dir, "Axis Program Management_Unformatted detailed.pdf")
    
    try:
        logger.info("Beginning document processing...")
        results = await coordinator.process_document(pdf_path)
        
        # Save reports from both models
        report_paths = save_reports(results.get('final_report', {}), base_dir)
        
        # Save logs
        log_path = save_logs(results, base_dir)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Analysis complete in {elapsed_time:.2f} seconds.")
        
        # Print executive summaries
        for model in ['claude']:
            try:
                if model in results.get('final_report', {}) and isinstance(results['final_report'][model], dict):
                    content = results['final_report'][model].get('content', '')
                    if content:
                        print(f"\n{model.upper()} Executive Summary:")
                        sections = content.split('\n\n')
                        print(sections[0] if sections else content[:2000])
                        if model in report_paths:
                            print(f"\nFull {model.upper()} reports available at:")
                            print(f"JSON: {report_paths[model][0]}")
                            print(f"Text: {report_paths[model][1]}")
                    else:
                        logger.warning(f"No content available for {model.upper()}")
                else:
                    logger.warning(f"No valid results for {model.upper()}")
            except Exception as e:
                logger.error(f"Error processing {model} summary: {str(e)}")
            
            print("\n" + "="*80)
        
        print(f"\nRun log available at: {log_path}")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
