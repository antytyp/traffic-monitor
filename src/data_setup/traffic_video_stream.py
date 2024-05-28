from datetime import datetime
from typing import Union

import cv2


class TrafficVideoStream:
    def __init__(self, stream_url: Union[str, None]):
        self.stream_url = stream_url
        self.cv2_video_capture = cv2.VideoCapture()

    def open_connection(self) -> None:
        self.cv2_video_capture.open(self.stream_url)
        print(
            f'VideoCapture connection opened at {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")}.'
        )

    def release_connection(self) -> None:
        self.cv2_video_capture.release()
        print(
            f'VideoCapture connection released at {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")}.'
        )

    def get_frame(self) -> cv2.typing.MatLike:
        self.open_connection()
        ret, frame = self.cv2_video_capture.read()
        self.release_connection()
        return frame
