import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataDownloader:
    def __init__(self, stream_url: str) -> None:
        self.stream_url = stream_url
        self.base_url = self._get_base_url()

    def _get_base_url(self) -> str:
        base_url = self.stream_url.rstrip(self.stream_url.split("/")[-1])
        logger.info(f"Prepared base url: {base_url}")
        return base_url
