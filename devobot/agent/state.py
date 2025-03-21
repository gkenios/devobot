from dataclasses import dataclass
from typing import Any


@dataclass
class NodeState:
    input: str
    output: str | dict | None
    step_output: str | None = None


@dataclass
class State:
    user_email: str
    lineage: list[NodeState]
    input: str
    output: str | dict[str, Any] | None = None


@dataclass
class NodeInteraction:
    input: str
    output: str | dict | None = None
