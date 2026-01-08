class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GitCloneError(AnalysisError):
    """Raised when git clone fails"""
    pass


class GitBlameError(AnalysisError):
    """Raised when git blame operation fails"""
    pass


class AIServiceError(AnalysisError):
    """Raised when AI API call fails"""
    pass


class CallbackError(AnalysisError):
    """Raised when callback to Spring fails"""
    pass
