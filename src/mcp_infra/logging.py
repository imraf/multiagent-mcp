import logging
import sys
from pathlib import Path
from typing import Any, Optional
import structlog
from mcp_infra.config import LogConfig

def configure_logging(
    config: LogConfig,
    service_name: str = "mcp-agent",
) -> None:
    """
    Configure structured logging for the application.
    Sets up:
    - JSON formatter for machine readability
    - Console handler
    - File handler (if configured)
    - Context vars (service_name)
    """
    
    # Shared processors for both structlog and stdlib logging
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # JSON renderer for final output
    json_renderer = structlog.processors.JSONRenderer()

    # Configure structlog
    structlog.configure(
        processors=processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Standard library logging configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(config.level.upper())
    
    # Clear existing handlers
    root_logger.handlers = []

    # formatter that renders the final JSON
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            json_renderer,
        ],
    )

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 2. File Handler (if path provided)
    if config.file_path:
        log_path = Path(config.file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Basic file handler - in production ideally use a rotating one,
        # but for this scope, a standard FileHandler is a good start.
        # User prompt asked for "log rotation", so let's use RotatingFileHandler.
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            config.file_path,
            maxBytes=10 * 1024 * 1024, # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Set initial context
    structlog.contextvars.bind_contextvars(service=service_name)

def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)
