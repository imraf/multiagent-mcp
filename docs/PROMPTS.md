# System Prompts Documentation

This document serves as a registry for the AI prompts used within the `multiagent-mcp` system. These prompts are defined in `src/mcp_server/prompts.py`.

## 1. Compose Dunning Email

*   **ID**: `compose_dunning_email`
*   **Description**: Generates a polite but firm payment reminder email for an overdue invoice.
*   **Goal**: To recover debt while maintaining customer relationship.

### Arguments

| Name | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `customer_name` | String | Name of the customer | Yes |
| `invoice_number` | String | Invoice number (e.g. INV-1001) | Yes |
| `amount_due` | String | Total amount due | Yes |
| `due_date` | String | Date the invoice was due | Yes |
| `tone` | String | Tone of the email (polite, firm, urgent) | No |

### Template Logic

The template dynamically adjusts based on the `tone` argument:
*   **Default/Polite**: "If you have already sent the payment, please disregard this email."
*   **Firm**: "We request that you settle this outstanding amount immediately."
*   **Urgent**: "URGENT: This invoice is significantly overdue."

---

## 2. Financial Summary

*   **ID**: `financial_summary`
*   **Description**: Generates a summary of outstanding debt for a customer.
*   **Goal**: Provide a quick snapshot for account managers or for inclusion in reports.

### Arguments

| Name | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `customer_name` | String | Name of the customer | Yes |
| `total_outstanding` | String | Total amount outstanding | Yes |
| `overdue_invoices` | List[Dict] | List of overdue invoices | Yes |

### Template Structure

1.  **Header**: Customer Name.
2.  **Summary**: Total Debt.
3.  **List**: Bullet points of overdue invoices (Number, Amount, Days Overdue).
4.  **Analysis**: Brief automated analysis (e.g., "Good standing" vs "Immediate follow-up").
