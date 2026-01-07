# Contributing to multiagent-mcp

First off, thanks for taking the time to contribute!

## Reporting Bugs

1.  **Search** the issue tracker to ensure the bug hasn't been reported.
2.  **Open a new issue** with a clear title and detailed description.
3.  Include steps to reproduce, expected behavior, and actual behavior.

## Suggesting Enhancements

1.  **Open a new issue** describing the enhancement.
2.  Explain why this enhancement would be useful to most users.

## Pull Requests

1.  **Fork** the repo and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  Ensure the test suite passes (`pytest`).
4.  Make sure your code lints (`ruff check .`).
5.  Issue that pull request!

## Development Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -e .
    pip install ruff pytest pytest-cov
    ```
3.  Install pre-commit hooks:
    ```bash
    pre-commit install
    ```

## Style Guide

*   We use `ruff` for linting and formatting.
*   We use `mypy` for static type checking.
*   Follow PEP 8 conventions.
