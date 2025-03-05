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
    question = state["question"]

    today = date.today()
    time = datetime.now()
    formated_prompt = prompt.format(today=today, time=time)

    json_schema = {
        "title": "Classify",
        "type": "object",
        "description": formated_prompt,
        "properties": schema,
        "required": required,
    }
    # TODO: Deal with State
    structured_llm = llm.with_structured_output(json_schema)
    answer = await structured_llm.ainvoke(question)
    return State(question=question, answer=answer)
