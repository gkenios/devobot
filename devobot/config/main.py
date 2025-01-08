import os


ENV = os.getenv("ENV", "dev")
USE_LLM = os.getenv("USE_LLM", "false") == "true"

# Paths
CONFIG_FILE = "devobot/config.yaml"
