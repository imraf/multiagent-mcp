from mcp_infra.config import Config


def test_config_defaults():
    """Test default values."""
    config = Config()
    assert config.app.environment == "development"
    assert config.app.debug is False
    assert config.logging.level == "INFO"

def test_config_env_vars(monkeypatch):
    """Test environment variable overrides."""
    monkeypatch.setenv("MCP_APP__ENVIRONMENT", "production")
    monkeypatch.setenv("MCP_APP__DEBUG", "true")
    monkeypatch.setenv("MCP_LOGGING__LEVEL", "DEBUG")

    config = Config()
    assert config.app.environment == "production"
    assert config.app.debug is True
    assert config.logging.level == "DEBUG"

def test_config_yaml_loading(tmp_path):
    """Test loading from YAML file."""
    config_file = tmp_path / "config.yaml"
    content = """
    app:
      service_name: "test-service"
      environment: "staging"
    logging:
      level: "WARNING"
    """
    config_file.write_text(content)

    config = Config.load(config_file)
    assert config.app.service_name == "test-service"
    assert config.app.environment == "staging"
    assert config.logging.level == "WARNING"
    # defaults preserved
    assert config.app.debug is False

def test_config_hierarchy(tmp_path, monkeypatch):
    """Test Env Vars > YAML > Defaults hierarchy."""
    # 1. Setup YAML
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
    app:
      environment: "yaml-env"
      service_name: "yaml-service"
    """)

    # 2. Setup Env Var (should override YAML)
    monkeypatch.setenv("MCP_APP__ENVIRONMENT", "env-env")

    # 3. Load
    config = Config.load(config_file)

    # Check hierarchy
    assert config.app.environment == "env-env"  # Env wins
    assert config.app.service_name == "yaml-service"  # YAML wins over default
    assert config.app.debug is False  # Default remains
