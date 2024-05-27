import json
import os

from dotenv import load_dotenv

from src.data_setup.traffic_video_frame_preprocessor import (
    TrafficVideoFramePreprocessor,
)
from src.data_setup.traffic_video_stream import TrafficVideoStream
from src.utils.utils import get_monitored_regions

DEFAULT_CONFIG_PATH = "../config/traffic_monitor_config.json"
NUM_ITERATIONS = 10


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    with open(DEFAULT_CONFIG_PATH) as f:
        config = json.load(f)

    camera_stream_url = os.getenv("CAMERA_STREAM_URL")
    region_configs = config.get("regions")

    monitored_regions = get_monitored_regions(region_configs)

    traffic_video_stream = TrafficVideoStream(stream_url=camera_stream_url)
    frame_preprocessor = TrafficVideoFramePreprocessor(monitored_regions)

    for _ in range(NUM_ITERATIONS):
        frame = traffic_video_stream.get_frame()
        prepared_frame = frame_preprocessor.prepare(frame)
