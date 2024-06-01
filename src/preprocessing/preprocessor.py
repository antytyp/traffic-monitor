from abc import ABC, abstractmethod
from typing import List

import numpy as np


class Preprocessor(ABC):
    @abstractmethod
    def prepare(self, frame: np.ndarray) -> List[np.ndarray]:
        pass
