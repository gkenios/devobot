from abc import ABC, abstractmethod
from typing import Any
import yaml

from jinja2 import Template


class File(ABC):
    @abstractmethod
    def read_file(cls, path: str) -> Any:
        raise NotImplementedError


class YamlFile(File):
    @classmethod
    def read_file(cls, path: str) -> Any:
        with open(path, "r") as f:
            content = yaml.safe_load(f)
        return content


def read_file(file_path: str, context: dict[str, Any] | None = None) -> Any:
    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
        obj = YamlFile
    data = obj.read_file(file_path)
    if context:
        return render_dict_with_jinja(data, context)
    return data


def render_dict_with_jinja(
    data: Any,
    context: dict[str, str],
) -> Any:
    """Recursively renders a dictionary structure with Jinja2 templates.

    Args:
        data: The data (loaded as a dictionary).
        context: A dictionary containing the values to replace the placeholders.

    Returns:
        The rendered data (as a Python object).
    """

    def _render(data: Any, context: dict[str, str]) -> Any:
        if isinstance(data, dict):
            new_data = dict()
            for key, value in data.items():
                # Recurse for dict values
                new_data[key] = _render(value, context)
            return new_data
        elif isinstance(data, list):
            # Recurse for list items
            return [_render(item, context) for item in data]
        elif isinstance(data, str):
            try:
                template = Template(data)
                return template.render(context)
            except Exception as error:
                raise Exception(f"Jinja2 error parsing: \n{data}") from error
        else:
            return data

    return _render(data, context)
