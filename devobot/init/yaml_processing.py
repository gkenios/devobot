from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel

from devobot.config import CONFIG_FILE, YamlConfig
from devobot.services import (
    Auth,
    AuthFactory,
    SecretFactory,
    VectorDB,
    VectorDBFactory,
    get_embeddings,
    get_llm,
)
from devobot.utils import Singleton, read_file


class ConfigSingleton(metaclass=Singleton):
    """Class to store the configuration."""

    def __init__(self) -> None:
        self.config = YamlConfig(**read_file(CONFIG_FILE))
        self.auth: dict[str, Auth] = dict()
        self.secrets: dict[str, str] = dict()
        self.models: dict[str, BaseChatModel | Embeddings] = dict()
        self.databases: dict[str, VectorDB] = dict()

        self.build_auth()
        self.get_secrets()
        self.get_models()

    def build_auth(self) -> None:
        for host in self.config.secrets.hosts:
            self.auth[host.name] = AuthFactory[host.name].value()

    def get_models(self) -> None:
        models_conf = self.config.models
        self.models["llm"] = get_llm(**models_conf.llm.__dict__)
        self.models["embeddings"] = get_embeddings(
            **models_conf.embeddings.__dict__
        )

    def get_databases(self) -> None:
        db = self.config.databases
        if db.vector:
            vector_db = VectorDBFactory[db.vector.host].value(
                embeddings=self.models["embeddings"],
                endpoint=db.vector.endpoint,
                collection=db.vector.collection,
            )
            self.databases["vector"] = vector_db
        if db.nosql:
            pass

    def get_secrets(self) -> None:
        # Iterate over hosts
        for host in self.config.secrets.hosts:
            auth = self.auth[host.name]

            # Iterate over vaults
            for vault in host.vaults:
                secrets_mapping = dict()
                for secret in vault.secrets:
                    secrets_mapping[secret.name] = secret.value

                # Get the secrets
                retrieved_secrets = (
                    SecretFactory[host.name]
                    .value(auth)
                    .get(secrets_mapping.values(), vault.name)
                )
                self.secrets.update(
                    {
                        key: retrieved_secrets[value]
                        for key, value in secrets_mapping.items()
                    }
                )
        # Re-red the config and parse the secrets
        self.config = YamlConfig(**read_file(CONFIG_FILE, self.secrets))


Config = ConfigSingleton()
llm = Config.models["llm"]
embeddings = Config.models["embeddings"]
vector_db = Config.databases["vector"]
