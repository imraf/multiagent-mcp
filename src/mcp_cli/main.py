import typer
from rich.console import Console
from rich.table import Table

from mcp_client.client import InvoiceStatus, InvoicingClient

app = typer.Typer(help="MCP Invoice CLI")
console = Console()
client = InvoicingClient()


@app.command()
def new(customer_id: str, description: str, quantity: int, price: float) -> None:
    """
    Create a new invoice.
    """
    console.print(f"[bold blue]Creating invoice for customer {customer_id}...[/bold blue]")
    try:
        items = [{"description": description, "quantity": quantity, "unit_price": price}]
        invoice = client.create_invoice(customer_id, items)

        table = Table(title="Invoice Created")
        table.add_column("ID", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Total", justify="right", style="green")

        table.add_row(invoice.id, invoice.status.value, f"${invoice.total_amount:.2f}")
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


@app.command()
def list(status: str | None = None) -> None:
    """
    List invoices, optionally filtered by status.
    """
    # map string to enum
    status_enum = None
    if status:
        try:
            status_enum = InvoiceStatus(status.lower())
        except ValueError:
            console.print(f"[red]Invalid status: {status}[/red]")
            return

    invoices = client.list_invoices(status_enum)

    if not invoices:
        console.print("No invoices found.")
        return

    table = Table(title=f"Invoices ({status or 'All'})")
    table.add_column("ID", style="cyan")
    table.add_column("Customer", style="white")
    table.add_column("Status", style="magenta")
    table.add_column("Total", justify="right", style="green")

    for inv in invoices:
        table.add_row(inv.id, inv.customer_id, inv.status.value, f"${inv.total_amount:.2f}")

    console.print(table)


@app.command()
def customer_add(
    name: str, email: str, vat_id: str | None = None, address: str | None = None
) -> None:
    """
    Add a new customer.
    """
    try:
        customer = client.register_customer(name, email, vat_id, address)
        console.print(f"[bold green]Customer added:[/bold green] {customer.name} ({customer.id})")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    app()
