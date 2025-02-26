from enum import Enum

from .yaml_config import Config, embeddings, llm
from agent import graph_node, rag

from services.database_vector import ChromaVectorDB


wrapped_rag = graph_node(
    rag,
    vector_db=ChromaVectorDB(collection_name="faq", embeddings=embeddings),
    llm=llm,
    prompt=Config.config["agent"]["rag"]["prompt"],
)


class AgentNode(Enum):
    rag = wrapped_rag
