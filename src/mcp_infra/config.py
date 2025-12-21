import os
from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import yaml

class LogConfig(BaseSettings):
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(default="json", description="Logging format: json or text")
    file_path: Optional[str] = Field(default=None, description="Path to log file")

class AppConfig(BaseSettings):
    environment: str = Field(default="development", description="Environment: development, production, test")
    debug: bool = Field(default=False, description="Debug mode")
    service_name: str = Field(default="mcp-agent", description="Name of the service")

class Config(BaseSettings):
    app: AppConfig = Field(default_factory=AppConfig)
    logging: LogConfig = Field(default_factory=LogConfig)

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            env_settings,
            init_settings,
            dotenv_settings,
            file_secret_settings,
        )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """
        Load configuration with hierarchy:
        1. Environment variables (highest priority, handled by Pydantic)
        2. YAML file
        3. Defaults (lowest priority)
        """
        # Start with defaults
        config_data = {}

        # Load from YAML if provided and exists
        if config_path and config_path.exists():
            with open(config_path, "r") as f:
                yaml_data = yaml.safe_load(f)
                if yaml_data:
                    config_data.update(yaml_data)
        
        # Determine strictness based on whether we found a file
        # If we have yaml data, we pass it to init. 
        # Pydantic Settings will overlay env vars on top of passed data.
        return cls(**config_data)
