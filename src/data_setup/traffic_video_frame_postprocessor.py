from typing import List

import cv2
import numpy as np
from PIL import Image, ImageDraw

from src.utils.monitored_region import MonitoredRegion


class TrafficVideoFramePostprocessor:
    def __init__(self, monitored_regions: List[MonitoredRegion]) -> None:
        self.monitored_regions = monitored_regions
        self.object_detected_color = (154, 205, 50, 75)
        self.object_not_detected_color = (236, 240, 241, 75)

    def prepare(self, frame: np.ndarray, predictions: np.ndarray) -> np.ndarray:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(rgb_frame)
        frame_draw = ImageDraw.Draw(pil_frame, "RGBA")

        for prediction, monitored_region in zip(predictions, self.monitored_regions):
            fill_color_rgba = (
                self.object_detected_color
                if prediction
                else self.object_not_detected_color
            )

            monitored_region_xy = monitored_region.get_pil_polygon_xy()

            frame_draw.polygon(
                xy=monitored_region_xy, fill=fill_color_rgba, outline=None, width=1
            )

        frame_with_predictions = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)

        return frame_with_predictions
