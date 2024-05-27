from datetime import datetime
from typing import Union

import cv2


class TrafficVideoStream:
    def __init__(self, stream_url: Union[str, None]):
        self.stream_url = stream_url

    def get_frame(self) -> cv2.typing.MatLike:
        cap = cv2.VideoCapture()
        cap.open(self.stream_url)
        print(
            f'VideoCapture connection opened at {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")}.'
        )
        ret, frame = cap.read()
        cap.release()
        print(
            f'VideoCapture connection released at {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")}.'
        )
        return frame
