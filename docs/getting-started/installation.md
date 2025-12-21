# Installation

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

## Step-by-Step Guide

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/mcp-docs.git
    cd mcp-docs
    ```

2.  **Create a virtual environment:**
    Using `uv`:
    ```bash
    uv venv
    source .venv/bin/activate
    ```
    Or using standard `venv`:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e .
    ```

4.  **Verify installation:**
    ```bash
    pytest
    ```
