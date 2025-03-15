from datetime import date, datetime
from typing import AsyncGenerator

from langchain_core.language_models.chat_models import BaseChatModel

from utils import format_prompt
from ._common import NodeInteraction, State


async def classify(
    state: State,
    llm: BaseChatModel,
    prompt: str,
    schema: dict,
    required: list[str],
) -> AsyncGenerator[NodeInteraction, None]:
    question = state.input

    # Potentially relevant information
    today = date.today()
    time = datetime.now()
    formatted_prompt = format_prompt(prompt, today=today, time=time)

    json_schema = {
        "title": "Classify",
        "type": "object",
        "description": formatted_prompt,
        "properties": schema,
        "required": required,
    }

    structured_llm = llm.with_structured_output(json_schema)
    answer = await structured_llm.ainvoke(question)
    return NodeInteraction(input=question, output=answer)
