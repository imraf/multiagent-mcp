from mcp_core.prompt import Prompt, PromptArgument, PromptManager


def register_advanced_prompts(prompt_manager: PromptManager):
    """
    Registers advanced primitives prompts.
    """

    # 1. compose_dunning_email: Context-aware payment reminders
    dunning_email_prompt = Prompt(
        name="compose_dunning_email",
        description="Generates a polite but firm payment reminder email for an overdue invoice.",
        arguments=[
            PromptArgument(name="customer_name", description="Name of the customer"),
            PromptArgument(name="invoice_number", description="Invoice number (e.g. INV-1001)"),
            PromptArgument(name="amount_due", description="Total amount due"),
            PromptArgument(name="due_date", description="Date the invoice was due"),
            PromptArgument(
                name="tone", description="Tone of the email (polite, firm, urgent)", required=False
            ),
        ],
        template="""
Subject: Payment Reminder: Invoice {{ invoice_number }}

Dear {{ customer_name }},

This is a reminder that payment for invoice {{ invoice_number }} (Amount: {{ amount_due }}) was due on {{ due_date }}.

{% if tone == 'firm' %}
We request that you settle this outstanding amount immediately to avoid any service interruptions.
{% elif tone == 'urgent' %}
URGENT: This invoice is significantly overdue. Please remit payment immediately.
{% else %}
If you have already sent the payment, please disregard this email. Otherwise, we would appreciate it if you could arrange payment at your earliest convenience.
{% endif %}

Thank you for your business.

Sincerely,
The Finance Team
""",
    )
    prompt_manager.register_prompt(dunning_email_prompt)

    # 2. financial_summary: AI-ready summary of outstanding debt
    financial_summary_prompt = Prompt(
        name="financial_summary",
        description="Generates a summary of outstanding debt for a customer.",
        arguments=[
            PromptArgument(name="customer_name", description="Name of the customer"),
            PromptArgument(name="total_outstanding", description="Total amount outstanding"),
            PromptArgument(
                name="overdue_invoices",
                description="List of overdue invoices (dicts with 'number', 'amount', 'days_overdue')",
            ),
        ],
        template="""
FINANCIAL SUMMARY FOR: {{ customer_name }}
------------------------------------------

Total Outstanding Debt: {{ total_outstanding }}

Overdue Invoices:
{% for invoice in overdue_invoices %}
- Invoice {{ invoice.number }}: {{ invoice.amount }} ({{ invoice.days_overdue }} days overdue)
{% else %}
No overdue invoices.
{% endfor %}

Analysis:
{% if overdue_invoices|length > 0 %}
This customer has {{ overdue_invoices|length }} overdue invoices. Immediate follow-up is recommended.
{% else %}
This customer is in good standing.
{% endif %}
""",
    )
    prompt_manager.register_prompt(financial_summary_prompt)
