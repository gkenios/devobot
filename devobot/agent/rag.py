from langchain_core.language_models.chat_models import BaseChatModel

from ._common import State
from devobot.services.database_vector import VectorDB


def rag(
    state: State,
    vector_db: VectorDB,
    llm: BaseChatModel,
    prompt: str,
    number_of_docs: int = 3,
) -> str:
    question = state["question"]

    # Retrieve documents
    retrieve = vector_db.search(question, k=number_of_docs)
    context = "\n\n".join(retrieve)

    # Generate response
    formated_prompt = prompt.format(question=question, context=context)
    response = llm.invoke(formated_prompt)
    return State(question=question, answer=response.content)
