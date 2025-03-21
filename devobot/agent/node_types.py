from typing import AsyncGenerator, Callable, Concatenate

from .state import NodeInteraction, State


NodeInputType = Concatenate[State, ...]
NodeOutputType = AsyncGenerator[NodeInteraction, None]
NodeFunctionType = Callable[NodeInputType, NodeOutputType]  # type: ignore
