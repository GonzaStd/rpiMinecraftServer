import yaml
from pathlib import Path
from typing import Type, TypeVar
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_ROOT = PROJECT_ROOT
GLOBAL_CONFIG_ROOT = Path(DEFAULT_CONFIG_ROOT)
PydanticChild = TypeVar("PydanticChild", bound=BaseModel)

_ENV_LOADED = False


class File:
    """Represent a generic file."""

    def __init__(
        self,
        name: str,
        file_type: str,
        path: str,
    ) -> None:
        self.file_type = file_type

        extension = f".{self.file_type}"

        if name.endswith(extension):
            name = name[:-len(extension)]

        self.name = name
        self.path = Path(path).resolve()
        self.file_path = Path(self.path / (name + extension))
        if not self.file_path.exists():
            raise ValueError(f"File {name + extension} not found in "
                             f"{str(self.path)}.")


class ConfigFile(File):
    """Represent a YAML configuration file."""

    file_type = "yaml"

    def __init__(
        self,
        name: str,
        schema_class: Type[PydanticChild],
        config_subpath: str = "",
        config_path: str | Path = GLOBAL_CONFIG_ROOT,
    ) -> None:

        self.schema_class = schema_class

        if config_subpath:
            path = Path(config_path) / config_subpath
        else:
            path = config_path

        super().__init__(
            name=name,
            file_type=self.file_type,
            path=str(path),
        )

    def read_raw(self):
        with open(self.file_path) as f:
            return yaml.safe_load(f)

    def read(self):
        data = self.read_raw()
        return self.schema_class(**data)

    def change(self, config):
        pass

    def write(self, config: Type[PydanticChild]):
        data = config.model_dump()
        with open(self.file_path, 'w') as f:
            yaml.safe_dump(data, f)