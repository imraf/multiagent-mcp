import pytest

from mcp_core.prompt import Prompt, PromptArgument, PromptManager


@pytest.fixture
def prompt_manager():
    return PromptManager()


def test_prompt_registration(prompt_manager):
    prompt = Prompt(
        name="test_prompt", template="Hello {{ name }}!", arguments=[PromptArgument(name="name")]
    )

    prompt_manager.register_prompt(prompt)
    assert prompt_manager.get_prompt("test_prompt") == prompt
    assert len(prompt_manager.list_prompts()) == 1


def test_prompt_rendering(prompt_manager):
    prompt = Prompt(
        name="greeting",
        template="Hello {{ name }}, welcome to {{ place }}!",
        arguments=[PromptArgument(name="name"), PromptArgument(name="place", required=False)],
    )
    prompt_manager.register_prompt(prompt)

    # Render with all args
    result = prompt_manager.render_prompt("greeting", {"name": "Alice", "place": "Wonderland"})
    assert result == "Hello Alice, welcome to Wonderland!"

    # Render with missing optional arg (Jinja handles missing as empty/none typically, but logic depends on template)
    # Our simple template just prints blank for missing vars
    result = prompt_manager.render_prompt("greeting", {"name": "Bob"})
    assert "Hello Bob" in result


def test_prompt_rendering_missing_required(prompt_manager):
    prompt = Prompt(
        name="required_arg",
        template="Value: {{ val }}",
        arguments=[PromptArgument(name="val", required=True)],
    )
    prompt_manager.register_prompt(prompt)

    with pytest.raises(ValueError, match="Missing required argument: val"):
        prompt_manager.render_prompt("required_arg", {})


def test_jinja2_logic(prompt_manager):
    prompt = Prompt(
        name="logic",
        template="{% if val > 10 %}High{% else %}Low{% endif %}",
        arguments=[PromptArgument(name="val")],
    )
    prompt_manager.register_prompt(prompt)

    assert prompt_manager.render_prompt("logic", {"val": 15}) == "High"
    assert prompt_manager.render_prompt("logic", {"val": 5}) == "Low"
