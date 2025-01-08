from devobot.utils import read_file, get_llm
from .main import CONFIG_FILE


llm = get_llm(**read_file(CONFIG_FILE)["llm"]["auth"])
