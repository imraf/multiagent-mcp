import json
import tempfile
from pathlib import Path

from mcp_infra.config import LogConfig
from mcp_infra.logging import configure_logging, get_logger


def test_logging_configuration(capsys):
    """Test that logging is configured correctly and outputs JSON."""
    config = LogConfig(level="INFO")
    configure_logging(config, service_name="test-service")

    logger = get_logger("test_logger")
    logger.info("hello world", key="value")

    # Capture stdout
    captured = capsys.readouterr()
    log_output = captured.out.strip()

    # Verify JSON structure
    log_entry = json.loads(log_output)
    assert log_entry["event"] == "hello world"
    assert log_entry["key"] == "value"
    assert log_entry["service"] == "test-service"
    assert log_entry["level"] == "info"
    assert "timestamp" in log_entry


def test_file_logging():
    """Test that logs are written to file with rotation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "app.log"
        config = LogConfig(level="INFO", file_path=str(log_file))

        configure_logging(config, service_name="file-test")
        logger = get_logger()
        logger.info("file log test")

        assert log_file.exists()
        content = log_file.read_text()
        log_entry = json.loads(content.strip())
        assert log_entry["event"] == "file log test"
        assert log_entry["service"] == "file-test"


def test_log_level_filtering(capsys):
    """Test that logs respect the configured level."""
    config = LogConfig(level="WARNING")
    configure_logging(config)

    logger = get_logger()
    logger.info("should not show")
    logger.warning("should show")

    captured = capsys.readouterr()
    output = captured.out.strip()

    assert "should not show" not in output
    assert "should show" in output
