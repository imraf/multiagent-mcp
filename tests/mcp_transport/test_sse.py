import pytest
from fastapi.testclient import TestClient

from mcp_transport.sse import SseTransport


@pytest.mark.asyncio
async def test_sse_transport_routes():
    transport = SseTransport()
    client = TestClient(transport._app)

    # Test POST /messages without handler
    response = client.post("/messages", json={"test": "data"})
    assert response.json() == {"status": "error", "message": "No handler set"}

    # Test POST /messages with handler
    received_msgs = []

    async def handler(msg):
        received_msgs.append(msg)

    transport.set_handler(handler)

    test_msg = {"key": "value"}
    response = client.post("/messages", json=test_msg)
    assert response.status_code == 200  # noqa: PLR2004
    assert response.json() == {"status": "ok"}
    assert len(received_msgs) == 1
    assert received_msgs[0] == test_msg


@pytest.mark.asyncio
async def test_sse_transport_send():
    transport = SseTransport()

    test_msg = {"event": "test"}
    await transport.send(test_msg)

    # Verify message is in queue
    queued_msg = await transport._message_queue.get()
    assert queued_msg == test_msg
