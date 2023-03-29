from dataclasses import dataclass
from typing import Tuple

import yaml

from loader.base_loader import BaseLoader


@dataclass
class Config:
    template_path: str
    data_path: str
    output_path: str
    tmp_dir: str
    templates_per_page: int


@dataclass
class ConfigLoader(BaseLoader):
    @staticmethod
    def supported_exts() -> Tuple[str, ...]:
        return ".yaml",

    def _load(self) -> Config:
        with open(self.path) as f:
            data = yaml.safe_load(f)

        return Config(
            template_path=data["template_path"],
            tmp_dir=data["tmp_directory"],
            data_path=data["data_path"],
            output_path=data["output_path"],
            templates_per_page=data["templates_per_page"]
        )
