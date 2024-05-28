import logging

from config import constants
from config.config import Config, ConfigError
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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    try:
        config = Config()
    except ConfigError as e:
        logger.error(e)
        return

    monitored_regions = get_monitored_regions(config.region_configs)

    traffic_video_stream = TrafficVideoStream(stream_url=config.camera_stream_url)
    frame_preprocessor = TrafficVideoFramePreprocessor(monitored_regions)
    traffic_monitor_model = StatisticalTrafficMonitorModel(monitored_regions)
    frame_postprocessor = TrafficVideoFramePostprocessor(monitored_regions)

    training_frames = traffic_video_stream.get_frames(
        num_frames=constants.NUM_TRAINING_FRAMES, fps=constants.FPS, verbose=True
    )
    print(f"Collected {len(training_frames)} frames.")

    traffic_monitor_model.fit(training_frames)

    frames_with_prediction = []

    for _ in range(constants.NUM_PREDICT_ITERATIONS):
        frame = traffic_video_stream.get_single_frame()
        prepared_frame = frame_preprocessor.prepare(frame)
        predictions = traffic_monitor_model.predict(prepared_frame)
        frame_with_predictions = frame_postprocessor.prepare(frame, predictions)
        frames_with_prediction.append(frame_with_predictions)


if __name__ == "__main__":
    main()
