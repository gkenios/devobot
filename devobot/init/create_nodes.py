from .yaml_processing import Config, embeddings, llm
import devobot.agent as agent
from devobot.agent.common import NodeFunctionType, graph_node
from devobot.config import AgentNodeConfig
from devobot.services.database_vector import ChromaVectorDB


def create_dynamic_nodes(
    agent_config: list[AgentNodeConfig],
) -> dict[str, NodeFunctionType]:
    nodes = dict()
    for node in agent_config:
        if node.function.lower() in ["start", "end"]:
            continue

        func: NodeFunctionType = getattr(agent, node.function)
        func_params = node.function_params or dict()

        if "vector_db" in func.__code__.co_varnames:
            func_params["vector_db"] = ChromaVectorDB(
                collection_name="faq",
                embeddings=embeddings,  # type: ignore
            )
        if "llm" in func.__code__.co_varnames:
            func_params["llm"] = llm

        nodes[node.id] = graph_node(func, config=node, **func_params)
    return nodes


AgentNodes: dict[str, NodeFunctionType] = create_dynamic_nodes(
    agent_config=Config.config.agent
)
