# C4 Architecture Diagrams

## Level 1: System Context Diagram

```mermaid
C4Context
    title System Context Diagram for MCP Invoicing System

    Person(user, "User", "A user using the CLI or Dashboard to manage invoices.")
    System(mcp_system, "MCP Invoicing System", "Allows users to create, manage, and send invoices.")
    System_Ext(email_system, "Email System", "The internal or external email system.")

    Rel(user, mcp_system, "Uses")
    Rel(mcp_system, email_system, "Sends e-mails using")
```

## Level 2: Container Diagram

```mermaid
C4Container
    title Container Diagram for MCP Invoicing System

    Person(user, "User", "A user using the CLI or Dashboard.")

    Container_Boundary(mcp, "MCP Invoicing System") {
        Container(cli, "CLI Application", "Python, Typer", "Command line interface for managing invoices.")
        Container(dashboard, "Web Dashboard", "Python, Streamlit", "Web-based dashboard for visualization.")
        Container(sdk, "Client SDK", "Python", "Provides a fluent API for interacting with the server.")
        Container(server, "MCP Server", "Python, FastAPI, SSE", "Handles requests and executes tools.")
        ContainerDb(json_db, "JSON Data Store", "JSON Files", "Stores invoices and customers.")
    }

    Rel(user, cli, "Uses")
    Rel(user, dashboard, "Uses")
    Rel(cli, sdk, "Uses")
    Rel(dashboard, sdk, "Uses")
    Rel(sdk, server, "Connects via HTTP/SSE", "JSON-RPC")
    Rel(server, json_db, "Reads/Writes")
```

## Level 3: Component Diagram (MCP Server)

```mermaid
C4Component
    title Component Diagram for MCP Server

    Container(sdk, "Client SDK", "Python", "Client library.")

    Container_Boundary(server, "MCP Server") {
        Component(transport, "Transport Layer", "SSE/HTTP", "Handles SSE connections and HTTP POSTs.")
        Component(dispatcher, "Dispatcher", "FastMCP", "Routes requests to appropriate tools.")
        Component(inv_tools, "Invoice Tools", "Python Functions", "Exposes invoice operations.")
        Component(cust_tools, "Customer Tools", "Python Functions", "Exposes customer operations.")
        Component(inv_service, "Invoice Service", "Python Class", "Business logic for invoices.")
        Component(cust_service, "Customer Service", "Python Class", "Business logic for customers.")
        Component(repo, "Repository", "JsonRepository", "Handles file I/O.")
    }

    Rel(sdk, transport, "Sends JSON-RPC")
    Rel(transport, dispatcher, "Forwards request")
    Rel(dispatcher, inv_tools, "Calls")
    Rel(dispatcher, cust_tools, "Calls")
    Rel(inv_tools, inv_service, "Uses")
    Rel(cust_tools, cust_service, "Uses")
    Rel(inv_service, repo, "Persists data")
    Rel(cust_service, repo, "Persists data")
```
