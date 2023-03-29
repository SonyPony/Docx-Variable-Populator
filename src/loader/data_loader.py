import pandas as pd
import numpy as np

from typing import Tuple
from dataclasses import dataclass
from loader.base_loader import BaseLoader


@dataclass
class DataLoader(BaseLoader):
    """
    Loads the data from a .csv file.
    """

    @staticmethod
    def supported_exts() -> Tuple[str, ...]:
        return ".csv",

    def _load(self) -> pd.DataFrame:
        data = pd.read_csv(self.path, sep=";")
        return data.replace(np.nan, "")
