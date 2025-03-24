from typing import (
    Annotated,
    AsyncGenerator,
    Callable,
    Concatenate,
    Generic,
    TypeVar,
)

from langchain_core.tools import InjectedToolArg

from .state import NodeInteraction, State


NodeInputType = Concatenate[State, ...]
NodeOutputType = AsyncGenerator[NodeInteraction, None]
NodeFunctionType = Callable[NodeInputType, NodeOutputType]  # type: ignore


class ConfigToolArg(Generic[TypeVar("T")]):
    def __class_getitem__(cls, item):
        return Annotated[item, InjectedToolArg]
