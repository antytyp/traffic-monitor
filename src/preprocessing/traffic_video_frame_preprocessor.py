from typing import List

import numpy as np

from src.preprocessing.preprocessor import Preprocessor
from src.utils.monitored_region import MonitoredRegion


class TrafficVideoFramePreprocessor(Preprocessor):
    def __init__(self, monitored_regions: List[MonitoredRegion]):
        self.monitored_regions = monitored_regions

    def prepare(self, frame: np.ndarray) -> List[np.ndarray]:
        return [
            frame[monitored_region.get_np_ranges()]
            for monitored_region in self.monitored_regions
        ]
