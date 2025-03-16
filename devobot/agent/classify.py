from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from .common import NodeInteraction, State
from devobot.utils import format_prompt_with_context


async def classify(
    state: State,
    llm: BaseChatModel,
    # Config parameters
    prompt: str,
    schema: dict[str, Any],
    required: list[str],
) -> NodeInteraction:
    question = state.input
    formatted_prompt = format_prompt_with_context(prompt)

    json_schema = {
        "title": "Classify",
        "type": "object",
        "description": formatted_prompt,
        "properties": schema,
        "required": required,
    }

    structured_llm = llm.with_structured_output(json_schema)
    answer = await structured_llm.ainvoke(question)
    return NodeInteraction(input=question, output=answer)  # type: ignore
