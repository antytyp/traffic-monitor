import logging
from typing import List

import cv2
import numpy as np
import requests  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE_FPS = 25
SOURCE_VIDEO_LENGTH_IN_SECONDS = 6
TEMP_TS_PATH = "tmp/temp_traffic_monitor_video.ts"


class TrafficVideoStream:
    def __init__(self, stream_url: str):
        self.stream_url = stream_url
        self.base_url = self.stream_url.rstrip(self.stream_url.split("/")[-1])

    def download_video_batch(self) -> List[np.ndarray]:
        frames: List[np.ndarray] = []

        response = requests.get(self.stream_url)

        if response.status_code != 200:
            return frames

        m3u8_url_suffix = [
            key for key in response.text.split("\n") if key.endswith(".m3u8")
        ][0]
        m3u8_url = self.base_url + m3u8_url_suffix

        response = requests.get(m3u8_url)

        if response.status_code != 200:
            return frames

        latest_ts_file_suffix = max(
            [key for key in response.text.split("\n") if key.endswith(".ts")]
        )
        latest_ts_url = self.base_url + latest_ts_file_suffix

        response = requests.get(latest_ts_url)

        if response.status_code != 200:
            return frames

        with open(TEMP_TS_PATH, "wb+") as f:
            f.write(response.content)

        cv2_video_capture = cv2.VideoCapture()
        cv2_video_capture.open(TEMP_TS_PATH)
        number_of_frames = int(cv2_video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(number_of_frames):
            _, frame = cv2_video_capture.read()
            frames.append(frame)

        cv2_video_capture.release()

        return frames
