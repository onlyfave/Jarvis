# src/tests/test_brain.py
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from ..services.brain import JarvisBrain

class MockResponse:
    def __init__(self, text):
        self.content = [type('Content', (), {'text': text})]

@pytest.fixture
def mock_client():
    """Create a mock client."""
    client = MagicMock()
    client.messages = MagicMock()
    client.messages.create = AsyncMock(return_value=MockResponse("Test response"))
    return client

@pytest.fixture
def brain(mock_client):
    """Create a JarvisBrain instance with a mock client."""
    return JarvisBrain(client=mock_client)

@pytest.mark.asyncio
async def test_process_command_success(brain):
    """Test successful command processing."""
    response = await brain.process_command("Test command")
    assert response["success"] is True
    assert "response" in response["data"]
    assert response["data"]["response"] == "Test response"

@pytest.mark.asyncio
async def test_process_command_with_context(brain):
    """Test command processing with additional context."""
    context = {"timezone": "UTC"}
    response = await brain.process_command("Test command", context)
    assert response["success"] is True
    assert "response" in response["data"]
    assert response["data"]["response"] == "Test response"

def test_conversation_history_management(brain):
    """Test conversation history is properly managed."""
    brain._update_conversation_history("Test command", "Test response")
    assert len(brain.conversation_history) == 2
    assert brain.conversation_history[0]["content"] == "Test command"
    assert brain.conversation_history[1]["content"] == "Test response"

def test_system_prompt_management(brain):
    """Test system prompt management."""
    initial_count = len(brain.system_prompts)
    brain.add_to_system_prompt("New capability: Testing")
    assert len(brain.system_prompts) == initial_count + 1
    assert brain.system_prompts[-1]["content"] == "New capability: Testing"

def test_clear_conversation_history(brain):
    """Test clearing conversation history."""
    brain._update_conversation_history("Test command", "Test response")
    assert len(brain.conversation_history) > 0
    brain.clear_conversation_history()
    assert len(brain.conversation_history) == 0

def test_prepare_messages_with_context(brain):
    """Test message preparation with context."""
    command = "Test command"
    context = {"key": "value"}
    messages = brain._prepare_messages(command, context)
    assert len(messages) > len(brain.system_prompts)
    assert any("context" in str(m["content"]).lower() for m in messages)
