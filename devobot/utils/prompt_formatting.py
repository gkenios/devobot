from datetime import date, datetime
from typing import Any


def extra_context() -> dict[str, Any]:
    """Extra information that can be help the agent get more context."""
    return {
        "today": date.today(),
        "time": datetime.now(),
    }


def format_prompt(prompt: str, **kwargs: str | Any) -> str:
    """Format the prompt with the given kwargs.

    Example:
    >>> format_prompt("Hello {name}!", name="World")
    "Hello World!"

    Args:
        prompt (str): The prompt to be formatted.
        **kwargs: The values to be replaced in the prompt.

    Returns:
        str: The formatted prompt.
    """
    for key, value in kwargs.items():
        if not isinstance(value, str):
            value = str(value)
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt


def format_prompt_with_context(prompt: str) -> str:
    """Format the prompt with the extra context."""
    return format_prompt(prompt, **extra_context())
