from dataclasses import dataclass
from typing import Any


@dataclass
class NodeConfig:
    id: str
    function: str
    function_params: dict[str, Any] | None = None
    next: str | list[str] | None = None
    next_conditional: dict[str, Any] | None = None


@dataclass
class Node:
    conf: NodeConfig
    input: str
    output: str | None = None
    other: Any | None = None


@dataclass
class State:
    lineage: list[Node]
    question: str
    answer: str | None = None


def graph_node(func, **wrapper_kwargs):
    async def wrapper(*args, **kwargs):
        result = func(*args, **kwargs, **wrapper_kwargs)

        # If it's an async generator
        if hasattr(result, "__aiter__"):
            async for item in result:
                # Stream each yielded value
                yield item
        else:
            # Yield final result
            yield await result

    return wrapper
