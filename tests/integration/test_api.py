import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_check_project_exists():
    """Test project existence endpoint"""
    response = client.get("/project/CACAI20230001/exists")
    assert response.status_code == 200
    assert "exists" in response.json()

def test_get_service_area():
    """Test service area retrieval"""
    response = client.get("/project/CACAI20230001/service-area")
    assert response.status_code == 200
    assert "state" in response.json()
    assert "mileage" in response.json()

@pytest.mark.asyncio
async def test_project_validation():
    """Test project validation endpoint"""
    client = TestClient(app)
    
    # Test valid project
    response = client.post(
        "/project/validate",
        json={
            "project_id": "CACAI20230001",
            "region": "West",
            "service_area": {
                "state": "CA",
                "county": "Los Angeles",
                "mileage": 50.0
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["is_valid"] == True
    
    # Test invalid project
    response = client.post(
        "/project/validate",
        json={
            "project_id": "INVALID",
            "region": "Invalid",
            "service_area": {
                "state": "XX",
                "county": "Invalid",
                "mileage": -1
            }
        }
    )
    assert response.status_code == 400
    assert "error" in response.json() or "detail" in response.json()