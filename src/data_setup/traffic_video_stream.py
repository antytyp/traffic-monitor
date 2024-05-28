from datetime import datetime
from time import time
from typing import Union, List

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

    def get_single_frame(self) -> cv2.typing.MatLike:
        self.open_connection()
        ret, frame = self.cv2_video_capture.read()
        self.release_connection()
        return frame

    def get_frames(
        self, num_frames: int, fps: int = 25, verbose: bool = False
    ) -> List[cv2.typing.MatLike]:
        frames: List[cv2.typing.MatLike] = []
        self.open_connection()
        prev_time = time()
        try:
            while len(frames) < num_frames:
                ret, frame = self.cv2_video_capture.read()
                read_time = time()
                time_delta = read_time - prev_time
                if time_delta > 1.0 / fps:
                    frames.append(frame)
                    prev_time = read_time
                    if verbose:
                        current_time = datetime.utcnow().strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        )
                        print(
                            f"Frame collected, time {current_time}, time delta = {time_delta}"
                        )
        except KeyboardInterrupt:
            print("Keyboard Interrupt!")
        finally:
            self.release_connection()
        return frames
