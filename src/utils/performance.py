import time
from functools import wraps
from typing import Callable, Any, Dict
import logging

logger = logging.getLogger(__name__)

def measure_time(func: Callable) -> Callable:
    """Decorator to measure procedure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if isinstance(result, dict):
            result['execution_time'] = f"{execution_time:.3f}s"
        
        return result
    return wrapper 