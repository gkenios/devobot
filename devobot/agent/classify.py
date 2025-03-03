from langchain_core.language_models.chat_models import BaseChatModel

from ._common import State


async def classify(
    state: State,
    llm: BaseChatModel,
    prompt: str,
    schema: dict
)-> State:
    structured_llm = llm.with_structured_output(schema=schema)
    yield structured_llm.ainvoke(prompt)
