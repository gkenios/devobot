from enum import Enum

from .yaml_config import Config, embeddings, llm
from agent import classify, graph_node, rag

from services.database_vector import ChromaVectorDB


wrapped_rag = graph_node(
    rag,
    vector_db=ChromaVectorDB(collection_name="faq", embeddings=embeddings),
    llm=llm,
    prompt=Config.config["agent"]["nodes"]["rag"]["prompt"],
)

wrapped_classify = graph_node(
    classify,
    llm=llm,
    prompt=Config.config["agent"]["nodes"]["intent"]["prompt"],
    schema=Config.config["agent"]["nodes"]["intent"]["classes"],
)

class AgentNode(Enum):
    classify = wrapped_classify
    rag = wrapped_rag
