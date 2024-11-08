import pytest
import time
from fastapi.testclient import TestClient
from src.api.main import app

def test_api_response_time():
    """Test API endpoint performance"""
    client = TestClient(app)
    
    start_time = time.time()
    response = client.get("/project/CACAI20230001/exists")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 0.5  # Response under 500ms 