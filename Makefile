.PHONY: install test lint clean build-docs run-sse

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

clean:
	rm -rf dist build *.egg-info .pytest_cache .ruff_cache

build-docs:
	mkdocs build

run-sse:
	uvicorn src.mcp_server.main:app --reload
