# Quick Start

Get your MCP agent up and running in minutes.

## Running the Agent

You can start the agent using the provided orchestrator script:

```bash
./orchestrate.sh
```

Alternatively, run the SSE server example directly:

```bash
uvicorn src.mcp_server.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## Interacting with the Agent

Once the server is running, you can interact with it using an MCP client or through the SSE endpoint `http://127.0.0.1:8000/sse`.
