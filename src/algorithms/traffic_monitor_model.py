from abc import ABC, abstractmethod
from typing import List

import numpy as np


class TrafficMonitorModel(ABC):
    @abstractmethod
    def predict(self, frames: List[np.ndarray]) -> np.ndarray:
        pass
