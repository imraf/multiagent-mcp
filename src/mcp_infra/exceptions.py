from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standardized error response structure."""
    error: str = Field(..., description="Error code or type")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(default=None, description="Additional error context")
    request_id: str | None = Field(default=None, description="Tracing ID")

class MCPException(Exception):
    """Base exception for all MCP related errors."""
    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        original_error: Exception | None = None
    ):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.original_error = original_error

    def to_response(self, request_id: str | None = None) -> ErrorResponse:
        return ErrorResponse(
            error=self.__class__.__name__,
            message=self.message,
            details=self.details,
            request_id=request_id
        )

class ConfigurationError(MCPException):
    """Raised when configuration is invalid or missing."""
    pass

class InfrastructureError(MCPException):
    """Raised when underlying infrastructure fails (IO, Network, etc)."""
    pass

class ServiceUnavailableError(InfrastructureError):
    """Raised when a dependent service is unreachable."""
    pass
