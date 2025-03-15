from dataclasses import dataclass
from typing import Any, AsyncGenerator, Callable, Concatenate

from config import AgentNodeConfig


@dataclass
class NodeState:
    config: AgentNodeConfig
    input: str
    output: str | None = None


@dataclass
class State:
    input: str
    lineage: list[NodeState]


@dataclass
class NodeInteraction:
    input: str
    output: str | None = None


def graph_node(
    func: Callable[
        Concatenate[State, ...], AsyncGenerator[NodeInteraction, None]
    ],
    config: AgentNodeConfig,
    **wrapper_kwargs: dict[str, Any],
) -> Callable[Concatenate[State, ...], AsyncGenerator[NodeInteraction, None]]:
    async def wrapper(*args, **kwargs) -> AsyncGenerator[NodeInteraction, None]:
        result = func(*args, **kwargs, **wrapper_kwargs)

        # If it's an async generator
        if hasattr(result, "__aiter__"):
            async for item in result:
                print("IT'S AN ASYNC GENERATOR")
                # Stream each yielded value
                yield item
        else:
            # Yield final result
            awaited_result: NodeInteraction = await result
            yield awaited_result

            # Get the state from the arguments
            state: State = wrapper_kwargs.get("state")
            if not state:
                state = args[0]

            # Update the lineage
            latest_update = NodeState(
                config=config,
                input=awaited_result.input,
                output=awaited_result.output,
            )
            state.lineage.append(latest_update)

    return wrapper
