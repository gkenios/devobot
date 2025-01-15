from devobot.utils import Singleton, get_llm, read_file
from .main import CONFIG_FILE


class ConfigSingleton(metaclass=Singleton):
    """Class to store the configuration."""

    def __init__(self) -> None:
        config = read_file(CONFIG_FILE)
        self.llm = get_llm(**config["llm"]["auth"])
        self.use_llm = config["llm"]["use"]


Config = ConfigSingleton()
llm = Config.llm
