# SwarmRAG: Multi-Agent Document Analysis System

## Overview
SwarmRAG is an advanced document analysis system that employs multiple specialized AI agents to process, analyze, and generate comprehensive technical reports from PDF documents. The system uses a swarm of agents powered by Anthropic's Claude model to provide detailed, accurate, and structured analysis.

## Features

### 1. Intelligent Document Processing
- PDF text extraction with page limit controls
- Smart text chunking and vectorization
- Efficient caching system for processed documents
- Progress tracking and logging
- Batch processing for large documents

### 2. Multi-Agent Architecture

#### Reader Agent
- Specializes in initial document comprehension
- Extracts key technical information
- Identifies core system components
- Recognizes technical requirements
- Maps document structure and relationships

#### Analyzer Agent
- Performs deep technical analysis
- Evaluates architectural decisions
- Identifies implementation patterns
- Assesses technical feasibility
- Provides risk analysis
- Recommends best practices

#### Report Agent
- Generates structured technical reports
- Customizable section organization
- Maintains consistent formatting
- Includes detailed examples and code snippets
- Supports configurable report length

#### Review Agent
- Validates technical accuracy
- Ensures completeness
- Verifies implementation feasibility
- Checks security considerations
- Provides revision recommendations
- Maintains quality control

### 3. Advanced Features
- Vector store caching for improved performance
- Automatic retry mechanism for API calls
- Progressive document processing
- Configurable report sections
- Detailed logging system
- Error handling and recovery
- Batch processing optimization

## Installation

### Prerequisites
- Python 3.9+
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/SwarmRAG.git
cd SwarmRAG
```

### Step 2: Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
MAX_PAGES=None  # or specific number
MAX_REPORT_SECTIONS=5  # or your preferred number
```

## Usage

### Basic Usage
```python
from src.coordinator import SwarmCoordinator

async def process_document(pdf_path: str):
    coordinator = SwarmCoordinator()
    results = await coordinator.process_document(pdf_path)
    return results
```

### Configuration Options

#### Page Limits
```python
# In config.py or via environment variables
MAX_PAGES = None  # Process all pages
MAX_PAGES = 50    # Limit to 50 pages
```

#### Report Sections
```python
# Configure sections in config.py
REPORT_SECTIONS = [
    "Executive Summary",
    "System Architecture",
    "Technical Requirements",
    # Add or remove sections as needed
]
```

#### Processing Settings
```python
# Adjust chunk size and overlap for document processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

## Project Structure
```
SwarmRAG/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── coordinator.py
│   ├── config.py
│   ├── document_processor.py
│   └── agents/
│       ├── __init__.py
│       ├── base_agent.py
│       ├── reader_agent.py
│       ├── analyzer_agent.py
│       ├── report_agent.py
│       └── review_agent.py
├── cache/
├── logs/
├── reports/
├── requirements.txt
├── .env
└── README.md
```

## Use Cases

### 1. Technical Documentation Analysis
- Process technical specifications
- Analyze system architecture documents
- Review implementation guides
- Evaluate API documentation

### 2. Project Documentation
- Generate implementation reports
- Create technical summaries
- Analyze requirements documents
- Produce architectural reviews

### 3. Code Documentation
- Analyze code documentation
- Generate implementation guides
- Review technical specifications
- Create API documentation

## Performance Considerations

### Optimization Tips
1. Use appropriate chunk sizes for your documents
2. Enable caching for frequently processed documents
3. Configure page limits for large documents
4. Adjust report sections based on needs
5. Monitor and tune retry settings

### Resource Requirements
- Memory: 4GB+ recommended
- Storage: Depends on document size and cache settings
- API Usage: Varies based on document size and complexity

## Error Handling
The system includes comprehensive error handling:
- Automatic retries for API failures
- Cache corruption recovery
- Document processing error handling
- Agent communication error recovery

## Logging
Detailed logging is available in the `logs` directory:
- Processing progress
- Agent interactions
- Error tracking
- Performance metrics

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Your chosen license]

## Support
[Your support information]

## Acknowledgments
- Anthropic's Claude for AI capabilities
- LangChain for embeddings and vector store
- FAISS for vector similarity search
- PyMuPDF for PDF processing