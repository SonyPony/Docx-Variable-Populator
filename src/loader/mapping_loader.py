import yaml

from loader.base_loader import BaseLoader
from src.mapping.validator import MappingsSyntaxValidator
from typing import List, Tuple
from dataclasses import dataclass
from mapping.csv_2_template_map import AttributeMap


@dataclass
class MappingLoader(BaseLoader):
    """
    Given a yaml config file it loads mappings and parse them into AttributeMap.
    """

    @staticmethod
    def supported_exts() -> Tuple[str, ...]:
        return ".yaml",

    def _load(self) -> List[AttributeMap]:
        with open(self.path) as f:
            data = yaml.safe_load(f)

        MappingsSyntaxValidator.check(data)

        return [
            AttributeMap(table_key=mapping["table_key"], template_key=mapping["template_key"])
            for mapping in data
        ]
