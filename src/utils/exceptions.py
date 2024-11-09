class ProjectError(Exception):
    """Base exception for project-specific errors"""
    pass

class DatabaseError(ProjectError):
    """Database-related errors"""
    pass

class ConfigurationError(Exception):
    """Raised when configuration errors occur"""
    pass

class ValidationError(ProjectError):
    """Data validation errors"""
    pass 