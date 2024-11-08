class ProjectError(Exception):
    """Base exception for project-specific errors"""
    pass

class DatabaseError(ProjectError):
    """Database-related errors"""
    pass

class ConfigurationError(ProjectError):
    """Configuration-related errors"""
    pass

class ValidationError(ProjectError):
    """Data validation errors"""
    pass 