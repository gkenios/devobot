from .main import CONFIG_FILE
from devobot.services import (
    Auth,
    AuthFactory,
    BaseChatModel,
    SecretFactory,
    get_llm,
)
from devobot.utils import Singleton, read_file


class ConfigSingleton(metaclass=Singleton):
    """Class to store the configuration."""

    def __init__(self) -> None:
        self.config = read_file(CONFIG_FILE)
        self.auth: dict[str, Auth] = dict()
        self.secrets: dict[str, str] = dict()
        self.models: dict[str, BaseChatModel] = dict()

        self.build_auth()
        self.get_secrets()
        self.get_models()

    def build_auth(self) -> None:
        for host_object in self.config["secrets"]["hosts"]:
            vault_host = host_object["name"]
            self.auth[vault_host] = AuthFactory[vault_host].value.login()

    def get_models(self):
        models_conf: dict = self.config["models"]
        for model in models_conf.keys():
            self.models[model] = get_llm(**models_conf[model])

    def get_secrets(self) -> None:
        # Iterate over hosts
        for secret_object in self.config["secrets"]["hosts"]:
            vault_host = secret_object["name"]
            auth = self.auth[vault_host]

            # Iterate over vaults
            for vault_obj in secret_object["vaults"]:
                vault_name = vault_obj["name"]
                secrets_mapping = dict()
                for element in vault_obj["secrets"]:
                    secrets_mapping[element["name"]] = element["value"]

                # Get the secrets
                retrieved_secrets = (
                    SecretFactory[vault_host]
                    .value(auth)
                    .get(secrets_mapping.values(), vault_name)
                )
                self.secrets.update(
                    {
                        key: retrieved_secrets[value]
                        for key, value in secrets_mapping.items()
                    }
                )
        # Re-red the config and parse the secrets
        self.config = read_file(CONFIG_FILE, self.secrets)


Config = ConfigSingleton()
llm = Config.models["llm"]
embeddings = Config.models["embeddings"]
