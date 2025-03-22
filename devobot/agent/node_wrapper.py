from dataclasses import asdict
from typing import Any

from .state import NodeInteraction, NodeState, State
from .types import NodeFunctionType, NodeOutputType
from devobot.config import AgentNodeConfig


def node_wrapper(
    func: NodeFunctionType,
    config: AgentNodeConfig,
    **wrapper_kwargs: Any,
) -> NodeFunctionType:
    async def wrapper(*args: Any, **kwargs: Any) -> NodeOutputType:
        state: State = kwargs.get("state")  # type: ignore
        if not state:
            state = args[0]

        result = func(*args, **kwargs, **wrapper_kwargs)

        # If it's an async generator
        if hasattr(result, "__aiter__"):
            async for item in result:
                # Stream each yielded value
                yield item
        else:
            awaited_result: NodeInteraction = await result
            # Update the lineage
            latest_update = NodeState(
                input=awaited_result.input,
                output=awaited_result.output,
                step_output=config.step_output,
            )
            state.output = awaited_result.output
            state.lineage.append(asdict(latest_update))

            # Yield final result
            yield state

    return wrapper
