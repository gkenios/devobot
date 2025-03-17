from dataclasses import dataclass

from devobot.config import AgentNodeConfig


@dataclass
class NodeState:
    input: str
    output: str | None
    config: AgentNodeConfig


@dataclass
class State:
    input: str
    lineage: list[NodeState]
    user_email: str


@dataclass
class NodeInteraction:
    input: str
    output: str | None = None
