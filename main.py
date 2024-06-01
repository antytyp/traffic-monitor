import logging
from time import time

import cv2

from config import constants
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


def show_live_stream_with_prediction(
    traffic_video_stream: TrafficVideoStream, inference_pipeline: InferencePipeline
) -> None:
    traffic_video_stream.open_connection()
    prev_time = time()
    num_collected_frames = 0
    stream_fps = 10
    try:
        while num_collected_frames < constants.MAX_NUM_FRAMES_LIVE_PREDICTION:
            ret, frame = traffic_video_stream.cv2_video_capture.read()
            read_time = time()
            time_delta = read_time - prev_time
            if time_delta > 1.0 / stream_fps:
                frame_with_predictions = inference_pipeline.process_data(raw_data=frame)

                cv2.imshow(constants.CV2_WINDOW_NAME, frame_with_predictions)
                if cv2.waitKey(50) & 0xFF == ord("q"):
                    break

                num_collected_frames += 1
                prev_time = read_time

    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt!")
    finally:
        traffic_video_stream.release_connection()
        cv2.destroyAllWindows()


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

    traffic_video_stream = TrafficVideoStream(stream_url=config.camera_stream_url)

    training_frames = traffic_video_stream.get_frames(
        num_frames=constants.NUM_TRAINING_FRAMES, fps=constants.FPS, verbose=True
    )
    logger.info(f"Collected {len(training_frames)} frames.")

    traffic_monitor_model.fit(training_frames)

    show_live_stream_with_prediction(traffic_video_stream, inference_pipeline)


if __name__ == "__main__":
    main()
