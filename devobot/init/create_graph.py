from typing import Type

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from .create_nodes import AgentNodes
from .yaml_processing import Config
from devobot.agent import NodeFunctionType, State
from devobot.config import AgentNodeConfig


def get_node_name(node_name: str) -> str:
    """Adjusts the node name for start and end nodes."""
    node_name = node_name.lower()
    if node_name == "start":
        return START
    elif node_name == "end":
        return END
    return node_name


def create_dynamic_graph(
    state: Type[State],
    agent_nodes: dict[str, NodeFunctionType],
    agent_config: list[AgentNodeConfig],
) -> CompiledStateGraph:
    builder = StateGraph(state)

    # Add nodes
    for node_id, node in agent_nodes.items():
        builder.add_node(node=node_id, action=node)

    for node in agent_config:
        current_node = get_node_name(node.id)

        # If 'next' is a string, convert to list
        if isinstance(node.next, str):
            next_nodes = [node.next]
        elif isinstance(node.next, list):
            next_nodes = node.next
        else:
            next_nodes = []

        # Add edges
        for next_node in next_nodes:
            builder.add_edge(current_node, get_node_name(next_node))

        # Add conditional edges
        if node.next_conditional:
            key = node.next_conditional.key
            # Create a mapping of output to node
            mapping = {
                output: get_node_name(node_name)
                for output, node_name in node.next_conditional.mapping.items()
            }
            builder.add_conditional_edges(
                source=current_node,
                path=lambda state: state.lineage[-1]["output"][key],
                path_map=mapping,
            )
    return builder.compile()


graph = create_dynamic_graph(State, AgentNodes, Config.config.agent)
