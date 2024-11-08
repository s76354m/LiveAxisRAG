import pytest
from src.utils.performance import PerformanceMonitor

def test_performance_monitor():
    """Test performance monitoring"""
    monitor = PerformanceMonitor()
    
    with monitor.measure("test_operation"):
        # Simulate some work
        for _ in range(1000000):
            pass
    
    metric = monitor.get_metric("test_operation")
    assert metric > 0
    assert isinstance(metric, float)
    
    # Test clear metrics
    monitor.clear_metrics()
    assert monitor.get_metric("test_operation") == 0.0