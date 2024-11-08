class ValidationError(Exception):
    """Raised when validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BusinessRuleError(Exception):
    """Raised when business rules are violated"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    """Database operation error"""
    pass
