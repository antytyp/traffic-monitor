import logging

import requests  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataDownloader:
    def __init__(self, stream_url: str) -> None:
        self.stream_url = stream_url
        self.base_url = self._get_base_url()
        self.m3u8_url = self._get_m3u8_url()

    def _get_base_url(self) -> str:
        base_url = self.stream_url.rstrip(self.stream_url.split("/")[-1])
        logger.info(f"Prepared base url: {base_url}")
        return base_url

    def _get_m3u8_url(self) -> str:
        response = requests.get(self.stream_url)
        response.raise_for_status()
        m3u8_url_suffix = next(
            (key for key in response.text.split("\n") if key.endswith(".m3u8")),
        )
        m3u8_url = self.base_url + m3u8_url_suffix
        logger.info(f"Prepared m3u8 url: {m3u8_url}")
        return m3u8_url
