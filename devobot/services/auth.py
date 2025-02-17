from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from azure.identity import DefaultAzureCredential


class Auth(ABC):
    def __init__(self) -> None:
        self.auth = self._auth()

    @classmethod
    @abstractmethod
    def _auth(cls) -> Any:
        raise NotImplementedError


class LocalAuth(Auth):
    @classmethod
    def _auth(cls) -> None:
        return


class AzureAuth(Auth):
    @classmethod
    def _auth(cls) -> "DefaultAzureCredential":
        try:
            from azure.identity import DefaultAzureCredential
        except ImportError as error:
            raise ImportError(
                "Unable to import azure.identity.DefaultAzureCredential. "
                "Please install with `pip install azure-identity`."
            ) from error
        return DefaultAzureCredential()


class GCPAuth(Auth):
    @classmethod
    def _auth(cls) -> Any:
        raise NotImplementedError("GCP authentication is not implemented yet.")


class AuthFactory(Enum):
    local = LocalAuth
    azure = AzureAuth
    gcp = GCPAuth
