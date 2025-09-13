"""
Custom exceptions for the Python Code Check System.
"""


class CodeCheckError(Exception):
    """Base exception for code checking errors."""

    pass


class StudentNotFoundError(CodeCheckError):
    """Raised when student is not found."""

    pass


class TaskNotFoundError(CodeCheckError):
    """Raised when task is not found."""

    pass


class SolutionNotFoundError(CodeCheckError):
    """Raised when solution is not found."""

    pass


class InvalidUserTypeError(CodeCheckError):
    """Raised when user type is invalid for the operation."""

    pass


class CodeExecutionError(CodeCheckError):
    """Raised when code execution fails."""

    pass
