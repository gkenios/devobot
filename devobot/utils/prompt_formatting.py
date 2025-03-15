def format_prompt(prompt: str, **kwargs) -> str:
    for key, value in kwargs.items():
        if not isinstance(value, str):
            value = str(value)
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt
