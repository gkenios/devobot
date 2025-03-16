from dataclasses import dataclass

from devobot.config import AgentNodeConfig


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
