from typing import Dict, List

import cv2
import numpy as np

from .traffic_monitor_model import TrafficMonitorModel
from ..utils.monitored_region import MonitoredRegion


class StatisticalTrafficMonitorModel(TrafficMonitorModel):
    def __init__(self, monitored_regions: List[MonitoredRegion]) -> None:
        self.monitored_regions = monitored_regions
        self.monitored_regions_backgrounds: Dict[
            MonitoredRegion, cv2.typing.MatLike
        ] = {}

    def fit(self, training_frames: List[cv2.typing.MatLike]) -> None:
        for monitored_region in self.monitored_regions:
            # collect frames from the monitored region
            monitored_region_frames = [
                frame[monitored_region.get_np_ranges()] for frame in training_frames
            ]

            # calculate background representations - median anchor
            background_representation = np.median(
                monitored_region_frames, axis=0
            ).astype(dtype=np.uint8)

            self.monitored_regions_backgrounds[monitored_region] = (
                background_representation
            )

    def predict(self, frame_monitored_regions: List[np.ndarray]) -> np.ndarray:
        # dummy prediction for now...
        return np.random.randint(0, 2, len(frame_monitored_regions))
