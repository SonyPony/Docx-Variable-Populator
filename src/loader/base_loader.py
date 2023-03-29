import os

from dataclasses import dataclass
from abc import abstractmethod
from typing import Any, Tuple
from loader.exception import UnsupportedFileError


@dataclass
class BaseLoader:
    path: str

    def load(self) -> Any:
        supported_exts = self.__class__.supported_exts()

        if not (ext := os.path.splitext(self.path)[-1]) in supported_exts and len(supported_exts):
            raise UnsupportedFileError(f"Only {supported_exts} files are supported, got {ext}")
        return self._load()

    @staticmethod
    @abstractmethod
    def supported_exts() -> Tuple[str, ...]:
        pass

    @abstractmethod
    def _load(self) -> Any:
        pass