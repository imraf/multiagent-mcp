# LLM Integration Guide

This guide explains how to integrate Large Language Models (LLMs) with the MCP agent.

## Local LLM (Ollama)

To run an LLM locally, we recommend using [Ollama](https://ollama.ai/).

1.  **Install Ollama**: Follow the instructions on their website.
2.  **Pull a Model**:
    ```bash
    ollama pull llama3
    ```
3.  **Configure the Agent**:
    Update your `.env` file or environment variables:
    ```env
    MCP_LLM_PROVIDER=ollama
    MCP_OLLAMA_BASE_URL=http://localhost:11434
    MCP_OLLAMA_MODEL=llama3
    ```

## Proprietary APIs

You can also use cloud-based providers like OpenAI or Anthropic.

### OpenAI

1.  Get your API key from OpenAI.
2.  **Configure the Agent**:
    ```env
    MCP_LLM_PROVIDER=openai
    OPENAI_API_KEY=sk-...
    MCP_OPENAI_MODEL=gpt-4-turbo
    ```

### Anthropic

1.  Get your API key from Anthropic.
2.  **Configure the Agent**:
    ```env
    MCP_LLM_PROVIDER=anthropic
    ANTHROPIC_API_KEY=sk-ant-...
    MCP_ANTHROPIC_MODEL=claude-3-opus-20240229
    ```
