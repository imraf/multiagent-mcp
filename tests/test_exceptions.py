from mcp_infra.exceptions import (
    ConfigurationError,
    InfrastructureError,
    MCPException,
    ServiceUnavailableError,
)


def test_mcp_exception_base():
    """Test base exception functionality."""
    err = MCPException("Something went wrong", details={"foo": "bar"})
    response = err.to_response(request_id="123")

    assert response.error == "MCPException"
    assert response.message == "Something went wrong"
    assert response.details == {"foo": "bar"}
    assert response.request_id == "123"

def test_exception_hierarchy():
    """Test inheritance structure."""
    assert issubclass(ConfigurationError, MCPException)
    assert issubclass(ServiceUnavailableError, InfrastructureError)
    assert issubclass(InfrastructureError, MCPException)

def test_nested_exceptions():
    """Test wrapping original errors."""
    original = ValueError("bad value")
    err = ConfigurationError("Invalid config", original_error=original)

    assert err.original_error == original
    assert str(err) == "Invalid config"

    # Response shouldn't leak original error stack trace by default,
    # but application logic might decide to log it.
    resp = err.to_response()
    assert resp.error == "ConfigurationError"
    assert resp.message == "Invalid config"
