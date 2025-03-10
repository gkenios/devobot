from datetime import date, datetime

from langchain_core.language_models.chat_models import BaseChatModel

from ._common import State


async def classify(
    state: State,
    llm: BaseChatModel,
    prompt: str,
    schema: dict,
    required: list[str],
) -> State:
    question = state.input

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
    return State(lineage=state.lineage, input=question, output=answer)


def format_prompt(prompt: str, **kwargs) -> str:
    for key, value in kwargs.items():
        if not isinstance(value, str):
            value = str(value)
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt
