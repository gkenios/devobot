from enum import Enum

from .yaml_processing import Config, embeddings, llm
import agent
from services.database_vector import ChromaVectorDB


wrapped_rag = agent.graph_node(
    getattr(agent, Config.config.agent[2].function),
    vector_db=ChromaVectorDB(collection_name="faq", embeddings=embeddings),
    llm=llm,
    **Config.config.agent[2].function_params,
)

wrapped_classify = agent.graph_node(
    getattr(agent, Config.config.agent[1].function),
    llm=llm,
    **Config.config.agent[1].function_params,
)


class AgentNode(Enum):
    classify = wrapped_classify
    rag = wrapped_rag
