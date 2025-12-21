from typer.testing import CliRunner
from mcp_cli.main import app

runner = CliRunner()


def test_cli_new_invoice():
    # Since the client is mocked in the CLI file logic (or rather the class is used directly),
    # this tests the CLI wrapper.
    result = runner.invoke(app, ["new", "cust1", "Item1", "2", "50.0"])
    assert result.exit_code == 0
    assert "Creating invoice for customer cust1" in result.stdout
    assert "Invoice Created" in result.stdout
    assert "$100.00" in result.stdout


def test_cli_add_customer():
    result = runner.invoke(app, ["customer-add", "NewCustomer", "new@example.com"])
    assert result.exit_code == 0
    assert "Customer added" in result.stdout
    assert "NewCustomer" in result.stdout
