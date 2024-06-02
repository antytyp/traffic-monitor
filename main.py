import logging

from config.config import Config, ConfigError
from src.inference_pipeline import InferencePipeline
from src.prediction.statistical_traffic_monitor_model import (
    StatisticalTrafficMonitorModel,
)
from src.postprocessing.traffic_video_frame_postprocessor import (
    TrafficVideoFramePostprocessor,
)
from src.preprocessing.traffic_video_frame_preprocessor import (
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

    frame_preprocessor = TrafficVideoFramePreprocessor(monitored_regions)
    traffic_monitor_model = StatisticalTrafficMonitorModel(monitored_regions)
    frame_postprocessor = TrafficVideoFramePostprocessor(monitored_regions)

    inference_pipeline = InferencePipeline(
        preprocessor=frame_preprocessor,
        predictor=traffic_monitor_model,
        postprocessor=frame_postprocessor,
    )
    logger.info(f"InferencePipeline {inference_pipeline} initialized.")

    traffic_video_stream = TrafficVideoStream(stream_url=config.camera_stream_url)
    logger.info(f"TrafficVideoStream {traffic_video_stream} initialized.")

    frames = traffic_video_stream.download_video_batch()
    logger.info(f"Downloaded {len(frames)} frames.")


if __name__ == "__main__":
    main()
