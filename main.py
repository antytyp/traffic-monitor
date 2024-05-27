import json
import os

from dotenv import load_dotenv

from src.algorithms.statistical_traffic_monitor_model import (
    StatisticalTrafficMonitorModel,
)
from src.data_setup.traffic_video_frame_postprocessor import (
    TrafficVideoFramePostprocessor,
)
from src.data_setup.traffic_video_frame_preprocessor import (
    TrafficVideoFramePreprocessor,
)
from src.data_setup.traffic_video_stream import TrafficVideoStream
from src.utils.utils import get_monitored_regions

DEFAULT_CONFIG_PATH = "config/traffic_monitor_config.json"
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
    traffic_monitor_model = StatisticalTrafficMonitorModel(monitored_regions)
    frame_postprocessor = TrafficVideoFramePostprocessor(monitored_regions)

    for _ in range(NUM_ITERATIONS):
        frame = traffic_video_stream.get_frame()
        prepared_frame = frame_preprocessor.prepare(frame)
        predictions = traffic_monitor_model.predict(prepared_frame)
        frame_with_predictions = frame_postprocessor.prepare(frame, predictions)