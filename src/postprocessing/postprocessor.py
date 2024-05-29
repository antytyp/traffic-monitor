from abc import ABC, abstractmethod

import numpy as np


class Postprocessor(ABC):
    @abstractmethod
    def prepare(self, frame: np.ndarray, predictions: np.ndarray) -> np.ndarray:
        pass
