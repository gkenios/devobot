from datetime import date, datetime

from langchain_core.language_models.chat_models import BaseChatModel

from .common import NodeInteraction, NodeOutputType, State
from devobot.utils import format_prompt


async def classify(
    state: State,
    llm: BaseChatModel,
    prompt: str,
    schema: dict,
    required: list[str],
) -> NodeOutputType:
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
