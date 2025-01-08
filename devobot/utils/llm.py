from abc import ABC, abstractmethod
import os

from langchain_openai import AzureChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from pydantic import BaseModel


class LLM(BaseModel, ABC):
    model: str
    api_key: str
    api_url: str | None = None
    api_version: str | None = None

    @abstractmethod
    def auth(self):
        raise NotImplementedError


class AzureLLM(LLM):
    def auth(self):
        return AzureChatOpenAI(
            azure_endpoint=self.api_url,
            deployment_name=self.model,
            openai_api_key=self.api_key,
            openai_api_version=self.api_version,
        )


def get_llm(
    model: str,
    api_key: str = os.getenv("API_KEY"),
    api_url: str | None = None,
    api_version: str | None = None,
) -> BaseChatOpenAI:
    stripped_api_url = api_url.strip("/")
    if stripped_api_url.endswith("azure.com"):
        obj = AzureLLM
    # This is a placeholder for future LLM
    return obj(
        model=model,
        api_key=api_key,
        api_url=api_url,
        api_version=api_version,
    ).auth()
