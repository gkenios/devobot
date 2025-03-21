from typing import Any, Literal

from pydantic import BaseModel


_SUPPORTED_CLOUD_PROVIDERS = ["azure", "gcp"]


# Agent
class NextConditional(BaseModel):
    key: str
    mapping: dict[str, str]


class AgentNodeConfig(BaseModel):
    id: str
    function: str
    function_params: dict[str, Any] | None = None
    next: str | list[str] | None = None
    next_conditional: NextConditional | None = None
    step_output: str | None = None


# Models
class ModelConfig(BaseModel):
    api_key: str
    api_url: str
    api_version: str
    model: str


class ModelsConfig(BaseModel):
    llm: ModelConfig
    embeddings: ModelConfig


# Secrets
class SecretsSecretConfig(BaseModel):
    name: str
    value: str


class SecretsVaultConfig(BaseModel):
    name: str | None
    secrets: list[SecretsSecretConfig]


class SecretsHostConfig(BaseModel):
    name: Literal["local", *_SUPPORTED_CLOUD_PROVIDERS]  # type: ignore
    vaults: list[SecretsVaultConfig]


class SecretsConfig(BaseModel):
    hosts: list[SecretsHostConfig]


# Yaml
class YamlConfig(BaseModel):
    agent: list[AgentNodeConfig]
    databases: dict[str, str | None]
    models: ModelsConfig
    secrets: SecretsConfig
