from enum import Enum
from typing import Callable

from .yaml_processing import Config, embeddings, llm
import agent
from config import YamlConfig
from services.database_vector import ChromaVectorDB


def create_dynamic_nodes(config: YamlConfig) -> None:
    nodes = dict()
    for node in config.agent:
        if node.function.lower() in ["start", "end"]:
            continue

        func: Callable = getattr(agent, node.function)
        func_params = node.function_params

        if "vector_db" in func.__code__.co_varnames:
            func_params["vector_db"] = ChromaVectorDB(
                collection_name="faq",
                embeddings=embeddings,
            )
        if "llm" in func.__code__.co_varnames:
            func_params["llm"] = llm

        nodes[node.id] = agent.graph_node(func, config=node, **func_params)
    return nodes


AgentNode = Enum("AgentNode", create_dynamic_nodes(Config.config))  # type: ignore
