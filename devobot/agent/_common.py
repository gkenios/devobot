from dataclasses import dataclass
from typing import Any, Self

from config import AgentNodeConfig


@dataclass
class NodeState:
    config: AgentNodeConfig
    input: str
    output: str | None = None

    def __or__(self, other: Self) -> Self:
        if not isinstance(other, NodeState):
            raise ValueError("Can only add NodeState objects")

        config = other.config
        input = self.input or other.input
        output = self.output or other.output
        return NodeState(config=config, input=input, output=output)


@dataclass
class State:
    lineage: list[NodeState]
    input: str
    output: str | None = None
    other: Any | None = None


def graph_node(func, config: AgentNodeConfig, **wrapper_kwargs):
    async def wrapper(*args, **kwargs):
        state: State = wrapper_kwargs.get("state")
        if not state:
            state = args[0]

        if not state.lineage:
            node_input = state.input
        else:
            node_input = state.lineage[-1].output

        before_state = NodeState(
            config=config,
            input=node_input,
        )
        state.lineage.append(before_state)

        result = func(*args, **kwargs, **wrapper_kwargs)
        result = result or before_state

        # If it's an async generator
        if hasattr(result, "__aiter__"):
            async for item in result:
                # Stream each yielded value
                yield item
        else:
            # Yield final result
            yield await result

    return wrapper
