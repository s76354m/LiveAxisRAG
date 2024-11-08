# Project Service Area Management

## Setup
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
Create .env file with:
```
DATABASE_URL=mssql+pyodbc:///?odbc_connect=...
API_VERSION=v1
DEBUG=True
```

4. Run tests:
```bash
pytest
```

5. Start API:
```bash
uvicorn src.api.main:app --reload
```

## API Documentation
Access at: http://localhost:8000/docs