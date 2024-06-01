import numpy as np

from src.postprocessing.postprocessor import Postprocessor
from src.prediction.traffic_monitor_model import TrafficMonitorModel
from src.preprocessing.preprocessor import Preprocessor


class InferencePipeline:
    def __init__(
        self,
        preprocessor: Preprocessor,
        predictor: TrafficMonitorModel,
        postprocessor: Postprocessor,
    ):
        self.preprocessor = preprocessor
        self.predictor = predictor
        self.postprocessor = postprocessor

    def process_data(self, raw_data: np.ndarray) -> np.ndarray:
        # Preprocess raw data
        preprocessed_data = self.preprocessor.prepare(raw_data)

        # Get predictions
        predictions = self.predictor.predict(preprocessed_data)

        # Postprocess predictions
        postprocessed_predictions = self.postprocessor.prepare(raw_data, predictions)

        return postprocessed_predictions
