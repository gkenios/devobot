from abc import ABC, abstractmethod
from typing import Any
import yaml


class File(ABC):
    @abstractmethod
    def read_file(cls, path: str) -> Any:
        raise NotImplementedError


class YamlFile(File):
    @classmethod
    def read_file(cls, path: str) -> Any:
        with open(path, "r") as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
        return content


def read_file(file_path: str) -> Any:
    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
        obj = YamlFile
    return obj.read_file(file_path)
