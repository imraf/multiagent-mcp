# Transport Module (`mcp_transport`)

The `mcp_transport` module abstracts the communication mechanism, allowing the agent to communicate over different protocols.

## Supported Transports

### SSE (Server-Sent Events)
Used for real-time communication over HTTP. Ideal for web-based clients and integrations that require streaming responses.

### Stdio
Standard Input/Output transport. This is essential for running the agent as a local process that can be piped into other tools or orchestrators.
