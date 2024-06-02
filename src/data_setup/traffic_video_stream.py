import logging
from typing import Union


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrafficVideoStream:
    def __init__(self, stream_url: Union[str, None]):
        self.stream_url = stream_url
