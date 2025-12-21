# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install the package
RUN pip install --no-cache-dir -e .

# Expose the port the app runs on
EXPOSE 8000

# Run the SSE server by default
CMD ["uvicorn", "src.mcp_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
