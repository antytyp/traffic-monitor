import logging
import os
from typing import List, Union

import cv2
import numpy as np
import requests  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE_FPS = 25
SOURCE_VIDEO_LENGTH_IN_SECONDS = 6


class TrafficVideoStream:
    TEMP_TS_PATH = "tmp/temp_traffic_monitor_video.ts"

    def __init__(self, stream_url: str):
        self.stream_url = stream_url
        self.base_url = self.stream_url.rstrip(self.stream_url.split("/")[-1])

    def _get_m3u8_url(self) -> Union[str, None]:
        response = requests.get(self.stream_url)

        if response.status_code != 200:
            return None

        m3u8_url_suffix = [
            key for key in response.text.split("\n") if key.endswith(".m3u8")
        ][0]
        m3u8_url = self.base_url + m3u8_url_suffix

        return m3u8_url

    def _get_latest_ts_url(self) -> Union[str, None]:
        m3u8_url = self._get_m3u8_url()

        response = requests.get(m3u8_url)

        if response.status_code != 200:
            return None

        latest_ts_file_suffix = max(
            [key for key in response.text.split("\n") if key.endswith(".ts")]
        )
        latest_ts_url = self.base_url + latest_ts_file_suffix

        return latest_ts_url

    def _fetch_latest_ts_file(self) -> Union[bytes, None]:
        latest_ts_url = self._get_latest_ts_url()

        response = requests.get(latest_ts_url)

        if response.status_code != 200:
            return None

        return response.content

    def _save_video_to_temp_ts_file(self, video_bytes: bytes) -> None:
        with open(self.TEMP_TS_PATH, "wb+") as f:
            f.write(video_bytes)

    def _get_frames_from_temp_ts_file(self) -> List[np.ndarray]:
        frames: List[np.ndarray] = []

        cv2_video_capture = cv2.VideoCapture()
        cv2_video_capture.open(self.TEMP_TS_PATH)
        number_of_frames = int(cv2_video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        for _ in range(number_of_frames):
            _, frame = cv2_video_capture.read()
            frames.append(frame)

        cv2_video_capture.release()

        return frames

    def _remove_temp_ts_file(self) -> None:
        try:
            os.remove(self.TEMP_TS_PATH)
            logger.info(f"File '{self.TEMP_TS_PATH}' removed successfully.")
        except OSError as e:
            logger.error(
                f"Error: Unable to remove file '{self.TEMP_TS_PATH}'. Reason: {e}"
            )

    def download_video_batch(self) -> List[np.ndarray]:
        video_bytes = self._fetch_latest_ts_file()
        self._save_video_to_temp_ts_file(video_bytes)  # type: ignore
        frames = self._get_frames_from_temp_ts_file()
        self._remove_temp_ts_file()

        return frames
