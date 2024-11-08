from dataclasses import dataclass
from typing import List, Dict, Any
import random
import string

@dataclass
class TestData:
    """Test data for stored procedures"""
    project_id: str
    mileage: int
    flag: str
    state: str
    county: str

class TestDataGenerator:
    """Generate test data for stored procedures"""
    
    def __init__(self):
        self.states = ['AZ', 'CA', 'TX', 'NY', 'FL']
        self.counties = ['County1', 'County2', 'County3', 'County4']
    
    def generate_project_id(self, state: str = None) -> str:
        """Generate valid project ID"""
        state = state or random.choice(self.states)
        year = str(random.randint(2020, 2024))
        sequence = ''.join(random.choices(string.digits, k=4))
        return f"{state}CAI{year}{sequence}"
    
    def generate_test_data(self, count: int = 1) -> List[TestData]:
        """Generate multiple test data records"""
        test_data = []
        for _ in range(count):
            state = random.choice(self.states)
            test_data.append(TestData(
                project_id=self.generate_project_id(state),
                mileage=random.choice([10, 20, 30, 40, 50]),
                flag=random.choice(['1', '2', '3']),
                state=state,
                county=random.choice(self.counties)
            ))
        return test_data 