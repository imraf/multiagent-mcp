# Operational Costs and Estimates

This document outlines the estimated operational costs for running the `multiagent-mcp` system, specifically focusing on LLM token usage and infrastructure.

## LLM Token Usage Estimates

The system primarily uses LLMs for generating invoice-related communications and summaries. Below are the estimated costs per operation, assuming a standard pricing model (e.g., GPT-4o or similar: $2.50/1M input, $10.00/1M output).

### 1. Payment Reminder Email (`compose_dunning_email`)

*   **Input Context**: ~200 tokens (Template + Variables like Customer Name, Invoice #, Amount)
*   **Output Generation**: ~150 tokens (The generated email)
*   **Frequency**: ~5 per active overdue customer per month.

**Cost per execution:**
*   Input: (200 / 1,000,000) * $2.50 = $0.0005
*   Output: (150 / 1,000,000) * $10.00 = $0.0015
*   **Total**: ~$0.002 per email.

### 2. Financial Summary (`financial_summary`)

*   **Input Context**: ~500 tokens (List of overdue invoices, history)
*   **Output Generation**: ~200 tokens (Summary and analysis)
*   **Frequency**: ~1 per customer per month (end of month report).

**Cost per execution:**
*   Input: (500 / 1,000,000) * $2.50 = $0.00125
*   Output: (200 / 1,000,000) * $10.00 = $0.0020
*   **Total**: ~$0.00325 per summary.

## Monthly Projection (Example)

For a small business with 100 active customers, 20% of whom have overdue invoices:

*   **Dunning Emails**: 20 customers * 3 reminders = 60 emails * $0.002 = $0.12
*   **Summaries**: 100 customers * 1 summary = 100 summaries * $0.00325 = $0.325

**Total Estimated Monthly LLM Cost**: ~$0.45

## Infrastructure Costs

*   **Compute**: Can run on a small VPS or Serverless instance (e.g., AWS Lambda / t3.micro). ~$5-10/month.
*   **Storage**: JSON file storage is negligible for small scale. S3/Blob storage for backups: <$0.10/month.

**Total Estimated Infrastructure**: ~$5.00 - $10.00 / month.

## Total Budget

See `budget.csv` for a detailed breakdown of development and operational budgets.
