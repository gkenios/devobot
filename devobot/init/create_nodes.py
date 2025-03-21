from .yaml_processing import Config, embeddings, llm
from devobot.agent import NodeFunctionType, node_wrapper
import devobot.agent.nodes
from devobot.config import AgentNodeConfig
from devobot.services.database_vector import ChromaVectorDB


def create_dynamic_nodes(
    agent_config: list[AgentNodeConfig],
) -> dict[str, NodeFunctionType]:
    nodes = dict()
    for node in agent_config:
        if node.function.lower() in ["start", "end"]:
            continue

        func: NodeFunctionType = getattr(devobot.agent.nodes, node.function)
        func_params = node.function_params or dict()

        if "vector_db" in func.__code__.co_varnames:
            func_params["vector_db"] = ChromaVectorDB(
                collection_name="faq",
                embeddings=embeddings,  # type: ignore
            )
        if "llm" in func.__code__.co_varnames:
            func_params["llm"] = llm

        nodes[node.id] = node_wrapper(func, config=node, **func_params)
    return nodes


def get_end_nodes(agent_config: list[AgentNodeConfig]) -> list[str]:
    end_nodes = []
    for node in agent_config:
        if node.next and node.next.lower() == "end":
            end_nodes.append(node.id)
    return end_nodes


end_nodes = get_end_nodes(agent_config=Config.config.agent)
AgentNodes: dict[str, NodeFunctionType] = create_dynamic_nodes(
    agent_config=Config.config.agent
)
