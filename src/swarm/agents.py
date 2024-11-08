import logging
from pathlib import Path
from typing import Dict, Any, List
import fitz  # PyMuPDF
import re
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Container for analysis results"""
    content: Dict[str, Any]
    rules: List[Dict[str, Any]]
    workflows: List[Dict[str, Any]]

class DocumentProcessor:
    """Process and extract content from PDF"""
    
    def __init__(self, doc_path: Path):
        self.doc_path = doc_path
    
    def process(self) -> Dict[str, Any]:
        """Extract and process document content"""
        try:
            doc = fitz.open(self.doc_path)
            content = []
            structured_content = {
                "service_areas": [],
                "products": [],
                "workflows": [],
                "business_rules": []
            }
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                content.append(text)
                
                # Extract service area information
                service_area_matches = re.finditer(
                    r"(?i)(?:service\s+area|project\s+area).*?(?=\n\n|\Z)",
                    text
                )
                for match in service_area_matches:
                    structured_content["service_areas"].append({
                        "text": match.group(),
                        "page": page_num + 1
                    })
                
                # Extract product information
                product_matches = re.finditer(
                    r"(?i)(?:product|CSP).*?(?=\n\n|\Z)",
                    text
                )
                for match in product_matches:
                    structured_content["products"].append({
                        "text": match.group(),
                        "page": page_num + 1
                    })
                
                # Extract workflow information
                workflow_matches = re.finditer(
                    r"(?i)(?:workflow|process|procedure).*?(?=\n\n|\Z)",
                    text
                )
                for match in workflow_matches:
                    structured_content["workflows"].append({
                        "text": match.group(),
                        "page": page_num + 1
                    })
                
                # Extract business rules
                rule_matches = re.finditer(
                    r"(?i)(?:must|shall|required|rule|policy).*?(?=\n\n|\Z)",
                    text
                )
                for match in rule_matches:
                    structured_content["business_rules"].append({
                        "text": match.group(),
                        "page": page_num + 1
                    })
            
            return {
                "content": "\n".join(content),
                "structured_content": structured_content,
                "page_count": len(doc),
                "metadata": doc.metadata
            }
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

class BusinessAnalyzer:
    """Analyze document for business rules"""
    
    def __init__(self, doc_content: Dict[str, Any]):
        self.content = doc_content
        self.structured_content = doc_content["structured_content"]
    
    def analyze(self) -> List[Dict[str, Any]]:
        """Extract business rules and workflows"""
        try:
            rules = []
            
            # Process service area rules
            for item in self.structured_content["service_areas"]:
                rules.append({
                    "type": "service_area",
                    "rule": item["text"],
                    "page": item["page"],
                    "category": "Service Area Management"
                })
            
            # Process product rules
            for item in self.structured_content["products"]:
                rules.append({
                    "type": "product",
                    "rule": item["text"],
                    "page": item["page"],
                    "category": "Product Management"
                })
            
            # Process workflow rules
            for item in self.structured_content["workflows"]:
                rules.append({
                    "type": "workflow",
                    "rule": item["text"],
                    "page": item["page"],
                    "category": "Workflow Management"
                })
            
            # Process explicit business rules
            for item in self.structured_content["business_rules"]:
                rules.append({
                    "type": "business_rule",
                    "rule": item["text"],
                    "page": item["page"],
                    "category": "Business Rules"
                })
            
            return rules
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            raise

class ImplementationPlanner:
    """Plan implementation based on analysis"""
    
    def __init__(self, business_rules: List[Dict[str, Any]]):
        self.rules = business_rules
    
    def create_plan(self) -> Dict[str, Any]:
        """Create implementation plan from rules"""
        try:
            return {
                "database": self._plan_database(),
                "api": self._plan_api(),
                "services": self._plan_services(),
                "validation": self._plan_validation()
            }
        except Exception as e:
            logger.error(f"Error creating implementation plan: {str(e)}")
            raise
    
    def _plan_database(self) -> Dict[str, Any]:
        """Plan database implementation"""
        db_plan = {
            "stored_procedures": [
                {
                    "name": "usp_CS_EXP_Check_ProjectID",
                    "purpose": "Validate project ID existence",
                    "parameters": ["ProjectID"]
                },
                {
                    "name": "usp_CS_EXP_SelCSP_Products",
                    "purpose": "Retrieve CSP products",
                    "parameters": ["Flag"]
                },
                {
                    "name": "usp_CS_EXP_Project_ServiceArea_Edit",
                    "purpose": "Update service area details",
                    "parameters": ["ProjectID", "Mileage", "Flag"]
                },
                {
                    "name": "usp_CS_EXP_Project_ServiceArea",
                    "purpose": "Manage service area",
                    "parameters": ["ProjectID", "Mileage"]
                },
                {
                    "name": "usp_CS_EXP_zTrxServiceArea",
                    "purpose": "Process service area transactions",
                    "parameters": ["ProjectID"]
                }
            ],
            "tables": [
                "CS_EXP_Project_Translation",
                "CS_EXP_zTrxServiceArea",
                "CS_EXP_Sel_PLProducts"
            ]
        }
        return db_plan
    
    def _plan_api(self) -> Dict[str, Any]:
        """Plan API implementation"""
        api_plan = {
            "endpoints": [
                {
                    "path": "/project/{project_id}/exists",
                    "method": "GET",
                    "purpose": "Check project existence"
                },
                {
                    "path": "/project/{project_id}/service-area",
                    "method": "GET",
                    "purpose": "Get service area details"
                },
                {
                    "path": "/project/{project_id}/service-area",
                    "method": "POST",
                    "purpose": "Update service area"
                },
                {
                    "path": "/products",
                    "method": "GET",
                    "purpose": "Get CSP products"
                }
            ]
        }
        return api_plan
    
    def _plan_services(self) -> Dict[str, Any]:
        """Plan services implementation"""
        services_plan = {
            "modules": [
                {
                    "name": "ProjectService",
                    "methods": [
                        "check_project_id",
                        "get_service_area",
                        "update_service_area",
                        "get_products"
                    ]
                },
                {
                    "name": "ValidationService",
                    "methods": [
                        "validate_project_id",
                        "validate_mileage",
                        "validate_service_area"
                    ]
                }
            ]
        }
        return services_plan
    
    def _plan_validation(self) -> Dict[str, Any]:
        """Plan validation implementation"""
        validation_plan = {
            "rules": [
                {
                    "field": "project_id",
                    "validations": [
                        "format_check",
                        "existence_check"
                    ]
                },
                {
                    "field": "mileage",
                    "validations": [
                        "range_check",
                        "numeric_check"
                    ]
                },
                {
                    "field": "service_area",
                    "validations": [
                        "completeness_check",
                        "business_rule_check"
                    ]
                }
            ]
        }
        return validation_plan

class ReportGenerator:
    """Generate analysis report"""
    
    def __init__(self, doc_content: Dict[str, Any], 
                 business_rules: List[Dict[str, Any]], 
                 implementation_plan: Dict[str, Any]):
        self.content = doc_content
        self.rules = business_rules
        self.plan = implementation_plan
    
    def generate_report(self) -> str:
        """Generate comprehensive markdown report"""
        try:
            report = []
            
            # Add header
            report.append("# SwarmRAG Analysis Report\n")
            
            # Add document summary
            report.append("## Document Summary")
            report.append(f"- Pages: {self.content['page_count']}")
            report.append(f"- Metadata: {self.content['metadata']}\n")
            
            # Add business rules
            report.append("## Business Rules")
            rules_by_category = {}
            for rule in self.rules:
                category = rule["category"]
                if category not in rules_by_category:
                    rules_by_category[category] = []
                rules_by_category[category].append(rule)
            
            for category, rules in rules_by_category.items():
                report.append(f"\n### {category}")
                for rule in rules:
                    report.append(f"- {rule['rule']} (Page {rule['page']})")
            
            # Add implementation plan
            report.append("\n## Implementation Plan")
            
            # Database section
            report.append("\n### Database")
            report.append("#### Stored Procedures")
            for proc in self.plan['database']['stored_procedures']:
                report.append(f"- **{proc['name']}**")
                report.append(f"  - Purpose: {proc['purpose']}")
                report.append(f"  - Parameters: {', '.join(proc['parameters'])}")
            
            report.append("\n#### Tables")
            for table in self.plan['database']['tables']:
                report.append(f"- {table}")
            
            # API section
            report.append("\n### API")
            for endpoint in self.plan['api']['endpoints']:
                report.append(f"- **{endpoint['method']} {endpoint['path']}**")
                report.append(f"  - Purpose: {endpoint['purpose']}")
            
            # Services section
            report.append("\n### Services")
            for module in self.plan['services']['modules']:
                report.append(f"#### {module['name']}")
                report.append("Methods:")
                for method in module['methods']:
                    report.append(f"- {method}")
            
            # Validation section
            report.append("\n### Validation")
            for rule in self.plan['validation']['rules']:
                report.append(f"#### {rule['field']}")
                report.append("Validations:")
                for validation in rule['validations']:
                    report.append(f"- {validation}")
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise