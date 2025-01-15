from abc import ABC, abstractmethod
import os

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr


class LLM(BaseModel, ABC):
    model: str
    api_key: SecretStr
    api_url: str | None = None
    api_version: str | None = None

    @abstractmethod
    def auth(self) -> BaseChatModel:
        raise NotImplementedError


class AzureLLM(LLM):
    def auth(self) -> BaseChatModel:
        return AzureChatOpenAI(
            azure_endpoint=self.api_url,
            azure_deployment=self.model,
            api_key=self.api_key,
            api_version=self.api_version,
        )


def get_llm(
    model: str,
    api_key: SecretStr = os.getenv("API_KEY"),  # type: ignore
    api_url: str | None = None,
    api_version: str | None = None,
) -> BaseChatModel:
    if isinstance(api_url, str) and api_url.strip("/").endswith("azure.com"):
        obj = AzureLLM
    # This is a placeholder for future LLM
    else:
        pass
    return obj(
        model=model,
        api_key=api_key,
        api_url=api_url,
        api_version=api_version,
    ).auth()
