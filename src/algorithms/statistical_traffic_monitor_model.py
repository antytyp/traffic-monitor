from typing import List

import numpy as np

from .traffic_monitor_model import TrafficMonitorModel
from ..utils.monitored_region import MonitoredRegion


class StatisticalTrafficMonitorModel(TrafficMonitorModel):
    def __init__(self, monitored_regions: List[MonitoredRegion]) -> None:
        self.monitored_regions = monitored_regions

    def predict(self, frame_monitored_regions: List[np.ndarray]) -> np.ndarray:
        # dummy prediction for now...
        return np.random.randint(0, 2, len(frame_monitored_regions))
