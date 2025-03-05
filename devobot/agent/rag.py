from langchain_core.language_models.chat_models import BaseChatModel

from ._common import NodeState, State
from devobot.services.database_vector import VectorDB


async def rag(
    state: State,
    vector_db: VectorDB,
    llm: BaseChatModel,
    prompt: str,
    number_of_docs: int = 3,
) -> NodeState:
    """Retrieve and generate response using RAG on the given vector database.

    Defined in config file node parameters:
    - prompt: The prompt to be used for the RAG model.
    - number_of_docs: The number of documents to retrieve from the database.

    Args:
        state: The State object passed between nodes.
        vector_db: The database object to retrieve documents.
        llm: The language model to generate response.
        prompt: The prompt to be used for the RAG model.
        number_of_docs: The number of documents to retrieve from the database.

    Returns:
        State: The State object with the answer to the question.
    """
    question = state.input

    # Retrieve documents
    retrieve = vector_db.search(question, k=number_of_docs)
    context = "\n\n".join(retrieve)

    # TODO: Deal with State
    # Generate response
    formated_prompt = prompt.format(question=question, context=context)
    response = ""
    async for chunk in llm.astream(formated_prompt):
        # Yield each chunk as it arrives
        yield {"output": chunk}
        response += chunk.content

    # Yield final response
    yield State(lineage=state.lineage, input=question, output=response)
