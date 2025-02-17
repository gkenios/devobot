from abc import ABC, abstractmethod
from enum import Enum
import os
from typing import TYPE_CHECKING

from .auth import Auth


if TYPE_CHECKING:
    from azure.keyvault.secrets import SecretClient


class Secret(ABC):
    def __init__(self, auth: Auth) -> None:
        self.auth = auth

    def get(
        self,
        secret_name: str | list[str],
        vault_name: str | None,
    ) -> str | dict[str, str]:
        if isinstance(secret_name, str):
            return self._get_one(secret_name, vault_name)
        return self._get_all(secret_name, vault_name)

    def _get_one(self, secret_name: str, vault_name: str | None)-> str:
        key = self._get(secret_name, vault_name)
        if not key:
            vault_name = vault_name or "environment variables"
            raise ValueError(
                f"Secret '{secret_name}' not found in '{vault_name}'."
            )
        return key

    def _get_all(
        self,
        secret_names: list[str],
        vault_name: str | None,
    ) -> dict[str, str]:
        return {
            secret_name: self._get_one(secret_name, vault_name)
            for secret_name in secret_names
        }

    @abstractmethod
    def _get(self, secret_name: str, vault_name: str) -> str:
        pass


class LocalSecret(Secret):
    def _get(self, secret_name: str, vault_name: str | None) -> str:
        if vault_name:
            raise ValueError("Local secrets do not have vaults.")
        return os.getenv(secret_name)


class AzureSecret(Secret):
    def __init__(self, auth: Auth) -> None:
        self.auth = auth

    def _get(self, secret_name: str, vault_name: str) -> "SecretClient":
        try:
            from azure.keyvault.secrets import SecretClient
        except ImportError as error:
            raise ImportError(
                "Unable to import azure.keyvault.secrets.SecretClient. "
                "Please install with `pip install azure-keyvault-secrets`."
            ) from error

        client = SecretClient(
            vault_url=f"https://{vault_name}.vault.azure.net",
            credential=self.auth,
        )
        return client.get_secret(secret_name).value


class GCPSecret(Secret):
    def _get(self, secret_name: str, vault_name: str) -> str:
        raise NotImplementedError("GCP secrets are not implemented yet.")


class SecretFactory(Enum):
    local = LocalSecret
    azure = AzureSecret
    gcp = GCPSecret
