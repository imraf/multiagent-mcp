import multiprocessing
from decimal import Decimal
from typing import Any

from .invoice_service import InvoiceService
from .models import Invoice, InvoiceItem


def _process_single_invoice_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Helper function to process a single invoice data dict.
    This must be a top-level function to be picklable by multiprocessing.

    Expected data format:
    {
        "customer_id": str,
        "items": List[Dict[str, Any]], # each with description, quantity, unit_price
        "tax_rate": float
    }
    """
    try:
        # Simulate CPU intensive work if needed, or just validate/transform
        customer_id = data["customer_id"]
        tax_rate = Decimal(str(data.get("tax_rate", 0.0)))

        items = []
        for item_data in data["items"]:
            items.append(
                InvoiceItem(
                    description=item_data["description"],
                    quantity=item_data["quantity"],
                    unit_price=Decimal(str(item_data["unit_price"])),
                )
            )

        return {"success": True, "customer_id": customer_id, "items": items, "tax_rate": tax_rate}
    except Exception as e:
        return {"success": False, "error": str(e), "data": data}


class BatchInvoiceProcessor:
    """
    Handles batch processing of invoices using multiprocessing for CPU-bound tasks
    (like heavy validation or data transformation before creation).
    """

    def __init__(self, invoice_service: InvoiceService, processes: int | None = None):
        self.invoice_service = invoice_service
        self.processes = processes or multiprocessing.cpu_count()

    def process_batch(self, batch_data: list[dict[str, Any]]) -> list[Invoice]:
        """
        Process a batch of invoice data and create drafts.

        Args:
            batch_data: List of dictionaries containing invoice data.

        Returns:
            List of created Invoice objects.
        """
        # 1. Parallel validation/transformation
        with multiprocessing.Pool(processes=self.processes) as pool:
            results = pool.map(_process_single_invoice_data, batch_data)

        # 2. Sequential persistence (IO-bound, usually safer to do in main process
        #    or use a specialized writer, here we keep it simple)
        created_invoices = []
        for res in results:
            if res["success"]:
                invoice = self.invoice_service.create_draft(
                    customer_id=res["customer_id"], items=res["items"], tax_rate=res["tax_rate"]
                )
                created_invoices.append(invoice)
            else:
                # Log error or handle failure
                # For now we skip
                pass

        return created_invoices
