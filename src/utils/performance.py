import time
from typing import Dict
from contextlib import contextmanager

class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, float] = {}

    @contextmanager
    def measure(self, name: str):
        """Measure execution time of a code block"""
        start = time.time()
        try:
            yield
        finally:
            end = time.time()
            self.metrics[name] = end - start

    def get_metric(self, name: str) -> float:
        """Get metric by name"""
        return self.metrics.get(name, 0.0)

    def clear_metrics(self):
        """Clear all metrics"""
        self.metrics.clear()